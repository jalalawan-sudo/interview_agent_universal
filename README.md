# 🎙️ Interview Agent Universal

**Real-time AI co-pilot for high-stakes conversations.**  
Transcribes live audio, surfaces talking points as you speak, and adapts to your professional profile — all running 100% locally on your machine.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey?logo=flask)](https://flask.palletsprojects.com)
[![Claude](https://img.shields.io/badge/Powered%20by-Claude%20Sonnet-orange)](https://anthropic.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Chrome](https://img.shields.io/badge/Browser-Chrome%20required-yellow?logo=googlechrome)](https://www.google.com/chrome/)

---

## What it does

You are in an investor call, a job interview, a board meeting, a negotiation. Someone asks a question. The Agent is listening — and before you even finish thinking, it has surfaced three precise, evidence-backed talking points drawn from your own professional background and the session briefing you set up.

No notes to flip through. No mental blanks. Just the right thing to say, right when you need it.

---

## Setup — two commands

```bash
git clone https://github.com/jalalawan-sudo/interview_agent_universal.git
cd interview_agent_universal
python run.py
```

A browser window opens. Enter your [Anthropic API key](https://console.anthropic.com/settings/keys). Done.

> **Requires Google Chrome** for the Web Speech API (microphone transcription).  
> Your API key is saved to a local `.env` file and never leaves your machine.

---

## Features

| Feature | Description |
|---|---|
| **Real-time transcription** | Chrome Web Speech API — no third-party transcription service |
| **Append-only talking points** | Responses accumulate; good content is never overwritten |
| **Tick / cross feedback** | Mark each bullet as useful or not — Claude learns and adapts per session |
| **Briefing sessions** | Paste topic background, financials, legislation — set as active context |
| **Source attachments** | Attach PDFs, DOCX files, or scrape URLs directly into a briefing |
| **Professional profile** | Upload your CV/resume — Claude synthesizes a structured profile used in every session |
| **History panel** | Scroll back through all talking points from the current session |
| **Post-call summaries** | One-click summary of the full session, saved per briefing |
| **Space bar trigger** | Manual assist mode — press Space to get talking points on demand |
| **100% local** | Flask app on `localhost:5055`. No cloud, no data leaving your machine |

---

## How it works

```
You speak  →  Chrome Web Speech API  →  transcript panel
                                              ↓
                              (every natural pause, ~600ms)
                                              ↓
                         POST /assist-stream  →  Claude Sonnet
                                              ↓
                     Talking points stream into the center panel
                         (append-only — never overwrites previous)
```

On each assist call, only the **new speech since the last call** is sent to Claude — not the full transcript. This keeps responses focused and avoids repetition.

---

## First run walkthrough

1. `python run.py` opens the browser automatically
2. **Setup page**: enter your Anthropic API key — it is verified and saved to `.env`
3. **Profile tab**: upload your CV, resume, or bio — Claude generates a structured profile in ~15 seconds
4. **Briefings tab**: create a named session, paste topic notes, attach PDFs or URLs, set as Active
5. **Live Session tab**: click Start, begin speaking — talking points appear in real time

---

## Project structure

```
interview_agent_universal/
├── app.py              # Flask backend — all routes, Claude API, security
├── run.py              # Smart launcher — installs deps, starts server, opens browser
├── requirements.txt    # Pinned Python dependencies
├── .env.example        # Template for API key
├── .gitignore          # Excludes .env, profile.json, __pycache__
└── templates/
    ├── index.html      # Main app UI (~1100 lines, all CSS/JS inlined)
    └── setup.html      # First-run setup page
```

---

## Security

- API key stored in local `.env` only — validated against Anthropic on first entry
- Server binds to `127.0.0.1` only — not exposed to your network
- SSRF protection blocks all private/loopback IPs on URL scraping
- File uploads: extension whitelist (PDF, DOCX, TXT), 20 MB cap, `secure_filename`
- Rate limiting per IP on all API-calling endpoints (30 req/min)
- Security headers on every response (`X-Frame-Options`, `X-Content-Type-Options`, etc.)
- `profile.json` and `.env` are `.gitignore`d — safe to fork without leaking personal data

---

## Configuration

| Variable | Default | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | *(required)* | Set in `.env` via setup page |
| Port | `5055` | Hardcoded in `app.py` — change if needed |
| Model | `claude-sonnet-4-6` | Edit `MODEL` constant in `app.py` |

---

## Contributing

PRs welcome. Keep it focused — this is a tool optimized for real-time use, not a platform.  
Open an issue before large changes.

---

## License

MIT — use it, fork it, build on it.

---

*Built with [Claude Code](https://claude.ai/code)*
