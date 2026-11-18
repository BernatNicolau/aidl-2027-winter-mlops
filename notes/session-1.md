# Session 1 notes

Self-contained study notes for this session. Concepts are repeated in the general notes
(index: [README.md](README.md)) and kept here in the context of the exercise.

## 1. Goal

From the session README: a **minimal PyTorch project** with a custom dataset, a custom
model and a training function. The task is to map random normal noise to 0 (a toy
regression, so the whole pipeline can be learnt without data-handling noise).

| File | What it does |
|---|---|
| `dataset.py` | `MyDataset(n_samples, n_features, n_outputs)`: `data = torch.randn(n_samples, n_features)`, `labels = torch.zeros(n_samples, n_outputs)`, `__len__`, `__getitem__` |
| `model.py` | `MyModel(n_features, n_hidden, n_outputs)`: `Linear -> Tanh -> Linear -> Tanh -> Linear` |
| `main.py` | `argparse` arguments, device selection, `DataLoader`, `MSELoss` + `SGD`, training loop, loss plot |
| `requirements.txt` | `torch`, `matplotlib` |

Run (from the repo root, with `.venv` active):

```bash
python session-1/main.py
python session-1/main.py --n_samples 100000 --n_features 10 --n_hidden 20 --n_outputs 5 --epochs 10 --batch_size 100 --lr 0.01
```

## 2. Concepts as applied here

- **Dataset**: `__getitem__` returns one `(x, y)` pair, `DataLoader` stacks them into
  batches `[B, n_features]` and `[B, n_outputs]`. Everything is in memory because it is
  synthetic. See [dl-01-pytorch-data.md](dl-01-pytorch-data.md).
- **Model**: layers defined in `__init__`, wired in `forward`. Tanh between the linear
  layers for non-linearity; no activation after the last one (unbounded regression
  output). See [dl-03-pytorch-models-and-loss.md](dl-03-pytorch-models-and-loss.md).
- **Loss**: `MSELoss` because the target is a float vector (not class indices), same
  shape as the output.
- **Training loop**: `zero_grad -> forward -> loss -> backward -> step` on every batch,
  `loss.item()` logged per step and averaged per epoch.
  See [dl-04-training-loop.md](dl-04-training-loop.md).
- **Device**: CUDA, else Apple `mps`, else CPU; both the model and each batch are moved
  with `.to(device)`.
- **CLI arguments**: all hyperparameters (`--lr`, `--epochs`, `--batch_size`, sizes) come
  from `argparse`, so experiments need no code edits.
  See [dev-03-cli-arguments.md](dev-03-cli-arguments.md).
- **Environment**: the README suggests conda or venv; this repo uses `.venv` + `uv`
  (see [dev-01-python-env-and-paths.md](dev-01-python-env-and-paths.md)).

## 3. How it was achieved / verification

- Code runs with the default arguments and with the README's debug configuration.
- Default run (`1000` samples, `lr=0.1`, 5 epochs): average loss
  0.0293 -> 0.0205 -> 0.0154 -> 0.0120 -> 0.0097, decreasing every epoch.
- README config (`100000` samples, `lr=0.01`, `batch_size=100`, 3 epochs):
  0.0091 -> 0.0016 -> 0.0007.
- Ran headless with `MPLBACKEND=Agg` (only a "cannot show" warning from `plt.show()`).
- Takeaway: with the same code, `lr`, dataset size and epochs change the result a lot;
  this motivates session 2 (hyperparameter tuning).

## 4. Status

- [x] `dataset.py`
- [x] `model.py`
- [x] `main.py` (training loop, loss plot)
- [x] Verified loss decreases
- [x] Notes written
