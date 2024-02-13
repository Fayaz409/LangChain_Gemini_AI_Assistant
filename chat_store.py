chat_history = [{"User": "", "Model": ""}]

def save_conversation(new_messages):
    global chat_history
    chat_history.extend(new_messages)

def load_conversation():
    global chat_history
    return chat_history

