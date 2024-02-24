from chat_store2 import save_conversation,load_unique_prompts,load_conversations_by_prompt
from imports import (
    PromptTemplate,
    LLMChain,
    ConversationChain,
    ConversationBufferMemory,
    ConversationSummaryBufferMemory,
    ConversationKGMemory,
    ConversationSummaryMemory,
    load_dotenv,
    os,
    genai,
    dotenv,
    st,
    langchain,
)

load_dotenv()
os.environ['GOOGLE_API_KEY']=os.getenv('GOOGLE_API_KEY')

llm=genai(model='gemini-pro')
def load_css(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("styles.css")  # Load your CSS file
memory = ConversationSummaryBufferMemory(llm=llm)
# Define global variables for avatars
human_avatar = 'https://th.bing.com/th/id/R.f307bf56791ab698472f57441c1f14fb?rik=kfAyyfpbDg92hQ&pid=ImgRaw&r=0'
ai_avatar = 'https://th.bing.com/th/id/R.26802dee07032f0f553419f19490e897?rik=YjFAxIlImCxxrA&pid=ImgRaw&r=0'

# Streamlit UI Components
st.header('Make Your Assistant')

# Sidebar for prompt template input
st.sidebar.header("Prompt Template")
prompt_template = st.sidebar.text_area('Enter your prompt template here:')
apply_button = st.sidebar.button("Apply Template")

def prompt(prompt_template: str, user_input: str = None):
    # Your updated and excellent prompt function
    formatted_prompt = f'''
    # Instructions:\n {prompt_template}\n
     # Query: {user_input}
      

    
        '''

    return PromptTemplate(template=formatted_prompt, input_variables=[user_input])

# Update and display unique prompts
def update_and_get_unique_prompts(new_prompt=None):
    unique_prompts = load_unique_prompts()
    if new_prompt and new_prompt not in unique_prompts:
        save_conversation({'Prompt': new_prompt, 'User': '', 'Model': ''})
        unique_prompts = load_unique_prompts()
    return unique_prompts

if apply_button and prompt_template:
    update_and_get_unique_prompts(new_prompt=prompt_template)

all_prompts = update_and_get_unique_prompts()
selected_prompt = st.sidebar.selectbox("Choose a Prompt", options=all_prompts, key='selected_prompt')

# Main conversation area
st.header("Conversation")
user_input = st.text_input('Enter your prompt:', key='user_input')
send_button = st.button("Send")

# Function to handle user input and model response
def handle_input():
    global template_chain
    global current_history
    # applied_prompt = ""
    current_prompt = selected_prompt if selected_prompt else prompt_template
    if send_button and user_input:
        # Create the model prompt
        # model_prompt = PromptTemplate(template=selected_prompt, input_variables=[user_input]).format_prompt()
        # Invoke the model with the prompt
        model_chain = LLMChain(
        llm=llm, 
        prompt=prompt(current_prompt, user_input), 
        memory=memory, 
        verbose=True
        )
        output = model_chain.invoke({'input': user_input})
        
        # Save the conversation to the database
        save_conversation({'Prompt': selected_prompt, 'User': user_input, 'Model': output.get('text',' ')})
        
        # Reload and display the conversation history
        current_history = load_conversations_by_prompt(selected_prompt)
        for message in current_history:
            print(message)
            user_message = message['user_input']
            model_output = message['model_output']
            
            # Display user message
            st.markdown(f"<div class='user-message'><img src='{human_avatar}' class='avatar'>{user_message}</div>", unsafe_allow_html=True)
            
            # Display model response
            st.markdown(f"<div class='model-message'><img src='{ai_avatar}' class='avatar'>{model_output}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    handle_input()









