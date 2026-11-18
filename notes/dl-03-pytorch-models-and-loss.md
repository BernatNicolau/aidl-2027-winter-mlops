# PyTorch: models and loss

## Classification loss

- `CrossEntropyLoss(logits, target)`: logits are raw scores `[B, n_classes]` (no softmax;
  it is applied inside), target is class indices `[B]` of dtype `long` in `0..n_classes-1`.
- A label outside that range gives `IndexError: Target N is out of bounds`.
- Sanity check: a randomly initialised model should start near `ln(n_classes)`
  (15 classes: about 2.71).

## Regression loss

- `MSELoss(pred, target)`: mean of squared differences; prediction and target must have
  the same shape (`[B, n_outputs]`) and a float dtype. No class indices here.
- Session 1 target: all zeros, so the loss is just the mean squared output; it starts near
  the output variance and decays towards 0 as the net learns to output 0.

## Models

- A simple start is an MLP: `Flatten -> Linear -> ReLU -> Linear(…, n_classes)`.
- The first `Linear`'s input size must equal the flattened input size, e.g.
  `channels * height * width`. Mismatch error:
  `mat1 and mat2 shapes cannot be multiplied (4x4096 and 784x128)`.
- Do not hardcode sizes: take `input_size`, `hidden_size`, `output_size` as arguments so
  they can be tuned as hyperparameters. `LazyLinear` infers the input size on the first
  forward pass, but the model has no weights until it has run once.
- The number of channels is never "checked": it is baked into the input size, and a
  wrong channel count fails with a shape error.
- Activations (`ReLU`, `Tanh`) between `Linear` layers give non-linearity; two stacked
  `Linear` layers without one collapse to a single linear map. Do not put one after the
  last layer when the loss expects raw logits / unbounded outputs.
- Define layers in `__init__` (so `model.parameters()` sees them) and wire them in
  `forward`.
- An MLP ignores 2D structure and plateaus earlier than a small CNN.
- Do not add defensive dtype/shape fix-ups in `forward` that the dataset already
  guarantees; they hide mistakes.
- Sanity-check a model by feeding one real batch and checking the output shape.
