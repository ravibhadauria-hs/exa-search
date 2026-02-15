import os

from exa_py import Exa

from utils import COL_WIDTHS, cell, result_to_rows, write_to_csv


def main():
    api_key = os.environ.get("EXA_API_KEY")
    if not api_key:
        raise SystemExit("Set EXA_API_KEY in the environment (e.g. export EXA_API_KEY=your-key)")
    exa = Exa(api_key)

    # Deep search may return fewer than num_results (e.g. 15); use type="neural" for full count up to 100.
    result = exa.search(
        "ML Engineers in Financial Services with experience in Agentic AI",
        num_results=100,
        type="neural",
        category="people",
        contents={
            "highlights": {"max_characters": 4000, "query": "skills"},
            "summary": True,
        },
    )

    rows = result_to_rows(result)
    header = rows[0]

    sep = " | ".join("-" * w for w in COL_WIDTHS)
    print(sep)
    print(" | ".join(cell(h, COL_WIDTHS[i]) for i, h in enumerate(header)))
    print(sep)
    for row in rows[1:]:
        print(" | ".join(cell(cell_val, COL_WIDTHS[i]) for i, cell_val in enumerate(row)))
    print(sep)
    print(f"Total: {len(result.results)} results (requested 100)")

    csv_path = os.environ.get("EXA_CSV_OUTPUT", "exa_results.csv")
    path = write_to_csv(rows, filepath=csv_path)
    print(f"Wrote to CSV: {path}")


if __name__ == "__main__":
    main()
