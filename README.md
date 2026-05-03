# ✈️ DelayDetailer: US Flight Delay Intelligence Dashboard

**Live Hosted Application:** https://019dee08-20a8-8420-f7d2-2b915adaaf63.share.connect.posit.cloud/
<img width="1895" height="899" alt="image" src="https://github.com/user-attachments/assets/2607e2a3-9f4e-4de2-87e7-4f7168d76f9f" />

---

# 1. Summary

DelayDetailer is an interactive Python Shiny dashboard that looks at trends in **US domestic flight punctuality, airline reliability, airport congestion, and operational disruption** from **2019 to 2023**. The main goal of the visualization is to turn a huge aviation dataset into a business intelligence app that is easy to use and can help people look into delays, cancellations, route inefficiencies, and the reasons for delays.
The target audience for this dashboard includes:

* aviation analysts,
* airline operations planners,
* transport researchers,
* and general users interested in understanding historical airline performance.

The visualization was made to balance high-level executive KPIs with deeper analytical tabs so that both casual users and those who are technically curious can get information. The app uses geographic mapping, comparative airline benchmarking, temporal trend exploration, and advanced analytics to give users a general but easy-to-understand idea of where, when, and why flight delays happen in US domestic aviation.
---

# 2. Background Research

Before making DelayDetailer, we looked at a number of existing aviation analytics apps and public dashboards to learn about common design patterns, user expectations, and visual opportunities in the airline intelligence field.

### (a) FlightAware Delay Tracker

FlightAware lets you track flights in real time, see how busy airports are, and keep an eye on cancellations. Its dashboards focus on quick operational visibility and make heavy use of tabular delay indicators. This helped us decide to add executive KPI cards and airport-level disruption summaries to DelayDetailer.

### (b) Bureau of Transportation Statistics Aviation Data Portal

The Bureau of Transportation Statistics gives raw operational airline performance reports, but they are hard to read and not very interactive. This showed that there should be a more accessible visual storytelling layer over similar aviation metrics.

### (c) Tableau Public Airline Delay Dashboards

We looked at a few Tableau dashboards that showed how on-time airlines were. These frequently utilized route comparisons, trend lines, and cancellation heatmaps, which impacted the incorporation of route intelligence, annual trends, and comparative airline benchmarking.


The review of these systems showed that many existing applications are either:

* highly technical but visually dry, or
* visually appealing but lacking analytical depth.

DelayDetailer was made to fit between these two extremes by combining detailed analysis with better user interaction.
---

# 3. Data Source and Data Cleaning

## 3.1 Data Source

The primary dataset used in this project is the **US Flight Delay and Cancellation Dataset (2019–2023)** obtained from Kaggle:

Dataset Source: https://www.kaggle.com/datasets/patrickzel/flight-delay-and-cancellation-dataset-2019-2023

This dataset contains approximately **2.5 million US domestic commercial flight records** and includes:

* airline identifiers,
* flight dates,
* origin and destination airports,
* scheduled and actual departure/arrival timings,
* departure and arrival delay values,
* cancellation and diversion indicators,
* elapsed time and distance,
* detailed delay cause fields.

To support geographic mapping functionality, a secondary airport coordinate dataset was used from the public OurAirports repository:

Airport Coordinate Source: https://davidmegginson.github.io/ourairports-data/airports.csv

---

## 3.2 Data Cleaning Activities Completed in Python

Substantial preprocessing was required before visualisation.

The main cleaning activities included:

* making sure that raw column names are the same,
* getting rid of unnecessary raw transport metadata,
* parsing dates and pulling out year/month/day time variables,
* changing all the timing and delay fields to numbers,
* how to deal with missing values in the structure caused by canceled flights,
* putting neutral zero values in empty records for delay causes,
* making new binary indicator fields like delayed, canceled, or diverted,
* making engineered variables, such as:

  * route labels,
  * delay severity,
  * dominant delay cause,
  * punctuality status,
  * seasonal category,
* creation of multiple summary tables for efficient Shiny rendering.

A dedicated notebook was used to perform this preprocessing and export cleaned CSV files to the application.

---

# 4. Honest Critical Review

## 4.1 Key Challenges Encountered

The biggest problem with this project was dealing with the size and inconsistency of the raw aviation dataset. The first attempts at preprocessing used a dataset that was much bigger and wider, which caused memory problems, unusable null structures, and raw transport fields that were too complicated. This meant that the preprocessing pipeline and the entire dataset had to be changed. The first dataset was https://www.kaggle.com/datasets/shubhamsingh42/flight-delay-dataset-2018-2024?select=flight_data_2018_2024.csv. It said it was for 2018-2024, but it only had data for 2024.

The second big problem was how easy it was to use the dashboard. The first Shiny prototypes worked well, but they looked boring, were too small, and were hard to use. To make Bootstrap's layout work better, the readability of charts, the naming of tables, and the clarity of hover labels, a lot of iterative refinement was needed.

<img width="1550" height="568" alt="b9615e2b-cd8b-4965-9829-326f5a3ea964" src="https://github.com/user-attachments/assets/c06c01c4-1978-4879-8411-1654a9bd1625" />


Another big problem was the size of dataset made it impossible to host anywhere, Github file storage limit was exceeded and converting it to paraquet alone wouldnt compress the file below 100mb so using ChatGPT and brotli compression was used to also reduce ram for posit

The hosted Shiny app also needed a lot of debugging because Python Shiny layouts have some problems, like `fillable=True` making plot heights unexpectedly smaller.

---

## 4.2 Two Key Strengths of the Visualisation

### Strength 1 — Breadth of Analytical Coverage

One of the best things about DelayDetailer is that it does not just show you one static dashboard but it gives you a multi-page analytical platform. Users can go from executive KPIs to airlines, airports, routes, time trends, geographic intelligence, and advanced diagnostics. This gives you a lot more analytical value than a one-page chart board.


### Strength 2 — Strong Interactivity and Comparative Exploration

The app uses a lot of:
* filters that change,
* labels that hover,
* data grids that can be searched,
* interaction with geographic maps,
* charts that show how things compare to each other.

Instead of just reading charts, this lets users actively explore and compare operational performance.

---

## 4.3 Main Weakness of the Work

The main problem with the project is that the dashboard does not predict what will happen; it just describes what has happened. The Smart Explorer shows historical route-based delay risk, but the app does not yet have a formal machine learning prediction engine. A future extension might add a classification model for predicting delays based on probability. It would also be nice to have an API that collects current data. 


---

## 4.4 Technical Issues and Limitations

There are still some technical problems:
* Sometimes, Python Shiny layout management needed manual overrides for plot height,
* Even though they are very big, Plotly tables can still be hard to render,
* To make some charts easier to read, the axes had to be manually limited.
* To find the geographic coordinates of an airport, you need to look up the airport code in a separate source.

Even with these problems, the deployed version works well for all major analytical tasks.

---

# 5. Hosted Application Link

The final deployed dashboard can be accessed here:

**DelayDetailer Hosted App:** https://019dee08-20a8-8420-f7d2-2b915adaaf63.share.connect.posit.cloud/

---

# 6. Additional Information: User Testing and Review

Informal user testing was conducted with housemates during the final dashboard refinement phase. Feedback was provided by vivienbenoy@gmail.com, d00260767@student.dkit.ie, estermarie.balgova@dkit.ie

Key feedback received included:
* overview page doesnt have much info
* charts that at first look boring,

 <img width="930" height="478" alt="730b60c6-c75c-4f82-9b5a-7a8b0ce752d6" src="https://github.com/user-attachments/assets/502798ed-60d7-4522-98ce-848f21ce17e4" />

* KPI sections feeling too tight,
* some hover labels show the technical names of dataframe variables,
* filtering airlines that shows too few by default,
* route delay charts that hide small but important differences.

<img width="1898" height="482" alt="9d4740e9-0393-4829-8fa3-ae3693a4031f" src="https://github.com/user-attachments/assets/a5e3ca90-e91c-486b-b3cc-dce4d0a00486" />



As a result of this testing, several improvements were implemented:

* All tabs now have bootstrap styling,
* The color palettes for graphs were improved,
* The hover labels were rewritten in language that is easy for  people to understand.
* All airlines were added to the airline filters,
* The names of the technical fields were changed to the names of the tables.
* the average arrival delay route chart axis was manually made narrower to make it easier to tell the difference between them,
* Banners with information about the page were added to help users.

This user review process significantly improved the dashboard’s readability and practical usability.

<img width="1883" height="765" alt="image" src="https://github.com/user-attachments/assets/3d167540-786e-4d0b-a396-93c918ad8f12" />


---

# 7. Technical Stack and Repository Structure

This project was developed using:

* Python 3.11
* Python Shiny
* Pandas
* Plotly
* ShinyWidgets
* Bootstrap
* Jupyter Notebook

Main files included:

* `app.py`
* `notebooks/01_cleaning_feature_engineering_v2.ipynb`
* `covertparaquet.py`
* processed CSV summary tables
* requirements.txt

---

# 8. Repository Link

GitHub Repository: https://github.com/Ferreter/DelayDetailer
