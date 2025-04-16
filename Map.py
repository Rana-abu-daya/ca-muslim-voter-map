import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json

st.set_page_config(layout="wide", page_title="California Map")

# App title
st.title("Eligible Muslim Voters by County in California")

# === Load Data ===
muslim_data = pd.read_csv("MuslimVoterStatsByCountyCode.csv")               # Contains countyCode, count
county_lookup = pd.read_csv("DHCS_County_Code_Reference_Table.csv")           # Contains DHCS_County_Code, County_Name

# === Join the two datasets on county code ===
merged_df = pd.merge(
    muslim_data,
    county_lookup.rename(columns={"DHCS_County_Code": "CountyCode"}),  # Rename for merging
    on="CountyCode",
    how="left"
)

# Clean & title-case county names
merged_df["County_Name"] = merged_df["County_Name"].str.strip().str.title()
# Format numbers with commas
merged_df["Muslim_Numbers"] = merged_df["Muslim_Total"].astype(int)
merged_df["Muslim_Voted"] = merged_df["Muslim_Voted"].fillna(0).astype(int)
merged_df["Muslim_Voted_Percent"] = merged_df["Muslim_Voted_Percent"].round(2)

# Create custom hover text
merged_df["hover_text"] = (
    "<b>" + merged_df["County_Name"] + "</b><br>" +
    "Total Muslims: <span style='color:red'>" + merged_df["Muslim_Numbers"].apply(lambda x: f"{x:,}") + "</span><br>" +
    "Voted Muslims: <span style='color:red'>" + merged_df["Muslim_Voted"].apply(lambda x: f"{x:,}") + "</span><br>" +
    "Voting %: <span style='color:red'>" + merged_df["Muslim_Voted_Percent"].astype(str) + "%</span>"
)


# Create hover text
# merged_df["hover_text"] = merged_df["County_Name"] + ": " + merged_df["Muslim_Numbers"].apply(lambda x: f"{x:,}") + " people"

# === Load GeoJSON for California counties ===
with open("California_County_Boundaries.geojson", "r") as file:
    geojson_data = json.load(file)

# === Plot Choropleth ===
fig = go.Figure(go.Choroplethmapbox(
    geojson=geojson_data,
    locations=merged_df["County_Name"],  # This must match featureidkey field
    z=merged_df["Muslim_Numbers"],
    text=merged_df["hover_text"],
    featureidkey="properties.CountyName",  # This must match what's inside the GeoJSON
    hovertemplate="%{text}<extra></extra>",
    colorscale=[
        [0, "white"],
        [0.01, "yellow"],
        [0.1, "lightgreen"],
        [1, "darkgreen"]
    ],
    marker_opacity=0.8,
    marker_line_width=1.2
))

# Map layout
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=5,
    mapbox_center={"lat": 36.7783, "lon": -119.4179},  # California center
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    height=600,
    width=500,
    coloraxis_colorbar=dict(
        title="Muslim Voter Count"
    )
)

# Show in Streamlit
st.plotly_chart(fig, use_container_width=True)

######################## City ########################
# Streamlit app title
st.title("Eligible Muslim Voters by City in California")

# Load the data
data = pd.read_csv("MuslimsPerCityVoting.csv")
data["City"] = data["City"].str.strip().str.title()

data["Muslim_Numbers"] = data["Muslim_Total"].astype(int)
data["Muslim_Voted"] = data["Muslim_Voted"].fillna(0).astype(int)
data["Muslim_Voted_Percent"] = data["Muslim_Voted_Percent"].round(2)

data["hover_text"] = (
    "<b>" + data["City"] + "</b><br>" +
    "Total Muslims: <span style='color:red'>" + data["Muslim_Numbers"].apply(lambda x: f"{x:,}") + "</span><br>" +
    "Voted Muslims: <span style='color:red'>" + data["Muslim_Voted"].apply(lambda x: f"{x:,}") + "</span><br>" +
    "Voting %: <span style='color:red'>" + data["Muslim_Voted_Percent"].astype(str) + "%</span>"
)


# Hover text
# data["hover_text"] = data["City"] + ": " + data["MuslimNumbers"].apply(lambda x: f"{x:,}")

# Load GeoJSON
with open("California_Incorporated_Cities.geojson", "r") as file:
    geojson_data = json.load(file)

# Choropleth map
fig = go.Figure(go.Choroplethmapbox(
    geojson=geojson_data,
    locations=data["City"],
    z=data["Muslim_Numbers"],
    featureidkey="properties.CITY",  # Adjust if different in GeoJSON
    colorscale=[
        [0, "white"],
        [0.01, "yellow"],
        [0.05, "lightgreen"],
        [0.25, "green"],
        [1, "darkgreen"]
    ],
    marker_opacity=0.8,
    marker_line_width=1,
    text=data["hover_text"],
    hovertemplate="%{text}<extra></extra>"
))

# Layout
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=5,
    mapbox_center={"lat": 36.7783, "lon": -119.4179},  # California center
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    height=600,
    width=500,
    coloraxis_colorbar=dict(
        title="Muslim Voter Count"
    )
)

st.plotly_chart(fig, use_container_width=True)


######################## School district ############

# Title
st.title("Eligible Muslim Voters by School District in California")

# === Step 1: Load Muslim voter data and matching results ===
data = pd.read_csv("MuslimPerSchoolDistrictVoted2.csv")  # columns: school_district, count
matches = pd.read_csv("district_name_matching_results.csv")  # columns: School District, Matched DistrictName

# Merge the cleaned district names
data = data.rename(columns={"school_district": "School District"})
merged = pd.merge(data, matches, on="School District", how="left")

# Drop rows with no valid match or no name
merged = merged.dropna(subset=["Matched DistrictName"])
merged = merged[merged["Matched DistrictName"].str.strip() != ""]



# === Step 2: Load California School District GeoJSON ===
with open("California_School_District_Areas_2022-23.geojson", "r") as file:
    geojson_data = json.load(file)


# Format data types
merged["Muslim_Total"] = merged["Muslim_Total"].astype(int)
merged["Muslim_Voted"] = merged["Muslim_Voted"].fillna(0).astype(int)
merged["Muslim_Voted_Percent"] = merged["Muslim_Voted_Percent"].round(2)

# Create hover text
merged["hover_text"] = (
    "<b>" + merged["Matched DistrictName"] + "</b><br>" +
    "Total Muslims: <span style='color:red'>" + merged["Muslim_Total"].apply(lambda x: f"{x:,}") + "</span><br>" +
    "Voted Muslims: <span style='color:red'>" + merged["Muslim_Voted"].apply(lambda x: f"{x:,}") + "</span><br>" +
    "Voting %: <span style='color:red'>" + merged["Muslim_Voted_Percent"].astype(str) + "%</span>"
)


# === Step 3: Create hover text ===
# merged["hover_text"] = merged["Matched DistrictName"] + ": " + merged["count"].apply(lambda x: f"{x:,}") + " people"

# === Step 4: Choropleth Map ===
fig = go.Figure(go.Choroplethmapbox(
    geojson=geojson_data,
    locations=merged["Matched DistrictName"],
    z=merged["Muslim_Total"],
    text=merged["hover_text"],
    featureidkey="properties.DistrictName",
    hovertemplate="%{text}<extra></extra>",
    colorscale=[
        [0, "white"],
        [0.05, "yellow"],
        [0.25, "lightgreen"],
        [0.5, "green"],
        [1, "darkgreen"]
    ],
    marker_opacity=0.8,
    marker_line_width=1.2
))


# === Step 5: Add District Labels at Centroids ===
district_centroids = []
for feature in geojson_data["features"]:
    district_name = feature["properties"]["DistrictName"]
    coordinates = feature["geometry"]["coordinates"]

    if feature["geometry"]["type"] == "MultiPolygon":
        coordinates = coordinates[0]

    lon = sum(pt[0] for pt in coordinates[0]) / len(coordinates[0])
    lat = sum(pt[1] for pt in coordinates[0]) / len(coordinates[0])

    district_centroids.append({"district": district_name, "lon": lon, "lat": lat})

centroid_df = pd.DataFrame(district_centroids)

# Add text labels
for _, row in centroid_df.iterrows():
    match = merged[merged["Matched DistrictName"] == row["district"]]
    if not match.empty:
        muslim_count = match["Muslim_Total"].values[0]
        fig.add_trace(go.Scattermapbox(
            lon=[row["lon"]],
            lat=[row["lat"]],
            mode="text",
            text=[match["hover_text"].values[0]],  # FIXED HERE
            hovertemplate="%{text}<extra></extra>",
            showlegend=False
        ))


# === Step 6: Layout ===
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=5,
    mapbox_center={"lat": 36.7783, "lon": -119.4179},  # California center
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    height=600,
    width=500,
    coloraxis_colorbar=dict(title="Muslim Population")
)

# === Step 7: Show the Map ===
st.plotly_chart(fig, use_container_width=True)


