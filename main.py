#import libraries
from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_widget
import pandas as pd
import plotly.express as px
from pathlib import Path
# path for dataset
DATA_DIR = Path("dataset/processed")
# load datasets
flights = pd.read_csv(DATA_DIR / "flights_cleaned.csv")
airline_summary = pd.read_csv(DATA_DIR / "airline_summary.csv")
airport_summary = pd.read_csv(DATA_DIR / "airport_summary.csv")
route_summary = pd.read_csv(DATA_DIR / "route_summary.csv")
monthly_summary = pd.read_csv(DATA_DIR / "monthly_summary.csv")
yearly_summary = pd.read_csv(DATA_DIR / "yearly_summary.csv")
weekday_summary = pd.read_csv(DATA_DIR / "weekday_summary.csv")
delay_cause_summary = pd.read_csv(DATA_DIR / "delay_cause_summary.csv")
status_summary = pd.read_csv(DATA_DIR / "status_summary.csv")
airport_map_summary = pd.read_csv(DATA_DIR / "airport_map_summary.csv")
# convert date column to datetime
flights["FL_DATE"] = pd.to_datetime(flights["FL_DATE"])
YEARS = sorted(flights["YEAR"].dropna().astype(int).unique().tolist()) # extract unique years from dataset for filter options
AIRLINES = sorted(flights["AIRLINE"].dropna().unique().tolist()) # extract unique airlines from dataset for filter options

# create UI with navbar and multiple panels for different sections of the dashboard
app_ui = ui.page_navbar(
    ui.nav_panel(
        "Overview",

        ui.div(
            {
                "class": "p-5 mb-4 rounded-3 text-white", #background gradient for header
                "style": "background: linear-gradient(90deg, #0d1b2a, #1b263b, #415a77);" 
            },
            
            ui.h1("DelayDetailer Aviation Intelligence Platform", class_="display-4 fw-bold"),
            ui.p(
                "An interactive multi-page dashboard for exploring US flight delays, airline reliability, airport congestion and operational disruption patterns.",
                class_="lead"
            ),
            ui.div(
                {"class": "mt-3"},
                ui.span("2019–2023 Coverage", class_="badge bg-warning text-dark me-2 p-2"),
                ui.span("US Domestic Aviation", class_="badge bg-info text-dark me-2 p-2"),
                ui.span("Airline + Airport Intelligence", class_="badge bg-success me-2 p-2"),
                ui.span("Delay Cause Diagnostics", class_="badge bg-danger p-2"),
            ),
        ),
    # sidebar layout for global filters and key metric value boxes, followed by overview charts and tables
        ui.layout_sidebar(
            ui.sidebar(
                ui.h5("Global Filters"),
                ui.input_selectize(
                    "global_years",
                    "Years",
                    choices=YEARS,
                    selected=YEARS,
                    multiple=True,
                ),
                ui.input_selectize(
                    "global_airlines",
                    "Airlines",
                    choices=AIRLINES,
                    selected=AIRLINES,
                    multiple=True,
                ),
                ui.hr(),
                ui.p(
                    "These filters update the overview and temporal trend charts.",
                    class_="text-muted small",
                ),
            ),

            ui.card(
                ui.card_header("Dashboard Interpretation"),
                ui.p(
                    "This overview summarises how airline reliability changes across selected years and carriers. "
                    "Delay rate is defined as the proportion of flights arriving at least 15 minutes late. "
                    "Use the tabs above to investigate airlines, airports, routes, temporal patterns, delay causes and advanced analytical relationships."
                ),
                class_="shadow-sm mt-3",
            ),

            ui.accordion(
                ui.accordion_panel(
                    "How to Use This Dashboard",
                    ui.p("Use the global filters to compare specific years and airlines."),
                    ui.p("Hover over charts to inspect exact values and operational statistics."),
                    ui.p("Use the later tabs to move from high-level summary into airline, route, geographic and advanced analytics."),
                ),
                open=False,
            ),
            ui.layout_columns(
            {
                "class": "p-5 mb-4 rounded-3",
            },
                ui.value_box("Total Flights", ui.output_text("total_flights"), showcase="✈️", theme="primary", style="  height:170px;"),
                ui.value_box("Average Arrival Delay", ui.output_text("avg_arr_delay"), showcase="⏱️", theme="warning"),
                ui.value_box("Delay Rate", ui.output_text("delay_rate"), showcase="📉", theme="danger"),
                ui.value_box("Cancellation Rate", ui.output_text("cancel_rate"), showcase="🚫", theme="secondary"),
                ui.value_box("Worst Avg Delay Route", ui.output_text("worst_route"), showcase="🛣️", theme="danger"),
                ui.value_box("Most Disrupted Airline", ui.output_text("worst_airline"), showcase="🏢", theme="warning")
            ),

            ui.layout_columns(
                ui.card(
                    ui.card_header("Yearly Flight Volume"),
                    ui.div(
                        output_widget("yearly_volume_chart", height="500px"),
                        style="min-height:520px;"
                    ),
                    class_="shadow-sm h-100",
                ),
                ui.card(
                    ui.card_header("Punctuality Status"),
                    output_widget("status_chart", height="600px"),
                    class_="shadow-sm",
                ),
            ),
            
            

            ui.card(
                ui.card_header("Top 10 Most Delayed Origin Airports"),
                output_widget("overview_top_delay_airports", height="650px"),
                class_="shadow-sm mt-3",
            ),


        ),
    ),ui.nav_panel(
    "Airlines",

    ui.div(
        {"class": "alert alert-primary"},
        "This section benchmarks airline operational reliability using average arrival delay, overall delay rate and a comparative airline performance ranking table."
    ),

    ui.layout_sidebar(
        ui.sidebar(
            ui.h5("Airline Controls"),
            ui.input_selectize(
                "airline_select",
                "Select airline",
                choices=AIRLINES,
                multiple=True,
                selected=AIRLINES,
            ),
            ui.hr(),
            ui.p(
                "Use the selector to compare one or multiple airlines across punctuality and delay performance metrics.",
                class_="text-muted small"
            ),
        ),

        ui.layout_columns(
            ui.card(
                ui.card_header("Average Arrival Delay by Airline"),
                output_widget("airline_delay_chart", height="500px"),
                class_="shadow-sm"
            ),
            ui.card(
                ui.card_header("Airline Delay Rate"),
                output_widget("airline_delay_rate_chart", height="500px"),
                class_="shadow-sm"
            ),
        ),

        ui.card(
            ui.card_header("Airline Ranking Table"),
            ui.output_data_frame("airline_table"),
            class_="shadow-sm mt-3"
        ),
    ),
),
    ui.nav_panel(
        "Airports & Routes",
        ui.div(
            {"class": "alert alert-info"},
            "This section identifies busy airports and high-risk routes based on historical operational performance."
        ),
        
        ui.card(
            ui.card_header("US Airport Delay Map"),
            output_widget("airport_map", height="750px"),
            class_="shadow-sm mb-3"
        ),

        ui.layout_columns(
            ui.card(
                ui.card_header("Top 15 Busiest Origin Airports"),
                output_widget("airport_volume_chart"),
                class_="shadow-sm"
            ),
            ui.card(
                ui.card_header("Worst Routes by Average Arrival Delay"),
                output_widget("route_delay_chart"),
                class_="shadow-sm"
            ),
        ),

        ui.card(
            ui.card_header("Route Performance Table"),
            ui.output_data_frame("route_table"),
            class_="shadow-sm mt-3"
        ),
    ),

    ui.nav_panel(
        "Temporal Trends",
        ui.div(
            {"class": "alert alert-secondary"},
            "The multi-year dataset allows comparison of pre-pandemic, pandemic and recovery-period flight reliability."
        ),

        ui.layout_columns(
            ui.card(
                ui.card_header("Average Arrival Delay by Year"),
                output_widget("yearly_delay_chart"),
                class_="shadow-sm"
            ),
            ui.card(
                ui.card_header("Monthly Delay Seasonality"),
                output_widget("monthly_delay_chart"),
                class_="shadow-sm"
            ),
        ),

        ui.card(
            ui.card_header("Weekday Delay Pattern"),
            output_widget("weekday_chart"),
            class_="shadow-sm mt-3"
        ),
    ),

    ui.nav_panel(
        "Delay Causes",
        ui.div(
            {"class": "alert alert-warning"},
            "Delay causes show whether disruption is mainly linked to airlines, weather, the national air system, security, or late aircraft."
        ),

    (
            ui.card(
                ui.card_header("Delay Causes by Year and Month"),
                output_widget("delay_cause_chart"),
                class_="shadow-sm"
            ),
            ui.card(
                ui.card_header("Total Delay Cause Contribution"),
                output_widget("delay_cause_total_chart"),
                class_="shadow-sm"
            ),
        ),
    ),
        
    ui.nav_panel(
        "Advanced Analytics",
        ui.div(
            {"class": "alert alert-dark"},
            "This section uses analytical visuals to identify relationships between operational variables and compare airport or airline risk."
        ),

        ui.layout_columns(
            ui.card(
                ui.card_header("Correlation Heatmap"),
                output_widget("correlation_heatmap", height="650px"),
                class_="shadow-sm"
            ),
            ui.card(
                ui.card_header("Airport Risk Quadrant"),
                output_widget("airport_risk_quadrant", height="650px"),
                class_="shadow-sm"
            ),
        ),

        ui.card(
            ui.card_header("Airline Reliability Matrix"),
            output_widget("airline_reliability_matrix", height="650px"),
            class_="shadow-sm mt-3"
        ),
    ),

    ui.nav_panel(
        "Smart Explorer",
        ui.layout_sidebar(
            ui.sidebar(
                ui.h5("Route Risk Explorer"),
                ui.input_select("year_filter", "Year", choices=YEARS),
                ui.input_select("origin_filter", "Origin airport", choices=sorted(flights["ORIGIN"].dropna().unique().tolist())),
                ui.input_select("dest_filter", "Destination airport", choices=sorted(flights["DEST"].dropna().unique().tolist())),
                ui.hr(),
                ui.p("This estimates route risk from historical matching flights.", class_="text-muted small"),
            ),

            ui.layout_columns(
                ui.value_box(
                    "Matching Flights",
                    ui.output_text("smart_flights"),
                    showcase="🔎",
                    theme="primary",
                ),
                ui.value_box(
                    "Estimated Delay Risk",
                    ui.output_text("smart_delay_risk"),
                    showcase="⚠️",
                    theme="danger",
                ),
                ui.value_box(
                    "Average Delay",
                    ui.output_text("smart_avg_delay"),
                    showcase="⏱️",
                    theme="warning",
                ),
            ),

            ui.card(
                ui.card_header("Filtered Route Records"),
                ui.output_data_frame("smart_table"),
                class_="shadow-sm mt-3"
            ),
        ),
    ),

    title="DelayDetailer",
    id="main_nav",
    bg="dark",
    inverse=True
)

# define server logic to populate outputs based on data and user inputs
def server(input, output, session):
    
    @output
    @render.text
    def worst_route():
        data = route_summary.query("total_flights >= 500").copy()

        if data.empty:
            return "No data"

        row = data.sort_values("avg_arr_delay", ascending=False).iloc[0] # find route with highest average arrival delay among routes with at least 500 flights for reliability
        return f"{row['ROUTE']} ({row['avg_arr_delay']:.1f} min)"
    
    @output
    @render.text
    def worst_airline(): # find airline with highest average arrival delay among all airlines for reliability benchmarking
        data = airline_summary.copy()

        if data.empty:
            return "No data"

        row = data.sort_values("avg_arr_delay", ascending=False).iloc[0] # find airline with highest average arrival delay among all airlines for reliability benchmarking
        return f"{row['AIRLINE_CODE']} ({row['avg_arr_delay']:.1f} min)"

    @output
    @render_widget
    def overview_top_delay_airports(): # identify top 10 worst performing origin airports by average arrival delay, filtering to those with at least 1000 departures for reliability and relevance, and visualise with a horizontal bar chart
        data = (
            airport_summary[airport_summary["total_departures"] >= 1000]
            .sort_values("avg_arr_delay", ascending=False)
            .head(10)
        )

        fig = px.bar(
            data,
            x="avg_arr_delay",
            y="ORIGIN",
            orientation="h",
            color="avg_arr_delay",
            title="Highest Average Arrival Delay Among Major Airports",
            hover_data={
                "ORIGIN_CITY": True,
                "total_departures": ":,",
                "delay_rate": ":.2%",
                "cancellation_rate": ":.2%",
            },
            labels={ #custom labels for hover and axes
                "avg_arr_delay": "Average Arrival Delay (min)",
                "ORIGIN": "Airport",
                "ORIGIN_CITY": "City",
                "total_departures": "Departures",
                "cancellation_rate": "Cancellation Rate",
                "delay_rate": "Delay Rate",
            },
        )

        fig.update_layout( 
            template="plotly_white",
            height=650,
            yaxis={"categoryorder": "total ascending"},
            margin={"r": 20, "t": 60, "l": 20, "b": 20},
        )

        return fig
    @reactive.calc # function to filter flights based on global year and airline selections, used by multiple outputs for consistent filtering across the overview section
    def filtered_flights():
        years = input.global_years()
        airlines = input.global_airlines()

        data = flights.copy()

        if years:
            data = data[data["YEAR"].isin([int(y) for y in years])]

        if airlines:
            data = data[data["AIRLINE"].isin(airlines)]

        return data

    @output
    @render.text
    def total_flights():
        return f"{len(flights):,}"

    @output
    @render.text
    def avg_arr_delay():
        data = filtered_flights()
        return f"{data['ARR_DELAY_MINUTES'].mean():.1f} min"

    @output
    @render.text
    def delay_rate():
        data = filtered_flights()
        return f"{data['IS_DELAYED'].mean() * 100:.1f}%"
    @output
    @render.text
    def cancel_rate():
        data = filtered_flights()
        return f"{data['IS_CANCELLED'].mean() * 100:.1f}%"

    @output
    @render_widget
    def yearly_volume_chart():
        data = (
            filtered_flights()
            .groupby("YEAR", observed=True)
            .size()
            .reset_index(name="total_flights")
        )

        fig = px.bar(
            data,
            x="YEAR",
            y="total_flights",
            title="Total Flights by Year",
            labels={"YEAR": "Year", "total_flights": "Flights"},
        )
        fig.update_layout(
            template="plotly_white",
            height=500
        )
        fig.update_layout(template="plotly_white")
        return fig

    @output
    @render_widget
    def status_chart():
        data = (
            filtered_flights()
            .groupby("PUNCTUALITY_STATUS", observed=True)
            .size()
            .reset_index(name="total_flights")
        )

        fig = px.pie(
            data,
            names="PUNCTUALITY_STATUS",
            values="total_flights",
            hole=0.45,
            title="Flight Status Distribution",
            labels={"PUNCTUALITY_STATUS": "Status", "total_flights": "Flights"},
        )
        fig.update_layout(template="plotly_white")
        return fig
    
    # reactive function to filter airline summary data based on airline selection for use in airline performance charts and table, allowing consistent filtering across multiple outputs in the airlines section
    @reactive.calc
    def selected_airline_data():
        selected = input.airline_select()
        if not selected:
            return airline_summary
        return airline_summary[airline_summary["AIRLINE"].isin(selected)]

    @output
    @render_widget
    def airline_delay_chart():
        data = selected_airline_data().sort_values("avg_arr_delay", ascending=False)
        fig = px.bar(
            data,
            x="AIRLINE",
            y="avg_arr_delay",
            title="Average Arrival Delay",
            labels={"AIRLINE": "Airline", "avg_arr_delay": "Avg arrival delay (min)"},
        )
        fig.update_layout(template="plotly_white", xaxis_tickangle=-35) #rotate x labels for readability with many airlinesw
        return fig

    @output
    @render_widget
    def airline_delay_rate_chart():
        data = selected_airline_data().copy()
        data["delay_rate_pct"] = data["delay_rate"] * 100
        fig = px.bar(
            data,
            x="AIRLINE",
            y="delay_rate_pct",
            title="Delay Rate by Airline",
            labels={"AIRLINE": "Airline", "delay_rate_pct": "Delay rate (%)"},
        )
        fig.update_layout(template="plotly_white", xaxis_tickangle=-35)
        return fig

    @output
    @render.data_frame
    def airline_table():
        data = airline_summary.copy()

        data["delay_rate"] = (data["delay_rate"] * 100).round(2)
        data["cancellation_rate"] = (data["cancellation_rate"] * 100).round(2)
        data["diversion_rate"] = (data["diversion_rate"] * 100).round(2)

        data["avg_dep_delay"] = data["avg_dep_delay"].round(2)
        data["avg_arr_delay"] = data["avg_arr_delay"].round(2)
        data["avg_distance"] = data["avg_distance"].round(0)
        data["avg_air_time"] = data["avg_air_time"].round(1)

        data = data.rename(
            columns={
                "AIRLINE_CODE": "Code",
                "AIRLINE": "Airline",
                "total_flights": "Total Flights",
                "avg_dep_delay": "Avg Departure Delay (min)",
                "avg_arr_delay": "Avg Arrival Delay (min)",
                "delay_rate": "Delay Rate (%)",
                "cancellation_rate": "Cancellation Rate (%)",
                "diversion_rate": "Diversion Rate (%)",
                "avg_distance": "Avg Distance (miles)",
                "avg_air_time": "Avg Air Time (min)",
            }
        )

        return render.DataGrid(
            data.sort_values("Total Flights", ascending=False),
            filters=True
        )
    @output
    @render_widget
    def airport_volume_chart():
        data = airport_summary.sort_values("total_departures", ascending=False).head(15).copy()

        fig = px.bar(
            data,
            x="total_departures",
            y="ORIGIN",
            orientation="h",
            color="avg_arr_delay",
            color_continuous_scale="Blues",
            hover_data={
                "ORIGIN_CITY": True,
                "total_departures": ":,",
                "avg_arr_delay": ":.2f",
                "delay_rate": ":.2%",
                "cancellation_rate": ":.2%",
            },
            labels={
                "total_departures": "Total Departures",
                "ORIGIN": "Airport",
                "avg_arr_delay": "Avg Arrival Delay (min)",
            },
        )

        fig.update_layout(
            template="plotly_white",
            height=520,
            yaxis={"categoryorder": "total ascending"},
            margin={"r": 20, "t": 20, "l": 20, "b": 20},
            coloraxis_colorbar=dict(title="Avg Delay"),
        )

        return fig
    @output
    @render_widget
    def airport_map():
        data = airport_map_summary.copy()

        data["Delay Rate (%)"] = data["delay_rate"] * 100
        data["Cancellation Rate (%)"] = data["cancellation_rate"] * 100

        data = data.rename(
            columns={
                "AIRPORT_NAME": "Airport",
                "ORIGIN": "Airport Code",
                "ORIGIN_CITY": "City",
                "total_departures": "Departures",
                "avg_arr_delay": "Average Arrival Delay (min)",
                "avg_dep_delay": "Average Departure Delay (min)",
            }
        )

        data = data.sort_values("Departures", ascending=False).head(150)

        fig = px.scatter_mapbox(
            data,
            lat="LATITUDE",
            lon="LONGITUDE",
            size="Departures",
            color="Average Arrival Delay (min)",
            hover_name="Airport",
            hover_data={
                "Airport Code": True,
                "City": True,
                "Departures": ":,",
                "Average Arrival Delay (min)": ":.2f",
                "Average Departure Delay (min)": ":.2f",
                "Delay Rate (%)": ":.2f",
                "Cancellation Rate (%)": ":.2f",
                "LATITUDE": False,
                "LONGITUDE": False,
            },
            zoom=3,
            height=750,
            title="Airport Volume and Average Arrival Delay",
            labels={
                "Average Arrival Delay (min)": "Avg Arrival Delay",
                "Departures": "Departures"
            },
        )

        fig.update_layout(
            mapbox_style="carto-positron",
            margin={"r": 0, "t": 50, "l": 0, "b": 0},
        )

        return fig
    
    @output
    @render_widget
    def correlation_heatmap():
        cols = [
            "DEP_DELAY_MINUTES",
            "ARR_DELAY_MINUTES",
            "TAXI_OUT",
            "TAXI_IN",
            "ELAPSED_TIME",
            "AIR_TIME",
            "DISTANCE",
            "DELAY_DUE_CARRIER",
            "DELAY_DUE_WEATHER",
            "DELAY_DUE_NAS",
            "DELAY_DUE_SECURITY",
            "DELAY_DUE_LATE_AIRCRAFT",
        ]

        data = filtered_flights()[cols].dropna()

        # Sample keeps app fast while preserving broad relationship structure
        if len(data) > 100000:
            data = data.sample(100000, random_state=42)

        corr = data.corr()

        fig = px.imshow(
            corr,
            text_auto=".2f",
            aspect="auto",
            title="Correlation Between Flight Delay and Operational Variables",
            labels=dict(color="Correlation"),
        )

        fig.update_layout(
            template="plotly_white",
            height=650,
            margin={"r": 20, "t": 60, "l": 20, "b": 20},
        )

        return fig
    
    @output
    @render_widget
    def airport_risk_quadrant():
        data = airport_summary.copy()

        data["Delay Rate (%)"] = data["delay_rate"] * 100
        data["Cancellation Rate (%)"] = data["cancellation_rate"] * 100
        data["Average Arrival Delay (min)"] = data["avg_arr_delay"]

        # Keep meaningful airports only
        data = data[data["total_departures"] >= 1000]

        fig = px.scatter(
            data,
            x="Cancellation Rate (%)",
            y="Average Arrival Delay (min)",
            size="total_departures",
            hover_name="ORIGIN",
            hover_data={
                "ORIGIN_CITY": True,
                "total_departures": ":,",
                "Delay Rate (%)": ":.2f",
                "Cancellation Rate (%)": ":.2f",
                "Average Arrival Delay (min)": ":.2f",
            },
            title="Airport Risk Quadrant: Delay vs Cancellation",
            labels={
                "total_departures": "Departures",
                "ORIGIN_CITY": "City",
            },
        )

        fig.add_vline(
            x=data["Cancellation Rate (%)"].median(),
            line_dash="dash",
            opacity=0.6,
        )

        fig.add_hline(
            y=data["Average Arrival Delay (min)"].median(),
            line_dash="dash",
            opacity=0.6,
        )

        fig.update_layout(
            template="plotly_white",
            height=650,
            margin={"r": 20, "t": 60, "l": 20, "b": 20},
        )

        return fig

    @output
    @render_widget
    def route_delay_chart():
        data = (
            route_summary
            .query("total_flights >= 500")
            .sort_values("avg_arr_delay", ascending=False)
            .head(15)
            .copy()
        )

        xmin = max(0, data["avg_arr_delay"].min() - 1)
        xmax = data["avg_arr_delay"].max() + 0.5

        fig = px.bar(
            data,
            x="avg_arr_delay",
            y="ROUTE",
            orientation="h",
            color="avg_arr_delay",
            color_continuous_scale="Reds",
            hover_data={
                "total_flights": ":,",
                "avg_dep_delay": ":.2f",
                "avg_arr_delay": ":.2f",
                "delay_rate": ":.2%",
                "cancellation_rate": ":.2%",
            },
            labels={
                "avg_arr_delay": "Average Arrival Delay (min)",
                "ROUTE": "Route",
            },
        )

        fig.update_xaxes(range=[xmin, xmax])

        fig.update_layout(
            template="plotly_white",
            height=520,
            yaxis={"categoryorder": "total ascending"},
            margin={"r": 20, "t": 20, "l": 20, "b": 20},
            coloraxis_colorbar=dict(title="Avg Delay"),
        )

        return fig
    
    @output
    @render_widget
    def airline_reliability_matrix():
        data = airline_summary.copy()

        data["Delay Rate (%)"] = data["delay_rate"] * 100
        data["Cancellation Rate (%)"] = data["cancellation_rate"] * 100
        data["Average Arrival Delay (min)"] = data["avg_arr_delay"]

        fig = px.scatter(
            data,
            x="Cancellation Rate (%)",
            y="Delay Rate (%)",
            size="total_flights",
            color="Average Arrival Delay (min)",
            hover_name="AIRLINE",
            hover_data={
                "AIRLINE_CODE": True,
                "total_flights": ":,",
                "Average Arrival Delay (min)": ":.2f",
                "Cancellation Rate (%)": ":.2f",
                "Delay Rate (%)": ":.2f",
            },
            title="Airline Reliability Matrix",
            labels={
                "total_flights": "Flights",
            },
        )

        fig.add_vline(
            x=data["Cancellation Rate (%)"].median(),
            line_dash="dash",
            opacity=0.6,
        )

        fig.add_hline(
            y=data["Delay Rate (%)"].median(),
            line_dash="dash",
            opacity=0.6,
        )

        fig.update_layout(
            template="plotly_white",
            height=650,
            margin={"r": 20, "t": 60, "l": 20, "b": 20},
        )

        return fig

    @output
    @render.data_frame
    def route_table():
        data = route_summary.query("total_flights >= 100").copy()

        data["delay_rate"] = (data["delay_rate"] * 100).round(2)
        data["cancellation_rate"] = (data["cancellation_rate"] * 100).round(2)
        data["avg_dep_delay"] = data["avg_dep_delay"].round(2)
        data["avg_arr_delay"] = data["avg_arr_delay"].round(2)
        data["avg_distance"] = data["avg_distance"].round(0)
        data["avg_air_time"] = data["avg_air_time"].round(1)

        data = data.rename(
            columns={
                "ORIGIN": "Origin",
                "DEST": "Destination",
                "ROUTE": "Route",
                "total_flights": "Total Flights",
                "avg_dep_delay": "Avg Departure Delay (min)",
                "avg_arr_delay": "Avg Arrival Delay (min)",
                "delay_rate": "Delay Rate (%)",
                "cancellation_rate": "Cancellation Rate (%)",
                "avg_distance": "Avg Distance (miles)",
                "avg_air_time": "Avg Air Time (min)",
            }
        )

        data = data[
            [
                "Origin",
                "Destination",
                "Route",
                "Total Flights",
                "Delay Rate (%)",
                "Cancellation Rate (%)",
                "Avg Arrival Delay (min)",
                "Avg Departure Delay (min)",
                "Avg Distance (miles)",
                "Avg Air Time (min)",
            ]
        ]

        return render.DataGrid(
            data.sort_values("Avg Arrival Delay (min)", ascending=False),
            filters=True
        )
    @output
    @render_widget
    def yearly_delay_chart():
        data = (
            filtered_flights()
            .groupby("YEAR", observed=True)
            .agg(avg_arr_delay=("ARR_DELAY_MINUTES", "mean"))
            .reset_index()
        )

        fig = px.line(
            data,
            x="YEAR",
            y="avg_arr_delay",
            markers=True,
            title="Average Arrival Delay by Year",
            labels={"YEAR": "Year", "avg_arr_delay": "Avg arrival delay (min)"},
        )
        fig.update_layout(template="plotly_white")
        return fig
    
    @output
    @render_widget
    def monthly_delay_chart():
        data = (
            filtered_flights()
            .groupby(["YEAR", "MONTH"], observed=True)
            .agg(avg_arr_delay=("ARR_DELAY_MINUTES", "mean"))
            .reset_index()
            .sort_values(["YEAR", "MONTH"])
        )

        fig = px.line(
            data,
            x="MONTH",
            y="avg_arr_delay",
            color="YEAR",
            markers=True,
            title="Monthly Delay Seasonality",
            labels={"MONTH": "Month", "avg_arr_delay": "Avg arrival delay (min)"},
        )
        fig.update_layout(template="plotly_white")
        return fig
    
    @output
    @render_widget
    def weekday_chart():
        data = weekday_summary.sort_values("DAY_OF_WEEK")
        fig = px.bar(
            data,
            x="DAY_NAME",
            y="avg_arr_delay",
            title="Average Arrival Delay by Weekday",
            labels={"DAY_NAME": "Day", "avg_arr_delay": "Avg arrival delay (min)"},
        )
        fig.update_layout(template="plotly_white")
        return fig

    @output
    @render_widget
    def delay_cause_chart():
        data = delay_cause_summary.sort_values(["YEAR", "MONTH"]).copy()

        rename_causes = {
            "DELAY_DUE_CARRIER": "Carrier",
            "DELAY_DUE_WEATHER": "Weather",
            "DELAY_DUE_NAS": "National Air System",
            "DELAY_DUE_SECURITY": "Security",
            "DELAY_DUE_LATE_AIRCRAFT": "Late Aircraft",
        }

        long = data.melt(
            id_vars=["YEAR", "MONTH"],
            value_vars=list(rename_causes.keys()),
            var_name="Cause",
            value_name="Minutes",
        )

        long["Cause"] = long["Cause"].map(rename_causes)
        long["Delay Hours"] = long["Minutes"] / 60

        fig = px.bar(
            long,
            x="MONTH",
            y="Delay Hours",
            color="Cause",
            facet_col="YEAR",
            facet_col_wrap=3,
            barmode="stack",
            category_orders={
                "MONTH": list(range(1, 13)),
                "Cause": ["Carrier", "Late Aircraft", "National Air System", "Weather", "Security"],
            },
            labels={
                "MONTH": "Month",
                "Delay Hours": "Delay Hours",
                "Cause": "Delay Cause",
            },
            hover_data={
                "YEAR": True,
                "MONTH": True,
                "Delay Hours": ":,.0f",
                "Minutes": False,
            },
        )

        fig.for_each_annotation(lambda a: a.update(text=a.text.replace("YEAR=", "")))

        fig.update_layout(
            template="plotly_white",
            height=620,
            legend_title_text="Delay Cause",
            margin={"r": 20, "t": 40, "l": 20, "b": 40},
        )

        fig.update_xaxes(dtick=1)
        fig.update_yaxes(title="Delay Hours")

        return fig
    @output
    @render_widget
    def delay_cause_total_chart():
        totals = delay_cause_summary[
            [
                "DELAY_DUE_CARRIER",
                "DELAY_DUE_WEATHER",
                "DELAY_DUE_NAS",
                "DELAY_DUE_SECURITY",
                "DELAY_DUE_LATE_AIRCRAFT",
            ]
        ].sum().reset_index()

        totals.columns = ["Cause", "Minutes"]

        fig = px.bar(
            totals.sort_values("Minutes", ascending=True),
            x="Minutes",
            y="Cause",
            orientation="h",
            title="Total Delay Minutes by Cause",
        )
        fig.update_layout(template="plotly_white")
        return fig

    @reactive.calc
    def smart_filtered():
        data = flights[
            (flights["YEAR"] == int(input.year_filter())) &
            (flights["ORIGIN"] == input.origin_filter()) &
            (flights["DEST"] == input.dest_filter())
        ].copy()
        return data

    @output
    @render.text
    def smart_flights():
        return f"{len(smart_filtered()):,}"

    @output
    @render.text
    def smart_delay_risk():
        data = smart_filtered()
        if len(data) == 0:
            return "No data"
        return f"{data['IS_DELAYED'].mean() * 100:.1f}%"

    @output
    @render.text
    def smart_avg_delay():
        data = smart_filtered()
        if len(data) == 0:
            return "No data"
        return f"{data['ARR_DELAY_MINUTES'].mean():.1f} min"

    @output
    @render.data_frame
    def smart_table():
        data = smart_filtered()[
            [
                "FL_DATE",
                "AIRLINE",
                "ORIGIN",
                "DEST",
                "DEP_DELAY_MINUTES",
                "ARR_DELAY_MINUTES",
                "PUNCTUALITY_STATUS",
                "DOMINANT_DELAY_CAUSE"
            ]
        ].head(1000).copy()

        data["FL_DATE"] = pd.to_datetime(data["FL_DATE"]).dt.date

        data["DEP_DELAY_MINUTES"] = data["DEP_DELAY_MINUTES"].round(2)
        data["ARR_DELAY_MINUTES"] = data["ARR_DELAY_MINUTES"].round(2)

        data = data.rename(
            columns={
                "FL_DATE": "Flight Date",
                "AIRLINE": "Airline",
                "ORIGIN": "Origin",
                "DEST": "Destination",
                "DEP_DELAY_MINUTES": "Departure Delay (min)",
                "ARR_DELAY_MINUTES": "Arrival Delay (min)",
                "PUNCTUALITY_STATUS": "Punctuality Status",
                "DOMINANT_DELAY_CAUSE": "Dominant Delay Cause",
            }
        )

        return render.DataGrid(
            data,
            filters=True
        )

app = App(app_ui, server)