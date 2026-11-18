# Command-line arguments with argparse

- `argparse` turns `python main.py --lr 0.01 --epochs 10` into an `args` object, so
  hyperparameters are changed without editing the code.

```python
parser = argparse.ArgumentParser()
parser.add_argument("--lr", help="learning rate", type=float, default=0.1)
args = parser.parse_args()
args.lr
```

- Always set `type=` (arguments arrive as strings) and a `default`, so the script runs with
  no flags. `--n_hidden` becomes `args.n_hidden`.
- `python main.py --help` prints every option with its `help` text for free.
- Keep argument parsing in `main()` under `if __name__ == "__main__":`, and have the
  rest of the code take plain parameters. Then the same functions can be called
  from another script (e.g. a hyperparameter search passing a `config` dict).
- This is a first step towards reproducibility: the arguments used for a run are
  explicit and can be logged next to its results.
