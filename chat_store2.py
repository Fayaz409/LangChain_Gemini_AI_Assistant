from imports import (
    os,
    load_dotenv
)
import mysql.connector

load_dotenv()

def get_db_connection():
    cnx = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )
    print('Connected To SQL Successfully')
    return cnx

def save_conversation(conversation):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    add_conversation = ("INSERT INTO conversations "
                        "(prompt, user_input, model_output) "
                        "VALUES (%s, %s, %s)")
    data_conversation = (conversation['Prompt'], conversation['User'], conversation['Model'])
    cursor.execute(add_conversation, data_conversation)
    cnx.commit()
    cursor.close()
    cnx.close()

def load_unique_prompts():
    cnx = get_db_connection()
    cursor = cnx.cursor()
    query = "SELECT DISTINCT prompt FROM conversations"
    cursor.execute(query)
    unique_prompts = [row[0] for row in cursor]
    cursor.close()
    cnx.close()
    return unique_prompts

def load_conversations_by_prompt(prompt_filter):
    cnx = get_db_connection()
    cursor = cnx.cursor(dictionary=True)
    query = "SELECT * FROM conversations WHERE prompt = %s"
    cursor.execute(query, (prompt_filter,))
    conversations = cursor.fetchall()
    cursor.close()
    cnx.close()
    return conversations

# Don't forget to close the connection when done
# cnx.close()