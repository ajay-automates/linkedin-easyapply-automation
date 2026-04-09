# LinkedIn Easy Apply Bot 🤖

**Automatically apply to jobs on LinkedIn with one click!**

This bot helps you apply to **ANY job** you want on LinkedIn using the **Easy Apply** feature. Instead of manually clicking through dozens of applications, the bot does it for you automatically.

---

## What It Does

✅ Searches LinkedIn for **any job titles you choose**  
✅ Applies to jobs automatically using **Easy Apply** (no lengthy applications)  
✅ **Auto-fills common questions** like phone number, experience, and work authorization  
✅ **Skips difficult applications** (cover letters, essay questions, etc.)  
✅ **Keeps a log** of every application in `applications.csv`  
✅ Works with **any job type** — tech, marketing, sales, design, etc.

**In short:** You set your job preferences once, and the bot applies to 50+ jobs in the time it would take you to apply to 2-3 manually.

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

### Step 2 — Create and customize `config.py`

**First time?** Copy the template:
```bash
cp config.example.py config.py
```

Then **open `config.py`** with any text editor (Notepad, VS Code, etc.) and update YOUR information:

#### 🔹 **Your Personal Details** (Required)
```python
CONFIG = {
    "phone": "YOUR_PHONE_NUMBER",        # ← Enter your phone number
    "years_experience": "2",             # ← Your years of experience (e.g., "5", "10")
    "linkedin_email": "your@email.com",  # ← Optional: your LinkedIn email
    ...
}
```

#### 🔹 **What Jobs to Apply For** (UPDATE THIS!)
```python
SEARCH_QUERIES = [
    "Software Engineer",        # ← Change to jobs YOU want!
    "Data Scientist",           # ← Add as many as you want
    "Product Manager",
    "Graphic Designer",
    # Examples: "Sales Manager", "Nurse", "Marketing", "Accountant", etc.
]
```

#### 🔹 **Job Filters** (Customize for your preferences)
```python
"location": "",                          # Leave empty for any location, or type "New York", "Remote", etc.
"work_authorization": "Yes",            # "Yes" if you need sponsorship, "No" if you're authorized
"require_sponsorship": "No",            # "Yes" or "No" — set based on your visa status
"max_applications": 50,                 # How many jobs to apply to per session
"skip_if_cover_letter_required": True,  # Skip jobs asking for essays? True = yes, False = no
```

---

### Step 3 — Run the Bot

Open your terminal/command prompt and type:

**Mac / Linux:**
```bash
python3 linkedin_apply.py
```

**Windows:**
```bash
python linkedin_apply.py
```

#### What happens next:
1. A **Chrome browser window** opens automatically
2. You'll see the **LinkedIn login page**
3. **You log in manually** (takes 30 seconds) — the bot waits up to 2 minutes
4. **Once logged in, the bot takes over** and automatically applies to jobs
5. Watch the browser or check `applications.csv` to see progress
6. After applying to your max number of jobs, it stops automatically

**That's it!** Go make a coffee ☕ while the bot works for you.

---

## 📊 Output & Results



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

---

## Complete Configuration Guide

Here's **every setting** you can customize in `config.py`:

### 📋 **Personal Information** (REQUIRED)

```python
CONFIG = {
    "phone": "555-123-4567",           # Your phone number (needed for applications)
    "years_experience": "2",           # How many years? Use: "0", "1", "2", "5", "10", etc.
    "linkedin_email": "you@email.com", # Optional: skips typing email at login
}
```

### 🎯 **Job Search Settings** (IMPORTANT - UPDATE THIS!)

```python
# What job titles to search for (you can add unlimited)
SEARCH_QUERIES = [
    "Software Engineer",        # Change to YOUR job titles
    "Product Manager",          # Examples: "Nurse", "Teacher", "Marketing", etc.
    "Data Analyst",
]

# Experience level filter (LinkedIn values)
EXPERIENCE_LEVELS = "1%2C2%2C3"  # 1=Internship, 2=Entry, 3=Associate, 4=Mid-Senior
                                 # %2C = comma, so this means: Entry, Associate, Mid-Senior

# Job type filter
JOB_TYPE = "F"  # F=Full-time, C=Contract, P=Part-time, T=Temp, I=Internship, V=Volunteer

# How recent the job posting should be
DATE_POSTED = "r86400"  # r86400=past 24h, r604800=past week, r2592000=past month
```

### ⚙️ **Application Behavior**

```python
# How many jobs to apply to per session
"max_applications": 50,

# Random wait between applications (in seconds)
# Set to (3, 8) to wait randomly between 3-8 seconds
"delay_between_apps": (4, 10),

# Auto-skip certain jobs?
"skip_if_cover_letter_required": True,   # Skip essays? True=yes, False=no
"skip_if_complex_questions": True,       # Skip tricky questions? True=yes, False=no
```

### 📍 **Work Authorization & Location**

```python
# Work authorization
"work_authorization": "Yes",    # "Yes" if authorized, "No" if needs visa
"require_sponsorship": "No",    # "Yes" if visa needed, "No" if already authorized

# Location preference
"location": "",                 # Leave empty for any location
                                # Or type: "San Francisco", "Remote", "New York", etc.
```

### 🔧 **Advanced Settings**

```python
# Show the browser while it works?
"headless": False,  # False=see it work (recommended), True=hidden/invisible
```

---

## Examples: How to Update for Your Situation

### Example 1: Looking for Marketing Jobs Anywhere
```python
SEARCH_QUERIES = [
    "Marketing Manager",
    "Digital Marketing",
    "Content Manager",
]
"location": "",  # Any location
"max_applications": 75  # Apply to more jobs
```

### Example 2: Seeking Remote Tech Jobs Only
```python
SEARCH_QUERIES = [
    "Software Engineer",
    "Full Stack Developer",
]
"location": "Remote"  # Only remote jobs
```

### Example 3: Recent Graduate - Any Entry-Level Job
```python
SEARCH_QUERIES = [
    "Associate",
    "Coordinator",
    "Junior Analyst",
    "Intern",
]
"years_experience": "0"  # Fresh out of school
```

---

## 💡 Pro Tips

### Getting the Most Out of the Bot

✅ **Run in shorter sessions** — Instead of applying to 500 jobs at once, run 2-3 sessions of 25-50 applications. LinkedIn notices patterns, so shorter sessions = safer.

✅ **Check your applications** — After each run, open `applications.csv` to see:
  - Which companies you applied to
  - Job titles
  - Whether it succeeded or had issues

✅ **Won't re-apply twice** — If you run the bot again, it automatically skips jobs you already applied to (LinkedIn shows "Applied" on those).

✅ **If you see a CAPTCHA** — The bot will pause and wait for you to solve it manually. Just solve it and continue.

✅ **The bot skips tricky questions** — If LinkedIn shows a question the bot doesn't understand, it skips that application to be safe. You can review these later and apply manually if you want.

✅ **Change settings between runs** — Want to search different job titles next time? Just edit `config.py` and run again!

### Finding the Right Job Titles

**Don't know what to search for?**  Go to LinkedIn.com, search for jobs YOU want, and look at the titles you see. Copy those exact titles into `SEARCH_QUERIES`.

Examples:
- Looking for design work? Try: "UX Designer", "Graphic Designer", "UI Designer"
- Looking for sales? Try: "Sales Manager", "Account Executive", "Business Development"
- Looking for creative roles? Try: "Content Writer", "Video Producer", "Copywriter"

---

## ⚠️ Important Notes

### What is "Easy Apply"?

**Easy Apply** is a LinkedIn feature that lets you apply to a job in seconds (just 1 click!). The company gets:
- Your LinkedIn profile
- Any answers you give to quick questions
- Your phone number / location (if you fill them in)

This bot **only applies to Easy Apply jobs**. It does NOT:
- Bypass LinkedIn security
- Hack or access private information
- Spam or flood LinkedIn
- View content you're not allowed to see

### Use Responsibly ⚖️

LinkedIn's Terms of Service don't encourage automated applications, but this bot uses the official Easy Apply feature (the same one you'd use manually). To stay safe:

✅ **DO:**
- Run in **short sessions** (25-50 jobs at a time)
- **Wait a few hours** between sessions
- **Review** the `applications.csv` to make sure it's applying to real jobs
- **Adjust your search terms** if you're not getting matches

❌ **DON'T:**
- Run 500+ applications in one session
- Run the bot 24/7 continuously
- Apply to obviously wrong jobs (easy apply filtering won't catch everything)
- Lie on your applications (resume mismatch = automatic rejection)

### Data Privacy

✅ Your login credentials are **NOT saved or stored**  
✅ Your personal data is **ONLY sent to LinkedIn** (the company you're applying to)  
✅ No tracking, no telemetry, no ads — it's just automation  
✅ The `applications.csv` file is **stored locally on your computer only**

---

## 🆘 Troubleshooting

### Common Issues & Fixes

| **Problem** | **Solution** |
|-----------|-----------|
| **Bot doesn't start** | Make sure you ran `setup.sh` (Mac/Linux) or `setup.bat` (Windows) first. This installs required software. |
| **"No such file: config.py"** | You need to copy the template: `cp config.example.py config.py`, then edit it. |
| **Bot applies to wrong jobs** | Check your `SEARCH_QUERIES` in config.py — make sure the job titles are correct. |
| **LinkedIn login timeout** | You have 2 minutes to log in. If it times out, just run the bot again. |
| **"ImportError: No module named playwright"** | Run: `pip3 install -r requirements.txt` |
| **Bot sees CAPTCHA** | Solve it manually — the bot will wait and continue automatically. |
| **Bot gets stuck on a job** | It automatically skips after 15 seconds and moves to the next job. |
| **Nothing in applications.csv** | It might have applied to 0 jobs (no matches). Try different search terms or broader filters. |

### Still Stuck?

1. **Watch the browser window** — See what the bot is doing. This usually shows what's wrong.
2. **Check `bot_log.txt`** — Open it to see detailed error messages.
3. **Try different job titles** — Your search terms might not match any LinkedIn jobs.
4. **Make sure LinkedIn is working** — Try applying to a job manually first to confirm LinkedIn is accessible.

---

## 🚀 Next Steps

### After Your First Run

1. **Check `applications.csv`** — See which jobs you applied to ✅
2. **Monitor your LinkedIn inbox** — Companies will start reaching out! 📧
3. **Run again** — Customize your search and apply to more jobs 🔄

### Tips for Success

- **Speed matters** — The faster you apply, the better. Most companies look at applications in the order they receive them.
- **Be picky with job titles** — A well-targeted search (5-10 job titles) beats a scattered approach (50+ random titles).
- **Check your profile** — Make sure your LinkedIn profile is complete and up-to-date. This is what companies see.
- **Personalize when possible** — While the bot handles Easy Apply, some jobs might need cover letters. Don't skip those if you're interested!

---

## ❓ Questions?

- **How to customize more?** → Read the `config.example.py` comments for detailed explanations
- **What if it doesn't work?** → Check the Troubleshooting section above or review `bot_log.txt`
- **Can I modify the code?** → Yes! This is open-source. Fork it, customize it, make it your own.

---

## 🎉 Ready to Apply?

1. Run setup: `./setup.sh` (Mac/Linux) or `setup.bat` (Windows)
2. Create config: `cp config.example.py config.py`
3. Edit config with YOUR information
4. Run the bot: `python3 linkedin_apply.py`
5. **Watch it work!**

**Good luck! You've got this.** 💪

---

*Built by Ajay | Open source | Made to save you time applying to jobs*
