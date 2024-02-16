import pymongo
import os
from dotenv import load_dotenv
load_dotenv()
try:
    # Attempting to create a MongoDB client and access the chat_database
    client = pymongo.MongoClient(os.getenv('MONGODB_API_KEY2'), ssl=True)
    db = client['chat_database']
    collection = db['conversations']

    # If no exception is raised, the connection was successful
    print("Connected to MongoDB successfully!")

    # Now we can perform operations on the 'collection' object

except Exception as e:
    # If an exception is raised, print the error message
    print(f"Error connecting to MongoDB: {e}")
# chat_history = []

def save_conversation(new_messages):
    conversation_id = collection.insert_one({'conversation': new_messages}).inserted_id


def load_conversation():
    global chat_history
    results=collection.find({})
    # print(results)
    # for result in results:
    #     print(result)
    all_conversations=[result['conversation'] for result in results]
    # print(all_conversations)
    return all_conversations

