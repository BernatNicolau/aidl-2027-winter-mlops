# Agentic coding: configuring Claude Code

How a coding agent is steered in a repo. Three mechanisms, from softest to hardest.

## 1. Instructions: `CLAUDE.md`

- A `CLAUDE.md` at the repo root is loaded into the agent's context every session. Use it
  for project facts (setup, conventions) and working rules ("guide, don't hand over
  solutions", "keep notes updated").
- It is *guidance*: the model reads it and usually follows it, but nothing enforces it.
  Gotcha seen in this repo: a rule written for "explaining a concept" was skipped on a
  short Q&A answer because the agent did not consider it an explanation. Fix: state the
  scope explicitly ("applies to every reply, including quick questions").
- Keep it short and specific; vague rules get applied inconsistently.

## 2. Memory

- Persistent per-project memory (`~/.claude/projects/<project>/memory/`): small files
  (user, feedback, project, reference) plus an index loaded each session. It stores
  preferences learnt in conversation, not things the repo already records.
- When a rule changes, update the memory too, or the old rule resurfaces.

## 3. Hooks: deterministic enforcement

- A hook is a command that the *harness* runs on an event (`PreToolUse`, `PostToolUse`,
  `Stop`, `SessionStart`, ...). Unlike CLAUDE.md or memory, it does not depend on the model
  remembering.
- Configured in `.claude/settings.json` (project, committed), `.claude/settings.local.json`
  (personal, git-ignored) or `~/.claude/settings.json` (global).
- The hook receives JSON on stdin and can answer with JSON, e.g. a `Stop` hook returning
  `{"decision": "block", "reason": "..."}` makes the agent continue and read the reason.
- **Avoid infinite loops:** when the agent continues because of a Stop hook, the next
  input has `stop_hook_active: true`; the script must exit 0 then, so it fires at most once
  per turn.
- Workflow to build one: write the command, pipe-test it with a synthetic JSON payload,
  add it to settings, validate with `jq`, then check it fires in a real turn. Settings in a
  folder that did not exist when the session started may need `/hooks` or a restart.
- A hook can remind, not judge: it cannot tell whether the agent actually taught
  something. It turns "please remember" into "you will be asked every turn".

## Example in this repo

- `.claude/hooks/notes-check.sh` + the `Stop` entry in `.claude/settings.json`: once per turn
  the agent is reminded to update the study notes. Tested with `stop_hook_active` false
  (blocks) and true (passes), and confirmed firing in a real turn.

## Keep the instructions short once a hook enforces them

- Once a hook guarantees a behaviour, the long emphasis in `CLAUDE.md` is redundant. Keep
  one plain sentence for the rule and let the hook do the enforcing; less text in the
  context and fewer places to keep in sync.

## Rule of thumb

- Preferences and context: `CLAUDE.md`. Things learnt about the user: memory. Anything that
  must happen every time: a hook.
