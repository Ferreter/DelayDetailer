# ✈️ DelayDetailer: US Flight Delay Intelligence Dashboard

DelayDetailer is an interactive **Python Shiny aviation analytics platform** designed to explore **US domestic airline punctuality, route disruption, airport congestion, cancellation behaviour, and delay causes** across the **2019–2023 period**.

---
Published Link : https://019dee08-20a8-8420-f7d2-2b915adaaf63.share.connect.posit.cloud/
---
## 📌 Project Objective

The primary goal of this project is to:

- clean and preprocess a multi-year US flight operations dataset,
- engineer analytical features for airline and airport intelligence,
- perform exploratory and comparative delay analysis,
- and deliver a polished **interactive Python Shiny dashboard** for end users.

The dashboard allows users to investigate:

- airline reliability,
- airport performance,
- problematic flight routes,
- yearly and monthly operational trends,
- causes of delays,
- and historical route-specific delay risk.

---

## 📊 Dataset Overview

This project uses a **US Domestic Flight Delay Dataset (2019–2023)** containing over **2.5 million commercial flight records**.

### Included variables:

- Flight date
- Airline and airline code
- Flight number
- Origin and destination airports
- Scheduled and actual departure/arrival times
- Departure and arrival delay
- Taxi-out and taxi-in durations
- Cancellation and diversion indicators
- Elapsed and air time
- Distance travelled
- Delay cause categories:
  - Carrier
  - Weather
  - National Air System
  - Security
  - Late Aircraft

---
Dataset Link : https://www.kaggle.com/datasets/patrickzel/flight-delay-and-cancellation-dataset-2019-2023?utm_source=chatgpt.com&select=flights_sample_3m.csv
Dataset Link for Geomapping : https://davidmegginson.github.io/ourairports-data/airports.csv
---

## 🖥️ Dashboard Modules

SkyScope consists of the following analytical pages:

### 1. Executive Overview
High-level KPI summary including:

- total flights analysed,
- average arrival delay,
- delay rate,
- cancellation rate,
- worst delay route,
- most disrupted airline.

---

### 2. Airline Performance Analysis
Compare airline punctuality and reliability through:

- average arrival delay benchmarking,
- airline delay rates,
- airline ranking tables.

---

### 3. Airport & Route Intelligence
Explore:

- busiest US origin airports,
- worst-performing routes,
- route-level operational metrics,
- US airport geographic delay map.

---

### 4. Temporal Trends
Investigate:

- yearly delay progression,
- monthly seasonality,
- weekday operational behaviour,
- pre-pandemic vs recovery changes.

---

### 5. Delay Cause Diagnostics
Understand what drives disruption:

- carrier delays,
- weather delays,
- NAS congestion,
- security delays,
- late aircraft effects.

---

### 6. Advanced Analytics
Includes:

- operational correlation heatmap,
- airport risk quadrant,
- airline reliability matrix.

---

### 7. Smart Explorer
A historical route risk explorer that allows users to estimate likely delay behaviour for specific:

- years,
- origin airports,
- destination airports.

---

## 🛠️ Technology Stack

This project was built using:

- **Python 3.11+**
- **Python Shiny**
- **Pandas**
- **Plotly**
- **ShinyWidgets**
- **Bootstrap UI Components**
- **Jupyter Notebook**
