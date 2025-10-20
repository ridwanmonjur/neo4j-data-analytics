# Human Development Index (HDI) Dataset - Data Dictionary

## Overview
This dataset contains Human Development Index (HDI) and related socioeconomic indicators compiled by the United Nations Development Programme (UNDP). It provides comprehensive development metrics across countries and years.

---

## Primary Identifiers

| Column | Data Type | Description |
|--------|-----------|-------------|
| `ISO` | String | ISO 3166-1 alpha-3 country code (e.g., "AFG", "USA") |
| `country` | String | Full country name |
| `year` | Integer | Year of observation |
| `region` | String | Geographic region (e.g., "SA" = Southern Asia, "SSA" = Sub-Saharan Africa) |
| `hdicode` | String | HDI classification level: "Low", "Medium", "High", "Very High" |
| `hdi_rank_2023` | Float | Country's HDI ranking in 2023 (1 = highest) |

---

## Core HDI Metrics

| Column | Data Type | Description | Unit/Scale |
|--------|-----------|-------------|------------|
| `hdi` | Float | Human Development Index - composite measure of health, education, and income | 0-1 scale |
| `ihdi` | Float | Inequality-adjusted HDI - HDI value adjusted for inequality | 0-1 scale |
| `phdi` | Float | Planetary pressures-adjusted HDI - HDI adjusted for environmental impact | 0-1 scale |
| `hdi_f` | Float | HDI value for females | 0-1 scale |
| `hdi_m` | Float | HDI value for males | 0-1 scale |
| `loss` | Float | Loss in HDI due to inequality | Percentage |
| `diff_hdi_phdi` | Float | Difference between HDI and PHDI | Absolute value |
| `rankdiff_hdi_phdi` | Float | Rank difference between HDI and PHDI | Integer |

---

## Health Indicators

| Column | Data Type | Description | Unit/Scale |
|--------|-----------|-------------|------------|
| `le` | Float | Life expectancy at birth (total population) | Years |
| `le_f` | Float | Life expectancy at birth for females | Years |
| `le_m` | Float | Life expectancy at birth for males | Years |
| `ineq_le` | Float | Inequality in life expectancy | Coefficient |
| `mmr` | Float | Maternal mortality ratio - deaths per 100,000 live births | Rate |
| `abr` | Float | Adolescent birth rate - births per 1,000 women ages 15-19 | Rate |

---

## Education Indicators

| Column | Data Type | Description | Unit/Scale |
|--------|-----------|-------------|------------|
| `mys` | Float | Mean years of schooling (total population, ages 25+) | Years |
| `mys_f` | Float | Mean years of schooling for females | Years |
| `mys_m` | Float | Mean years of schooling for males | Years |
| `eys` | Float | Expected years of schooling (total population) | Years |
| `eys_f` | Float | Expected years of schooling for females | Years |
| `eys_m` | Float | Expected years of schooling for males | Years |
| `ineq_edu` | Float | Inequality in education | Coefficient |
| `se_f` | Float | Population with at least some secondary education, females (% ages 25+) | Percentage |
| `se_m` | Float | Population with at least some secondary education, males (% ages 25+) | Percentage |

---

## Economic Indicators

| Column | Data Type | Description | Unit/Scale |
|--------|-----------|-------------|------------|
| `gnipc` | Float | Gross National Income per capita (total population) | 2017 PPP $ |
| `gni_pc_f` | Float | GNI per capita for females | 2017 PPP $ |
| `gni_pc_m` | Float | GNI per capita for males | 2017 PPP $ |
| `ineq_inc` | Float | Inequality in income | Coefficient |
| `coef_ineq` | Float | Coefficient of human inequality (average of inequalities) | Coefficient |

---

## Gender Indicators

| Column | Data Type | Description | Unit/Scale |
|--------|-----------|-------------|------------|
| `gii` | Float | Gender Inequality Index - composite measure of gender disparities | 0-1 scale (0=equality) |
| `gii_rank` | Float | Rank based on GII value | Integer |
| `gdi` | Float | Gender Development Index - ratio of female to male HDI | Ratio |
| `gdi_group` | String | GDI classification group (1-5, where 1=highest equality) | Category |
| `mf` | Float | Male-to-female ratio (population or other metric) | Ratio |
| `lfpr_f` | Float | Labor force participation rate for females (% ages 15+) | Percentage |
| `lfpr_m` | Float | Labor force participation rate for males (% ages 15+) | Percentage |
| `pr_f` | Float | Parliamentary representation, females (% of seats) | Percentage |
| `pr_m` | Float | Parliamentary representation, males (% of seats) | Percentage |

---

## Environmental & Demographic Indicators

| Column | Data Type | Description | Unit/Scale |
|--------|-----------|-------------|------------|
| `co2_prod` | Float | CO2 production per capita | Tonnes per capita |
| `pop_total` | Float | Total population | Millions |

---


## Key Relationships for Neo4j Graph

### Recommended Node Label
- `HDI_Record`

### Composite Key
- `iso` + `year` (unique identifier for each record)

### Common Relationships
- `HAPPENED_IN_COUNTRY_YEAR` (from Disaster nodes)
- Can link to country-level nodes, regional aggregations

---
