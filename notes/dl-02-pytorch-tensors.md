# PyTorch: tensors, dtypes and reshaping

## dtypes: inputs vs labels

| | dtype | why |
|---|---|---|
| input image | `float32`, usually scaled to 0..1 | goes through the model's float weights |
| class label | `long` (int64) class index | used as an index to pick the correct class in the loss |

- `read_image` returns `uint8`. Convert with `.float() / 255.0` (divide by 255, not the
  image's own max).
- Make a label explicit with `torch.tensor(label, dtype=torch.long)`. A numpy int also
  works because `DataLoader` converts it, but the explicit form is clearer.

## Reshaping: `flatten`, `view`, `reshape`

- `torch.flatten(x, start_dim=1)`, `x.view(x.size(0), -1)` and `x.reshape(x.size(0), -1)`
  all give `[B, C*H*W]` from `[B, C, H, W]`. `torch.nn.Flatten()` is the same as a layer.
- `x.size(0)` keeps the batch dimension; `-1` means "compute this one so the number of
  elements stays the same" (only one `-1` per call).
- `x.view(-1)` flattens the batch too: a classic bug.
- `view` never copies and needs contiguous memory; `reshape` copies if needed.
  After `permute`/`transpose`, use `reshape` or `.contiguous().view(...)`.
- `view`/`reshape` keep element **order**; to swap axes use `permute`/`transpose`.
- Other uses: splitting heads in attention, `[B, T, ...] -> [B*T, ...]`, vector back to
  image, aligning shapes. `view_as(other)` reshapes to another tensor's shape, e.g.
  `true_labels.view_as(preds)` so `[B,1]` vs `[B]` does not broadcast to `[B,B]`.
