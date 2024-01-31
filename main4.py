import streamlit as st
import pandas as pd
import numpy as np
#from streamlit_tags import  st_tags_sidebar, st_tags



excel_file_path = 'data/Chinese Policy News_Jan 24 Sample.xlsx'
data = pd.read_excel(excel_file_path)
print(f"HEREEE UNIQUE URLS {len(data['Policy Link'].unique())}")
print(f"HEREEE UNIQUE URLS {len(data['Link'].unique())}")
data["Topic"].fillna("No Category", inplace=True)
data["Summary"].fillna("No Available Summary", inplace=True)
data["Policy (English)"].fillna("No Available English Policy Name", inplace=True)
data['Date'] = pd.to_datetime(data['Date']).dt.date
data = data.sort_values(by='Date', ascending=False)
print("UNIQQUEEE " + str(len(data["Policy"].unique())))
print(data.shape)
print(f"DATE {data['Date'].isna().sum()}")


def filter_categories(df, chosen_categories):
    # Join the categories into a regex pattern
    regex_pattern = chosen_categories

    # Create a boolean mask
    mask = df['Topic'].str.contains(regex_pattern, na=False)

    # Filter the DataFrame
    return df[mask]
def empty_page():
    st.title("No Available Data")

    if st.button("Back to Homepage"):
        if "selected_policy" in st.session_state:
            del st.session_state.selected_policy
        if "country" in st.session_state:
            del st.session_state.country
        if "format_view" in st.session_state:
            del st.session_state.format_view
        st.experimental_rerun()
def main_page():
    st.title("APAC ESG Policy Monitor")
    country = st.selectbox("Choose a country", ["China", "Singapore", "Australia"])
    format_view = st.radio("Choose your viewing format", ["View by Policy", "View by Date"])

    if st.button("Submit"):
        st.session_state.country = country
        st.session_state.format_view = format_view
        st.experimental_rerun()

def view_by_date_x(data):
    for date in data['Date'].unique():
        if date is pd.NaT:
            day_data = data[data["Date"].isna()]
            st.subheader(f"No Available Date")
        else:
            st.subheader(f"Date: {date}")
            day_data = data[data['Date'] == date]

        for link in day_data["Link"].unique():
            for _ , row in day_data[day_data["Link"] == link].iterrows():
                if st.button(f"{row['Policy Link']}", key=row):
                    st.session_state.selected_policy = row
                    st.experimental_rerun()

def view_by_date(data):
    # Display URLs grouped by date
    for date in data['Date'].dropna().unique():
        st.subheader(f"Date: {date}")
        day_data = data[data['Date'] == date]
        for _, row in day_data.iterrows():
            expand = st.expander(f"View policies for {row['Link']}")
            #if st.button(f"View policy for {row['Link']}", key=row['Link']):
            if expand:
                if expand.button(f"**Policy:** {row['Policy']}", key=row["Policy (English)"]):
                    st.session_state.selected_policy = row
                    st.experimental_rerun()


    # Handle entries with no available date
    no_date_data = data[data['Date'].isna()]
    if not no_date_data.empty:
        st.subheader("No Available Date")
        for _, row in no_date_data.iterrows():
            expand = st.expander(f"View policy for {row['Link']}")
            # if st.button(f"View policy for {row['Link']}", key=row['Link']):
            if expand:
                if expand.button(f"**Policy:** {row['Policy']}", key=row["Policy Link"]):
                    st.session_state.selected_policy = row
                    st.experimental_rerun()

def show_policy_details(expand, row):
    # Display policy details for the selected URL
    expand.write(f"**Policy:** {row['Policy']}")
    expand.write(f"**Title:** {row['Policy (English)']}")
    expand.write(f"**Category:** {row['Topic']}")
    expand.write(f"**Link to Policy:** [Link]({row['Policy Link']})")
    expand.write(f"**Summary:** {row['Summary']}")
    expand.write(f"**Related News:** [{row['Title']}]({row['Link']})")
def policy_detail_page():
    st.set_page_config(layout="wide")
    policy = st.session_state.selected_policy
    # st.title(f"{policy['Policy']}")
    # st.write(f"**Title:** {policy['Policy (English)']}")
    st.markdown(f"<h1 style='text-align: center;'>{policy['Policy']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>{policy['Policy (English)']}</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)


   # show_policy_details(st,policy)
    with col1:
        # st.title(f"{policy['Policy']}")
        # st.write(f"**Title:** {policy['Policy (English)']}")
        st.write("\n \n \n")
        st.write("\n \n \n")
        st.write("\n \n \n")
        st.write("\n \n \n")
        st.write("\n \n \n")
        st.write("\n \n \n")

        st.write(f"**Category:** {policy['Topic']}")
        st.write(f"**Link to Policy:** [Link]({policy['Policy Link']})")
        st.write(f"**Summary:** {policy['Summary']}")
        st.write(f"**Related News:** [{policy['Title']}]({policy['Link']})")

        if st.button("Back to Policy List"):
            del st.session_state.selected_policy
            st.experimental_rerun()
    with col2:
        url = policy['Link']
        # Embed the webpage
        st.components.v1.iframe(url, width=700, height=600, scrolling=True)

def policy_detail_page_view_by_policy():
    st.set_page_config(layout="wide")
    policy = st.session_state.policy
    filtered_data = st.session_state.filtered_data
    st.markdown(f"<h1 style='text-align: center;'>{policy}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>{filtered_data[filtered_data['Policy'] == policy]['Policy (English)'].iloc[0]}</h2>", unsafe_allow_html=True)
    # st.subheader(policy)
    # st.write(f"**Title:** {filtered_data[filtered_data['Policy'] == policy]['Policy (English)'].iloc[0]}")
    col1, col2 = st.columns(2)
    with col1:
        st.write("\n \n \n")
        st.write("\n \n \n")
        st.write("\n \n \n")
        st.write("\n \n \n")
        st.write("\n \n \n")
        st.write("\n \n \n")
        st.write(f"**Category:** {filtered_data[filtered_data['Policy'] == policy]['Topic'].iloc[0]}")
        st.write(f"**Link to Policy:** [Link]({filtered_data[filtered_data['Policy'] == policy]['Policy Link'].iloc[0]})")
        st.write(filtered_data[filtered_data['Policy'] == policy]['Summary'].iloc[0])
        expand = st.expander(f"Show sources for {policy}")
        for title, link in zip(filtered_data[filtered_data["Policy"] == policy]['Title'],
                               filtered_data[filtered_data["Policy"] == policy]['Link']):
            expand.write(f"**Related News:** [{title}]({link}")

        if st.button("Back to Policy List"):
            del st.session_state.policy
            del st.session_state.filtered_data
            st.experimental_rerun()
    with col2:
        for link in filtered_data[filtered_data["Policy"] == policy]['Link']:
            st.components.v1.iframe(link, width=700, height=600, scrolling=True)




def view_by_policy(filtered_data):
    for policy in filtered_data['Policy'].unique():
        st.subheader(f"{filtered_data[filtered_data['Policy'] == policy]['Policy'].iloc[0]}")
        st.write(f"**Title:** {filtered_data[filtered_data['Policy'] == policy]['Policy (English)'].iloc[0]}")
        st.write(f"**Categories:** {filtered_data[filtered_data['Policy'] == policy]['Topic'].iloc[0]}")
        expand = st.expander("View Summary")
        if expand:
            expand.write(f"**Summary:** \n {filtered_data[filtered_data['Policy'] == policy]['Summary'].iloc[0]}")
        if st.button(f"View Policy Details", key=filtered_data[filtered_data['Policy'] == policy]['Policy'].iloc[0]):
            st.session_state.policy = policy
            st.session_state.filtered_data = filtered_data
            st.experimental_rerun()

def reset_state():
    keys_to_delete = ["country", "format_view", "selected_policy"]
    for key in keys_to_delete:
        if key in st.session_state:
            del st.session_state[key]

def country_page():
    st.title(f"Viewing Data for {st.session_state.country}")
    st.write(f"Format: {st.session_state.format_view}")
    st.sidebar.header("Filter by Topic")
    topics = data['Topic'].unique().tolist()
    new_topics = ["All"]
    for x in topics:
        for y in x.split(','):
            new_topics.append(y)

    #st.sidebar.multiselect("select", topics)
    selected_hashtag = st.sidebar.selectbox("Choose a Topic", new_topics)
    print(type(selected_hashtag))

    if selected_hashtag == "All":
        filtered_data = data
    else:
        # selected hashtag in
        filtered_data = filter_categories(data, selected_hashtag)
        # def check_tags(topic):
        #     if pd.isnull(topic) or not isinstance(topic, str):  # Check if the topic is a string
        #         return False
        #     return any(tag in topic.split(",") for tag in selected_hashtag)
        # print(data["Topic"].apply(check_tags))
        # filtered_data = data[data['Topic'].apply(check_tags)]

    csv = filtered_data.to_csv(index=False)
    st.sidebar.download_button(label="Download Filtered Data", data=csv, file_name='policy_data.csv', mime='text/csv')

    if st.button("Back to Homepage"):
        del st.session_state.country
        del st.session_state.format_view
        st.experimental_rerun()

    if st.session_state.format_view == "View by Policy":
        st.header("Policies Overview")
        view_by_policy(filtered_data)

    if st.session_state.format_view == "View by Date":
        st.header("Policies Overview")
        view_by_date(filtered_data)

if "country" not in st.session_state or "format_view" not in st.session_state:
    main_page()
elif st.session_state.country in ["Singapore", "Australia"]:
    empty_page()
elif "selected_policy" in st.session_state:
    policy_detail_page()
elif "filtered_data" and "policy" in st.session_state:
    policy_detail_page_view_by_policy()
else:
    country_page()
