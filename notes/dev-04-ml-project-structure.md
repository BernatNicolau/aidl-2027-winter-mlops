# Structuring an ML training project (industry standard)

## Separation of concerns

| Piece | Where | Notes |
|---|---|---|
| `Dataset` class, transforms | `dataset.py` / `data.py` | knows how to read one sample |
| Loader factory | same data module: `get_dataloaders(config)` | builds the dataset, splits it, returns `train_loader`, `val_loader` (and `test_loader`) |
| Model | `model.py` | `nn.Module`, sizes as constructor arguments |
| Train / eval functions | `train.py` / `main.py` | `train_one_epoch`, `evaluate`, and a `train_model(config)` that wires everything |
| Entry point | `if __name__ == "__main__":` or a CLI | reads the config and calls `train_model` |
| Config | dict / dataclass / YAML / `argparse` (Hydra in bigger projects) | no hardcoded hyperparameters or paths |

- A separate `dataloader.py` is not the convention: `DataLoader(...)` is one line. What is
  standard is a **factory function** in the data module, so the training code never knows how
  the data is split or shuffled.
- PyTorch Lightning formalises it as a `LightningDataModule` (`setup`, `train_dataloader`,
  `val_dataloader`, `test_dataloader`).
- Whatever the file layout, the order is: dataset -> split -> one loader per split.

## Passing configuration to the data module

- Information flows one way: `main` -> function arguments. The data module never imports
  `main` (it would be a circular import, since `main` imports the data module) and does not
  read a global config.
- Tunable values (`batch_size`, later `lr`, `hidden_size`) are **arguments**, passed from
  `config` by the caller; a hardcoded module-level `batch_size` cannot be varied by a search
  tool such as Ray.
- Fixed design choices (split ratios, seed) are **defaults** in the signature, and only go in
  `config` when you want to override them:

```python
def get_dataloaders(images_path, labels_path, batch_size=64,
                    val_ratio=0.15, test_ratio=0.15, seed=42): ...
```

## Train / validation / test

- Industry projects hold out a third set, **test**, used once at the end to report the final
  number. Validation is for tuning (hyperparameters, early stopping); if you tune on the test
  set it stops being an honest estimate.
- The course exercises only have train and validation; keep the distinction in mind.

## Reproducibility basics

- Seed the split (`generator=...manual_seed(...)`), and put every tunable value in the config
  so a run can be reproduced and a search tool can vary it.

## Exercise vs standard

- Course skeletons are minimal and leave some decisions open (e.g. session 2 does not say where
  the `DataLoader`s are built). Where it is open, use the standard shape above; where the
  skeleton is explicit and differs, follow it to complete the exercise but say which one you
  are using.
