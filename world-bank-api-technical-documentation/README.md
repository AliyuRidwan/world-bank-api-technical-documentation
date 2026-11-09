# World Bank API: Technical Documentation & Data Analysis

A portfolio project demonstrating technical writing, API research, JSON interpretation, data handling, and evidence-based communication using the **World Bank Indicators API**.

> **Portfolio note:** This is an independently created demonstration project. It is not affiliated with or endorsed by the World Bank. The analysis script retrieves data from the live public API when you run it; numerical findings should be generated and checked at that time rather than assumed from this README.

## Project overview

This repository explains how to retrieve public development data, understand the API's JSON response, and turn observations into a short, responsible analysis.

**Questions explored**
- How can a reader retrieve GDP per capita and population observations for selected African economies?
- What does the API return, and how should missing values and pagination be handled?
- What patterns can be described without confusing nominal GDP measures with real economic growth?

**Countries:** Nigeria, Ghana, Kenya, and South Africa  
**Period:** 2010–2023 (editable in the analysis script)  
**Indicators:**

| Indicator | World Bank code | Meaning |
|---|---|---|
| GDP per capita (current US$) | `NY.GDP.PCAP.CD` | GDP divided by midyear population, expressed in current US dollars |
| Population, total | `SP.POP.TOTL` | Total population |

The project uses GDP per capita and population as descriptive indicators. GDP per capita in current US dollars is affected by price changes and exchange rates; it is **not** a measure of inflation-adjusted growth or household income.

## Repository contents

```text
world-bank-api-technical-documentation/
├── README.md
├── API_Guide.md
├── JSON_Explained.md
├── Data_Analysis.md
├── Troubleshooting.md
├── SOURCES.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── examples/
│   ├── curl_requests.sh
│   └── sample_response.json
├── scripts/
│   └── analyze_world_bank_data.py
└── data/
    └── .gitkeep
```

The script creates CSV files and a Markdown summary in `data/` when executed. Generated data is excluded from Git by default so that you can decide whether to commit a dated snapshot.

## Quick start

### 1. Requirements

- Python 3.9 or later
- Internet connection
- `pip`

### 2. Install dependencies

```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Run the analysis

```bash
python scripts/analyze_world_bank_data.py
```

Optional arguments:

```bash
python scripts/analyze_world_bank_data.py --start-year 2010 --end-year 2023
python scripts/analyze_world_bank_data.py --countries NGA GHA KEN ZAF
```

The script writes:
- `data/world_bank_observations.csv`
- `data/analysis_summary.md`

It also prints a concise summary to the terminal. The API may return missing observations for some country-year combinations; the script preserves those as blank values rather than inventing data.

## Try the API directly

Open this URL in a browser to request Nigeria's GDP per capita observations from 2010 to 2023 in JSON:

<https://api.worldbank.org/v2/country/NGA/indicator/NY.GDP.PCAP.CD?date=2010:2023&format=json&per_page=100>

The API's JSON response is an array containing metadata followed by the observation records. See [API_Guide.md](API_Guide.md) and [JSON_Explained.md](JSON_Explained.md).

## Documentation map

| Document | Purpose |
|---|---|
| [API_Guide.md](API_Guide.md) | Endpoint structure, parameters, request examples, and response handling |
| [JSON_Explained.md](JSON_Explained.md) | JSON syntax and the World Bank response schema |
| [Data_Analysis.md](Data_Analysis.md) | Methodology, interpretation, limitations, and how to report findings |
| [Troubleshooting.md](Troubleshooting.md) | Common API, Python, and data-quality issues |
| [SOURCES.md](SOURCES.md) | Primary references and attribution |

## Skills demonstrated

- Technical research using primary documentation
- API concepts: endpoints, path parameters, query parameters, HTTP status codes
- JSON reading, validation, and transformation
- Python scripting and CSV output
- Data quality checks and missing-value handling
- Clear technical explanations for readers
- Communicating findings with caveats and reproducible steps

## Suggested improvements

To make this project your own, consider adding:
1. A chart comparing the four countries over time.
2. A Jupyter notebook showing the analysis step by step.
3. Unit tests for the API parsing and calculation functions.
4. A short executive summary aimed at a non-technical audience.
5. A second indicator, such as inflation or unemployment, with a clear explanation of its limitations.

## Data and attribution

Data is retrieved from the World Bank Indicators API. Refer to [SOURCES.md](SOURCES.md) for official API documentation and attribution guidance. Always include the retrieval date when publishing a data snapshot.
