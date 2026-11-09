#!/usr/bin/env python3
"""Retrieve and summarize selected World Bank indicators.

The script intentionally keeps missing observations as None/blank values.
It does not infer or manufacture missing data.
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from pathlib import Path
from typing import Any

import requests

API_BASE = "https://api.worldbank.org/v2"
DEFAULT_COUNTRIES = ["NGA", "GHA", "KEN", "ZAF"]

INDICATORS = {
    "NY.GDP.PCAP.CD": "GDP per capita (current US$)",
    "SP.POP.TOTL": "Population, total",
}


def fetch_indicator(
    countries: list[str],
    indicator_code: str,
    start_year: int,
    end_year: int,
) -> list[dict[str, Any]]:
    """Fetch one indicator for the selected countries and year range."""
    country_path = ";".join(countries)
    url = f"{API_BASE}/country/{country_path}/indicator/{indicator_code}"
    params = {
        "date": f"{start_year}:{end_year}",
        "format": "json",
        "per_page": 1000,
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        raise RuntimeError(f"Network/API request failed: {exc}") from exc
    except ValueError as exc:
        raise RuntimeError("The API response was not valid JSON.") from exc

    if not isinstance(payload, list) or not payload:
        raise RuntimeError("Unexpected API response structure.")

    metadata = payload[0]
    if isinstance(metadata, dict) and metadata.get("message"):
        raise RuntimeError(f"World Bank API error: {metadata['message']}")

    if len(payload) < 2:
        return []

    records = payload[1] or []
    if not isinstance(records, list):
        raise RuntimeError("The API data element was not a list or null.")

    # The requested period and four-country scope should fit in one page
    # with per_page=1000. Fail visibly rather than silently dropping pages.
    pages = int(metadata.get("pages", 1)) if isinstance(metadata, dict) else 1
    if pages > 1:
        raise RuntimeError(
            f"API returned {pages} pages. Increase per_page or add pagination."
        )

    normalized: list[dict[str, Any]] = []
    for record in records:
        country = record.get("country") or {}
        indicator = record.get("indicator") or {}
        raw_value = record.get("value")

        try:
            numeric_value = float(raw_value) if raw_value is not None else None
        except (TypeError, ValueError):
            numeric_value = None

        normalized.append(
            {
                "country_code": record.get("countryiso3code", ""),
                "country": country.get("value", ""),
                "indicator_code": indicator.get("id", indicator_code),
                "indicator": indicator.get("value", INDICATORS[indicator_code]),
                "year": record.get("date", ""),
                "value": numeric_value,
                "unit": record.get("unit", ""),
                "observation_status": record.get("obs_status", ""),
            }
        )

    return normalized


def write_csv(rows: list[dict[str, Any]], output_path: Path) -> None:
    """Write normalized observations to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    columns = [
        "country_code",
        "country",
        "indicator_code",
        "indicator",
        "year",
        "value",
        "unit",
        "observation_status",
    ]

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def endpoint_summary(
    rows: list[dict[str, Any]], country_code: str, indicator_code: str
) -> dict[str, Any] | None:
    """Return earliest/latest available observation and change for one series."""
    series = [
        row for row in rows
        if row["country_code"] == country_code
        and row["indicator_code"] == indicator_code
        and row["value"] is not None
    ]
    series.sort(key=lambda row: int(row["year"]))

    if not series:
        return None

    first = series[0]
    last = series[-1]
    start_value = first["value"]
    end_value = last["value"]

    absolute_change = end_value - start_value
    percentage_change = (
        (absolute_change / start_value) * 100
        if start_value != 0
        else None
    )

    return {
        "country": first["country"],
        "country_code": country_code,
        "indicator": first["indicator"],
        "start_year": first["year"],
        "start_value": start_value,
        "end_year": last["year"],
        "end_value": end_value,
        "absolute_change": absolute_change,
        "percentage_change": percentage_change,
        "available_observations": len(series),
    }


def format_number(value: float | None) -> str:
    if value is None:
        return "not available"
    return f"{value:,.2f}"


def build_summary(
    rows: list[dict[str, Any]],
    countries: list[str],
    start_year: int,
    end_year: int,
    output_path: Path,
) -> str:
    """Create a Markdown report using values returned by the API."""
    retrieval_date = date.today().isoformat()
    lines = [
        "# World Bank Data Analysis Summary",
        "",
        f"- **Retrieved:** {retrieval_date}",
        f"- **Requested period:** {start_year}–{end_year}",
        f"- **Countries:** {', '.join(countries)}",
        "- **Source:** World Bank Indicators API",
        "",
        "> This report is generated from the API response at run time. "
        "The earliest and latest values shown are the earliest and latest "
        "non-missing observations returned within the requested period; "
        "they are not necessarily the exact boundary years.",
        "",
        "## Summary of available observations",
        "",
        "| Country | Indicator | First year | First value | Last year | Last value | Change |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]

    for country_code in countries:
        for indicator_code in INDICATORS:
            result = endpoint_summary(rows, country_code, indicator_code)
            if result is None:
                lines.append(
                    f"| {country_code} | {INDICATORS[indicator_code]} | — | "
                    "— | — | — | No observations returned |"
                )
                continue

            change = (
                f"{result['percentage_change']:.2f}%"
                if result["percentage_change"] is not None
                else "not calculable (starting value is zero)"
            )
            lines.append(
                f"| {result['country']} | {result['indicator']} | "
                f"{result['start_year']} | {format_number(result['start_value'])} | "
                f"{result['end_year']} | {format_number(result['end_value'])} | "
                f"{change} |"
            )

    lines.extend(
        [
            "",
            "## Interpretation guidance",
            "",
            "- GDP per capita (current US$) is a current-price measure. "
            "It is affected by price changes and exchange rates and should "
            "not be described as inflation-adjusted economic growth.",
            "- Population values describe total population; they do not "
            "explain the causes of population change.",
            "- Missing observations are excluded from endpoint calculations, "
            "not converted to zero.",
            "- Percentage changes are descriptive and do not establish causation.",
            "",
            "## Data-quality notes",
            "",
            f"- Rows retrieved: {len(rows)}",
            "- Check the first and last observation years before making "
            "cross-country comparisons.",
            "- Consult the indicator metadata and source notes before publication.",
            "",
            "## Source",
            "",
            "https://datahelpdesk.worldbank.org/knowledgebase/articles/889392",
            "",
        ]
    )

    report = "\n".join(lines)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare World Bank GDP per capita and population indicators."
    )
    parser.add_argument("--start-year", type=int, default=2010)
    parser.add_argument("--end-year", type=int, default=2023)
    parser.add_argument(
        "--countries",
        nargs="+",
        default=DEFAULT_COUNTRIES,
        help="ISO3 country codes (default: NGA GHA KEN ZAF)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data"),
        help="Directory for generated CSV and Markdown files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.start_year > args.end_year:
        print("Error: start year must not be later than end year.", file=sys.stderr)
        return 2

    countries = [code.upper() for code in args.countries]
    all_rows: list[dict[str, Any]] = []

    for indicator_code in INDICATORS:
        print(f"Fetching {INDICATORS[indicator_code]}...")
        try:
            all_rows.extend(
                fetch_indicator(
                    countries,
                    indicator_code,
                    args.start_year,
                    args.end_year,
                )
            )
        except RuntimeError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1

    all_rows.sort(
        key=lambda row: (
            row["country_code"],
            row["indicator_code"],
            int(row["year"]) if row["year"].isdigit() else 0,
        )
    )

    csv_path = args.output_dir / "world_bank_observations.csv"
    report_path = args.output_dir / "analysis_summary.md"

    write_csv(all_rows, csv_path)
    report = build_summary(
        all_rows,
        countries,
        args.start_year,
        args.end_year,
        report_path,
    )

    print(f"\nSaved observations: {csv_path}")
    print(f"Saved report: {report_path}")
    print("\n" + report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
