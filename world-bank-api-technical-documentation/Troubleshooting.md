# Troubleshooting Guide

This guide covers common problems when calling the World Bank Indicators API and running the accompanying Python script.

## 1. The API returns XML instead of JSON

**Likely cause:** The request omitted `format=json`.

**Fix:** Add the query parameter:

```text
?format=json
```

The World Bank API can return XML by default. The examples in this repository explicitly request JSON.

## 2. The API returns an error message

**Likely cause:** A country code, indicator code, or query parameter may be invalid.

**Fix:**
1. Check the spelling of the endpoint.
2. Verify the country code.
3. Verify the indicator code in the World Bank indicator catalogue.
4. Read the API error message instead of assuming the second response element contains data.

Official reference: [Indicator API Queries](https://datahelpdesk.worldbank.org/knowledgebase/articles/898599-indicator-api-queries).

## 3. The data element is `null`

**Likely cause:** The request is valid, but there are no observations for the requested filter, or no records are available for that selection.

**Fix:** Handle the data element as an empty list:

```python
observations = payload[1] or []
```

Do not replace missing values with zero.

## 4. Some country-year values are missing

**Likely cause:** The indicator may not be reported for every year, or the latest observation may not yet be available.

**Fix:**
- Check the indicator's source notes.
- Check the latest available year for each country.
- Report missing years transparently.
- Avoid comparing different time periods without explaining the difference.

## 5. Only some records are returned

**Likely cause:** The response is paginated.

**Fix:** Read the `pages` value in the first response element and request subsequent pages. The `per_page` parameter controls the number of records returned per page.

## 6. Python reports `ModuleNotFoundError: No module named 'requests'`

**Cause:** The dependency is not installed in the active Python environment.

**Fix:**

```bash
python -m pip install -r requirements.txt
```

If you use a virtual environment, activate it before installing dependencies and running the script.

## 7. Python reports a timeout or connection error

**Possible causes:** Network interruption, temporary service unavailability, firewall restrictions, or a slow connection.

**Fix:**
- Check your internet connection.
- Try the endpoint in a browser.
- Run the script again later.
- Keep a reasonable request timeout.
- Do not create a rapid retry loop.

## 8. A percentage change cannot be calculated

**Likely cause:** The starting value is missing or zero, or the ending value is missing.

**Fix:** Only calculate percentage change when both values are present and the starting value is non-zero. Otherwise, report that the percentage change is unavailable.

## 9. The results differ from an earlier run

**Possible cause:** The World Bank may revise historical observations or publish new data.

**Fix:** Record the retrieval date and, when reproducibility matters, archive the exact downloaded response or CSV with a clear timestamp and source description.
