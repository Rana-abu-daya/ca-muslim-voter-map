import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import geopandas as gpd
import re
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

population_min = merged_df["Muslim_Numbers"].min()
population_max = merged_df["Muslim_Numbers"].max()
# Create hover text
# merged_df["hover_text"] = merged_df["County_Name"] + ": " + merged_df["Muslim_Numbers"].apply(lambda x: f"{x:,}") + " people"
population_min = max(1, population_min)  # Ensures that the smallest value is at least 1

# === Load GeoJSON for California counties ===
with open("California_County_Boundaries.geojson", "r") as file:
    geojson_data = json.load(file)

# === Plot Choropleth ===
fig = go.Figure(go.Choroplethmapbox(
    geojson=geojson_data,
    locations=merged_df["County_Name"],  # Match with featureidkey
    z=merged_df["Muslim_Numbers"],  # Use Muslim population as color scale
    text=merged_df["hover_text"],
    featureidkey="properties.CountyName",  # Match with GeoJSON property
    hovertemplate="%{text}<extra></extra>",
    colorscale=[
        [0, "white"],
        [0.2, "yellow"],
        [0.4, "lightgreen"],
        [0.7, "green"],
        [1, "darkgreen"]
    ],
    zmin=population_min,  # Set min value for color scale
    zmax=population_max,  # Set max value for color scale
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

z_values = merged["Muslim_Voted_Percent"]

# Voting % dynamic range
voting_min = z_values.min()
voting_max = z_values.max()
# === Step 3: Create hover text ===
# merged["hover_text"] = merged["Matched DistrictName"] + ": " + merged["count"].apply(lambda x: f"{x:,}") + " people"

# === Step 4: Choropleth Map ===
fig = go.Figure(go.Choroplethmapbox(
    geojson=geojson_data,
    locations=merged["Matched DistrictName"],
    z=z_values,
    zmin=voting_min,
    zmax=voting_max,
    text=merged["hover_text"],
    featureidkey="properties.DistrictName",
    hovertemplate="%{text}<extra></extra>",
    colorscale=[
        [0.0, "white"],
        [0.2, "yellow"],
        [0.4, "lightgreen"],
        [0.7, "green"],
        [1.0, "darkgreen"]
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
            text=[match["Matched DistrictName"].values[0]],  # ✅ PLAIN text here
            textfont=dict(size=9, color="black"),
            hoverinfo="text",
            hovertext=[match["hover_text"].values[0]],  # ✅ fancy HTML hover
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
################### CD ##################
st.title("Eligible Muslim Voters by Congressional District in California")

# === Load Data ===
data = pd.read_csv("MuslimsPerCongressionalDistrictVoting.csv")
def extract_district_number(text):
    match = re.search(r'(\d+)', str(text))
    if match:
        return int(match.group(1))
    return None

data["District_Number"] = data["Congressional District"].apply(extract_district_number)

# Step 2: Force proper formatting
data["District_Number"] = data["District_Number"].apply(lambda x: f"{int(x):02d}" if pd.notna(x) else None)

# === Load GeoJSON ===
with open("Congressional_Districts_CA.geojson", "r") as file:
    geojson_data = json.load(file)

# === Format the hover text ===
data["Muslim_Total"] = data["Muslim_Total"].astype(int)
data["Muslim_Voted"] = data["Muslim_Voted"].fillna(0).astype(int)
data["Muslim_Voted_Percent"] = data["Muslim_Voted_Percent"].round(2)

data["hover_text"] = (
    "<b>Congressional District " + data["District_Number"].astype(str) + "</b><br>" +
    "Total Muslims: <span style='color:red'>" + data["Muslim_Total"].apply(lambda x: f"{x:,}") + "</span><br>" +
    "Voted Muslims: <span style='color:red'>" + data["Muslim_Voted"].apply(lambda x: f"{x:,}") + "</span><br>" +
    "Voting %: <span style='color:red'>" + data["Muslim_Voted_Percent"].astype(str) + "%</span>"
)

# Choose to color by % instead of total number
z_values = data["Muslim_Voted_Percent"]

# Voting % dynamic range
voting_min = z_values.min()
voting_max = z_values.max()

# Choropleth
fig = go.Figure(go.Choroplethmapbox(
    geojson=geojson_data,
    locations='Congressional District '+data["District_Number"],
    z=z_values,
    zmin=voting_min,
    zmax=voting_max,
    featureidkey="properties.CongDistri",
    text=data["hover_text"],
    hovertemplate="%{text}<extra></extra>",
    colorscale=[
        [0.0, "white"],
        [0.2, "yellow"],
        [0.4, "lightgreen"],
        [0.7, "green"],
        [1.0, "darkgreen"]
    ],
    marker_opacity=0.8,
    marker_line_width=1.2
))


# Layout
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=5,
    mapbox_center={"lat": 36.7783, "lon": -119.4179},
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    height=600,
    width=500,
    coloraxis_colorbar=dict(
        title="Muslim Voter Count"
    )
)

st.plotly_chart(fig, use_container_width=True)

################## LD ##################

# Title
st.title("Eligible Muslim Voters by Legislative District in California")
st.subheader("State Assembly District")


# --- Load Data ---
data = pd.read_csv("MuslimsPerStateAssemblyDistrictVoting.csv")
data["State Assembly District"] = data["State Assembly District"].astype(str).str.strip()

# Extract District Numbers
def extract_district_numberAssembly(text):
    match = re.search(r'(\d+)', str(text))
    if match:
        return int(match.group(1))
    return None

data["District_Number"] = data["State Assembly District"].apply(extract_district_numberAssembly)
data["District_Number"] = data["District_Number"].apply(lambda x: f"{int(x):02d}" if pd.notna(x) else None)
data = data.dropna(subset=["District_Number"])

# Build Assembly District Name (e.g., "Assembly District 18")
data["AssemblyDistrictName"] = "Assembly District " + data["District_Number"]


with open("CA_AssemblyDistricts_WGS84.geojson") as f:
    geojson_data = json.load(f)

# --- Load GeoJSON ---
# with open("Legislative-AssemblyDistrict.geojson", "r") as f:
#     geojson_data = json.load(f)

# --- Hover text and z values ---
data["Muslim_Total"] = data["Muslim_Total"].astype(int)
data["Muslim_Voted"] = data["Muslim_Voted"].fillna(0).astype(int)
data["Muslim_Voted_Percent"] = data["Muslim_Voted_Percent"].round(2)

data["hover_text"] = (
    "<b>Assembly District " + data["District_Number"] + "</b><br>" +
    "Total Muslims: <span style='color:red'>" + data["Muslim_Total"].apply(lambda x: f"{x:,}") + "</span><br>" +
    "Voted Muslims: <span style='color:red'>" + data["Muslim_Voted"].apply(lambda x: f"{x:,}") + "</span><br>" +
    "Voting %: <span style='color:red'>" + data["Muslim_Voted_Percent"].astype(str) + "%</span>"
)

# --- Choropleth Map ---
voting_min = data["Muslim_Voted_Percent"].min()
voting_max = data["Muslim_Voted_Percent"].max()
# 1. Extract valid Assembly District names from GeoJSON
valid_district_names = {
    feature["properties"]["AssemblyDistrictName"]
    for feature in geojson_data["features"]
}

# 3. Filter only rows where AssemblyDistrictName matches GeoJSON
# Only keep rows where AssemblyDistrictName exists in the GeoJSON
valid_names = {f["properties"]["AssemblyDistrictName"] for f in geojson_data["features"]}
data = data[data["AssemblyDistrictName"].isin(valid_names)]

fig = go.Figure(go.Choroplethmapbox(
    geojson=geojson_data,
    locations=data["AssemblyDistrictName"],
    z=data["Muslim_Voted_Percent"],
    featureidkey="properties.AssemblyDistrictName",  # check your geojson key
    text=data["hover_text"],
    hovertemplate="%{text}<extra></extra>",
    colorscale=[
        [0.0, "white"],
        [0.3, "yellow"],
        [0.5, "lightgreen"],
        [0.7, "green"],
        [1.0, "darkgreen"]
    ],
    zmin=voting_min,
    zmax=voting_max,
    marker_opacity=0.8,
    marker_line_width=1.2
))

fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=5,
    mapbox_center={"lat": 36.7783, "lon": -119.4179},
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    height=600,
    width=700,
    coloraxis_colorbar=dict(
        title="Muslim Voting %"
    )
)

st.plotly_chart(fig, use_container_width=True)

################### Senta
st.subheader("State Senate District")
data = pd.read_csv("MuslimsPerStateSenateDistrictVoting.csv")

# Extract and clean District Numbers
def extract_district_numberSenta(text):
    match = re.search(r'(\d+)', str(text))
    if match:
        return int(match.group(1))
    return None

data["District_Number"] = data["State Senate District"].apply(extract_district_numberSenta)
data = data.dropna(subset=["District_Number"])

import json

with open("CA_SenateDistricts_WGS84.geojson") as f:
    geojson_data = json.load(f)

# === Prepare Hover Text ===
data["Muslim_Total"] = data["Muslim_Total"].astype(int)
data["Muslim_Voted"] = data["Muslim_Voted"].fillna(0).astype(int)
data["Muslim_Voted_Percent"] = data["Muslim_Voted_Percent"].round(2)
data["District_Number"] = data["District_Number"].astype(int).astype(str)
data["hover_text"] = (
    "<b>State Senate District " + data["District_Number"] + "</b><br>" +
    "Total Muslims: <span style='color:red'>" + data["Muslim_Total"].apply(lambda x: f"{x:,}") + "</span><br>" +
    "Voted Muslims: <span style='color:red'>" + data["Muslim_Voted"].apply(lambda x: f"{x:,}") + "</span><br>" +
    "Voting %: <span style='color:red'>" + data["Muslim_Voted_Percent"].astype(str) + "%</span>"
)

z_values = data["Muslim_Voted_Percent"]
voting_min = data["Muslim_Voted_Percent"].min()
voting_max = data["Muslim_Voted_Percent"].max()

# === Build Choropleth Map ===
# Check GeoJSON keys

# Keep only districts that exist in the GeoJSON
geojson_districts = {str(f["properties"]["district"]).strip() for f in geojson_data["features"]}
data = data[data["District_Number"].isin(geojson_districts)].copy()
print(data['District_Number'])
fig = go.Figure(go.Choroplethmapbox(
    geojson=geojson_data,
    locations=data["District_Number"],
    z=data["Muslim_Voted_Percent"],
    zmin=voting_min,
    zmax=voting_max,
    featureidkey="properties.district",
    text=data["hover_text"],
    hovertemplate="%{text}<extra></extra>",
    colorscale=[
        [0.0, "white"],
        [0.5, "yellow"],
        [0.7, "lightgreen"],
        [0.8, "green"],
        [1.0, "darkgreen"]
    ],
    marker_opacity=0.8,
    marker_line_width=1.2,
))


# Layout
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=5,
    mapbox_center={"lat": 36.7783, "lon": -119.4179},
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    height=600,
    width=600,
    coloraxis=dict(
        colorbar=dict(title="Muslim Voting %"),
        cmin=0,
        cmax=100
    )
)

st.plotly_chart(fig, use_container_width=True)
