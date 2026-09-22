"""
Bluestock Fintech — Capstone Project I: Mutual Fund Analytics
Day 7 — Master Pipeline Script

Runs the full Day 1-2 ETL pipeline end to end:
  1. Ingest and inspect the 10 provided CSV datasets
  2. Fetch live NAV data from mfapi.in (requires internet access)
  3. Clean all datasets
  4. Load cleaned data into the SQLite star schema

Day 3-6 analysis lives in the Jupyter notebooks under notebooks/, since
those are exploratory/analytical rather than repeatable ETL steps — run
them directly in Jupyter or via:
    jupyter nbconvert --to notebook --execute --inplace notebooks/<name>.ipynb

Usage:
    python run_pipeline.py             # full pipeline, including live fetch
    python run_pipeline.py --skip-live # skip the live mfapi.in fetch (e.g. no internet)
"""

import argparse
import subprocess
import sys
import time


STEPS = [
    ("Data ingestion (10 provided CSVs)", "scripts/data_ingestion.py"),
    ("Live NAV fetch (mfapi.in)", "scripts/live_nav_fetch.py"),
    ("Data cleaning", "scripts/clean_data.py"),
    ("Load to SQLite", "scripts/load_to_sqlite.py"),
]


def run_step(label: str, script_path: str) -> None:
    print(f"\n{'=' * 70}\n>>> {label}  ({script_path})\n{'=' * 70}")
    start = time.time()
    result = subprocess.run([sys.executable, script_path])
    elapsed = time.time() - start
    if result.returncode != 0:
        print(f"\n!!! Step failed: {label} (exit code {result.returncode})")
        sys.exit(result.returncode)
    print(f"--- {label} completed in {elapsed:.1f}s ---")


def main():
    parser = argparse.ArgumentParser(description="Run the Bluestock MF Capstone ETL pipeline.")
    parser.add_argument("--skip-live", action="store_true",
                         help="Skip the live mfapi.in NAV fetch step (e.g. if offline)")
    args = parser.parse_args()

    pipeline_start = time.time()
    for label, script in STEPS:
        if args.skip_live and "live_nav_fetch" in script:
            print(f"\n(skipping: {label})")
            continue
        run_step(label, script)

    total = time.time() - pipeline_start
    print(f"\n{'=' * 70}\nPipeline complete in {total:.1f}s.")
    print("Next: run the Day 3-6 notebooks under notebooks/ for analysis,")
    print("      or open dashboard/bluestock_mf_dashboard.html for the preview.")
    print("=" * 70)


if __name__ == "__main__":
    main()
