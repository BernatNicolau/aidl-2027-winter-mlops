# PyTorch: the training loop

## The five steps per batch

```python
for x, y in dataloader:
    x, y = x.to(device), y.to(device)   # data and model must be on the same device
    optimizer.zero_grad()                # 1. clear old gradients
    y_ = model(x)                        # 2. forward pass
    loss = criterion(y_, y)              # 3. loss
    loss.backward()                      # 4. gradients (backprop)
    optimizer.step()                     # 5. update weights
```

- Gradients **accumulate** in `.grad` on every `backward()`. Without `zero_grad()` each
  step uses the sum of all previous gradients, so training diverges or behaves oddly.
- `optimizer = SGD(model.parameters(), lr=...)`: it must be given the parameters
  (`model.parameters()`), and it is created after the model is on its device.
- Epoch = one full pass over the dataset; step = one batch. Steps per epoch =
  `ceil(n_samples / batch_size)`.

## Logging the loss

- `loss` is a tensor attached to the graph; use `loss.item()` to get a Python float.
  Appending `loss` itself keeps the whole graph alive (memory leak).
- Keep two things: a per-step list (for a curve) and a per-epoch average
  (`epoch_loss / n_batches`) for printing. A noisy per-step curve is normal with
  small batches.
- With a smaller last batch, a plain mean of batch losses is slightly biased; weight by
  batch size if it matters (relevant once you add validation).
- `matplotlib`: `plt.plot(history)`, then `plt.show()`. Headless runs (no display):
  `MPLBACKEND=Agg python script.py` (it only warns that `show()` does nothing).

## Choosing the device

```python
if torch.cuda.is_available():            device = torch.device("cuda")
elif torch.backends.mps.is_available():  device = torch.device("mps")   # Apple Silicon
else:                                    device = torch.device("cpu")
```

- On a Mac the GPU backend is `mps`, not `cuda`. A plain `cuda`-or-`cpu` check silently
  leaves the Mac GPU unused.
- `model.to(device)` moves the parameters in place; tensors need `x = x.to(device)`
  (it returns a new tensor).

## Learning rate and convergence

- `lr` is the most sensitive hyperparameter. Too high: loss oscillates or becomes `nan`;
  too low: the loss moves very slowly.
- Quick experiment (session 1, regression to 0): `lr=0.1, 5 epochs` went from loss
  0.029 to 0.010; `lr=0.01` with 100k samples (1000 steps per epoch) reached 0.0007 in
  3 epochs, because more steps also means more progress. Both `lr` and the number of
  steps matter.
- This kind of comparison is exactly what hyperparameter tuning automates.
