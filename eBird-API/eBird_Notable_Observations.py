# import dependencies
import os
import requests
import json
import pandas as pd
import plotly.express as px
from config import api_key
from config import mapbox_token

px.set_mapbox_access_token(mapbox_token)

# Obtain list of Texas cities and codes
regionType = "subnational2"
parentRegionCode = "US-TX"

url = (
    "https://api.ebird.org/v2/ref/region/list/"
    + regionType
    + "/"
    + parentRegionCode
    + ".json"
)

r = requests.get(url, params={"key": api_key})

df = pd.DataFrame(r.json())

# save cities to a list to be able to iterate over later
cities = df["code"].to_list()

regionCode = "US-TX"
url_notables = (
    "https://api.ebird.org/v2/data/obs/"
    + regionCode
    + "/recent/notable?back=30"  # max number of days back for observations = 30, default = 14
)

r_notables = requests.get(url_notables, params={"key": api_key})

df_notables = pd.DataFrame(r_notables.json())

# Get data for specific hotspot(s)
url_notables_hotspots = (
    "https://api.ebird.org/v2/data/obs/"
    + regionCode
    + "/recent/notable"  # max number of days back for observations = 30
)

r_notables_hotspots = requests.get(
    url_notables_hotspots, params={"key": api_key, "back": 30, "hotspot": "True"}
)

df_notables_hotspots = pd.DataFrame(r_notables_hotspots.json())

# Map observations with Plotly
fig_hotspots = px.scatter_mapbox(
    df_notables_hotspots,
    lat="lat",
    lon="lng",
    color="comName",
    hover_data=["howMany", "obsDt", "subId"],
    title="Notable Observations at Hotspots",
)
fig_hotspots.show()

# Another map (specific species, just to see what results would look like)
red_necked_phalarope = df_notables.loc[df_notables["comName"] == "Red-necked Phalarope"]
fig_red_necked_phalarope = px.scatter_mapbox(
    red_necked_phalarope,
    lat="lat",
    lon="lng",
    color="comName",
    hover_data=["howMany", "obsDt"],
)
fig_red_necked_phalarope.show()

name_count = df_notables["comName"].value_counts()

names = df_notables["comName"].unique()

# Bar chart of counts of all species observed over specified timeframe
px.bar(
    x=names,
    y=name_count,
    title="Count of sightings by bird name",  # add Title and Labels
    labels={"y": "Bird Count"},
)  # next, try a bar chart of top 10 or 50. do the same for least observed?

# A look at notable observations across the US
regionCodeUS = "US"
url_notables_US = (
    "https://api.ebird.org/v2/data/obs/"
    + regionCodeUS
    + "/recent/notable?back=7"  # max number of days back for observations = 30
)

r_notables_US = requests.get(url_notables_US, params={"key": api_key})

df_notables_US = pd.DataFrame(r_notables_US.json())

# US map
fig_US = px.scatter_mapbox(
    df_notables_US,
    lat="lat",
    lon="lng",
    color="comName",
    hover_data=["howMany", "obsDt", "subId"],
    title="Notable Observations in the US - past 7 days",
)
fig_US.show()

names_US = df_notables_US["comName"].unique()
name_count_US = df_notables_US["comName"].value_counts()

# US bar chart
px.bar(
    x=names_US,
    y=name_count_US,
    title="Count of sightings by bird name",  # add Title and Labels
    labels={"y": "Bird Count"},
)  

# Focus on specific area(s), time period?
# What other stats to consider besides counts of observations?
# Look for certain interesting species?
# 