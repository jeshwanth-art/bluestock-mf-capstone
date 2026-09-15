"""
Bluestock Fintech — Capstone Project I: Mutual Fund Analytics
Day 1 — Live NAV Fetch

Pulls live NAV history from the free, no-auth MFapi.in API for
HDFC Top 100 Direct plus 5 benchmark schemes named in the project brief.

IMPORTANT: as documented in reports/day1_data_quality_summary.txt, scheme
codes can be reassigned over time (e.g. code 125497 now returns SBI Small
Cap Fund on the live API, not HDFC Top 100 as fund_master.csv and the
project brief assume). This script validates the returned scheme_name
against the expected fund name and flags any mismatch rather than silently
trusting the scheme_code.
"""

import time
import requests
import pandas as pd

BASE_URL = "https://api.mfapi.in/mf"

# Scheme codes + expected name keyword, as given in the Day 1 task
SCHEMES = {
    "HDFC_Top_100_Direct": (125497, "hdfc"),
    "SBI_Bluechip":        (119551, "sbi"),
    "ICICI_Bluechip":      (120503, "icici"),
    "Nippon_Large_Cap":    (118632, "nippon"),
    "Axis_Bluechip":       (119092, "axis"),
    "Kotak_Bluechip":      (120841, "kotak"),
}


def fetch_scheme_nav_history(scheme_code: int) -> dict:
    """GET the full NAV history + meta for one scheme code."""
    url = f"{BASE_URL}/{scheme_code}"
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response.json()


def save_scheme_csv(label: str, scheme_code: int, payload: dict, out_dir: str) -> pd.DataFrame:
    """Flatten one scheme's JSON payload into a DataFrame and save as raw CSV."""
    meta = payload.get("meta", {})
    records = payload.get("data", [])

    df = pd.DataFrame(records)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
        df["nav"] = pd.to_numeric(df["nav"], errors="coerce")
        df = df.sort_values("date").reset_index(drop=True)

    df.insert(0, "scheme_code", scheme_code)
    df.insert(1, "scheme_name_requested", label)
    df.insert(2, "scheme_name_actual", meta.get("scheme_name"))
    df.insert(3, "fund_house", meta.get("fund_house"))
    df.insert(4, "scheme_category", meta.get("scheme_category"))

    out_path = f"{out_dir}/{label}_{scheme_code}_nav_history.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved {len(df):>6} rows -> {out_path}  ({meta.get('scheme_name')})")
    return df


def main():
    out_dir = "data/raw"
    all_frames = []
    mismatches = []

    for label, (code, expected_keyword) in SCHEMES.items():
        payload = fetch_scheme_nav_history(code)
        df = save_scheme_csv(label, code, payload, out_dir)
        all_frames.append(df)

        actual_name = (payload.get("meta") or {}).get("scheme_name", "")
        if expected_keyword.lower() not in actual_name.lower():
            mismatches.append((label, code, actual_name))

        time.sleep(0.5)  # be polite to the free public API

    combined = pd.concat(all_frames, ignore_index=True)
    combined.to_csv(f"{out_dir}/all_schemes_live_nav_combined.csv", index=False)
    print(f"\nCombined dataset: {len(combined)} total rows -> "
          f"{out_dir}/all_schemes_live_nav_combined.csv")

    if mismatches:
        print("\n--- DATA QUALITY FLAG: scheme code / name mismatches ---")
        for label, code, actual_name in mismatches:
            print(f"  Requested '{label}' (code {code}) but live API returned: "
                  f"'{actual_name}'")
        print("These scheme codes appear to have been reassigned since the "
              "project brief was written. Cross-check against "
              "data/raw/01_fund_master.csv (which has the correct, "
              "internally-consistent codes for this project) rather than "
              "trusting the live API's current mapping blindly.")
    else:
        print("\nAll fetched scheme names matched their expected fund.")


if __name__ == "__main__":
    main()
