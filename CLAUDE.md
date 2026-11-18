# Project context for Claude

This is a student's fork of a postgraduate Deep Learning course repo (MLOps module,
`aidl-2027-winter-mlops`). The student solves each `session-N/` exercise themselves.

## How to work with me (the student)

- **Guide, don't hand over solutions.** Explain the concept, point out gotchas, give a
  skeleton or a tiny snippet, and let me write the code. Then review it by actually
  running it (shapes, dtypes, loss, DataLoader) and report results. If I explicitly ask
  you to do something ("can you do it?", "yes add"), do it.
- **Keep study notes up to date without being asked.** Notes are in two layers:
  - `notes/` holds **general knowledge by topic**, not tied to a session. Index in
    `notes/README.md`. File names are prefixed and ordered: `dl-NN-` for deep learning
    (`dl-01-pytorch-data.md`, `dl-02-pytorch-tensors.md`, `dl-03-pytorch-models-and-loss.md`) and
    `mlops-NN-` for real MLOps topics (hyperparameter tuning, experiment tracking,
    reproducibility, packaging, deployment; none yet), and `dev-NN-` for general software
    engineering (`dev-01-python-env-and-paths.md`, `dev-02-git-fork-workflow.md`). Put any concept that would still be true in another
    session here. `NN` is the reading order (data -> tensors -> models and loss; env -> git). Do not be
    limited by the existing files: create as many new topic files as needed (e.g. training
    loops, optimizers, evaluation, hyperparameter tuning, experiment tracking, Docker), give
    them the next number, split a file when it grows to cover several topics, and list
    every new file in `notes/README.md`.
    Keep the notes on **deep learning and MLOps**; do not write notes on editor
    shortcuts, VS Code or other IDE tooling.
  - `notes/session-N.md` is the study file for that exercise: goal (what the session
    asks), the data/setup, the concepts **that are new in this session**, how it was
    achieved (timeline, problems hit and fixed, verification), and a status checklist;
    it links to the general notes. The two layers do different jobs: `notes/` is the
    cumulative collection of everything learnt in the course, a session file is what is
    new in that session. **Duplication between a session file and `notes/` is intended**:
    every new concept goes in both (general wording in `notes/`, exercise context in the
    session file). **Do not duplicate between sessions**: a concept already explained in
    an earlier session file is only linked from later ones (e.g. "see session-1").
    Start the file when a session begins and keep it current.
  After explaining a concept, fixing a bug, or changing the setup, add a short factual
  entry (the rule, why, the gotcha) in the right place in the same turn, avoid duplicates,
  and tell me in one line what you updated.
  **This applies to every reply, including short answers to quick questions** ("how do I
  X?", "what does Y do?"): if the answer teaches a concept, a command or a gotcha, update
  the notes in that same turn, before finishing. Before sending any reply, check: "did I
  explain or change something? then notes updated?" Never wait to be asked.
- I'm new to torchvision, uv and Mac/VS Code, so short explanations of tooling are welcome.

## Setup facts

- macOS, VS Code. Python env: `.venv` at the repo root (`source .venv/bin/activate`),
  packages managed by `uv` from the root `pyproject.toml` (`uv sync`, `uv add <pkg>`,
  `uv run poe all` for ruff lint + format check). When adding a dependency, also add it to
  that session's `requirements.txt`.
- Git: `origin` is my fork (`BernatNicolau/aidl-2027-winter-mlops`), `upstream` is the
  course repo (`upcschool-ai/aidl-2027-winter-mlops`). New sessions come from
  `git fetch upstream && git merge upstream/main`. Never push to `upstream`, never use
  GitHub's "Discard commits". Details in `notes/dev-02-git-fork-workflow.md`.
- Do not edit the course's root `README.md` or session READMEs (merge conflicts);
  personal notes go in separate files (`notes/`).
- Do not commit or push unless I ask.
- `session-2/data/` (Chinese MNIST from Kaggle) is git-ignored. Download command is in
  `notes/session-2.md`.
- The type checker is intentionally disabled.

## Session 2 status (update as it progresses)

- `dataset.py`: done and verified (image float32 `[1,64,64]` in 0..1, label `code - 1`
  as a long tensor, 15 classes).
- `model.py`: simple MLP with configurable `input_size` / `hidden_size` / `output_size`,
  verified to output `[B, 15]`.
- To do: `train_single_epoch`, `eval_single_epoch`, `train_model` in `main.py`, then the
  hyperparameter search in `main_hyperparam_optimize.py`.
