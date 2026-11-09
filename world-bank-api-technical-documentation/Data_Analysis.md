# Data Analysis: Comparing Selected African Economies

## 1. Objective

This project demonstrates a repeatable way to retrieve and describe two World Bank indicators for Nigeria, Ghana, Kenya, and South Africa:

- GDP per capita (current US$): `NY.GDP.PCAP.CD`
- Population, total: `SP.POP.TOTL`

The default observation period is 2010–2023. The period can be changed when running the script.

## 2. Research questions

1. How did reported GDP per capita change over the selected period in each country?
2. How did population change over the same period?
3. Are there missing observations that affect comparisons?
4. What limitations should be communicated alongside the results?

## 3. Data source and collection

The data is retrieved from the World Bank Indicators API:

```text
https://api.worldbank.org/v2
```

The script requests each indicator for all four countries, asks for JSON, and filters the selected year range. It saves the returned observations to a CSV file.

Run:

```bash
python scripts/analyze_world_bank_data.py
```

The script reports the retrieval date and writes a summary based on the actual API response. Run it again before publishing if you want an up-to-date snapshot.

## 4. Method

1. Request the two indicators for the four selected countries.
2. Check the HTTP response and API response structure.
3. Convert observation records into a tabular structure.
4. Keep missing values as missing rather than replacing them with zero.
5. Sort observations by country, indicator, and year.
6. Compare the earliest and latest available observations within the chosen period.
7. Calculate absolute and percentage change only when both endpoint values are present and the starting value is non-zero.
8. Generate a concise Markdown summary.

### Percentage change

For a starting value \(V_s\) and ending value \(V_e\):

\[
\text{Percentage change} = \frac{V_e - V_s}{V_s} \times 100
\]

This calculation is descriptive. It does not establish why a change occurred.

## 5. How to interpret the indicators

### GDP per capita (current US$)

This indicator expresses GDP per person in current US dollars. It can be useful for comparing the scale of economic output per person, but it is influenced by domestic price changes and exchange-rate movements.

**Do not describe it as real GDP growth.** For inflation-adjusted comparisons, use a constant-price indicator such as GDP per capita (constant 2015 US$), after checking the indicator's current definition and source notes.

It is also not the same as average salary, disposable income, or the amount an individual earns.

### Population, total

This indicator estimates the total population. It can provide context for changes in economic output per person, but it does not explain the causes of population change.

## 6. Results template

The analysis script creates `data/analysis_summary.md` with calculated values from the live API response.

When communicating the results, use a structure like this:

> **Finding:** Between [start year] and [end year], [country] recorded a [increase/decrease] in GDP per capita (current US$) from [starting value] to [ending value], equivalent to [percentage change]%.
>
> **Interpretation:** This is a change in a current-US-dollar measure. It may reflect changes in domestic output, prices, and exchange rates. It should not be interpreted on its own as a change in real living standards.
>
> **Data caveat:** [State any missing years, latest available year, or other coverage limitation.]

Do not fill this template with guessed values. Use the generated output and verify the indicator metadata before publishing.

## 7. Limitations

- **Current-dollar measure:** GDP per capita in current US dollars is not adjusted for inflation.
- **Exchange-rate effects:** Currency movements can affect cross-country comparisons.
- **Data availability:** Some countries may have missing or delayed observations.
- **Revisions:** Historical World Bank series can be revised.
- **Descriptive analysis:** A change over time does not prove causation.
- **Country comparability:** Differences in national statistical systems and data coverage may affect comparisons.

## 8. Quality checks before publishing

- Confirm the indicator codes and labels.
- Record the retrieval date.
- Check the latest year available for each country.
- Check missing observations before comparing endpoints.
- Verify calculations independently for at least one row.
- Do not treat missing data as zero.
- State units in every chart and table.
- Avoid causal claims unless supported by additional evidence.

## 9. Possible next steps

- Add a chart of GDP per capita and population over time.
- Add inflation-adjusted GDP per capita for a more meaningful real-value comparison.
- Compare additional countries with a clear selection rationale.
- Add a notebook showing the full analysis workflow.
- Include a short plain-language executive summary for a non-technical audience.
