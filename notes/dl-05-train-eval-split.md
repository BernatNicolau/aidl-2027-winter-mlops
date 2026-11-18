# Train / validation split and evaluation

## Why split

- Training loss only says how well the model fits data it has seen. A held-out
  **validation** set measures generalisation and is what hyperparameter tuning minimises
  (e.g. `val_loss`). Never tune on the training numbers.

## Splitting a `Dataset`

```python
n_val = int(0.2 * len(ds))
train_ds, val_ds = torch.utils.data.random_split(
    ds, [len(ds) - n_val, n_val], generator=torch.Generator().manual_seed(42)
)
```

- `random_split` returns two `Subset`s that share the original dataset (no copy).
- Pass a seeded `generator`, otherwise every run gets a different split and results of
  different runs (or different hyperparameters) are not comparable.
- `random_split` takes any number of sizes, so a third (test) split is one more entry:
  `[n_train, n_val, n_test]`.
- Sizes must add up to `len(ds)`; compute the train size as `len(ds) - n_val` to avoid
  rounding errors.

## DataLoaders

- Split first, then build one `DataLoader` per split (one loader over the whole dataset
  cannot shuffle only the train part). The loaders are passed to the train / eval
  functions, not the dataset.
- A `DataLoader` is a batch iterator, not something to split: `random_split` works on a
  `Dataset` (returns `Subset`s). Splitting after batching, or shuffling across the whole
  dataset, lets validation samples leak into training.
- A `DataLoader` is an **iterable over batches**, not a tensor or a list: `for x, y in loader`
  yields `x` `[B, 1, 64, 64]` float32 and `y` `[B]` long. `len(loader)` = number of batches
  (`ceil(n / batch_size)`); `len(loader.dataset)` = number of samples (needed to weight the
  epoch average).
- `shuffle=True` for **train** only; validation needs no shuffling.
- `batch_size` is a hyperparameter: put it in `config`, not hardcoded.
- `num_workers=N` loads batches in parallel processes. Helps when `__getitem__` is slow
  (reading a JPG + a pandas `.iloc` lookup per item); on CPU-only runs an epoch can be
  slow without it.

## Evaluation loop

- `model.eval()` switches layers like dropout / batch-norm to inference behaviour. Call
  `model.train()` again at the start of each training epoch.
- Wrap the loop in `with torch.no_grad():` (no graph, less memory, faster). No
  `zero_grad`, `backward` or `step`.
- Forgetting either does not crash; it only gives wrong numbers and wastes memory.
- Return the mean loss and the accuracy for the whole set.

## Averaging the epoch loss

- Batches can have different sizes (the last one is smaller). Accumulate
  `loss.item() * batch_size` and divide by the number of samples, instead of averaging
  batch means.
- `utils.accuracy(true_labels, logits)` takes raw logits (it does `argmax` itself) and
  labels; average it the same way, weighted by batch size.

## Quick test settings

- While debugging use few epochs (3-5), not 100: check that the loss goes down and the
  shapes are right before spending time on long runs.
- Each hyperparameter you want to tune (`lr`, `batch_size`, `hidden_size`, `epochs`) must
  be in the `config` dict so a search tool can vary it
  (see [dl-04-training-loop.md](dl-04-training-loop.md)).
