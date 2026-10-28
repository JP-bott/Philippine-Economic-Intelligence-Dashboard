# Philippine Economic Intelligence Dashboard

**Independent Philippine regional economics atlas** built by **John Paul Torres**. A responsive React/Vite data application with a map of all **18 Philippine regions**, source-traceable PSA observations, dynamic regional comparisons, and reproducible offline data preparation.

> **Real, published PSA data. Not a simulated dashboard.** Figures in the shipped snapshot were transcribed from the linked Philippine Statistics Authority (PSA) publications and official PSA OpenSTAT tables. Data is a fixed, clearly dated snapshot, **not a live PSA feed**, and coverage differs by indicator and publication period. This application is not affiliated with or endorsed by the PSA.

## Questions the dashboard answers

- Which regional economies grew fastest at **2018 constant prices** in 2024 and 2025?
- How did **2025 annual average inflation** differ between regions? Which regions experienced year-average declines in prices?
- Where was the **July 2025 preliminary unemployment rate** highest? How does it differ from regional growth?
- Which regions showed falling or rising **family poverty incidence** between the 2018, 2021, and 2023 FIES survey waves?
- How can two or three regional profiles be compared without accidentally mixing reporting periods?

## Features

- 18-region SVG choropleth; clickable, keyboard-selectable regions, synchronized details, map zoom, accessible hover/focus labels
- Realtime client-side metric switching, island-group filters, searchable region names, period selectors and ranking order
- KPI cards, national benchmark (when published), region leaderboard, selected-region profile, data-driven insight summaries
- Region comparison matrix and per-metric trend plots from actual reporting periods; no interpolation of missing observations
- Downloadable filtered CSV, methodology section with direct PSA source references
- Responsive enterprise-style UI; no credentials, paid APIs or database required
- Versioned source CSV catalog and Python validation/snapshot build, Node unit tests and GitHub Actions build verification

## The source data

| Metric | Coverage shipped | Meaning | Source |
|---|---|---|---|
| Real GRDP growth | 2024–2025; 18/18 in 2025, 17/18 in 2024 | Year-on-year **real** growth, constant 2018 prices; **not GDP levels** | [PSA Regional Accounts](https://psa.gov.ph/statistics/grdp), [PSA OpenSTAT GRDP matrix](https://openstat.psa.gov.ph/PXWeb/pxweb/en/DB/DB__2B__GP__RG__GRD/?tablelist=true) |
| Regional inflation | 2025; 18/18 | Annual average CPI-based inflation, all-income households, 2018 basket | [PSA 2025 regional annual inflation release](https://rsso08.psa.gov.ph/content/summary-inflation-report-consumer-price-index-all-income-households-2018-base-year-december) |
| Unemployment | July 2025; 18/18 | **Preliminary monthly** unemployment rate; not the 2025 annual rate | [PSA July 2025 Labor Force Survey infographic](https://psa.gov.ph/sites/default/files/infographics/July%202025%20LAbor%20Force%20Survey.pdf) |
| Family poverty | 2018, 2021, 2023; 18/18 in each | Full-year poverty incidence **among families**, not population | [PSA 2023 Full Year Official Poverty Statistics, Table 3](https://psa.gov.ph/sites/default/files/phdsd/2023%20FY%20Official%20PovStat%20Publication%20Report_r2.pdf) |
| Boundaries | 18 regions (NIR included) | Low-resolution visualization-only boundaries | [PSA PSGC](https://psa.gov.ph/classification/psgc/regions) / [faeldon/philippines-json-maps](https://github.com/faeldon/philippines-json-maps) |

**Important interpretation:** 2025 growth, 2025 inflation, July 2025 unemployment and 2023 poverty were not measured in the same period. Never treat these series as synchronous, infer causality from visually coincident patterns, or present the 2023 family-poverty estimate as a 2025 figure. Results may be revised by PSA. The 2024/2025 GRDP series reflects changes in the definition of regions, including NIR and the Sulu transfer. A blank figure is intentionally absent data, never zero.

### Data provenance and boundary licensing

The 2025 growth values are reported in the PSA April 23, 2026 Regional Accounts release and summary; 2024 values were taken from the April 22, 2025 release and PSA regional growth chart. The 2024 SOCCSKSARGEN observation was not verified in our accessible source subset and remains missing. Inflation was compiled from the PSA all-income-households 2025 annual average figure, *not* the separate bottom-30%-income statistic. Poverty values use PSA's post-NIR 2023 publication Table 3 (including the adjusted 2018/2021 back estimates). If new PSA releases revise historical values, update the CSV and citations together.

Regional boundary geometry comes from the community open-data repository `faeldon/philippines-json-maps`, its `latest/topojson/country/lowres/country.topo.0.001.json` file, whose source PSGC shapefiles are described in that repository. It is not a legal boundary service. Review [source project license](https://github.com/faeldon/philippines-json-maps/blob/master/LICENSE) before redistributing map assets separately.

## Run locally

```sh
npm install
npm run dev
```

Open the address printed by Vite, typically `http://localhost:5173`.

## Rebuild and check the data

The human-auditable source catalog is `data/regions.csv` and `data/observations.csv`. The static artifact `public/data/snapshot.json` is produced with:

```sh
python scripts/prepare_data.py
npm test
npm run build
```

The pipeline validates uniqueness of the region / metric / period key, all 18 PSGC identifiers, source families, finite numeric values, accepted reporting periods and range bounds. Any bad values fail before producing the JSON snapshot. The chart, map and CSV export all consume that same generated file. GitHub Actions regenerates the dataset and fails if the checked-in snapshot differs.

### Optional OpenSTAT CSV updates

To expand or revise the catalog with verified PSA OpenSTAT downloads, export a long-format table from [OpenSTAT](https://openstat.psa.gov.ph/) (one region/metric/period per row), inspect units and valuation type, then run the opt-in import utility:

```sh
python scripts/import_openstat.py --input /path/to/long-format-grdp.csv \
  --metric grdp_growth --period 2025 \
  --region-column Region --value-column Value \
  --filter-column 'Type of Valuation' --filter-value 'At Constant 2018 Prices'
# Preview only unless --write is added. Validate first, then:
python scripts/import_openstat.py ... --write
python scripts/prepare_data.py
npm test
```

CSV layouts from PXWeb vary. The importer intentionally requires explicit column mapping, performs a dry-run by default, rejects unknown region names, and never silently interpolates missing values. It is not a fully automated PSA API integration or a guarantee of current availability. Updates require research and manual source review.

## Deploy on Vercel

Import `JP-bott/Philippine-Economic-Intelligence-Dashboard` as a Vite project. Build command: `npm run build`. Output directory: `dist`. No environment variables are required. Static geography and observations are checked into `public/data/`; they work without a third-party API during site visits.

## Tech stack

React 19, Vite 6, Recharts, D3 Geo, TopoJSON Client, Lucide icons, vanilla CSS design tokens, Python standard-library ETL, Node test runner, GitHub Actions.

## Future extensions

- Direct PSA PXWeb API ingestion with release-to-release change detection and schema validation (subject to official API availability)
- Regional GDP **levels** and sector breakdown from normalized OpenSTAT matrices
- Additional monthly CPI and labor histories, consistently disaggregated by 18-region geography
- Release metadata/version diffs, regional demographics, per-capita GDP, and cross-indicator scatterplots

## Attribution

Statistics: Philippine Statistics Authority. Source links above and within the app. Map geometry: faeldon/philippines-json-maps. Application: © 2026 John Paul Torres. Original application code: MIT License (excluding third-party map data and PSA source documents).