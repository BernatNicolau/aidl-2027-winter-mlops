# Fork workflow notes

Personal notes on how this workspace is set up. Kept in a separate file (not
`README.md`) so merges from the course repo never conflict with it.

## Remotes

| Name       | URL                                                       | Purpose                          |
|------------|-----------------------------------------------------------|----------------------------------|
| `origin`   | https://github.com/BernatNicolau/aidl-2027-winter-mlops   | My fork. I push my solutions here |
| `upstream` | https://github.com/upcschool-ai/aidl-2027-winter-mlops    | Course repo. I only pull from it  |

Local `main` tracks `origin/main`, so a plain `git push` goes to my fork.

### How it was set up

The repo was originally cloned from the course repo, so `origin` pointed at it.
After forking on GitHub:

```bash
git remote rename origin upstream
git remote add origin https://github.com/BernatNicolau/aidl-2027-winter-mlops.git
git fetch origin
git branch -u origin/main main     # main tracks my fork
git remote -v                      # verify
```

## Getting new sessions from the course repo

Commit (or stash) my work first, then:

```bash
git fetch upstream
git merge upstream/main     # brings in e.g. session-3/, keeps my commits
git push origin main        # update my fork on GitHub
```

Alternative: click **Sync fork** on my fork's GitHub page, then `git pull`
locally. If GitHub offers **Discard commits**, do NOT click it: it deletes my
solutions. Use **Update branch** (merge) instead.

New sessions normally add new folders, so conflicts are unlikely. If one
happens, resolve it manually; nothing is lost.

## Checking where a push will go

```bash
git remote -v         # origin = my fork
git branch -vv        # main should show [origin/main]
git push --dry-run    # prints the target URL without pushing
```

A commit is always local; only `git push` sends it anywhere. Never run
`git push upstream`.

## Session 2 dataset (Chinese MNIST)

The data is not committed (`session-2/data/` is in `.gitignore`). To download it
again, from the repo root:

```bash
mkdir -p session-2/data
curl -L --fail -o chinese-mnist.zip \
  'https://www.kaggle.com/api/v1/datasets/download/gpreda/chinese-mnist'
unzip -o -q chinese-mnist.zip -d session-2/data
rm chinese-mnist.zip
```

Resulting layout:

```
session-2/data/
├── chinese_mnist.csv                 # columns: suite_id, sample_id, code, value, character
├── chinese_mnist.tfrecords           # TensorFlow format, not used
└── data/data/input_{suite_id}_{sample_id}_{code}.jpg   # 15000 images
```

Notes:
- Images are individual JPG files; only the labels come from the CSV.
- `code` and `value` differ (e.g. `code=10`, `value=9`); the classifier needs
  labels in `0..14`.
