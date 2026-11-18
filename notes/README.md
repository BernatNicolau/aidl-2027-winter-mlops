# Notes index

All study notes live in this folder, in two layers that do different jobs:

- Topic files (`dl-`, `mlops-`, `dev-`, `agent-`) are the cumulative collection of everything
  learnt in the course, not tied to a session.
- Per-session files (`session-N.md`) hold the goal, the concepts that are **new in that
  session**, how it was solved, and status.

Content is intentionally duplicated between a session file and the topic files, but never
between sessions: a later session links to the earlier one instead of repeating it.

File prefixes: `dl-` = deep learning, `mlops-` = MLOps (tuning, tracking, reproducibility,
deployment), `dev-` = general software engineering (environments, git), `agent-` = agentic / LLM-assisted coding (Claude Code configuration, hooks), `session-` =
per-session notes. The number after `dl-`/`mlops-`/`dev-` is the suggested reading
order (data -> tensors -> models and loss; environment -> git). New topics get as many new
files as needed; the next topic takes the next number, and files are renumbered only when
the order really matters.

## Deep learning

- [dl-01-pytorch-data.md](dl-01-pytorch-data.md): `torch`, `Dataset`/`DataLoader`, loading images with torchvision
- [dl-02-pytorch-tensors.md](dl-02-pytorch-tensors.md): dtypes for inputs vs labels, `flatten`/`view`/`reshape`
- [dl-03-pytorch-models-and-loss.md](dl-03-pytorch-models-and-loss.md): `CrossEntropyLoss`, `MSELoss`, sizing an MLP, activations
- [dl-04-training-loop.md](dl-04-training-loop.md): the five steps per batch, `zero_grad`, logging loss, device (`mps`), learning rate

- [dl-05-train-eval-split.md](dl-05-train-eval-split.md): `random_split` with a seed, train vs validation loaders, `eval()` / `no_grad`, weighted averages

## Agentic coding

- [agent-01-claude-code-config.md](agent-01-claude-code-config.md): `CLAUDE.md` vs memory vs hooks, Stop hook, avoiding loops

## Development basics

- [dev-01-python-env-and-paths.md](dev-01-python-env-and-paths.md): `.venv`, `uv`, `requirements.txt`, relative paths, `pathlib`
- [dev-02-git-fork-workflow.md](dev-02-git-fork-workflow.md): fork + upstream, getting new sessions, pushing safely
- [dev-03-cli-arguments.md](dev-03-cli-arguments.md): `argparse`, configurable scripts
- [dev-04-ml-project-structure.md](dev-04-ml-project-structure.md): where dataset, loaders, model, train loop and config live; train/val/test

## Per-session notes

- [session-1.md](session-1.md): minimal PyTorch project, noise-to-zero regression, first training loop
- [session-2.md](session-2.md): custom Chinese MNIST dataset, MLP, hyperparameter tuning
