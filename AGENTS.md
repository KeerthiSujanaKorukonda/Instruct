# Agent instructions — groq-tldr

## What this is
A one-file CLI that summarizes a text file using Groq's hosted inference
(fast Llama models). Nothing more. Resist scope creep.

## Setup
```
pip install -r requirements.txt
cp .env.example .env   # then fill in GROQ_API_KEY
```

## Run
```
python summarize.py notes.txt
python summarize.py notes.txt --model llama-3.3-70b-versatile --bullets 5
```

## Secrets
- `GROQ_API_KEY` comes from `.env`, loaded via `python-dotenv`. Never hardcode it,
  never print it, never put it in a commit, an error message, or a log line.
- `.env` is gitignored. `.env.example` holds placeholder values only.

## Model choice
- Default model is `llama-3.1-8b-instant` because this tool optimizes for
  latency, not quality. Don't silently upgrade the default to a bigger model
  to "improve" results — ask first, since it changes cost/latency tradeoffs
  the user may be relying on.
- Model name is a CLI flag (`--model`), not a constant buried in the function.
  Groq deprecates model names occasionally — if a call fails with a model
  decommission error, that's an environment issue, not a bug in this code.

## Conventions
- Single file (`summarize.py`), stdlib argparse, no framework. Keep it that way
  unless the user asks for more than one command.
- Network calls go through the `groq` SDK, not raw `requests` — the SDK
  handles retries/rate-limit headers correctly.
- Fail loudly and specifically: if `GROQ_API_KEY` is missing, say that exact
  thing and exit non-zero. Don't let it fall through to a generic traceback.

## Testing
No test suite for a script this small. Before calling a change done, run it
against `notes.txt` and eyeball the output — check it's not truncated by
`max_tokens` and didn't silently swallow an API error.

## Out of scope (don't add without asking)
- Chunking/map-reduce for long documents
- A web UI or server
- Streaming output
- Retry/backoff logic beyond what the SDK already does
