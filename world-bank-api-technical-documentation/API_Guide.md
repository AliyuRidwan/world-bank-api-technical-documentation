# API Guide: Retrieving World Bank Indicator Data

## 1. Purpose

This guide explains how to retrieve country-level time-series data from the World Bank Indicators API. It is written for readers who understand basic web concepts but may be new to APIs.

The API exposes public development indicators, including population, national accounts, education, health, and other subjects. The World Bank's official documentation describes the available calls and parameters.

## 2. Base URL and endpoint

The API's version 2 base URL is:

```text
https://api.worldbank.org/v2
```

A common indicator-data endpoint follows this pattern:

```text
GET /country/{country_code}/indicator/{indicator_code}
```

For example:

```text
https://api.worldbank.org/v2/country/NGA/indicator/NY.GDP.PCAP.CD
```

### Path parameters

| Parameter | Required | Description | Example |
|---|---:|---|---|
| `country_code` | Yes | Country/economy code. Multiple codes can be separated by semicolons. | `NGA` or `NGA;GHA` |
| `indicator_code` | Yes | Unique code for the requested indicator. | `NY.GDP.PCAP.CD` |

### Useful query parameters

| Parameter | Example | Purpose |
|---|---|---|
| `format` | `format=json` | Requests JSON output. Without it, the API may return XML. |
| `date` | `date=2010:2023` | Restricts observations to a year or year range. |
| `per_page` | `per_page=100` | Sets the number of records returned per page. |
| `page` | `page=2` | Requests a particular result page. |
| `mrv` | `mrv=5` | Requests the most recent number of values. |

For a complete and current parameter list, consult the official [API Basic Call Structures](https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structures) reference.

## 3. Example request

Retrieve Nigeria's GDP per capita (current US$) for 2010–2023:

```http
GET https://api.worldbank.org/v2/country/NGA/indicator/NY.GDP.PCAP.CD?date=2010:2023&format=json&per_page=100
```

Equivalent cURL command:

```bash
curl --get \
  --data-urlencode "date=2010:2023" \
  --data-urlencode "format=json" \
  --data-urlencode "per_page=100" \
  "https://api.worldbank.org/v2/country/NGA/indicator/NY.GDP.PCAP.CD"
```

The API is public and does not require an API key for ordinary Indicators API access, according to the World Bank's API documentation.

## 4. Example Python request

Install the dependency:

```bash
pip install requests
```

Then:

```python
import requests

url = (
    "https://api.worldbank.org/v2/country/NGA/"
    "indicator/NY.GDP.PCAP.CD"
)

params = {
    "date": "2010:2023",
    "format": "json",
    "per_page": 100,
}

response = requests.get(url, params=params, timeout=30)
response.raise_for_status()

payload = response.json()
metadata, observations = payload

for observation in observations or []:
    print(
        observation["date"],
        observation["country"]["value"],
        observation["value"],
    )
```

### What this code does

1. Defines the endpoint for Nigeria and the selected indicator.
2. Supplies the year range and JSON response format as query parameters.
3. Sends an HTTP GET request.
4. Raises an exception for unsuccessful HTTP status codes.
5. Parses the response body as JSON.
6. Separates pagination metadata from observation records.
7. Prints the year, country name, and indicator value.

**Important:** A successful HTTP response does not guarantee that observations exist. The second array element can be `null` when no records match the request. Production code should also check for API-level error messages.

## 5. Multiple countries

Country codes can be separated with semicolons:

```text
https://api.worldbank.org/v2/country/NGA;GHA;KEN;ZAF/indicator/NY.GDP.PCAP.CD?date=2010:2023&format=json&per_page=1000
```

This example requests GDP per capita for Nigeria, Ghana, Kenya, and South Africa.

## 6. Response structure

For a normal JSON indicator query, the response is generally a two-element array:

```json
[
  {
    "page": 1,
    "pages": 1,
    "per_page": "100",
    "total": 14
  },
  [
    {
      "indicator": {
        "id": "NY.GDP.PCAP.CD",
        "value": "GDP per capita (current US$)"
      },
      "country": {
        "id": "NG",
        "value": "Nigeria"
      },
      "countryiso3code": "NGA",
      "date": "2023",
      "value": null,
      "unit": "",
      "obs_status": "",
      "decimal": 0
    }
  ]
]
```

The numeric value above is a placeholder for explanation, not a published observation. See `examples/sample_response.json` for a valid illustrative structure.

| Element | Meaning |
|---|---|
| First array element | Pagination and response metadata |
| `page` | Current page number |
| `pages` | Total number of pages |
| `total` | Total matching records |
| Second array element | Observation records |
| `country` | Country identifier and display name |
| `indicator` | Indicator code and display name |
| `date` | Observation year |
| `value` | Numeric observation, or `null` if unavailable |

## 7. Pagination

Large responses may be split across pages. Use the `pages` value in the metadata to determine whether another request is needed. Do not assume that page one contains every matching record.

The script in `scripts/analyze_world_bank_data.py` requests a sufficiently large page size for this small comparison, then checks the response metadata. For larger datasets, implement a page loop and stop when the current page reaches the total page count.

## 8. Responsible API usage

- Set a request timeout.
- Check HTTP status codes.
- Handle API-level error messages.
- Respect pagination metadata.
- Avoid repeatedly requesting the same data without a reason.
- Preserve `null` values as missing data.
- Record the date on which you retrieved the data.
- Read the indicator's definition and source notes before interpreting it.

## 9. Further reading

- [World Bank: About the Indicators API](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392)
- [World Bank: API Basic Call Structures](https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structures)
- [World Bank: Indicator API Queries](https://datahelpdesk.worldbank.org/knowledgebase/articles/898599-indicator-api-queries)
