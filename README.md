# LinkedIn Easy Apply Bot 🤖

Automatically applies to AI engineering roles on LinkedIn using the **Easy Apply** feature.

---

## What it does

- Searches LinkedIn for 9 AI engineering job titles (AI Engineer, ML Engineer, LLM Engineer, MLOps, etc.)
- Filters to **Easy Apply** jobs only
- Targets **Entry-level and Mid-level** positions
- Auto-fills common form fields: phone number, years of experience, work authorization
- Skips jobs that require cover letters or open-ended essay questions
- Logs every application to `applications.csv` so you have a full record

---

## Quick Start

### Step 1 — First-time setup

**Mac / Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
Double-click `setup.bat`

This installs the Playwright browser automation library and the Chromium browser.

---

### Step 2 — Edit your details in `config.py`

Open `config.py` and update:

```python
CONFIG = {
    "phone": "555-123-4567",     # ← Your phone number
    "years_experience": "2",     # ← Your years of experience
    "linkedin_email": "",        # ← Optional: pre-fills the login field
    "max_applications": 50,      # ← Stop after this many applications
    ...
}
```

---

### Step 3 — Run the bot

```bash
python3 linkedin_apply.py
```

A **Chrome browser window** will open and navigate to the LinkedIn login page.
**Log in manually** (the bot waits up to 2 minutes). After login, it takes over automatically.

---

## Output Files

| File | Description |
|------|-------------|
| `applications.csv` | Full log of every job attempted — title, company, URL, status |
| `bot_log.txt` | Detailed runtime log with timestamps |

### Application statuses

| Status | Meaning |
|--------|---------|
| `submitted` | ✅ Successfully applied |
| `skipped` | Skipped (cover letter required / complex question) |
| `no_easy_apply` | No Easy Apply button found |
| `timeout` | Page loaded too slowly |
| `error` | Unexpected error (see notes column) |

---

## Configuration Reference

```python
# config.py

CONFIG = {
    # Personal info
    "phone": "555-123-4567",
    "years_experience": "2",
    "linkedin_email": "",            # Optional — pre-fills email field on login

    # Application behavior
    "max_applications": 50,          # Max per session
    "delay_between_apps": (4, 10),   # Random seconds between applications

    # Work authorization
    "work_authorization": "Yes",
    "require_sponsorship": "No",

    # Location — leave empty for "open to anything"
    "location": "",

    # Skip logic
    "skip_if_cover_letter_required": True,
    "skip_if_complex_questions": True,

    # Browser visibility
    "headless": False,               # False = visible browser (recommended)
}
```

---

## Tips

- **Run in short sessions** — 25–50 applications per session looks more natural to LinkedIn.
- **Check `applications.csv`** after each run to see what was applied to.
- **Re-run anytime** — the bot won't re-apply to jobs where LinkedIn shows "Applied".
- If you get a **CAPTCHA**, just solve it manually — the bot will wait.
- If LinkedIn asks a question the bot doesn't recognize, it skips that job to be safe.

---

## Important Notes

> ⚠️ **LinkedIn's Terms of Service** discourage automated activity on their platform. Use this tool responsibly:
> - Keep `max_applications` reasonable (25–50 per session)
> - Don't run it continuously 24/7
> - Review the `applications.csv` log to make sure applications look correct

---

## Troubleshooting

**"No listings found"** — LinkedIn may have changed its HTML structure. Try running the bot and watching the browser window to see what's happening.

**Bot stuck on a step** — It will automatically skip after 15 steps and move to the next job.

**Login timeout** — Make sure you log in within 2 minutes of the browser opening.

**ImportError for playwright** — Run `pip3 install playwright` and `python3 -m playwright install chromium` again.
