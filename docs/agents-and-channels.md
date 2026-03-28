# Agents and channels recommendations

For full-stack projects, a small fixed set of agents is usually better than an overgrown matrix.

## Suggested agent split

- `main` — general planning, orchestration, triage
- `frontend` — UI, UX, component work, browser-facing flows
- `backend` — APIs, data, services, infra-adjacent backend work
- `reviewer` — code review, risk review, architecture sanity checks

## Why this split works

- It matches the way most engineering work gets divided
- It avoids constant model/context switching in one session
- It keeps thread bindings useful in Discord or Slack
- It is simple enough to understand after a month away

## Channel suggestions

### Discord

Good for:

- thread-bound work
- lightweight orchestration
- team-visible progress

Recommended pattern:

- one main bot account
- require mention in group channels
- use threads for task-focused work
- keep DMs on pairing mode

### Telegram or Signal

Good for:

- direct personal access
- quick notes and reminders
- low-friction mobile access

### Web / local UI

Good for:

- onboarding
- config edits
- session inspection

## Recommendation

Start with one channel first, then add more only when the routing problem is real.
A clean routing model beats a feature-rich but confusing setup.
