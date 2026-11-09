# JSON Explained: Understanding a World Bank API Response

## 1. What is JSON?

JSON (JavaScript Object Notation) is a text format for representing structured data. It is widely used by APIs because it is readable by people and can be parsed by most programming languages.

JSON supports:
- **Objects**, written with `{ }`, which contain key-value pairs.
- **Arrays**, written with `[ ]`, which contain ordered values.
- **Strings**, written in double quotes.
- **Numbers**, such as `2023` or `1250.5`.
- **Booleans**, `true` and `false`.
- **Null**, which represents an absent or unavailable value.

## 2. An illustrative API response

The following is a shortened, illustrative response showing the shape of a World Bank indicator query. The `value` is deliberately set to `null` to demonstrate missing-data handling; it is not a reported GDP figure.

```json
[
  {
    "page": 1,
    "pages": 1,
    "per_page": "100",
    "total": 1
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

## 3. How to read the structure

The outer response is an array with two elements:

1. **Metadata object:** describes the result set and pagination.
2. **Data array:** contains one object per country-year observation.

The observation object includes nested objects. For example, `country.value` contains the readable country name, while `country.id` contains its country code.

### Field reference

| JSON path | Type | Description |
|---|---|---|
| `[0].page` | Number | Current response page |
| `[0].pages` | Number | Number of available pages |
| `[0].total` | Number | Total number of matching observations |
| `[1][0].indicator.id` | String | Indicator code |
| `[1][0].indicator.value` | String | Indicator label |
| `[1][0].country.value` | String | Country name |
| `[1][0].date` | String | Observation year |
| `[1][0].value` | Number or null | Indicator value |

## 4. Why `null` matters

A `null` value is not the same as zero.

- `0` is a numeric value.
- `null` means the API has no numeric observation for that record.

Replacing missing values with zero can distort averages, comparisons, and trend analysis. Keep missing values explicit and explain how they are handled.

## 5. Parsing JSON in Python

```python
import json

with open("response.json", "r", encoding="utf-8") as file:
    payload = json.load(file)

metadata = payload[0]
observations = payload[1] or []

print("Pages:", metadata.get("pages"))

for row in observations:
    value = row.get("value")

    if value is None:
        print(row["date"], "No observation available")
    else:
        print(row["date"], value)
```

### Key methods

- `json.load(file)` parses JSON from a file.
- `json.loads(text)` parses JSON from a string.
- `.get("key")` safely retrieves a dictionary value.
- `is None` checks whether a value is explicitly missing.

## 6. Practical validation checklist

Before using JSON data in an analysis:

- [ ] Confirm that the response is valid JSON.
- [ ] Check for an API error message.
- [ ] Confirm that the expected metadata and data elements exist.
- [ ] Check that country and indicator codes match the request.
- [ ] Confirm that years fall within the requested range.
- [ ] Preserve missing values.
- [ ] Check whether numeric values are numbers rather than strings.
- [ ] Record the source and retrieval date.

## 7. Communicating JSON to a non-technical reader

Instead of saying:

> The response contains a nested array of objects with nullable numeric fields.

Try:

> The API returns a short section describing the results, followed by the actual country-year records. Each record identifies the country, indicator, year, and reported value. A blank value means that no observation is available for that period.

The second explanation keeps the technical meaning while reducing unnecessary jargon.
