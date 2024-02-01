import streamlit as st
import pandas as pd
import requests
import base64
import os
from pdf2image import convert_from_path
from io import BytesIO
from passlib.hash import bcrypt
import numpy as np
#from streamlit_tags import  st_tags_sidebar, st_tags


#TODO authentication
#TODO add logout button in country page and in sidebar
#TODO add title to login in page

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



def display_embeded_pdf_in_streamlit_x(pdf_link):
    try:
        # Download PDF to a temporary location
        # response = requests.get(pdf_link)
        # response.raise_for_status()  # Raise an error for bad status codes

        # Write the PDF to a temporary file
        file_path = os.path.join("data",f"{pdf_link.split('/')[-1]}")


        # Open the temp PDF file and encode it in base64
        with open(file_path, "rb") as file:
            base64_pdf = base64.b64encode(file.read()).decode('utf-8')

        # Embedding PDF in HTML
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

        # Clean up: delete the temp file
        #os.remove(temp_file_path)

    except requests.exceptions.RequestException as e:
        # Handle any errors during the download
        st.error("Couldn't render")

def display_embeded_pdf_in_streamlit(pdf_link):
    pdf_file = os.path.join("data", f"{pdf_link.split('/')[-1]}")
    pages = convert_from_path(pdf_file)

    # Encode images in base64 and create an HTML string to embed
    embedded_images = ""
    for page in pages:
        buffered = BytesIO()
        page.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        embedded_images += f'<img src="data:image/jpeg;base64,{img_str}" style="width:100%; margin-bottom: 10px;">'

    # Define the HTML for the scrollable mini window
    mini_window_html = f"""
            <div style="width: 700px; height: 500px; overflow-y: scroll; border: 1px solid #ccc;">
                {embedded_images}
            </div>
            """
    st.markdown(mini_window_html, unsafe_allow_html=True)
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
    #st.set_page_config(layout="centered")
    st.title("APAC ESG Policy Monitor")
    country = st.selectbox("Choose a country", ["China", "Singapore", "Australia"])
    format_view = st.radio("Choose your viewing format", ["View by Policy", "View by Date"])
    col1, col2 = st.columns([.15, 1])
    with col1:
        if st.button("Submit"):
            st.session_state.country = country
            st.session_state.format_view = format_view
            st.experimental_rerun()
    with col2:
        if st.button("Logout"):
            # Reset session state
            st.session_state['loggedin'] = False
            st.session_state['username'] = ''
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
    #st.set_page_config(layout="wide")
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
    #st.set_page_config(layout="wide")
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
        url = policy['Policy Link']
        if "pdf" not in url:
        # Embed the webpage
            st.components.v1.iframe(url, width=700, height=600, scrolling=True)
        else:
            display_embeded_pdf_in_streamlit(url)

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
        #for link in filtered_data[filtered_data["Policy"] == policy]['Link']:
        url = filtered_data[filtered_data['Policy'] == policy]['Policy Link'].iloc[0]
        print(url)
        if "pdf" not in url:
        # Embed the webpage
            st.components.v1.iframe(url, width=700, height=600, scrolling=True)
        else:
            display_embeded_pdf_in_streamlit(url)





def view_by_policy(filtered_data):
   # st.set_page_config(layout="wide")
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
    #st.set_page_config(layout="wide")
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
    if st.sidebar.button("Logout"):
            st.session_state['loggedin'] = False
            st.session_state['username'] = ''
            st.experimental_rerun()

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

def verify_password(input_password):
    hashed_passwords = st.secrets["authentication"]["hashed_passwords"]
    for hashed_password in hashed_passwords:
        if bcrypt.verify(input_password, hashed_password):
            return True
    return False

# Login Page
def login_page():
    st.set_page_config(layout="centered")
    st.title("APAC ESG Policy Monitor")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            if verify_password(password):
                # Update session state
                st.session_state['loggedin'] = True
                st.session_state['username'] = username
                st.experimental_rerun()
            else:
                st.error("Login failed. Please check your username and password.")

def main():
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

if 'loggedin' not in st.session_state or not st.session_state['loggedin']:
        login_page()
else:
        main()

