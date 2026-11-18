# Session 2 notes

Self-contained study notes for this session. Concepts here are intentionally repeated in
the general notes (index: [README.md](README.md)); this file keeps them in the context
of the exercise so it can be read on its own.

## 1. Goal

From the session README: *train your own model with a custom dataset (Chinese MNIST),
using hyperparameter tuning.* The skeleton gives the pieces to fill in:

| File | What it must do |
|---|---|
| `dataset.py` | a custom `Dataset` over the Chinese MNIST images + CSV labels |
| `model.py` | a `MyModel` (`torch.nn.Module`) that classifies the 15 characters |
| `main.py` | `train_single_epoch`, `eval_single_epoch`, `train_model(config)` and a `__main__` that runs one training |
| `main_hyperparam_optimize.py` | the same training function driven by **Ray Tune** (`tune.run`) over a search space, minimising `val_loss`, printing the best config |
| `utils.py` | provided `accuracy(true_labels, logits)` metric |

The idea: build the full pipeline once (data -> model -> train/eval loop), then let Ray try
several hyperparameter combinations (`num_samples`, `tune.uniform`, `tune.grid_search`) and
report the best one. `hidden_size` of the model is a natural hyperparameter to tune.

## 2. The data (Chinese MNIST, Kaggle `gpreda/chinese-mnist`)

Not committed (`session-2/data/` is in `.gitignore`: 15k images should not be in git).
To download again, from the repo root:

```bash
mkdir -p session-2/data
curl -L --fail -o chinese-mnist.zip \
  'https://www.kaggle.com/api/v1/datasets/download/gpreda/chinese-mnist'
unzip -o -q chinese-mnist.zip -d session-2/data
rm chinese-mnist.zip
```

```
session-2/data/
├── chinese_mnist.csv                 # suite_id, sample_id, code, value, character
├── chinese_mnist.tfrecords           # TensorFlow format, not used
└── data/data/input_{suite_id}_{sample_id}_{code}.jpg   # 15000 images, 64x64, grayscale
```

- Images are individual JPG files; only the labels come from the CSV. So `pd.read_csv`
  is for the CSV, and each image is loaded separately (it cannot be a `read_csv`).
- Image path from a row: `input_{suite_id}_{sample_id}_{code}.jpg`; mind the 3-level
  `data/data/data` nesting.
- 15 classes. `code` is `1..15` (contiguous), `value` is `0..10, 100, 1000, 10000,
  100000000` (gaps), `character` is the glyph. **Class index = `code - 1`.**
- `read_image` returns `uint8`, shape `[1, 64, 64]` (1 channel = grayscale).

## 3. Concepts and how they apply here

### Building on session 1

[Session 1](session-1.md) already has a working loop (`zero_grad -> forward -> loss ->
backward -> step`, see [dl-04-training-loop](dl-04-training-loop.md)). Session 2 reuses it
and changes:

| | Session 1 | Session 2 |
|---|---|---|
| data | synthetic `randn`, labels all 0 | real images + CSV labels |
| task / loss | regression, `MSELoss` (float targets) | 15-class classification, `CrossEntropyLoss` (long indices) |
| metric | loss only | loss + `accuracy` |
| evaluation | none | separate `eval_single_epoch` (`model.eval()`, `torch.no_grad()`) |
| hyperparameters | `argparse` flags | `config` dict, so Ray Tune can drive `train_model` |
| device | `cuda` / `mps` / `cpu` | `main.py` still has `cuda` / `cpu` only: add `mps` for the Mac GPU |

### The `Dataset` class (only what is new vs session 1)

The `Dataset`/`DataLoader` basics (`__getitem__`, `__len__`, batching) are in
[session 1](session-1.md). Here the data is real, which adds:

- `__len__` is `len(self.labels)` (the CSV rows = 15000).
- Load images in `__getitem__`, not in `__init__`: one image per call keeps memory small
  and lets `DataLoader(num_workers=...)` parallelise (session 1 held everything in memory
  because it was synthetic). `__init__` only reads the CSV.
- Every sample must have the same shape/dtype or the batch cannot be stacked
  (`[B, 1, 64, 64]` images, `[B]` labels).
- Leave no test code at module level in `dataset.py`: it runs on every import from `main.py`.

### Loading images with torchvision

- `torchvision.io.read_image(path)` reads **one file** into a `uint8` tensor `[C, H, W]`.
  Passing the folder instead of a file fails.
- `ImageFolder` does not fit (needs one subfolder per class; ours is a flat folder + CSV).
- `read_image` is typed `path: str`; a `Path` works in the installed torchvision
  (0.29.2) but `str(path)` is the supported form.

### dtypes: image float, label long

| | dtype | why |
|---|---|---|
| image | `float32`, scaled to 0..1 | goes through float weights |
| label | `long` class index `0..14` | `CrossEntropyLoss` uses it as an index into the 15 outputs |

- `image = read_image(...).float() / 255.0` (divide by 255, not by the image's max).
- `label = torch.tensor(code - 1, dtype=torch.long)`. A numpy int also works because
  `DataLoader` converts it, but the explicit tensor is clearer.
- The label must stay an **integer**, not a float.
- A string label (`character`) cannot be batched into a tensor; use the integer index and
  map back to the glyph only for display.

### Paths

- Relative paths resolve against the **current working directory**. The README runs
  `python session-2/main.py` from the repo root, so `data/chinese_mnist.csv` was wrong
  (`session-2/data/...` is right).
- Robust version: `DATA_DIR = Path(__file__).parent / "data"`, works from any directory.
- The `/` join only works on `Path`, so `__init__` does `Path(images_path)`.
- Better still, pass the paths in from `main.py` via `config`.

### The model

- Same idea as session 1's MLP (layers in `__init__`, wired in `forward`), now
  `Flatten -> Linear(4096, hidden) -> ReLU -> Linear(hidden, 15)`.
- Input size is `1 * 64 * 64 = 4096`. The `784` (28x28) of standard MNIST crashes with
  `mat1 and mat2 shapes cannot be multiplied (4x4096 and 784x128)`.
- `input_size`, `hidden_size`, `output_size` are constructor arguments (not hardcoded) so
  `hidden_size` can be a hyperparameter in the Ray search. `LazyLinear` is the alternative
  that infers the input size on the first forward pass.
- Grayscale is never explicitly checked: the files are 1-channel, so the batch is
  `[B, 1, 64, 64]` and the `1` is baked into `4096`. A 3-channel input fails with a shape
  error (`4x12288 and 4096x128`).
- Output are raw **logits** (no softmax); `CrossEntropyLoss` applies it.
- No dtype/shape fix-ups in `forward`; the dataset already guarantees them.
- An MLP ignores 2D structure; a small CNN would reach higher accuracy later.

### Flatten, `view`, `reshape`

- `torch.flatten(x, start_dim=1)`, `x.view(x.size(0), -1)`, `x.reshape(x.size(0), -1)`,
  and `nn.Flatten()` all turn `[B, 1, 64, 64]` into `[B, 4096]`.
- `x.size(0)` keeps the batch; `-1` means "infer this dimension" (one `-1` only).
  `x.view(-1)` would flatten the batch too (a classic bug).
- `view` needs contiguous memory, `reshape` copies if needed; neither reorders elements
  (use `permute`/`transpose` to swap axes).
- `utils.accuracy` uses `true_labels.view_as(preds)` so `[B,1]` vs `[B]` cannot broadcast
  to `[B,B]` and silently give a wrong accuracy.

### Loss sanity checks

- `CrossEntropyLoss(logits [B,15], labels [B] long)`.
- Wrong label range gives `IndexError: Target 100 is out of bounds` (that is what returning
  `value` produced).
- A random model should start near `ln(15) ≈ 2.71`.

### Training and evaluation (design for `main.py`)

General rules in [dl-04-training-loop](dl-04-training-loop.md) and
[dl-05-train-eval-split](dl-05-train-eval-split.md). Applied here:

- Review of the first `main.py` (dataset + model loading worked: 15000 samples, image
  `[1, 64, 64]` float32, label long, output `[1, 15]`). Still missing: device `mps` branch
  (it resolved to `cpu` although MPS is available), train/validation split, `DataLoader`s,
  loss, optimizer, `lr` and `batch_size` in `config`, the `...` placeholders, and importing
  `accuracy` from `utils`.
- Split with `random_split(my_dataset, [n_train, n_val], generator=...manual_seed(42))`;
  `shuffle=True` on the train loader only. `main.py` had no `DataLoader` yet.
- Decision: the skeleton does not say where loaders live (it only creates the dataset and
  model in `train_model`). We follow the industry standard: a `get_dataloaders(...)`
  factory in `dataset.py` (dataset -> seeded split -> one loader per split, `batch_size`
  from `config`), called from `train_model`. No separate `dataloader.py`. It also lets
  `main.py` and the Ray script (`main_hyperparam_optimize.py`) share it.
  Signature: `get_dataloaders(images_path, labels_path, batch_size=64, val_ratio=0.15,
  test_ratio=0.15, seed=42)`: `batch_size` is passed from `config` (tunable), ratios and seed
  are defaults; `dataset.py` must not import `main` (circular import). Builds `MyDataset`
  itself and returns three `DataLoader`s (`tuple[DataLoader, DataLoader, DataLoader]`):
  `train_loader, val_loader, test_loader`; the test loader is only used once at the end. See
  [dev-04-ml-project-structure](dev-04-ml-project-structure.md).
- `train_single_epoch` trains (`model.train()`, five-step loop); `eval_single_epoch` uses
  `model.eval()` + `torch.no_grad()`; both return mean loss and accuracy weighted by batch size.
- `epochs: 100` is too many for a first test; use 3-5 until the loop works.
- `__getitem__` reads a JPG and does a pandas `.iloc` per call; `num_workers` speeds up an
  epoch if it is slow.

- Order: split the dataset first (`random_split` -> `Subset`s), then one `DataLoader` per
  subset; never split a loader (leakage, and shuffle differs per split).
- Imports in `dataset.py`: `import torch` (for `torch.tensor`, `torch.long`, `torch.Generator`)
  and `from torch.utils.data import Dataset, DataLoader, random_split` are not redundant: one
  gives the namespace, the other short names. Pick one style per file; `ruff` flags unused
  imports (`F401`). See [dev-01-python-env-and-paths](dev-01-python-env-and-paths.md).

### Dependencies

- Env setup is as in [session 1](session-1.md) (`.venv` + `uv`).
- New here: `requirements.txt` did not list `pandas` or `torchvision` although `dataset.py`
  needs them (`ModuleNotFoundError: No module named 'pandas'`); both are now added.
  Installing a package does not update `requirements.txt` by itself.
- The repo now has a root `pyproject.toml` (`uv sync`, `uv add -r session-N/requirements.txt`,
  `uv run poe all` = ruff lint + format check). Details in
  [dev-01-python-env-and-paths](dev-01-python-env-and-paths.md).

### Git

- The repo is my fork: `origin` = fork, `upstream` = course repo. New sessions come from
  `git fetch upstream && git merge upstream/main`, then `git push origin main`.
  Never "Discard commits". See [dev-02-git-fork-workflow](dev-02-git-fork-workflow.md).

## 4. How it was achieved (timeline)

1. Downloaded the Kaggle dataset, inspected layout and CSV, and found that images are JPGs
   and only labels are in the CSV, so the skeleton's two `read_csv` calls did not apply.
2. Wrote `MyDataset`: CSV read once, `__len__` from the dataframe, `__getitem__` builds the
   filename from `suite_id`, `sample_id`, `code`, loads with `read_image`, converts to
   float in 0..1, returns `(image, long label)`.
3. Fixed along the way: file vs folder in `read_image`, string label, `value` as label
   (out of bounds), module-level test code, relative paths -> `pathlib`, missing deps.
4. Chose `code - 1` as the label: 15 contiguous classes `0..14`.
5. Wrote `MyModel` as a configurable MLP; fixed `784 -> 4096`.
6. Verified with real data: 15000 items, all files exist, batch `[4,1,64,64]` float32,
   labels `0..14`, model output `[4,15]`, initial loss about 2.7.

## 5. Status

- [x] `dataset.py`
- [x] `model.py`
- [ ] `train_single_epoch`, `eval_single_epoch`, `train_model` in `main.py`
- [ ] hyperparameter search in `main_hyperparam_optimize.py`

## Related general notes

[dl-01-pytorch-data](dl-01-pytorch-data.md) · [dl-02-pytorch-tensors](dl-02-pytorch-tensors.md) ·
[dl-03-pytorch-models-and-loss](dl-03-pytorch-models-and-loss.md) ·
[dev-01-python-env-and-paths](dev-01-python-env-and-paths.md) ·
[dl-04-training-loop](dl-04-training-loop.md) · [dev-02-git-fork-workflow](dev-02-git-fork-workflow.md) ·
[dev-03-cli-arguments](dev-03-cli-arguments.md) · [session-1](session-1.md)
