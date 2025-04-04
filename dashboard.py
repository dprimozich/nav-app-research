import pandas as pd
import streamlit as st

# Title
st.title("🏞️ Outdoor Navigation Apps - Market Research Dashboard")

# Read the CSV data
csv_file = 'market_research_results.csv'
data = pd.read_csv(csv_file)

# Sidebar filters
st.sidebar.header("Filter Options")
companies = st.sidebar.multiselect(
    "Select Companies",
    options=data["Company"].unique(),
    default=data["Company"].unique()
)

# Filter data
filtered_data = data[data["Company"].isin(companies)]

# Show DataFrame
st.subheader("Market Research Summary")
st.dataframe(filtered_data, use_container_width=True)

# Show individual sections
st.subheader("Detailed Insights")

for index, row in filtered_data.iterrows():
    st.markdown(f"### {row['Company']}")
    st.markdown(f"**URL:** [Visit Website]({row['URL']})")
    st.markdown(f"**Target Audience:** {row['Target Audience']}")
    st.markdown(f"**Key Product Features:** {row['Key Product Features']}")
    st.markdown(f"**Unique Selling Points:** {row['Unique Selling Points']}")
    st.markdown(f"**Brand Tone/Personality:** {row['Brand Tone/Personality']}")
    st.markdown("---")
