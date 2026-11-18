#!/usr/bin/env bash
# Stop hook: once per turn, remind Claude to keep the study notes up to date.
# stop_hook_active is true when Claude is already continuing because of this hook,
# so the second stop is allowed and there is no infinite loop.
input=$(cat)
if [ "$(printf '%s' "$input" | jq -r '.stop_hook_active // false')" = "true" ]; then
  exit 0
fi
jq -n '{decision: "block", reason: "Notes check: did you explain a concept, fix a bug, review code or change setup this turn? If yes and notes/ + notes/session-N.md are not updated yet, update them now (topic file + session file + notes/README.md index), then tell the user in one line what you updated. If nothing needs a note, just say so briefly and finish."}'
