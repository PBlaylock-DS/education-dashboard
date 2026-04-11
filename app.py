import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("County Education & Civic Insights Dashboard")

import pandas as pd
import numpy as np

# For visualizing data
import matplotlib.pyplot as plt
import seaborn as sns

# Dashbaords
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from google.colab import drive
drive.mount('/content/drive')

# Write your code here to read the data
data = pd.read_csv('/content/drive/MyDrive/11 DSC-525/Topic 6/socioeconomic_voting.csv')

# Create barplot for Bachelor's Degree or Higher Percentage (2018-2022) and State
df = data.copy()
education_col = "Bachelor's Degree or Higher Percentage (2018-2022)"
state_col = "State"

# Aggregate to state level (mean)
state_avg = (
    df.groupby(state_col)[education_col]
    .mean()
    .reset_index()
    .sort_values(by=education_col, ascending=False)
)

# Create horizontal bar chart
fig = px.bar(
    state_avg,
    x=education_col,
    y=state_col,
    orientation="h",
    title="Average Bachelor's Degree Attainment by State",
    labels={
        education_col: "Average Bachelor's Degree or Higher (%)",
        state_col: "State"
    },
    color=education_col,
    color_continuous_scale="Reds" 
)

fig.update_layout(
    template="plotly_white",
    yaxis=dict(categoryorder="total ascending")  # Highest at top
)

st.plotly_chart(fig, use_container_width=True)

top_10 = state_avg.head(10)

fig = px.bar(
    top_10,
    x=education_col,
    y=state_col,
    orientation="h",
    title="Top 10 States by Bachelor's Degree Attainment",
    labels={
        education_col: "Average Bachelor's Degree or Higher (%)",
        state_col: "State"
    },
    color=education_col,
    color_continuous_scale="Blues"
)

fig.update_layout(template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

bottom_10 = state_avg.tail(10)

fig = px.bar(
    bottom_10,
    x=education_col,
    y=state_col,
    orientation="h",
    title="Bottom 10 States by Bachelor's Degree Attainment",
    labels={
        education_col: "Average Bachelor's Degree or Higher (%)",
        state_col: "State"
    },
    color=education_col,
    color_continuous_scale="Reds"
)

fig.update_layout(template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# Create barchart for Bachelor's Degree or Higher Percentage (2018-2022) and Bachelor's Degree or Higher Percentage (2018-2022) and Vote Percentage with Party
education_col = "Bachelor's Degree or Higher Percentage (2018-2022)"
vote_col = "Vote Percentage"
party_col = "Party"
county_col = "County Name"
state_col = "State"

# Party color mapping
party_colors = {
    "REPUBLICAN": "red",
    "DEMOCRAT": "blue"
}

fig = px.scatter(
    df,
    x=education_col,
    y=vote_col,
    color=party_col,
    color_discrete_map=party_colors,
    hover_data=[county_col, state_col],
    trendline="ols",  # <-- Adds regression line
    title="Educational Attainment vs Vote Percentage (OLS Trendline)",
    labels={
        education_col: "Bachelor's Degree or Higher (%)",
        vote_col: "Vote Percentage (%)"
    }
)

fig.update_traces(marker=dict(size=6, opacity=0.7))
fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

# Create scatterplot for Bachelor's Degree or Higher Percentage (2018-2022) and County Median Household Income (2021)
education_col = "Bachelor's Degree or Higher Percentage (2018-2022)"
income_col = "County Median Household Income (2021)"
party_col = "Party"
county_col = "County Name"
state_col = "State"

# Define party color mapping
party_colors = {
    "REPUBLICAN": "red",
    "DEMOCRAT": "blue"
}

# Create scatterplot
fig = px.scatter(
    df,
    x=education_col,
    y=income_col,
    color=party_col,
    color_discrete_map=party_colors,  # <-- Added mapping
    hover_data=[county_col, state_col],
    title="Education vs Income Across U.S. Counties",
    labels={
        education_col: "Bachelor's Degree or Higher (%)",
        income_col: "Median Household Income ($)"
    }
)

# Adjust marker styling
fig.update_traces(marker=dict(size=6, opacity=0.7))

st.plotly_chart(fig, use_container_width=True)

# Create scatterplot for Bachelor's Degree or Higher Percentage (2018-2022) and Unemployment Rate 2020
# Column references
education_col = "Bachelor's Degree or Higher Percentage (2018-2022)"
unemployment_col = "Unemployment Rate 2020"
party_col = "Party"
county_col = "County Name"
state_col = "State"

# Party color mapping
party_colors = {
    "REPUBLICAN": "red",
    "DEMOCRAT": "blue"
}

# Create scatterplot
fig = px.scatter(
    df,
    x=education_col,
    y=unemployment_col,
    color=party_col,
    color_discrete_map=party_colors,
    hover_data=[county_col, state_col],
    title="Educational Attainment vs Unemployment Rate (2020)",
    labels={
        education_col: "Bachelor's Degree or Higher (%)",
        unemployment_col: "Unemployment Rate (%)"
    }
)

# Improve readability
fig.update_traces(marker=dict(size=6, opacity=0.7))

st.plotly_chart(fig, use_container_width=True)

# Create scatterplot for Bachelor's Degree or Higher Percentage (2018-2022) and Vote Percentage
# Column references
education_col = "Bachelor's Degree or Higher Percentage (2018-2022)"
vote_col = "Vote Percentage"
party_col = "Party"
county_col = "County Name"
state_col = "State"

# Party color mapping
party_colors = {
    "REPUBLICAN": "red",
    "DEMOCRAT": "blue"
}

# Create scatterplot
fig = px.scatter(
    df,
    x=education_col,
    y=vote_col,
    color=party_col,
    color_discrete_map=party_colors,
    hover_data=[county_col, state_col],
    title="Educational Attainment vs Vote Percentage",
    labels={
        education_col: "Bachelor's Degree or Higher (%)",
        vote_col: "Vote Percentage (%)"
    }
)

# Improve readability
fig.update_traces(marker=dict(size=6, opacity=0.7))


# Create scatterplot for Bachelor's Degree or Higher Percentage (2018-2022) and Urban Influence Code 2013 
# Column references
education_col = "Bachelor's Degree or Higher Percentage (2018-2022)"
urban_col = "Urban Influence Code 2013"
party_col = "Party"
county_col = "County Name"
state_col = "State"

# Ensure Urban Influence Code is treated as categorical
df[urban_col] = df[urban_col].astype(str)

# Party color mapping
party_colors = {
    "REPUBLICAN": "red",
    "DEMOCRAT": "blue"
}

# Create scatterplot
fig = px.scatter(
    df,
    x=education_col,
    y=urban_col,
    color=party_col,
    color_discrete_map=party_colors,
    hover_data=[county_col, state_col],
    title="Educational Attainment vs Urban Influence Classification",
    labels={
        education_col: "Bachelor's Degree or Higher (%)",
        urban_col: "Urban Influence Code (2013)"
    }
)

# Improve readability
fig.update_traces(marker=dict(size=6, opacity=0.7))
fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

# Create scatterplot for Bachelor's Degree or Higher Percentage (2018-2022) and Party
# Column references
education_col = "Bachelor's Degree or Higher Percentage (2018-2022)"
party_col = "Party"
county_col = "County Name"
state_col = "State"

# Party color mapping
party_colors = {
    "REPUBLICAN": "red",
    "DEMOCRAT": "blue"
}

# Add small jitter to reduce overlap
df["Party Jitter"] = df[party_col] + np.random.uniform(-0.02, 0.02, len(df)).astype(str)

# Create scatterplot
fig = px.strip(
    df,
    x=party_col,
    y=education_col,
    color=party_col,
    color_discrete_map=party_colors,
    hover_data=[county_col, state_col],
    title="Bachelor's Degree Attainment by Party",
    labels={
        party_col: "Political Party",
        education_col: "Bachelor's Degree or Higher (%)"
    }
)

fig.update_traces(marker=dict(size=6, opacity=0.7))
fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

# Add boxplot to the above for better
fig = px.box(
    df,
    x=party_col,
    y=education_col,
    color=party_col,
    color_discrete_map=party_colors,
    points="all",
    hover_data=[county_col, state_col],
    title="Distribution of Bachelor's Degree Attainment by Party"
)

fig.update_layout(template="plotly_white")
st.plotly_chart(fig, use_container_width=True)