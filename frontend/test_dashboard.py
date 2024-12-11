import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from dotenv import load_dotenv
from openai import OpenAI
from swarm import Swarm
import matplotlib.pyplot as plt
import json
from ai_agents import *  

load_dotenv()

ollama_client = OpenAI(
    base_url="http://localhost:11434/v1",        
    api_key="ollama"            
)



#Database connection function
def fetch_emails_from_db():
    conn = sqlite3.connect('../backend/emails.db')  #Connect to your SQLite database
    cursor = conn.cursor()  
    
    #Query to fetch emails
    cursor.execute("SELECT id, sender, recipients, subject, body, timestamp, attachments FROM Emails")
    emails = cursor.fetchall()  
    
    #Format emails for the app
    email_list = []
    for email in emails:
        email_list.append({
            "id": email[0],
            "sender": email[1],
            "recipients": email[2],
            "subject": email[3],
            "body": email[4],
            "timestamp": email[5],
            "attachments": email[6].split(",") if email[6] else []
        })
    
    conn.close()
    return email_list

#Metrics (Sample Data)
campaigns = [
    {"Campaign": "Finance Department", "Emails Sent": 50, "Failures": 10, "Training Completed": 5},
    {"Campaign": "HR Department", "Emails Sent": 40, "Failures": 15, "Training Completed": 8},
    {"Campaign": "IT Department", "Emails Sent": 60, "Failures": 12, "Training Completed": 10},
    {"Campaign": "Marketing Department", "Emails Sent": 45, "Failures": 8, "Training Completed": 7},
    {"Campaign": "Sales Department", "Emails Sent": 30, "Failures": 5, "Training Completed": 2},
    {"Campaign": "Legal Department", "Emails Sent": 35, "Failures": 7, "Training Completed": 3},
    {"Campaign": "Operations Department", "Emails Sent": 50, "Failures": 11, "Training Completed": 6},
    {"Campaign": "R&D Department", "Emails Sent": 55, "Failures": 9, "Training Completed": 4},
    {"Campaign": "Procurement Department", "Emails Sent": 40, "Failures": 6, "Training Completed": 3},
]

user_profiles = [
    {'email': 'john.doe@company.com', 'department': 'HR', 'role': 'Manager', 'training_status': 'Completed'},
    {'email': 'jane.smith@company.com', 'department': 'IT', 'role': 'Developer', 'training_status': 'In Progress'},
    {'email': 'mary.jones@company.com', 'department': 'Finance', 'role': 'Accountant', 'training_status': 'Not Started'},
    {'email': 'lucas.brown@company.com', 'department': 'HR', 'role': 'Assistant', 'training_status': 'Completed'},
    {'email': 'emily.davis@company.com', 'department': 'Marketing', 'role': 'Lead', 'training_status': 'In Progress'},
    {'email': 'william.king@company.com', 'department': 'IT', 'role': 'SysAdmin', 'training_status': 'Completed'},
    {'email': 'olivia.martin@company.com', 'department': 'Sales', 'role': 'Sales Manager', 'training_status': 'Not Started'},
    {'email': 'emma.white@company.com', 'department': 'Marketing', 'role': 'Coordinator', 'training_status': 'In Progress'},
    {'email': 'noah.miller@company.com', 'department': 'Legal', 'role': 'Paralegal', 'training_status': 'Not Started'},
    {'email': 'ava.johnson@company.com', 'department': 'Legal', 'role': 'Attorney', 'training_status': 'Completed'},
    {'email': 'mason.roberts@company.com', 'department': 'Operations', 'role': 'Logistics Manager', 'training_status': 'In Progress'},
    {'email': 'mia.clark@company.com', 'department': 'Operations', 'role': 'Coordinator', 'training_status': 'Not Started'},
    {'email': 'logan.moore@company.com', 'department': 'R&D', 'role': 'Researcher', 'training_status': 'Completed'},
    {'email': 'sophia.lewis@company.com', 'department': 'R&D', 'role': 'Scientist', 'training_status': 'In Progress'},
    {'email': 'jacob.walker@company.com', 'department': 'Procurement', 'role': 'Buyer', 'training_status': 'Completed'},
    {'email': 'isabella.allen@company.com', 'department': 'Procurement', 'role': 'Analyst', 'training_status': 'Not Started'},
]

df = pd.DataFrame(user_profiles)


campaign_df = pd.DataFrame(campaigns)




st.title("AI-Driven Phishing Susceptibility Testing")

#Navigation
menu = st.sidebar.radio("Navigation", ["Dashboard", "Email Viewer", "Campaign Management", "Training Progress"])

if menu == "Dashboard":
    st.header("Admin Dashboard")
    
    #Campaign metrics
    st.subheader("Campaign Overview")
    fig = px.bar(campaign_df, x="Campaign", y="Emails Sent", color="Failures", 
                 labels={"Failures": "Phishing Failures"}, title="Campaign Performance")
    st.plotly_chart(fig)
    
    st.subheader("Failure Rate by Campaign")
    failure_rate_fig = px.pie(campaign_df, names="Campaign", values="Failures", 
                              title="Failure Rates Across Campaigns")
    st.plotly_chart(failure_rate_fig)

elif menu == "Email Viewer":
    st.header("Email Inbox")
    
    email_data = fetch_emails_from_db()
    
    #Display emails
    for email in email_data:
        with st.expander(f"Subject: {email['subject']}"):
            st.write(f"Sender: {email['sender']}")
            st.write(f"Recipients: {email['recipients'] or 'N/A'}")
            st.write(f"Content: {email['body']}")
            st.write(f"Timestamp: {email['timestamp']}")
            st.write("Attachments:")
            for attachment in email["attachments"]:
                st.write(f"- {attachment}")

elif menu == "Campaign Management":
    st.header("Campaign Management")

    #Initialize the client and conversation history if not already done
    if 'client' not in st.session_state:
        st.session_state.client = Swarm(client=ollama_client)
        print("Starting client")
        st.session_state.messages = []
        st.session_state.user_input = ""  #Initialize the user input state

    st.subheader("Start New Campaign")
    campaign_name = st.text_input("Campaign request")
    
    if st.button("Submit Campaign"):
        try:
            #Send the campaign request to the AI agent
            response = st.session_state.client.run(
                agent=sql_router_agent,
                messages=[{"role": "user", "content": f"{campaign_name}"}],
                context_variables={}
            )
            
            #Check if the campaign was successfully configured
            if response.messages[-1]["content"] == "Campaign configured.":
                st.success(f"Campaign '{campaign_name}' launched successfully!")
            else:
                st.error(f"Failed to launch campaign. Response content: {response.messages[-1]['content']}")
        except Exception as e:
            #Capture any errors that occur during the campaign launch process
            st.error(f"An error occurred while launching the campaign: {str(e)}")
    
    st.subheader("Active Campaigns")
    st.write("Currently no active campaigns.")  

    #Ongoing communication with AI after campaign submission
    st.subheader("Communicate with AI Agent")
    def clear_user_input():
        st.session_state.user_input = ""

    user_input = st.text_input(
        "Ask something:", 
        key="user_input", 
        on_change=clear_user_input
    )
    
    if user_input:
        #Append the user input to the conversation
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        #Send the conversation history to the AI agent
        response = st.session_state.client.run(
            agent=sql_router_agent,
            messages=st.session_state.messages,
            context_variables={}
        )
        
        #Display the AI's response
        st.session_state.messages.append({"role": "assistant", "content": response.messages[-1]["content"]})

    #Display the conversation history
    if st.session_state.messages:
        st.subheader("Conversation History")
        for message in st.session_state.messages:
            if message['role'] == "user":
                st.write(f"User: {message['content']}")
            else:
                st.write(f"AI: {message['content']}")



elif menu == "Training Progress":
    st.header("Training Progress")


    #Initialize a new DataFrame for modifying the training status
    df_copy = df.copy()

    st.subheader("Update Training Status")
    user_email = st.selectbox(
        "Select user to update their training status",
        options=df_copy['email'].tolist()
    )

    #Find the selected user's current status
    selected_user = df_copy[df_copy['email'] == user_email]
    current_status = selected_user['training_status'].values[0]

    #Select a new status for the chosen user
    new_status = st.selectbox(
        f"Update Status for {user_email}",
        options=["Completed", "In Progress", "Not Started"],
        index=["Completed", "In Progress", "Not Started"].index(current_status)
    )

    #Update the training status in the DataFrame
    df_copy.loc[df_copy['email'] == user_email, 'training_status'] = new_status


    #Multiselect to filter the table based on training status
    selected_statuses = st.multiselect(
        "Filter by Training Status",
        options=["Completed", "In Progress", "Not Started"],
        default=["Completed", "In Progress", "Not Started"],
        help="Filter users based on their training status."
    )

    filtered_df = df_copy[df_copy['training_status'].isin(selected_statuses)]

    #Display the filtered dataframe
    st.dataframe(filtered_df[['email', 'department', 'role', 'training_status']])

    #Calculate training completion rate
    completed = df_copy[df_copy['training_status'] == "Completed"].shape[0]
    total = df_copy.shape[0]
    st.write(f"Training Completion Rate: {completed}/{total} ({(completed / total) * 100:.2f}%)")

    #Graph: Training status distribution
    st.subheader("Training Status Distribution")
    status_counts = df_copy['training_status'].value_counts()
    fig, ax = plt.subplots()
    status_counts.plot(kind='bar', ax=ax, color=['green', 'orange', 'red'])
    ax.set_title("Training Status Distribution")
    ax.set_xlabel("Training Status")
    ax.set_ylabel("Number of Users")
    st.pyplot(fig)
