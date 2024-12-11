from dotenv import load_dotenv
from swarm import Agent
import sqlite3
import os



load_dotenv()
model = os.getenv('LLM_MODEL', 'qwen2.5-coder:3b')

conn = sqlite3.connect('../backend/emails.db')
cursor = conn.cursor()

with open("../backend/emails.sql", "r") as table_schema_file:
    table_schemas = table_schema_file.read()

def get_sql_router_agent_instructions():
    return """You are an orchestrator of different SQL data experts and it is your job to
    determine which of the agent is best suited to handle the user's request, 
    and transfer the conversation to that agent."""

def fetch_sample_data():
    """Fetch sample data from the database for each table."""
    sample_data = {}
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")  #Fetch 5 rows from each table
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        sample_data[table_name] = {"columns": columns, "rows": rows}
    
    return sample_data

def format_sample_data(sample_data):
    """Format sample data into a string representation."""
    formatted_data = ""
    for table, data in sample_data.items():
        formatted_data += f"\nTable: {table}\nColumns: {', '.join(data['columns'])}\nSample Rows:\n"
        for row in data['rows']:
            formatted_data += f"{row}\n"
    return formatted_data

def get_sql_agent_instructions():
    sample_data = fetch_sample_data()
    formatted_sample_data = format_sample_data(sample_data)
    
    return f"""You are a SQL expert who takes in a request from a user for information
    they want to retrieve from the DB, creates a SELECT statement to retrieve the
    necessary information, and then invoke the run_sql_select_statement(sql_statement) function to run the query and
    get the results back to then report to the user the information they wanted to know.
    
    Here are the table schemas for the DB you can query:
    
    {table_schemas}

    Here is some example data from the database:
    {formatted_sample_data}
    
    Write all of your SQL SELECT statements to work 100% with these schemas and nothing else.
    You are always willing to create and execute the SQL statements to answer the user's question.
    
    Examples:
    - If the user asks for "emails that are in the HR department", you should construct a query like:
      `SELECT * FROM UserProfiles WHERE department = 'HR'`
    - If the user asks for "users who have completed training", you should construct a query like:
      `SELECT * FROM UserProfiles WHERE training_status = 'Completed'`
    - If the user asks for "emails of developers in the IT department", you should construct a query like:
      `SELECT email FROM UserProfiles WHERE department = 'IT' AND role = 'Developer'`
    
    If the user's request is unclear, ask for clarification.
    If no results are found, return "No results found."
    """


#Define the SQL Router Agent
sql_router_agent = Agent(
    name="Router Agent",
    instructions=get_sql_router_agent_instructions(),
    model="qwen2.5:3b"
)

def generate_phishing_email(context_variables, target):
    """Generates a spear-phishing email for the given target."""
    
    #Check that target is a valid string
    if not isinstance(target, str):
        return "Invalid target email format."
    
    #Fetch user profile
    cursor.execute(f"SELECT * FROM UserProfiles WHERE email = ?", (target,))
    user_profile = cursor.fetchone()
    
    if not user_profile:
        print(f"User not found")
        return "User not found."
    
    #Extract data from the user profile tuple (email, department, role, training_status)
    email, department, role, training_status = user_profile[0], user_profile[1], user_profile[2], user_profile[3]
    
    #Compose phishing email content
    subject = f"Important: {department} Department Update"
    body = f"Dear {role},\n\nWe have a critical update for your {department} department. Please verify your details immediately."
    
    #Add warning for users who haven't completed training
    if training_status.lower() == "not started":
        body += "\n\nNote: You haven't completed the mandatory security training. Please complete it ASAP!"
    
    body += "\n\nKind regards,\nIT Support"
    
    print(f"Generated Email:\nSubject: {subject}\nBody:\n{body}")


    return {"subject": subject, "body": body}


email_generation_agent = Agent(
    name="Email Generation Agent",
    instructions="Create phishing emails based on provided target email addresses. If you do not have the profiles, transfer back to the routing agent",
    functions=[generate_phishing_email],
    model=model

)

def run_sql_select_statement(sql_statement):
    """Executes a SQL SELECT statement and returns the results of running the SELECT. Make sure you have a full SQL SELECT query created before calling this function."""
    print(f"Executing SQL statement: {sql_statement}")
    cursor.execute(sql_statement)
    records = cursor.fetchall()

    if not records:
        print("No results found from sql search")
        return "No results found."
    
    #Get column names
    column_names = [description[0] for description in cursor.description]
    
    #Calculate column widths
    col_widths = [len(name) for name in column_names]
    for row in records:
        for i, value in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(value)))
    
    #Format the results
    result_str = ""
    
    #Add header
    header = " | ".join(name.ljust(width) for name, width in zip(column_names, col_widths))
    result_str += header + "\n"
    result_str += "-" * len(header) + "\n"
    
    #Add rows
    for row in records:
        row_str = " | ".join(str(value).ljust(width) for value, width in zip(row, col_widths))
        result_str += row_str + "\n"
    print(result_str)
    return result_str   

data_management_agent = Agent(
    name="SQL Query Agent",
    instructions=get_sql_agent_instructions() + "\n\nHelp the user with data relating to UserProfiles email.",
    functions=[run_sql_select_statement],
    model=model
)

#Define the Admin Support Agent
def configure_campaign(context_variables, parameters):
    """Set up the spear-phishing campaign."""
    print(f"Configuring campaign with parameters: {parameters}")
    return {"campaign_configured": True, "agent": email_generation_agent}

admin_support_agent = Agent(
    name="Admin Support Agent",
    instructions="Interface with admin for managing campaigns and viewing results.",
    functions=[configure_campaign],
    model=model
)




#Define the Campaign Analytics Agent
def generate_campaign_report(context_variables):
    """Generate a campaign report based on user responses."""
    conn = sqlite3.connect('../backend/emails.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_email, response_type FROM EmailResponses")
    records = cursor.fetchall()
    conn.close()
    
    if not records:
        return "No responses found."
    
    #Process the records to create a report
    response_counts = {}
    for record in records:
        user_email, response_type = record
        if user_email not in response_counts:
            response_counts[user_email] = {"opened": 0, "clicked_link": 0, "ignored": 0}
        if response_type.lower() == "opened":
            response_counts[user_email]["opened"] += 1
        elif response_type.lower() == "clicked":
            response_counts[user_email]["clicked_link"] += 1
        elif response_type.lower() == "ignored":
            response_counts[user_email]["ignored"] += 1
    
    report = "Campaign Report:\n"
    for user_email, responses in response_counts.items():
        report += f"{user_email}: Opened {responses['opened']} times, Clicked Link {responses['clicked_link']} times, Ignored {responses['ignored']} times\n"
    
    return report

campaignanalyticsagent = Agent(
    name="Campaign Analytics Agent",
    instructions="Generate analytics and reports for phishing campaigns.",
    functions=[generate_campaign_report],
    model=model
)


def transfer_to_email_agent():
    print("Transferring to Email Generation Agent...")
    return email_generation_agent


def transfer_to_data_agent():
    print("Transferring to Data Management Agent...")
    return data_management_agent

def transfer_to_admin_agent():
    print("Transferring to Admin Support Agent...")
    return admin_support_agent


def transfer_to_campaign_agent():
    print(f"Transferring to Campaign Analytics Agent...")
    return campaignanalyticsagent



def transfer_back_to_router_agent():
    print("Transferring Back to Router Agent...")
    return sql_router_agent


#Set up the router agent functions
sql_router_agent.functions = [
    transfer_to_email_agent,
    transfer_to_data_agent,
    transfer_to_admin_agent,
    transfer_to_campaign_agent
]



#Set up the transfer functions for each agent
email_generation_agent.functions.append(transfer_back_to_router_agent)
data_management_agent.functions.append(transfer_back_to_router_agent)
admin_support_agent.functions.append(transfer_back_to_router_agent)
campaignanalyticsagent.functions.append(transfer_back_to_router_agent)
