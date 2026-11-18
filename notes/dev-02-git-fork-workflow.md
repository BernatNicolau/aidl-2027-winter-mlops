# Git: fork + upstream

## Remotes

| Name       | URL                                                       | Purpose                           |
|------------|-----------------------------------------------------------|-----------------------------------|
| `origin`   | https://github.com/BernatNicolau/aidl-2027-winter-mlops   | My fork. I push my solutions here |
| `upstream` | https://github.com/upcschool-ai/aidl-2027-winter-mlops    | Course repo. I only pull from it  |

Local `main` tracks `origin/main`, so a plain `git push` goes to my fork.

### How it was set up

The repo was cloned from the course repo, so `origin` pointed at it. After forking:

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

Alternative: **Sync fork** on my fork's GitHub page, then `git pull`. If GitHub offers
**Discard commits**, do NOT click it: it deletes my solutions. Use **Update branch**.

New sessions normally add new folders, so conflicts are unlikely. If one happens,
resolve it manually; nothing is lost. Do not edit the course's own READMEs (that is
what causes conflicts); keep personal notes in separate files.

## Checking where a push will go

```bash
git remote -v         # origin = my fork
git branch -vv        # main should show [origin/main]
git push --dry-run    # prints the target URL without pushing
```

A commit is always local; only `git push` sends it anywhere. Never `git push upstream`.

## Ignoring files

`.gitignore` only affects untracked files. VS Code still shows ignored files in the
Explorer (dimmed); check with `git check-ignore -v <path>`.
