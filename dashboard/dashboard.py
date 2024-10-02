import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
day_df = pd.read_csv("../data/day.csv")
hour_df = pd.read_csv("../data/hour.csv")

# Set the title of the Streamlit app
st.title("Bike Sharing Data Analysis")

# Sidebar for navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Select a page:", ["Overview", "Weather and Seasonal Analysis", "Day and Holiday Analysis", "RFM Analysis"])

# Overview page
if options == "Overview":
    st.header("Dataset Overview")
    st.write("This dashboard provides insights into the bike sharing dataset.")
    st.subheader("Day Dataset")
    st.write(day_df.head())
    st.subheader("Hour Dataset")
    st.write(hour_df.head())

# Weather and Seasonal Analysis page
elif options == "Weather and Seasonal Analysis":
    st.header("Analysis of Weather and Seasonal Effects on Bike Rentals")
    
    st.subheader("Weather Effect on Rentals")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x='weathersit', y='cnt', data=day_df, ax=ax)
    ax.set_title('Box Plot of Bike Rentals by Weather')
    ax.set_xlabel('Weather Condition (1: Clear, 2: Mist, 3: Light Rain, 4: Heavy Rain)')
    ax.set_ylabel('Number of Rentals')
    st.pyplot(fig)

    st.subheader("Seasonal Effect on Rentals")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='season', y='cnt', data=day_df, estimator=sum, ax=ax)
    ax.set_title('Total Bike Rentals by Season')
    ax.set_xlabel('Season (1: Spring, 2: Summer, 3: Fall, 4: Winter)')
    ax.set_ylabel('Number of Rentals')
    st.pyplot(fig)

# Day and Holiday Analysis page
elif options == "Day and Holiday Analysis":
    st.header("Analysis of Rentals by Day and Holiday")
    
    st.subheader("Rentals on Working Days vs Holidays")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='workingday', y='cnt', data=day_df, estimator=sum, ax=ax)
    ax.set_title('Total Bike Rentals by Working Day and Holiday')
    ax.set_xlabel('Working Day (1: Yes, 0: No)')
    ax.set_ylabel('Number of Rentals')
    st.pyplot(fig)

    st.subheader("Hourly Rentals by Working Day")
    fig, ax = plt.subplots(figsize=(12, 6))
    hour_df.groupby(['hr', 'workingday'])['cnt'].sum().unstack().plot(kind='line', ax=ax)
    ax.set_title('Hourly Bike Rentals by Working Day and Holiday')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Number of Rentals')
    ax.legend(['Holiday', 'Working Day'])
    ax.grid()
    st.pyplot(fig)

# RFM Analysis page
elif options == "RFM Analysis":
    st.header("RFM Analysis")
    
    # Perform RFM Analysis
    data = hour_df
    data['dteday'] = pd.to_datetime(data['dteday'])
    reference_date = data['dteday'].max() + pd.DateOffset(days=1)
    rfm_df = data.groupby('casual').agg({
        'dteday': lambda x: (reference_date - x.max()).days,
        'cnt': 'sum',
    }).reset_index()

    rfm_df.columns = ['user_id', 'recency', 'frequency']
    rfm_df['monetary'] = rfm_df['frequency'] * 1
    rfm_df['recency_segment'] = pd.qcut(rfm_df['recency'], 4, labels=['4', '3', '2', '1'])
    rfm_df['frequency_segment'] = pd.qcut(rfm_df['frequency'], 4, labels=['1', '2', '3', '4'])
    rfm_df['monetary_segment'] = pd.qcut(rfm_df['monetary'], 4, labels=['1', '2', '3', '4'])
    rfm_df['RFM_Score'] = rfm_df['recency_segment'].astype(str) + rfm_df['frequency_segment'].astype(str) + rfm_df['monetary_segment'].astype(str)

    st.subheader("RFM Table")
    st.write(rfm_df.head())

    st .subheader("Distribution of Recency")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(rfm_df['recency'], bins=30, kde=True, color='blue', ax=ax)
    ax.set_title('Distribution of Recency')
    ax.set_xlabel('Recency (Days since last rental)')
    ax.set_ylabel('Frequency')
    ax.axvline(rfm_df['recency'].mean(), color='red', linestyle='dashed', linewidth=2, label='Mean Recency')
    ax.legend()
    st.pyplot(fig)

    st.subheader("Distribution of Frequency")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(rfm_df['frequency'], bins=30, kde=True, color='green', ax=ax)
    ax.set_title('Distribution of Frequency')
    ax.set_xlabel('Frequency of Rentals')
    ax.set_ylabel('Frequency')
    ax.axvline(rfm_df['frequency'].mean(), color='red', linestyle='dashed', linewidth=2, label='Mean Frequency')
    ax.legend()
    st.pyplot(fig)

    st.subheader("Distribution of Monetary Value")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(rfm_df['monetary'], bins=30, kde=True, color='purple', ax=ax)
    ax.set_title('Distribution of Monetary Value')
    ax.set_xlabel('Monetary Value')
    ax.set_ylabel('Frequency')
    ax.axvline(rfm_df['monetary'].mean(), color='red', linestyle='dashed', linewidth=2, label='Mean Monetary Value')
    ax.legend()
    st.pyplot(fig)

    st.subheader("Count of Customers by RFM Score")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=rfm_df, x='RFM_Score', ax=ax)
    ax.set_title('Count of Customers by RFM Score')
    ax.set_xlabel('RFM Score')
    ax.set_ylabel('Count of Customers')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)
