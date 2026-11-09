# Sources and Attribution

This project uses the World Bank's public Indicators API for demonstration and learning.

## Primary documentation

1. **About the Indicators API**  
   https://datahelpdesk.worldbank.org/knowledgebase/articles/889392  
   Overview of the Indicators API, its version 2 structure, coverage, and access.

2. **API Basic Call Structures**  
   https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structures  
   Official reference for endpoint structures, query parameters, formats, pagination, and response behavior.

3. **Indicator API Queries**  
   https://datahelpdesk.worldbank.org/knowledgebase/articles/898599-indicator-api-queries  
   Official reference for indicator queries and indicator metadata.

4. **New Features and Enhancements in the V2 API**  
   https://datahelpdesk.worldbank.org/knowledgebase/articles/1886674-new-features-and-enhancements-in-the-v2-api  
   Notes on JSON responses and enhancements to the version 2 API.

## API endpoints used

- GDP per capita (current US$), selected countries:  
  `https://api.worldbank.org/v2/country/NGA;GHA;KEN;ZAF/indicator/NY.GDP.PCAP.CD?date=2010:2023&format=json&per_page=1000`

- Population, total, selected countries:  
  `https://api.worldbank.org/v2/country/NGA;GHA;KEN;ZAF/indicator/SP.POP.TOTL?date=2010:2023&format=json&per_page=1000`

These endpoints are examples. The analysis script constructs requests based on the command-line arguments.

## Attribution

When reusing or publishing World Bank data, identify the World Bank as the source and follow the applicable World Bank data-use and attribution terms. Consult the official [World Bank Data Terms of Use](https://www.worldbank.org/en/about/legal/terms-of-use-for-datasets) before redistribution.

This repository is an independent educational portfolio project and is not an official World Bank product.
