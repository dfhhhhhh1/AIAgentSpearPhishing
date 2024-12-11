# Phishing Email Generation and Campaign Management System

This project aims to do phishing email generation and campaign management system that integrates with SQLite, SQL query agents, and AI agents to orchestrate tasks such as generating phishing emails, managing campaigns, and analyzing responses.

## Overview

This system uses AI agents to handle various tasks involved in spear-phishing campaigns. The system integrates multiple components to query databases, generate phishing emails, and produce campaign reports. It features:

- **SQL Query Agents**: Query and manage database information related to user profiles and emails.
- **Phishing Email Generation**: Generate personalized phishing emails based on user profiles.
- **Campaign Management**: Configure, run, and track phishing campaigns.
- **Analytics**: Generate detailed campaign reports based on user responses.

## Technologies Used

- Python
- SQLite
- Swarm (AI Agent Framework)
- Streamlit (for the web interface)
- Plotly (for data visualization)
- Ollama API , Qwen2.5:3b model (for language models)

## Setup

1. Clone the repository:
```bash
   git clone https://github.com/your-repo/phishing-campaign-management.git
```
2. Run the backend data loader: Navigate to the backend folder and run the load_data.py script to load the necessary data into your SQLite database:
```bash
cd backend
python load_data.py
```
3. Set up the frontend: Navigate to the frontend folder:
```bash
cd ../frontend
```
4. Create a virtual environment: Create a virtual environment to manage dependencies:
```bash
python3 -m venv venv
```
5. Activate the virtual environment:

On Windows:
```bash
venv\Scripts\activate
```

On Mac/Linux:
```bash
source venv/bin/activate
```
6. Install required dependencies: Install the necessary Python packages listed in requirements.txt:
```bash
pip install -r requirements.txt
```
7. Set up environment variables: Create a .env file in the frontend folder and add the required configuration, such as the model to be used for generating phishing emails:
```bash
MODEL=your_model_name
```
8. Run the Streamlit dashboard: Finally, launch the Streamlit app to visualize and interact with the phishing campaign data:
```bash
streamlit run test_dashboard.py
```