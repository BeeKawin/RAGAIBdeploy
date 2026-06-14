"""
scimath_url_finder.py
─────────────────────
Discovers SciMath lesson URLs by scraping the site structure.
Outputs entries in SCIMATH_CURRICULUM format.

Usage
─────
    python scraper/scimath_url_finder.py [--subject SUBJECT] [--max-pages 50]
"""

import asyncio
import json
import re
from urllib.parse import urljoin, urlparse
from typing import Optional, Set

import httpx
from bs4 import BeautifulSoup
from loguru import logger


SCIMATH_BASE = "https://www.scimath.org"
SUBJECTS = ["mathematics", "chemistry", "physics", "biology"]
GRADE_KEYWORDS = {"ม.4": "M4", "ม.5": "M5", "ม.6": "M6", "grade 10": "M4", "grade 11": "M5", "grade 12": "M6"}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "th-TH,th;q=0.9,en-US;q=0.8,en;q=0.7",
}


async def fetch_page(client: httpx.AsyncClient, url: str) -> Optional[str]:
    """Fetch a page with retry logic."""
    try:
        logger.debug(f"Fetching {url}")
        resp = await client.get(url, timeout=15, follow_redirects=True)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        logger.warning(f"Failed to fetch {url}: {e}")
        return None


def extract_lesson_urls(html: str, base_url: str) -> Set[str]:
    """Extract lesson URLs from a page."""
    soup = BeautifulSoup(html, "lxml")
    lesson_urls: Set[str] = set()

    # Look for links to lesson pages
    patterns = [
        r"/lesson-\w+/item/\d+-[\w-]+",  # /lesson-chemistry/item/7121-atomic-model
        r"/content/\w+/[\w-]+",           # Alternative pattern
    ]

    for link in soup.find_all("a", href=True):
        href = link.get("href")
        if not href:
            continue

        # Convert relative to absolute
        if href.startswith("/"):
            href = urljoin(SCIMATH_BASE, href)

        # Check if it matches lesson patterns
        for pattern in patterns:
            if re.search(pattern, href):
                lesson_urls.add(href)
                break

    return lesson_urls


def find_next_page_url(html: str, base_url: str, current_page: int = 1) -> Optional[str]:
    """Find the next pagination link, or construct it."""
    soup = BeautifulSoup(html, "lxml")

    # Try to find pagination controls
    # Look for "next" links
    for link in soup.find_all("a", href=True):
        text = link.get_text(strip=True).lower()
        href = link.get("href", "")

        # Check for "next" button
        if "next" in text or "→" in text or "ถัดไป" in text:
            if href.startswith("/"):
                return urljoin(SCIMATH_BASE, href)
            elif href.startswith("http"):
                return href

    # Try to find pagination by looking for page numbers
    for link in soup.find_all("a", href=True):
        text = link.get_text(strip=True)
        href = link.get("href", "")

        # Check if it's a numbered page link
        if text.isdigit():
            page_num = int(text)
            if page_num == current_page + 1:
                if href.startswith("/"):
                    return urljoin(SCIMATH_BASE, href)
                elif href.startswith("http"):
                    return href

    # Fallback: try appending ?page=N to the current URL
    # if "?" not in base_url:
    #     return f"{base_url}?page={current_page + 1}"
    # else:
    #     return f"{base_url}&page={current_page + 1}"


def extract_lesson_info(html: str, url: str) -> Optional[dict]:
    """Extract subject, grade, and topic from a lesson page."""
    soup = BeautifulSoup(html, "lxml")

    # Extract title
    title_tag = soup.find("h1") or soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else "Unknown"

    # Try to find grade and subject in URL or page content
    url_lower = url.lower()
    subject = None
    grade = None

    for subj in SUBJECTS:
        if f"lesson-{subj}" in url_lower or f"/content/{subj}" in url_lower:
            subject = subj
            break

    # Look for grade hints in page text
    text = soup.get_text().lower()
    for keyword, grade_code in GRADE_KEYWORDS.items():
        if keyword in text:
            grade = grade_code
            break

    if not subject or not grade:
        return None

    return {
        "subject": subject,
        "grade": grade,
        "topic": title,
        "scimath_url": url,
    }


async def discover_urls(subject: Optional[str] = None, max_pages: int = 50) -> list[dict]:
    """Discover SciMath lesson URLs with pagination support."""
    discovered: list[dict] = []
    visited_landing_urls: Set[str] = set()
    visited_lesson_urls: Set[str] = set()

    subjects_to_scan = [subject] if subject else SUBJECTS

    async with httpx.AsyncClient(headers=HEADERS) as client:
        for subj in subjects_to_scan:
            logger.info(f"Scanning {subj} lessons (with pagination)...")

            # Try common landing page patterns
            landing_urls = [
                f"{SCIMATH_BASE}/lesson-{subj}",
                f"{SCIMATH_BASE}/content/{subj}",
                f"{SCIMATH_BASE}/lessons?category={subj}",
            ]

            for base_landing_url in landing_urls:
                if base_landing_url in visited_landing_urls:
                    continue

                # Paginate through all pages for this subject
                current_url = base_landing_url
                page_num = 1
                page_count = 0

                while current_url and page_count < 50:  # Safety limit
                    if current_url in visited_landing_urls:
                        break

                    visited_landing_urls.add(current_url)

                    html = await fetch_page(client, current_url)
                    if not html:
                        logger.warning(f"Could not fetch {current_url}, stopping pagination")
                        break

                    # Extract lesson URLs from this page
                    lesson_urls = extract_lesson_urls(html, current_url)

                    if not lesson_urls:
                        logger.debug(f"No lessons found on {current_url}, stopping pagination")
                        break

                    logger.info(f"Page {page_num}: Found {len(lesson_urls)} lesson URLs for {subj}")

                    # Fetch and parse each lesson
                    for lesson_url in lesson_urls:
                        if lesson_url in visited_lesson_urls:
                            continue

                        visited_lesson_urls.add(lesson_url)
                        lesson_html = await fetch_page(client, lesson_url)

                        if not lesson_html:
                            continue

                        info = extract_lesson_info(lesson_html, lesson_url)
                        if info:
                            discovered.append(info)
                            logger.success(
                                f"Found: {info['subject']} / {info['grade']} / {info['topic']}"
                            )

                        if len(discovered) >= max_pages:
                            logger.info(f"Reached max pages limit ({max_pages})")
                            return discovered

                    # Find next page
                    next_url = find_next_page_url(html, current_url, page_num)

                    # Only follow next if it's different from current and hasn't been visited
                    if next_url and next_url != current_url and next_url not in visited_landing_urls:
                        current_url = next_url
                        page_num += 1
                        page_count += 1
                        await asyncio.sleep(1)  # Be polite with requests
                    else:
                        break

                if len(discovered) >= max_pages:
                    return discovered

    return discovered


async def main():
    import argparse

    parser = argparse.ArgumentParser(description="Discover SciMath lesson URLs")
    parser.add_argument("--subject", choices=SUBJECTS, help="Limit to one subject")
    parser.add_argument("--max-pages", type=int, default=50, help="Max pages to discover")
    parser.add_argument("--output", default="scimath_urls.json", help="Output JSON file")
    args = parser.parse_args()

    logger.info(f"Discovering SciMath URLs (max {args.max_pages})...")
    discovered = await discover_urls(subject=args.subject, max_pages=args.max_pages)

    # Group by subject/grade
    grouped = {}
    for entry in discovered:
        key = (entry["subject"], entry["grade"])
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(entry)

    logger.info(f"\nDiscovered {len(discovered)} entries")
    logger.info("\nGrouped by Subject/Grade:")
    for (subj, grade), entries in sorted(grouped.items()):
        logger.info(f"  {subj.upper()} {grade}: {len(entries)} entries")

    # Save to JSON
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(discovered, f, ensure_ascii=False, indent=2)

    logger.success(f"Saved {len(discovered)} entries to {args.output}")

    # Print Python code for easy copy-paste
    print("\n" + "=" * 80)
    print("Python code to add to SCIMATH_CURRICULUM:")
    print("=" * 80)
    for entry in discovered[:20]:  # Show first 20
        print(f"""    {{
        "subject": "{entry['subject']}",
        "grade": "{entry['grade']}",
        "topic": "{entry['topic']}",
        "scimath_url": "{entry['scimath_url']}",
    }},""")


if __name__ == "__main__":
    asyncio.run(main())
