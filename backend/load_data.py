import sqlite3
#Create db file from sql file
def create_and_load_database(sql_file, db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        with open(sql_file, 'r') as f:
            sql_script = f.read()
        
        cursor.executescript(sql_script)
        conn.commit()
        
        print(f"Database {db_file} created and loaded successfully.")
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

#Define file paths
sql_file_path = "emails.sql"  
db_file_path = "emails.db"    

create_and_load_database(sql_file_path, db_file_path)