"""Shared utilities for Exa search: formatting, CSV, table layout, URL display names."""
import csv
import os
from urllib.parse import urlparse

# -----------------------------------------------------------------------------
# Text / display
# -----------------------------------------------------------------------------


def truncate(s: str | None, max_len: int) -> str:
    """Truncate string to max_len, strip newlines; append '...' if truncated."""
    if s is None:
        return ""
    s = s.replace("\n", " ").strip()
    return (s[: max_len - 3] + "...") if len(s) > max_len else s


def cell(s: str, width: int) -> str:
    """Format a cell string to fixed width (truncate then pad)."""
    s = str(s)[:width]
    return s.ljust(width)


# -----------------------------------------------------------------------------
# Exa result helpers
# -----------------------------------------------------------------------------


def name_from_result(r) -> str:
    """Extract display name from an Exa search result (person entity or title)."""
    if r.entities:
        for e in r.entities:
            if getattr(e, "properties", None) and getattr(e.properties, "name", None):
                return e.properties.name or ""
    return r.title or "(no title)"


# -----------------------------------------------------------------------------
# Table layout (default columns for search results)
# -----------------------------------------------------------------------------

TABLE_HEADER = ("#", "Name / Title", "Score", "Author", "URL", "Snippet", "Summary", "Text")
COL_WIDTHS = (4, 32, 8, 20, 48, 40, 50, 60)


def result_to_rows(result) -> list[tuple[str, ...]]:
    """Turn an Exa SearchResponse result into (header, data rows) for table/CSV."""
    header = TABLE_HEADER
    rows = [header]
    for i, r in enumerate(result.results, 1):
        name = name_from_result(r)
        score = f"{r.score:.2f}" if r.score is not None else ""
        author = (r.author or "").strip()
        url = (r.url or "").strip()
        snippet = (r.highlights[0] if r.highlights else "").replace("\n", " ").strip()
        summary = (r.summary or "").strip()
        text = (r.text or "").strip()
        rows.append((str(i), name, score, author, url, snippet, summary, text))
    return rows


# -----------------------------------------------------------------------------
# CSV
# -----------------------------------------------------------------------------


def write_to_csv(
    rows: list[tuple[str, ...]],
    filepath: str = "exa_results.csv",
) -> str:
    """Write rows (header + data) to a CSV file. Returns absolute path."""
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    return os.path.abspath(filepath)


def load_csv(filepath: str) -> tuple[list[str] | None, list[list[str]] | None]:
    """Load CSV; returns (headers, data_rows) or (None, None) if missing/empty."""
    if not os.path.isfile(filepath):
        return None, None
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        return None, None
    return rows[0], rows[1:]


# -----------------------------------------------------------------------------
# URL → friendly source name (for web app / display)
# -----------------------------------------------------------------------------

SOURCE_NAMES = {
    "linkedin.com": "LinkedIn",
    "github.com": "GitHub",
    "twitter.com": "Twitter",
    "x.com": "X",
    "medium.com": "Medium",
    "youtube.com": "YouTube",
    "stackoverflow.com": "Stack Overflow",
    "facebook.com": "Facebook",
    "instagram.com": "Instagram",
    "substack.com": "Substack",
    "reddit.com": "Reddit",
    "quora.com": "Quora",
    "wikipedia.org": "Wikipedia",
    "arxiv.org": "arXiv",
    "scholar.google.com": "Google Scholar",
}


def source_name(url: str | None) -> str:
    """Return a friendly page source name for a URL (e.g. 'LinkedIn')."""
    if not url or not isinstance(url, str):
        return "Link"
    s = url.strip().lower()
    if not s:
        return "Link"
    if "://" not in s:
        s = "https://" + s
    try:
        parsed = urlparse(s)
        host = (parsed.netloc or parsed.path or "").strip()
        host = host.replace("www.", "").split("/")[0]
        if not host:
            return "Link"
        return SOURCE_NAMES.get(host, host.split(".")[0].title())
    except Exception:
        return "Link"
