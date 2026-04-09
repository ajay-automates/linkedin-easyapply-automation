# ============================================================
#  LinkedIn Easy Apply Bot — USER CONFIGURATION
#  Copy this file to config.py and edit with your settings.
# ============================================================

CONFIG = {
    # ── Personal Info ──────────────────────────────────────
    "phone": "YOUR_PHONE_NUMBER",       # Your phone number
    "years_experience": "2",             # Years of relevant experience (as a string)
    "linkedin_email": "",                # Optional: pre-fills email on login page

    # ── Application Behavior ───────────────────────────────
    "max_applications": 50,              # Stop after this many successful applications
    "delay_between_apps": (2, 5),        # Random pause (seconds) between applications
                                         # — keeps activity looking human (2-5 sec = fast & natural)

    # ── Work Authorization ─────────────────────────────────
    "work_authorization": "Yes",         # "Yes" or "No"
    "require_sponsorship": "No",         # "Yes" or "No"

    # ── Location Filter ────────────────────────────────────
    # Leave empty for "open to anything" (your preference)
    "location": "",

    # ── Advanced ───────────────────────────────────────────
    "headless": False,                   # False = visible browser (recommended)
                                         # True  = invisible (may trigger detection)
    "skip_if_cover_letter_required": True,   # Skip jobs asking for a cover letter
    "skip_if_complex_questions": True,       # Skip jobs with open-ended essay questions
}

# ── Job Search Queries ────────────────────────────────────
# The bot cycles through all of these searches.
SEARCH_QUERIES = [
    "Software Developer",
    "Software Engineer",
]

# ── Experience Levels (LinkedIn encoded values) ───────────
# 1 = Internship, 2 = Entry Level, 3 = Associate, 4 = Mid-Senior
# Targeting entry + mid-level per your preference:
EXPERIENCE_LEVELS = "1%2C2%2C3"

# ── Job Type Filter ───────────────────────────────────────
# F=Full-time, C=Contract, P=Part-time, T=Temporary, I=Internship, V=Volunteer, O=Other
JOB_TYPE = "C"  # Contract only

# ── Date Posted Filter ────────────────────────────────────
# r86400 = past 24 hours, r604800 = past week, r2592000 = past month
DATE_POSTED = "r86400"  # Past 24 hours
