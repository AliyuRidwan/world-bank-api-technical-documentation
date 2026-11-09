#!/usr/bin/env bash
# Example requests for the World Bank Indicators API.
# Requires curl. These requests retrieve live data when executed.

set -euo pipefail

BASE="https://api.worldbank.org/v2/country/NGA;GHA;KEN;ZAF/indicator"

echo "GDP per capita (current US$)"
curl --fail --silent --show-error \
  "$BASE/NY.GDP.PCAP.CD?date=2010:2023&format=json&per_page=1000"
echo

echo "Population, total"
curl --fail --silent --show-error \
  "$BASE/SP.POP.TOTL?date=2010:2023&format=json&per_page=1000"
echo
