import streamlit as st
import pandas as pd
import openpyxl

# Load the data
excel_file_path = 'data/Chinese Policy News_Jan 24 Sample.xlsx'
data = pd.read_excel(excel_file_path)

# Initialize the Streamlit app
st.title("Policy Overview App")

# Home Page for Selections
st.header("Home")
selected_country = st.selectbox("Select a Country", ["China", "Australia", "Singapore"])
selected_view_format = st.radio("Select View Format", ["View by Policy", "View by Date"])

# Proceed button to Overview page
if st.button('Go to Overview'):
    st.session_state['country'] = selected_country
    st.session_state['view_format'] = selected_view_format
    st.experimental_rerun()

# Check if selections are made
if 'country' in st.session_state and 'view_format' in st.session_state:
    # Overview Page
    st.header(f"Overview - {st.session_state['country']}")
    if st.session_state['view_format'] == "View by Policy":
        # (Previous implementation for "View by Policy")
        # Filtering by Policy
        selected_policy = st.selectbox("Filter by Policy", data['Policy'].unique())
        filtered_data_policy = data[data['Policy'] == selected_policy]

        # Display Filtered Policies
        for policy in filtered_data_policy['Policy'].unique():
            st.subheader(policy)
            st.write(filtered_data_policy[filtered_data_policy['Policy'] == policy]['Summary'].iloc[0])
            expand = st.expander(f"Show sources for {policy}")
            for link in filtered_data_policy[filtered_data_policy['Policy'] == policy]['Link']:
                expand.write(link)

    elif st.session_state['view_format'] == "View by Date":
        # "View by Date" Implementation
        for date in sorted(data['Date'].dropna().unique(), reverse=True):
            st.subheader(f"Date: {date}")
            for idx, row in data[data['Date'] == date].iterrows():
                if st.button(row['Title'], key=idx):
                    st.write(f"Policy: {row['Policy']}")
                    st.write(f"Link: {row['Link']}")
                    # Add more details as needed

    # (Previous implementation for Hashtag Filtering and Download Button)

# Policy Detail Page
if 'selected_policy' in st.session_state:
    st.header(f"Policy Details - {st.session_state['selected_policy']}")
    policy_data = data[data['Policy'] == st.session_state['selected_policy']]
    st.write(policy_data[['Summary', 'Policy Link']].drop_duplicates().iloc[0])
    # Add more details or functionality as needed

# Remember to replace 'path_to_your_excel_file.xlsx' with your actual Excel file path
