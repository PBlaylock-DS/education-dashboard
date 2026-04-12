import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")
st.title("County Education & Civic Insights Dashboard")
st.markdown(
    "Explore how educational attainment relates to income, unemployment, urban influence, and voting patterns across U.S. counties."
)

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("socioeconomic_voting.csv")

    numeric_cols = [
        "Bachelor's Degree or Higher Percentage (2018-2022)",
        "County Median Household Income (2021)",
        "Unemployment Rate 2020",
        "Vote Percentage",
        "Urban Influence Code 2013"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["Party"] = df["Party"].astype(str).str.upper().str.strip()
    return df

df = load_data()

# -----------------------------
# Column names
# -----------------------------
education_col = "Bachelor's Degree or Higher Percentage (2018-2022)"
income_col = "County Median Household Income (2021)"
unemployment_col = "Unemployment Rate 2020"
vote_col = "Vote Percentage"
party_col = "Party"
county_col = "County Name"
state_col = "State"
urban_col = "Urban Influence Code 2013"

party_colors = {
    "REPUBLICAN": "red",
    "DEMOCRAT": "blue"
}

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Filter Dashboard")

state_options = sorted(df[state_col].dropna().unique())
selected_states = st.sidebar.multiselect(
    "Select State(s)",
    options=state_options,
    default=state_options
)

party_options = sorted(df[party_col].dropna().unique())
selected_parties = st.sidebar.multiselect(
    "Select Party",
    options=party_options,
    default=party_options
)

edu_min = float(df[education_col].min())
edu_max = float(df[education_col].max())

selected_edu_range = st.sidebar.slider(
    "Bachelor's Degree or Higher (%)",
    min_value=float(np.floor(edu_min)),
    max_value=float(np.ceil(edu_max)),
    value=(float(np.floor(edu_min)), float(np.ceil(edu_max)))
)

top_n = st.sidebar.slider(
    "Number of states to show in Top/Bottom charts",
    min_value=5,
    max_value=20,
    value=10
)

# -----------------------------
# Apply filters
# -----------------------------
filtered_df = df[
    (df[state_col].isin(selected_states)) &
    (df[party_col].isin(selected_parties)) &
    (df[education_col].between(selected_edu_range[0], selected_edu_range[1]))
].copy()

st.subheader("Filtered Dataset Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Counties", f"{len(filtered_df):,}")
col2.metric("Avg Bachelor's %", f"{filtered_df[education_col].mean():.1f}")
col3.metric("Avg Income", f"${filtered_df[income_col].mean():,.0f}")

# -----------------------------
# State-level bar charts
# -----------------------------
st.subheader("State-Level Educational Attainment")

state_avg = (
    filtered_df.groupby(state_col)[education_col]
    .mean()
    .reset_index()
    .sort_values(by=education_col, ascending=False)
)

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
fig.update_layout(template="plotly_white", yaxis=dict(categoryorder="total ascending"))
st.plotly_chart(fig, use_container_width=True)

col_a, col_b = st.columns(2)

with col_a:
    top_states = state_avg.head(top_n)
    fig_top = px.bar(
        top_states,
        x=education_col,
        y=state_col,
        orientation="h",
        title=f"Top {top_n} States by Bachelor's Degree Attainment",
        labels={
            education_col: "Average Bachelor's Degree or Higher (%)",
            state_col: "State"
        },
        color=education_col,
        color_continuous_scale="Blues"
    )
    fig_top.update_layout(template="plotly_white", yaxis=dict(categoryorder="total ascending"))
    st.plotly_chart(fig_top, use_container_width=True)

with col_b:
    bottom_states = state_avg.tail(top_n)
    fig_bottom = px.bar(
        bottom_states,
        x=education_col,
        y=state_col,
        orientation="h",
        title=f"Bottom {top_n} States by Bachelor's Degree Attainment",
        labels={
            education_col: "Average Bachelor's Degree or Higher (%)",
            state_col: "State"
        },
        color=education_col,
        color_continuous_scale="Reds"
    )
    fig_bottom.update_layout(template="plotly_white", yaxis=dict(categoryorder="total ascending"))
    st.plotly_chart(fig_bottom, use_container_width=True)

# -----------------------------
# Scatterplots
# -----------------------------
st.subheader("County-Level Relationships")

fig_vote = px.scatter(
    filtered_df,
    x=education_col,
    y=vote_col,
    color=party_col,
    color_discrete_map=party_colors,
    hover_data=[county_col, state_col],
    trendline="ols",
    title="Educational Attainment vs Vote Percentage",
    labels={
        education_col: "Bachelor's Degree or Higher (%)",
        vote_col: "Vote Percentage (%)"
    }
)
fig_vote.update_traces(marker=dict(size=6, opacity=0.7))
fig_vote.update_layout(template="plotly_white")
st.plotly_chart(fig_vote, use_container_width=True)

col_c, col_d = st.columns(2)

with col_c:
    fig_income = px.scatter(
        filtered_df,
        x=education_col,
        y=income_col,
        color=party_col,
        color_discrete_map=party_colors,
        hover_data=[county_col, state_col],
        title="Education vs Income Across U.S. Counties",
        labels={
            education_col: "Bachelor's Degree or Higher (%)",
            income_col: "Median Household Income ($)"
        }
    )
    fig_income.update_traces(marker=dict(size=6, opacity=0.7))
    fig_income.update_layout(template="plotly_white")
    st.plotly_chart(fig_income, use_container_width=True)

with col_d:
    fig_unemp = px.scatter(
        filtered_df,
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
    fig_unemp.update_traces(marker=dict(size=6, opacity=0.7))
    fig_unemp.update_layout(template="plotly_white")
    st.plotly_chart(fig_unemp, use_container_width=True)

# -----------------------------
# Urban Influence scatter
# -----------------------------
st.subheader("Educational Attainment and Urban Influence")

filtered_df[urban_col] = filtered_df[urban_col].astype("Int64").astype(str)

fig_urban = px.scatter(
    filtered_df,
    x=education_col,
    y=urban_col,
    color=party_col,
    color_discrete_map=party_colors,
    hover_data=[county_col, state_col],
    title="Educational Attainment vs Urban Influence Code (2013)",
    labels={
        education_col: "Bachelor's Degree or Higher (%)",
        urban_col: "Urban Influence Code (2013)"
    }
)
fig_urban.update_traces(marker=dict(size=6, opacity=0.7))
fig_urban.update_layout(template="plotly_white")
st.plotly_chart(fig_urban, use_container_width=True)

# -----------------------------
# Party comparison plots
# -----------------------------
st.subheader("Educational Attainment by Party")

fig_strip = px.strip(
    filtered_df,
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
fig_strip.update_traces(marker=dict(size=6, opacity=0.7))
fig_strip.update_layout(template="plotly_white")
st.plotly_chart(fig_strip, use_container_width=True)

fig_box = px.box(
    filtered_df,
    x=party_col,
    y=education_col,
    color=party_col,
    color_discrete_map=party_colors,
    points="all",
    hover_data=[county_col, state_col],
    title="Distribution of Bachelor's Degree Attainment by Party"
)
fig_box.update_layout(template="plotly_white")
st.plotly_chart(fig_box, use_container_width=True)

# -----------------------------
# Underlying data
# -----------------------------
with st.expander("View Filtered Data"):
    st.dataframe(filtered_df, use_container_width=True)