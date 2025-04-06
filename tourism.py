
# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Lebanon Tourism Dashboard", layout="centered")

# --- LOAD DATA ---
file_path = 'Tourism.csv'
tourism = pd.read_csv(file_path)
tourism.columns = tourism.columns.str.strip()

# --- TITLE & BANNER ---
st.image("pic.jpeg", use_container_width=True)

st.markdown("<h1 style='text-align: center;'>Lebanon Tourism Dashboard</h1>", unsafe_allow_html=True)

st.markdown(
    "This dashboard provides an overview of tourism in Lebanon by examining the presence of key facilities such as hotels, restaurants, cafes, and guest houses across various towns. "
    "It also explores patterns and relationships between these facilities to better understand how tourism infrastructure is distributed and connected throughout the country."
)

st.markdown("> *“From the mountains to the sea, Lebanon invites the world to discover its beauty.”*")
st.markdown("<br>", unsafe_allow_html=True)


# --- BAR CHART SECTION ---
st.markdown("### Top Towns by Number of Hotels")
st.markdown("This bar chart highlights the towns with the greatest hotel presence.")

num_towns = st.slider("Select number of top towns to display", min_value=5, max_value=30, value=15)

top_towns = tourism.sort_values(by='Total number of hotels', ascending=False).head(num_towns)
fig_bar = px.bar(
    top_towns,
    x='Total number of hotels',
    y='Town',
    orientation='h',
    color_discrete_sequence=['#1f77b4']
)
fig_bar.update_layout(
    yaxis={'categoryorder': 'total ascending', 'title': None, 'showgrid': False},
    xaxis={'title': 'Number of Hotels', 'showgrid': False},
    showlegend=False
)
st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# --- PIE CHART SECTION ---
st.markdown("### Distribution of Facilities Across Towns")
st.markdown(
    "This pie chart shows the distribution of facilities in towns of Lebanon that have each selected type of tourism facility"
)

facility_options = {
    'Restaurants': 'Existence of restaurants - does not exist',
    'Hotels': 'Existence of hotels - does not exist',
    'Cafes': 'Existence of cafes - does not exist',
    'Guest Houses': 'Existence of guest houses - does not exist'
}

selected_facilities = st.multiselect(
    "Select facilities to include in the pie chart:",
    options=list(facility_options.keys()),
    default=list(facility_options.keys())
)

if selected_facilities:
    distribution = pd.Series({
        name: (tourism[col] == 0).sum()
        for name, col in facility_options.items() if name in selected_facilities
    })

    fig_pie = px.pie(
        names=distribution.index,
        values=distribution.values,
        hole=0.3,
        color_discrete_sequence=px.colors.sequential.Blues_r  
    )
    st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.info("Please select at least one facility to display the pie chart.")

st.markdown("<br><br>", unsafe_allow_html=True)


# --- SCATTER PLOT SECTION ---
st.markdown("### Tourism Facility Correlation")
st.markdown("""
Use the dropdown menus below to explore relationships between different tourism facility types.  
The bubble size represents a third variable, adding another layer of insight.
""")

available_metrics = {
    "Total number of hotels": "Hotels",
    "Total number of cafes": "Cafes",
    "Total number of restaurants": "Restaurants",
    "Total number of guest houses": "Guest Houses"
}
metric_keys = list(available_metrics.keys())

x_axis = st.selectbox("X-axis Metric", metric_keys, index=0)
y_axis = st.selectbox("Y-axis Metric", metric_keys, index=1)
bubble = st.selectbox("Bubble Size Metric", metric_keys, index=2)

fig_scatter = px.scatter(
    tourism,
    x=x_axis,
    y=y_axis,
    size=bubble,
    color_discrete_sequence=['#1f77b4'],
    hover_name="Town" if "Town" in tourism.columns else None
)
fig_scatter.update_traces(marker=dict(opacity=0.7, line=dict(width=0.5, color='DarkSlateGrey')))
fig_scatter.update_layout()
st.plotly_chart(fig_scatter, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("**Course: MSBA 601 – Data Visualization and Communication**")
st.markdown("*Instructor: Dr. Fouad Zablith*")
st.caption("Created by Noor Hamad | April 2025")
