"""Simple web app to display Exa search results (CSV) in a table, with Summary emphasized."""
import os

from flask import Flask, render_template

from utils import load_csv, source_name

app = Flask(__name__)

_BASE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.environ.get("EXA_CSV_OUTPUT") or os.path.join(_BASE, "exa_results.csv")

app.jinja_env.filters["source_name"] = source_name


def load_results():
    """Load results from CSV. Returns (headers, rows) or (None, None) if file missing."""
    return load_csv(CSV_PATH)


@app.route("/")
def index():
    headers, rows = load_results()
    return render_template("index.html", headers=headers, rows=rows)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
