# Exa Search + Results Viewer

Run [Exa](https://exa.ai) search (people, companies, etc.), dump results to CSV, and view them in a simple web app.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # or: .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Set your Exa API key: `export EXA_API_KEY=your-key` (or add to a `.env` and load it; do not commit the key).

## Run search → CSV

```bash
python test_search.py
```

- Writes **exa_results.csv** (override with `EXA_CSV_OUTPUT=path/to/file.csv`).
- Prints a table to the terminal.

## Run web app

```bash
python app.py
```

Open http://127.0.0.1:5000 to view the same CSV in a table (Summary and Snippet in card-style blocks, URLs as friendly names like "LinkedIn").

---

## Tips & tricks (Exa Search API)

### Search type (`type`)

| Type      | Use when | Result count |
|-----------|----------|--------------|
| `auto`    | Default; let Exa choose. | Varies. |
| `neural`  | Semantic / meaning-based search; **honors `num_results`** up to 100. | Up to 100. |
| `deep`    | Broader, multi-query search; **number of results is dynamic** (often ~15). | API-decided. |
| `fast`    | Speed over depth. | Varies. |
| `instant` | Lowest latency. | Varies. |

- **Need a predictable count?** Use `type="neural"` and `num_results=100` (or less).
- **Deep search** often returns fewer results than requested; use neural if you want the full `num_results`.

### Category

- **`category="people"`** – People/profiles (e.g. LinkedIn); returns structured person entities when available.
- **`category="company"`** – Company pages.
- Others: `news`, `research paper`, `tweet`, `personal site`, `financial report`.

### Contents (text, highlights, summary)

Request as much as you need; each adds cost and size:

```python
contents={
    "text": {"max_characters": 10_000},   # full page text
    "highlights": {"max_characters": 4_000, "query": "skills"},  # snippets; optional query
    "summary": True,
}
```

- **`highlights`** – Relevant snippets per URL; `query` biases what’s extracted.
- **`summary`** – One summary per result.
- **`text`** – Full page text; use `max_characters` to cap length.

### Result count (`num_results`)

- Default is 10.
- **Neural / deep**: API max is 100 per request.
- Deep search often returns fewer than `num_results`; neural respects it.

### People category limits

With `category="people"` (and `company`), these are **not** supported:  
`startPublishedDate`, `endPublishedDate`, `startCrawlDate`, `endCrawlDate`, `includeText`, `excludeText`, `excludeDomains`.  
`includeDomains` for people only accepts LinkedIn-related domains.

### Environment variables

| Variable           | Purpose |
|--------------------|--------|
| `EXA_API_KEY`      | Exa API key (required). Set in env; do not commit. |
| `EXA_CSV_OUTPUT`   | CSV path for search output and for the web app to load. |

---

## Project layout

- **test_search.py** – Runs Exa search, prints table, writes CSV.
- **app.py** – Flask app that reads the CSV and shows the table (Summary/Snippet as cards, URLs as source names).
- **utils.py** – Shared helpers: `truncate`, `cell`, `name_from_result`, `result_to_rows`, `write_to_csv`, `load_csv`, `source_name`, `TABLE_HEADER`, `COL_WIDTHS`.
- **templates/index.html** – Table view and styling.
- **requirements.txt** – `exa_py`, `flask`.
