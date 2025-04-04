import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("market_research_results.csv")

# Clean column names (remove whitespace if any)
df.columns = [col.strip() for col in df.columns]

# Streamlit app
st.set_page_config(page_title="Outdoor Navigation Market Dashboard", layout="wide")

# Title
st.title("🧭 Outdoor Navigation Market Dashboard")
st.markdown("Professional insights on competitors in the outdoor navigation app space.")

# Sidebar filters
st.sidebar.header("Filter Options")
competitors = df["Company"].unique().tolist()
selected_competitor = st.sidebar.selectbox("Select Competitor", ["All"] + competitors)

# Filter data based on selection
if selected_competitor != "All":
    filtered_df = df[df["Company"] == selected_competitor]
else:
    filtered_df = df

# Show data table
st.subheader("Market Research Data")
st.dataframe(filtered_df, use_container_width=True)

# Add download button
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df_to_csv(filtered_df)
st.download_button(
    label="📥 Download Data as CSV",
    data=csv,
    file_name='market_research_filtered.csv',
    mime='text/csv',
)

# Visualize: Target Audience word count
st.subheader("Target Audience Focus")

# Prepare data for visualization
audience_data = filtered_df['Target Audience'].str.split(', ').explode().value_counts().reset_index()
audience_data.columns = ['Audience', 'Count']

if not audience_data.empty:
    fig = px.bar(
        audience_data,
        x='Audience',
        y='Count',
        title='Target Audience Breakdown',
        labels={'Count': 'Frequency'},
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No data to display for the selected competitor.")

# Visualize: Key product features (word cloud style list)
st.subheader("Key Product Features")
if not filtered_df.empty:
    features_list = filtered_df['Key Product Features'].dropna().tolist()
    for feature in features_list:
        st.markdown(f"- {feature}")
else:
    st.info("No features to display for the selected competitor.")
# --- Feature Comparison Table ---
st.subheader("🧩 Feature Comparison Across Competitors")

# Step 1: Explode features into individual rows
features_exploded = df.copy()
features_exploded = features_exploded.dropna(subset=['Key Product Features'])
features_exploded['Key Product Features'] = features_exploded['Key Product Features'].str.split(', ')
features_exploded = features_exploded.explode('Key Product Features')

# Step 2: Create pivot table
feature_matrix = pd.crosstab(
    features_exploded['Company'],
    features_exploded['Key Product Features']
)

# Step 3: Clean display (optional: show checkmarks)
feature_matrix = feature_matrix.applymap(lambda x: '✔️' if x > 0 else '')

# Step 4: Display in Streamlit
st.dataframe(feature_matrix, use_container_width=True)



# Footer
st.markdown("---")
st.caption("Dashboard built with ❤️ using Streamlit and Plotly.")
