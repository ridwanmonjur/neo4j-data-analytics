# EM-DAT Disaster Dataset - Data Dictionary

## Overview
The Emergency Events Database (EM-DAT) contains essential core data on the occurrence and effects of over 26,000 mass disasters worldwide from 1900 to the present. Maintained by the Centre for Research on the Epidemiology of Disasters (CRED) at the Université catholique de Louvain, Belgium.

**Neo4j Implementation**: This dictionary describes the **27 properties** loaded into  `Disaster` nodes, which represent a curated subset of the full EM-DAT dataset optimized for graph analysis and relationship to HDI data.

---

## Primary Identifiers

| Column | Neo4j Property | Data Type | Description |
|--------|----------------|-----------|-------------|
| `DisNo.` | `disNo` | String | **Primary Key** - Unique disaster identifier (e.g., "2000-0001-AGO") |
| `ISO` | `iso` | String | ISO 3166-1 alpha-3 country code (e.g., "USA", "CHN") |
| `Country` | `country` | String | Full country name where disaster occurred |

---

## Geographic Information

| Column | Neo4j Property | Data Type | Description |
|--------|----------------|-----------|-------------|
| `Region` | `region` | String | Geographic region (e.g., "Asia", "Africa", "Americas", "Europe") |
| `Subregion` | `subregion` | String | Geographic subregion (e.g., "Southern Asia", "Sub-Saharan Africa") |
| `Location` | `location` | String | Specific location details within country (cities, provinces, districts) |
| `Latitude` | `latitude` | Float | Geographic latitude coordinate (decimal degrees) |
| `Longitude` | `longitude` | Float | Geographic longitude coordinate (decimal degrees) |
| `River Basin` | `riverBasin` | String | Name of river basin(s) affected (for water-related disasters) |

---

## Disaster Classification

| Column | Neo4j Property | Data Type | Description | Example Values |
|--------|----------------|-----------|-------------|----------------|
| `Disaster Group` | `disasterGroup` | String | High-level disaster category | Natural, Technological |
| `Disaster Type` | `disasterType` | String | Specific disaster type | Earthquake, Flood, Storm, Drought, Epidemic, Fire |
| `Disaster Subtype` | `disasterSubtype` | String | Detailed disaster subtype | Riverine flood, Tropical cyclone, Ground movement, etc. |
| `Event Name` | `eventName` | String | Named event if applicable (e.g., "Hurricane Katrina", "Pacaya") |

---

## Disaster Characteristics

| Column | Neo4j Property | Data Type | Description | Unit/Scale |
|--------|----------------|-----------|-------------|------------|
| `Magnitude` | `magnitude` | Float | Intensity measurement of the disaster | Varies by type |
| `Magnitude Scale` | `magnitudeScale` | String | Scale used for magnitude | Moment Magnitude, Kph, °C, Km2, etc. |

---

## Temporal Information

| Column | Neo4j Property | Data Type | Description |
|--------|----------------|-----------|-------------|
| `Start Year` | `startYear` | Integer | Year disaster began |
| `Start Month` | `startMonth` | Integer | Month disaster began (1-12, null if unknown) |
| `Start Day` | `startDay` | Integer | Day disaster began (1-31, null if unknown) |
| `End Year` | `endYear` | Integer | Year disaster ended |
| `End Month` | `endMonth` | Integer | Month disaster ended (1-12, null if unknown) |
| `End Day` | `endDay` | Integer | Day disaster ended (1-31, null if unknown) |

---

## Human Impact

| Column | Neo4j Property | Data Type | Description | Unit/Scale |
|--------|----------------|-----------|-------------|------------|
| `Total Deaths` | `totalDeaths` | Integer | Number of fatalities | Count |
| `No. Injured` | `injured` | Integer | Number of people injured | Count |
| `No. Affected` | `affected` | Integer | People affected (requiring immediate assistance) | Count |
| `No. Homeless` | `homeless` | Integer | People left homeless | Count |
| `Total Affected` | `totalAffected` | Integer | Sum of injured, affected, and homeless | Count |

**Note**: "Affected" refers to people requiring immediate assistance during emergency (food, water, shelter, sanitation, medical assistance).

---

## Economic Impact

| Column | Neo4j Property | Data Type | Description | Unit/Scale |
|--------|----------------|-----------|-------------|------------|
| `Total Damage, Adjusted ('000 US$)` | `totalDamage` | Float | **Inflation-adjusted** total economic damage | Thousands USD (2023) |

**Note**: Neo4j schema stores the adjusted damage value for consistent temporal comparisons.

---

## Disaster Classification Hierarchy

### Natural Disasters
1. **Geophysical**
   - Earthquake (ground movement, tsunami)
   - Volcanic activity (ash fall, lava flow, pyroclastic flow)
   - Dry mass movement (rockfall, landslide, avalanche)

2. **Hydrological**
   - Flood (riverine, coastal, flash flood)
   - Mass movement wet (landslide, mudslide, avalanche)

3. **Meteorological**
   - Storm (tropical cyclone, tornado, blizzard, extratropical)
   - Extreme temperature (heat wave, cold wave, severe winter)

4. **Climatological**
   - Drought
   - Wildfire (forest, land, bush fire)
   - Glacial lake outburst

5. **Biological**
   - Epidemic (viral, bacterial, parasitic, fungal, prion)
   - Insect infestation
   - Animal incident

### Technological Disasters
1. **Industrial Accident**
   - Chemical spill, explosion, fire, gas leak, poisoning, radiation, collapse

2. **Transport Accident**
   - Air, rail, road, water transport

3. **Miscellaneous Accident**
   - Collapse, explosion, fire, other

---

## Data Quality Notes

### Inclusion Criteria
A disaster is entered into EM-DAT if at least one of the following criteria is met:
- 10 or more people killed
- 100 or more people affected
- Declaration of state of emergency
- Call for international assistance

### Missing Values
- Null/empty cells indicate data not available or not applicable
- Economic damage often incomplete, especially for older events
- Some locations may lack precise coordinates

### Geographic Coverage
- Global coverage, but reporting quality varies by country and time period
- Better coverage for more recent disasters and developed countries

### Temporal Coverage
- Database starts from 1900
- More comprehensive coverage from 1970s onwards
- Most recent events may have preliminary data subject to revision

---

## Key Relationships for Neo4j Graph

### Node Label
- `Disaster`

### Primary Key
- `disNo` (unique identifier for each disaster event)

### Composite Key for Relationships
- `iso` + `startYear` (used to link to HDI_Record nodes)

### Loaded Properties (27 total)
```cypher
CREATE (d:Disaster {
  disNo: string,           // Primary identifier
  iso: string,             // Country code (for relationships)
  country: string,         // Country name
  region: string,          // Geographic region
  subregion: string,       // Geographic subregion
  disasterGroup: string,   // Natural/Technological
  disasterType: string,    // Earthquake, Flood, Storm, etc.
  disasterSubtype: string, // Specific subtype
  eventName: string,       // Named event (if applicable)
  location: string,        // Specific location details
  startYear: integer,      // Year (for relationships)
  startMonth: integer,     // Month (nullable)
  startDay: integer,       // Day (nullable)
  endYear: integer,        // End year (nullable)
  endMonth: integer,       // End month (nullable)
  endDay: integer,         // End day (nullable)
  totalDeaths: integer,    // Fatalities
  injured: integer,        // Number injured
  affected: integer,       // Number affected
  homeless: integer,       // Number homeless
  totalAffected: integer,  // Total impact
  totalDamage: float,      // Adjusted economic damage (thousands USD)
  magnitude: float,        // Disaster magnitude
  magnitudeScale: string,  // Scale used
  latitude: float,         // Geographic coordinate
  longitude: float,        // Geographic coordinate
  riverBasin: string,      // River basin (if applicable)
  createdAt: datetime      // Timestamp when loaded
})
```

### Main Relationship
```cypher
(:Disaster)-[:HAPPENED_IN_COUNTRY_YEAR]->(:HDI_Record)
```
Links disasters to socioeconomic context based on country (iso) and year (startYear)

---

## Properties NOT Loaded from Source CSV

The following columns exist in the source EM-DAT CSV but are **not loaded** into Neo4j database:

- `Historic` - Whether disaster is historic
- `Classification Key` - Hierarchical code
- `Disaster Subgroup` - Additional classification layer
- `Origin` - Cause/origin
- `Associated Types` - Related disaster types
- `OFDA/BHA Response` - US aid response
- `Appeal` - International appeal status
- `Declaration` - Emergency declaration
- `AID Contribution` - Aid amounts
- `External IDs` - External database IDs
- `Reconstruction Costs` - Reconstruction expenses
- `Insured Damage` - Insurance claims
- `CPI` - Consumer Price Index
- `Admin Units` - Administrative unit details
- `Entry Date` - Database entry date
- `Last Update` - Last modification date


---

## Common Analysis Patterns

1. **Temporal Trends**: Disaster frequency and severity over time
2. **Geographic Patterns**: High-risk regions and countries
3. **Disaster Types**: Most deadly/costly disaster categories
4. **Socioeconomic Context**: Impact varies by development level (link to HDI)
5. **Response Patterns**: International aid and declaration patterns
6. **Climate Change**: Increasing frequency of weather-related disasters

---


