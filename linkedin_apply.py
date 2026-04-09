#!/usr/bin/env python3
"""
LinkedIn Easy Apply Bot
=======================
Automatically applies to AI engineering roles on LinkedIn using Easy Apply.

Usage:
    python linkedin_apply.py

Requirements:
    pip install -r requirements.txt
    playwright install chromium
"""

import asyncio
import csv
import logging
import os
import random
import shutil
import sys
import tempfile
from datetime import datetime
from pathlib import Path

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

# Import user configuration
try:
    from config import CONFIG, SEARCH_QUERIES, EXPERIENCE_LEVELS, JOB_TYPE, DATE_POSTED
except ImportError:
    print("ERROR: config.py not found. Make sure it's in the same folder.")
    sys.exit(1)

# ─────────────────────────────────────────────
#  LOGGING
# ─────────────────────────────────────────────
log = logging.getLogger("linkedin_bot")
log.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s  %(message)s", datefmt="%H:%M:%S")

# Console handler
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)

# File handler
fh = logging.FileHandler("bot_log.txt", encoding="utf-8")
fh.setFormatter(formatter)
log.addHandler(fh)


# ─────────────────────────────────────────────
#  APPLICATION LOG (CSV)
# ─────────────────────────────────────────────
LOG_FILE = Path("applications.csv")

def init_log():
    if not LOG_FILE.exists():
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Job Title", "Company", "URL", "Status", "Notes"])

def save_application(title: str, company: str, url: str, status: str, notes: str = ""):
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            title, company, url, status, notes
        ])


# ─────────────────────────────────────────────
#  FORM HELPERS
# ─────────────────────────────────────────────
async def try_fill(page, keywords: list[str], value: str) -> bool:
    """Find a visible input matching any keyword and fill it."""
    for kw in keywords:
        selectors = [
            f'input[aria-label*="{kw}" i]',
            f'textarea[aria-label*="{kw}" i]',
            f'input[placeholder*="{kw}" i]',
            f'textarea[placeholder*="{kw}" i]',
        ]
        for sel in selectors:
            try:
                el = page.locator(sel).first
                if await el.count() > 0 and await el.is_visible():
                    await el.clear()
                    await el.fill(value)
                    log.info(f"    ✏  Filled '{kw}' → {value!r}")
                    return True
            except Exception:
                pass
    return False


async def dismiss_modal(page):
    """Close the Easy Apply modal and confirm discard."""
    try:
        close = page.locator(
            'button[aria-label="Dismiss"], '
            'button[data-test-modal-close-btn], '
            'button[aria-label="Close"]'
        )
        if await close.count() > 0:
            await close.first.click()
            await page.wait_for_timeout(400)

        # Confirm discard dialog
        discard = page.locator('button:has-text("Discard"), button:has-text("Confirm")')
        if await discard.count() > 0:
            await discard.first.click()
            await page.wait_for_timeout(300)
    except Exception:
        pass


# ─────────────────────────────────────────────
#  EASY APPLY MODAL HANDLER
# ─────────────────────────────────────────────
SKIP_PHRASES = [
    "cover letter",
    "why do you want to work",
    "why are you interested",
    "tell us about yourself",
    "describe yourself",
    "additional information",
    "please describe",
    "in your own words",
]

async def handle_modal(page) -> tuple[str, str]:
    """
    Walk through the Easy Apply modal step by step.
    Returns (status, notes) where status is one of:
        'submitted', 'skipped', 'error'
    """
    for step in range(15):
        await page.wait_for_timeout(400)

        # Check if modal is still visible
        modal = page.locator(".jobs-easy-apply-modal, [data-test-modal]")
        if await modal.count() == 0:
            return "submitted", "modal closed naturally"

        page_text = (await page.inner_text(".jobs-easy-apply-modal")).lower()

        # ── Skip conditions ──────────────────────────────────────────
        if CONFIG.get("skip_if_cover_letter_required") and "cover letter" in page_text:
            log.info("    ⚠  Skipping — cover letter required")
            await dismiss_modal(page)
            return "skipped", "cover letter required"

        if CONFIG.get("skip_if_complex_questions"):
            for phrase in SKIP_PHRASES[1:]:  # skip "cover letter" (already handled)
                if phrase in page_text:
                    log.info(f"    ⚠  Skipping — complex question: '{phrase}'")
                    await dismiss_modal(page)
                    return "skipped", f"complex question: {phrase}"

        # ── Fill known fields ────────────────────────────────────────
        await try_fill(page, ["phone", "mobile", "cell", "contact number"], CONFIG["phone"])
        await try_fill(page, ["city", "location"], CONFIG.get("location", ""))

        # Years of experience — fill any numeric input related to experience with 5
        try:
            number_inputs = page.locator('input[type="text"], input[type="number"]')
            n = await number_inputs.count()
            for i in range(n):
                inp = number_inputs.nth(i)
                if not await inp.is_visible():
                    continue
                aria = (await inp.get_attribute("aria-label") or "").lower()
                placeholder = (await inp.get_attribute("placeholder") or "").lower()
                label_by = await inp.get_attribute("aria-labelledby") or ""
                # Resolve labelledby text
                label_by_text = ""
                if label_by:
                    for lid in label_by.split():
                        el = page.locator(f"#{lid}")
                        if await el.count() > 0:
                            label_by_text += (await el.inner_text()).lower()
                combined = aria + placeholder + label_by_text
                is_experience = (
                    "year" in combined or "experience" in combined
                    or "how many" in combined
                )
                current = await inp.input_value()
                if is_experience and not current.strip():
                    await inp.fill("5")
                    log.info(f"    ✏  Filled experience → 5")
        except Exception:
            pass

        # Yes/No radio buttons — always select "Yes" for any unanswered radio group
        try:
            # Find all fieldsets or question containers with radio buttons
            radio_inputs = page.locator('input[type="radio"]')
            rc = await radio_inputs.count()
            # Group radios by name attribute
            seen_names = set()
            for j in range(rc):
                r = radio_inputs.nth(j)
                if not await r.is_visible():
                    continue
                name = await r.get_attribute("name") or ""
                if name in seen_names:
                    continue
                # Check if any radio in this group is already checked
                group = page.locator(f'input[type="radio"][name="{name}"]')
                gc = await group.count()
                any_checked = False
                for k in range(gc):
                    if await group.nth(k).is_checked():
                        any_checked = True
                        break
                if any_checked:
                    seen_names.add(name)
                    continue
                # Try to find and click the "Yes" option in this group
                clicked = False
                for k in range(gc):
                    radio = group.nth(k)
                    label_id = await radio.get_attribute("aria-labelledby") or ""
                    radio_id = await radio.get_attribute("id") or ""
                    label_text = ""
                    if label_id:
                        for lid in label_id.split():
                            el = page.locator(f"#{lid}")
                            if await el.count() > 0:
                                label_text += (await el.inner_text()).lower()
                    if not label_text and radio_id:
                        lbl = page.locator(f'label[for="{radio_id}"]')
                        if await lbl.count() > 0:
                            label_text = (await lbl.inner_text()).lower()
                    if "yes" in label_text:
                        await radio.check()
                        log.info(f"    ✏  Selected Yes for radio group '{name}'")
                        clicked = True
                        break
                if not clicked:
                    # Fallback: click the first radio in the group
                    await group.first.check()
                    log.info(f"    ✏  Selected first option for radio group '{name}'")
                seen_names.add(name)
        except Exception:
            pass

        # Sponsorship — select "No" if asked
        try:
            if "sponsor" in page_text:
                await try_fill(page, ["sponsor"], CONFIG.get("require_sponsorship", "No"))
        except Exception:
            pass

        # ── Select dropdowns set to empty ────────────────────────────
        try:
            selects = page.locator("select")
            sc = await selects.count()
            for i in range(sc):
                sel = selects.nth(i)
                val = await sel.input_value()
                if not val or val == "Select an option":
                    # Try to pick the first meaningful option
                    options = await sel.locator("option").all_inner_texts()
                    for opt in options:
                        if opt.strip() and opt.strip().lower() not in (
                            "select an option", "please select", "--", ""
                        ):
                            await sel.select_option(label=opt.strip())
                            log.info(f"    ✏  Selected dropdown → {opt.strip()!r}")
                            break
        except Exception:
            pass

        # ── Progress: click Next / Review / Submit ───────────────────
        for btn_label in [
            "Submit application",
            "Submit",
            "Review",
            "Next",
            "Continue to next step",
            "Continue",
        ]:
            btn = page.locator(f'button:has-text("{btn_label}")')
            cnt = await btn.count()
            if cnt > 0:
                b = btn.first
                if not await b.is_disabled():
                    log.info(f"    → Clicking '{btn_label}'")
                    await b.click()
                    await page.wait_for_timeout(600)

                    if btn_label in ("Submit application", "Submit"):
                        # Wait for confirmation banner then click Done
                        await page.wait_for_timeout(500)
                        done_btn = page.locator('button:has-text("Done")')
                        if await done_btn.count() > 0:
                            log.info("    → Clicking 'Done'")
                            await done_btn.first.click()
                            await page.wait_for_timeout(300)
                        return "submitted", ""
                    break  # clicked something, re-loop

        else:
            # No clickable button found — stuck
            log.warning("    ⚠  No navigation button found on this step")
            await page.wait_for_timeout(1000)

    log.warning("    ⚠  Exceeded max steps without submitting")
    await dismiss_modal(page)
    return "error", "exceeded max steps"


# ─────────────────────────────────────────────
#  JOB SEARCH + APPLY LOOP
# ─────────────────────────────────────────────
async def process_query(page, query: str, applied_count: list[int]):
    log.info(f"\n{'═'*55}")
    log.info(f"  🔍  Searching: {query}")
    log.info(f"{'═'*55}")

    encoded = query.replace(" ", "%20")
    url = (
        f"https://www.linkedin.com/jobs/search/"
        f"?keywords={encoded}"
        f"&f_AL=true"                    # Easy Apply only
        f"&f_E={EXPERIENCE_LEVELS}"      # Experience levels
        f"&f_JT={JOB_TYPE}"             # Job type (C = Contract)
        f"&f_TPR={DATE_POSTED}"         # Date posted (r86400 = past 24h)
        f"&sortBy=DD"                    # Newest first
    )
    if CONFIG.get("location"):
        loc = CONFIG["location"].replace(" ", "%20")
        url += f"&location={loc}"

    await page.goto(url)
    try:
        await page.wait_for_load_state("networkidle", timeout=12000)
    except PlaywrightTimeout:
        pass
    await page.wait_for_timeout(800)

    page_num = 0

    while applied_count[0] < CONFIG["max_applications"]:
        page_num += 1

        # Collect job card links
        job_links = page.locator(
            "a.job-card-container__link, "
            "a.jobs-search-results__list-item-link, "
            ".job-card-list__title"
        )
        total = await job_links.count()
        log.info(f"\n  Page {page_num} — {total} listings found")

        if total == 0:
            # Try alternative selector
            job_links = page.locator(".jobs-search-results__list-item")
            total = await job_links.count()
            if total == 0:
                log.info("  No listings on this page, moving on.")
                break

        for i in range(total):
            if applied_count[0] >= CONFIG["max_applications"]:
                return

            title = "Unknown"
            company = "Unknown"
            job_url = page.url

            try:
                card = job_links.nth(i)
                await card.scroll_into_view_if_needed()
                await asyncio.sleep(0.2)
                await card.click()
                await page.wait_for_timeout(700)
                job_url = page.url

                # Extract job title
                for sel in [
                    ".job-details-jobs-unified-top-card__job-title",
                    ".jobs-unified-top-card__job-title",
                    "h1.t-24",
                ]:
                    el = page.locator(sel)
                    if await el.count() > 0:
                        title = (await el.first.inner_text()).strip()
                        break

                # Extract company name
                for sel in [
                    ".job-details-jobs-unified-top-card__company-name a",
                    ".jobs-unified-top-card__company-name",
                    ".topcard__org-name-link",
                ]:
                    el = page.locator(sel)
                    if await el.count() > 0:
                        company = (await el.first.inner_text()).strip()
                        break

                log.info(f"\n  [{i+1}/{total}] {title}  @  {company}")

                # Already applied?
                applied_indicator = page.locator(
                    '.jobs-s-apply__application-link, '
                    'span:has-text("Applied"), '
                    '.artdeco-inline-feedback--success'
                )
                if await applied_indicator.count() > 0:
                    log.info("    → Already applied, skipping")
                    continue

                # Find Easy Apply button
                easy_btn = page.locator(
                    'button.jobs-apply-button:has-text("Easy Apply"), '
                    '.jobs-apply-button--top-card'
                )
                if await easy_btn.count() == 0:
                    log.info("    → No Easy Apply button")
                    save_application(title, company, job_url, "no_easy_apply")
                    continue

                if await easy_btn.first.is_disabled():
                    log.info("    → Easy Apply button disabled")
                    continue

                # Click Easy Apply
                await easy_btn.first.click()
                await page.wait_for_timeout(600)

                # Handle the application form
                status, notes = await handle_modal(page)
                save_application(title, company, job_url, status, notes)

                if status == "submitted":
                    applied_count[0] += 1
                    log.info(
                        f"    ✅  Applied! ({applied_count[0]}/{CONFIG['max_applications']})"
                    )
                else:
                    log.info(f"    ↩  {status.upper()} — {notes}")

                # Human-like random pause
                delay = random.uniform(*CONFIG["delay_between_apps"])
                log.info(f"    ⏳  Waiting {delay:.1f}s...")
                await asyncio.sleep(delay)

            except PlaywrightTimeout:
                log.warning(f"    ⚠  Timeout on listing {i+1}, skipping")
                save_application(title, company, job_url, "timeout")
                continue
            except Exception as exc:
                log.error(f"    ✗  Error: {exc}")
                save_application(title, company, job_url, "error", str(exc))
                continue

        # Navigate to next page
        next_btn = page.locator(
            'button[aria-label="View next page"], '
            'li[data-test-pagination-page-btn] + li button'
        )
        if await next_btn.count() > 0 and not await next_btn.first.is_disabled():
            log.info("  → Next page")
            await next_btn.first.click()
            await page.wait_for_timeout(1200)
        else:
            log.info("  No further pages for this query.")
            break


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
async def main():
    init_log()

    log.info("")
    log.info("╔══════════════════════════════════════════════╗")
    log.info("║      LinkedIn Easy Apply Bot  🤖              ║")
    log.info("╚══════════════════════════════════════════════╝")
    log.info(f"  Max applications : {CONFIG['max_applications']}")
    log.info(f"  Queries          : {', '.join(SEARCH_QUERIES)}")
    log.info(f"  Job type         : Contract")
    log.info(f"  Date posted      : Past 24 hours")
    log.info(f"  Experience levels: Entry + Associate + Mid-Senior")
    log.info(f"  Log file         : {LOG_FILE.resolve()}")
    log.info("")

    applied_count = [0]
    SESSION_FILE = Path("session.json")

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=CONFIG["headless"],
            args=["--start-maximized", "--disable-blink-features=AutomationControlled"],
        )

        # Load saved session if available
        if SESSION_FILE.exists():
            log.info("  Loading saved session...")
            context = await browser.new_context(
                storage_state=str(SESSION_FILE),
                viewport={"width": 1280, "height": 820},
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                ),
            )
        else:
            context = await browser.new_context(
                viewport={"width": 1280, "height": 820},
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                ),
            )

        page = await context.new_page()

        # ── Step 1: Login ──────────────────────────────────────────
        await page.goto("https://www.linkedin.com/feed/")
        try:
            await page.wait_for_load_state("networkidle", timeout=15000)
        except PlaywrightTimeout:
            pass

        # Check if session is still valid
        if "/feed" not in page.url:
            log.info("┌─────────────────────────────────────────────┐")
            log.info("│  ACTION REQUIRED                             │")
            log.info("│  Please log in to LinkedIn in the browser.  │")
            log.info("│  Session will be saved for future runs.      │")
            log.info("└─────────────────────────────────────────────┘")
            if CONFIG.get("linkedin_email"):
                try:
                    await page.fill("#username", CONFIG["linkedin_email"])
                except Exception:
                    pass
            try:
                await page.wait_for_url("**/feed/**", timeout=120_000)
            except PlaywrightTimeout:
                log.error("❌  Login timeout (2 min). Please restart and try again.")
                await browser.close()
                return
            # Save session so next run skips login
            await context.storage_state(path=str(SESSION_FILE))
            log.info("✅  Session saved to session.json — no login needed next time!")
        else:
            log.info("✅  Logged in via saved session!")

        await page.wait_for_timeout(2000)

        # ── Step 2: Apply for each query ──────────────────────────
        for query in SEARCH_QUERIES:
            if applied_count[0] >= CONFIG["max_applications"]:
                log.info(f"\n🏁  Reached max applications ({CONFIG['max_applications']}). Done!")
                break
            try:
                await process_query(page, query, applied_count)
            except Exception as exc:
                log.error(f"Unexpected error for query '{query}': {exc}")
                continue

        # ── Summary ───────────────────────────────────────────────
        log.info("")
        log.info("╔══════════════════════════════════════════════╗")
        log.info(f"║  Session complete!                            ║")
        log.info(f"║  ✅  Applied to : {applied_count[0]} jobs{' '*(27-len(str(applied_count[0])))}║")
        log.info(f"║  📄  Full log   : applications.csv            ║")
        log.info("╚══════════════════════════════════════════════╝")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
