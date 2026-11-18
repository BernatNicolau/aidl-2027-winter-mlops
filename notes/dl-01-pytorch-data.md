# PyTorch: data loading

## Package name

- **`import torch`, not `import pytorch`.** PyTorch is the project name; `torch` is
  the Python package (a holdover from the old Lua "Torch"). `pip install torch`;
  with conda the package is called `pytorch`, but you still `import torch`.

## `Dataset` and `DataLoader`

- A *map-style* dataset needs `__getitem__(idx)` (returns **one** sample) and
  `__len__()` (number of samples). `DataLoader` uses both: the sampler picks
  indices (shuffling happens there), then `__getitem__` is called per index and
  the results are stacked into a batch.
- You rarely call it by name: `dataset[0]` is the same as `dataset.__getitem__(0)`;
  `len(dataset)` calls `__len__`. (`dataset.__getitem__[0]` is wrong: it is a method.)
- Load data **lazily** in `__getitem__` (one item per call), not in `__init__`.
  Memory stays small and `DataLoader(num_workers=...)` can parallelise it.
- `IterableDataset` (`__iter__` instead of `__getitem__`) is for streams where random
  access makes no sense.
- Every sample must have the same shape and type, otherwise the batch cannot be stacked.
- Code at module level in a file runs on every import. Keep test code under
  `if __name__ == "__main__":` or remove it.

## Images with torchvision

- `torchvision.io.read_image(path)` loads **one** file into a `uint8` tensor `[C, H, W]`.
  It is annotated `path: str`; a `Path` happens to work, `str(path)` is the supported form.
- `torchvision.datasets.ImageFolder` expects one subfolder per class; it does not fit a
  flat folder with labels in a CSV, so write your own `Dataset`.
- Use pandas only for the CSV (labels); images are loaded per sample.
- A string label cannot be put in a tensor; map it to an integer class index first
  (see [dl-02-pytorch-tensors.md](dl-02-pytorch-tensors.md) for dtypes).
