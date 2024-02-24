from chat_store import save_conversation,load_unique_prompts,load_conversations_by_prompt
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
def extract_unique_prompts(conversation_history):
    all_prompts = [message['Prompt'] for message in conversation_history]
    print(all_prompts)
    return list(set(all_prompts))  # Using a set removes duplicates

def update_and_get_unique_prompts(new_prompt=None):
    # Load all unique prompts to check if the new_prompt already exists
    unique_prompts = load_unique_prompts()
    print(unique_prompts)
    
    if new_prompt and new_prompt not in unique_prompts:
        # Save the new prompt to your conversation history or a separate prompt storage
        save_conversation({'Prompt': new_prompt, 'User': '', 'Model': ''})
        # Reload the unique prompts as the list has changed
        unique_prompts = load_unique_prompts()
    
    return unique_prompts


memory = ConversationSummaryBufferMemory(llm=llm)
human_avatar='https://th.bing.com/th/id/R.f307bf56791ab698472f57441c1f14fb?rik=kfAyyfpbDg92hQ&pid=ImgRaw&r=0'
ai_avatar='https://th.bing.com/th/id/R.26802dee07032f0f553419f19490e897?rik=YjFAxIlImCxxrA&pid=ImgRaw&r=0'

st.header('Make Your Assistant')

# Sidebar: Prompt Template 
st.sidebar.header("Prompt Template")
prompt_template = st.sidebar.text_area('Enter your prompt template here:')
apply_button = st.sidebar.button("Apply Template")
st.sidebar.header("Prompt Selection")

# Main Chat Area
# Main conversation area
st.header("Conversation")
user_input = st.text_input('Enter your prompt:', key='user_input')
send_button = st.button("Send")


def prompt(prompt_template: str, user_input: str = None):
    # Your updated and excellent prompt function
    formatted_prompt = f'''
    # Instructions:\n {prompt_template}\n
     # Query: {user_input}
      

    
        '''

    return PromptTemplate(template=formatted_prompt, input_variables=[user_input])

general_chain = LLMChain(
    llm=llm, 
    prompt=prompt("", user_input=user_input), 
    memory=memory, 
    verbose=True
)



template_chain = None  # Initialize template_chain outside the loop
if apply_button and prompt_template:
    all_prompts = update_and_get_unique_prompts(new_prompt=prompt_template)

# st.sidebar.header("Prompt Selection")
all_prompts = update_and_get_unique_prompts()  # Update prompts from storage
selected_prompt = st.sidebar.selectbox("Choose a Prompt", options=all_prompts, key='selected_prompt')


current_history=[]
def handle_input():
    
    global template_chain
    global current_history
    # applied_prompt = ""
    current_prompt = selected_prompt if selected_prompt else prompt_template

    if send_button and user_input:

      # Use the current prompt for model invocation
        model_chain = LLMChain(
        llm=llm, 
        prompt=prompt(current_prompt, user_input), 
        memory=memory, 
        verbose=True
        )
        output = model_chain.invoke({'input': user_input})
        # Save the information to database
        save_conversation({'Prompt': current_prompt, 'User': user_input, 'Model': output.get('text','')})
        # Reload conversation history to display the latest interaction
        current_history = load_conversations_by_prompt(current_prompt)
        # print(current_history)
 
    # Display Chat History
    for message in current_history:
       # Display user/model messages accordingly
       user_message = message['User']
       model_output=message['Model']
       
    
    # Display user message with avatar
       st.markdown(
        f"<div class='user-message'><img src='{human_avatar}' class='avatar'>{user_message}</div>",
        unsafe_allow_html=True
       )
    
    # Display model message with robot avatar
       st.markdown(
        f"<div class='model-message'><img src='{ai_avatar}' class='avatar'>{model_output}</div>",
        unsafe_allow_html=True
            )
  
if __name__ == "__main__":
    handle_input()




