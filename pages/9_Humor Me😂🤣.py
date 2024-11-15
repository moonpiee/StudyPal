import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory,InMemoryChatMessageHistory


session_id_runn="runn_chat_history9"
session_id_wo_runn="wo_runn_chat_history9"
st.title("Study Pal🌱📚💪")
languages=["English","Telugu","Hindi","Malayalam","Marathi","Bengali","Kannada"]
instructions_lis=["Tutor Me","Teacher Pal","Translate","Learn Language","Communicate","Surprise Me","Tell Me Why","Tongue Twister","Humor Me","Story Time", "More Fun Games","Inspire Me"]
st.header(instructions_lis[8]+"😂🤣")
instruction = instructions_lis[8]
sel_language=st.selectbox(label="Your Language?",options=languages) #1st one by default
sel_model="llama-3.1-70b-versatile" #default
sel_temp=0#default
with st.sidebar:
    adv_opt=st.toggle("More Options")
    if adv_opt:
     sel_model = st.selectbox("Select model", ("llama-3.1-70b-versatile","llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma2-9b-it", "gemma-7b-it", "llama-3.2-11b-text-preview"))
     sel_temp = st.slider("Temperature",0.0,1.0,0.0)
    #  groq_api_key=st.text_input("Your Groq API Key")

match instruction:
    case "Tutor Me":
          instruction_desc=f"Talk in {sel_language}. You are an excellent Tutor. You ask me my subject I want help with. Then ask what I want help with. Help me in explaining, clarifying concepts, doubts etc., If I ask you to solve anything, give me upto 3 hints before telling me the solution. You also provide flowcharts in ascii for easy memorisation of topics if needed etc.,"
    case "Teacher Pal":
          instruction_desc=f"Talk in {sel_language}. You are an excellent Teacher. My aim is to teach my students (learning should be fun) in the best way possible academically and professionally. You ask me my subject I want help with. Then ask what I want help with. Help me in teaching students effectively, creatively, interactively etc.,You also provide me useful short study materials, Short quiz Q&A, flowcharts in ascii for easy memorisation of topics if needed etc.,"
    case "Translate":
          instruction_desc=f"Talk in {sel_language}.You are a translator. Ask me word/sentence and language i want to translate. You translate the user input to language I mention"
    case "Learn Language":
          instruction_desc=f"You are an expert at language teaching. You ask me language I wish to learn and the language I know already. Teach me {sel_language} using the language I know"
    case "Communicate":
          instruction_desc=f"You are an excellent communicator in {sel_language}. You help me enhnace my communication skills by conversing with me, improving me if necessary thus making me an excellent communicator.Answer as short as possible, straight to point"
    case "Surprise Me":
          instruction_desc=f"Talk in {sel_language}.You like to surprise students with amazing facts. Be it related to  Science, Social, Math or whatever.One surprise at a time. Ask no questions, no headers. Use emojis, symbols wherever if needed"
    case "Tell Me Why":
          instruction_desc=f"Talk in {sel_language}.This is a question-and-answer format telling about a thing/fact/concept/anything that aims to spark curiosity and encourage learning. Like why so & so things are so & so. One at a time. Should be interesting and make me curious. Ask no questions and no headers. Use emojis, symbols wherever if needed"
    case "Tongue Twister":
        instruction_desc=f"In {sel_language} spin out a tongue twister. One at a time. Ask no questions, no headers. Use emojis, symbols wherever if needed"
    case "Humor Me":
        instruction_desc=f"In {sel_language} make a joke. One at a time. Should be humorous, laughable. Ask no questions. No headers. Use emojis, symbols wherever if needed"
    case "Story Time":
        instruction_desc=f"In {sel_language} tell an interesting children story as short as possible. Ask no questions. Use emojis, symbols wherever if needed"
    case "More Fun Games":
        instruction_desc=f"In {sel_language} provide fun games like puzzles, challenges, make a story with hints or make a story with a structure of happenings/characters something like forest - rabbit - stars make your own story kind of etc., to improve aptitude and cognitive abilities with fun"
    case "Inspire Me":
        instruction_desc=f"Talk in {sel_language}. You inspire, motivate, enlighten me as a student through your words. One at a time. You can use quotes, inspirational stories etc., Be as short as possible. Ask no uestions"
    case _:
        instruction_desc=f"You are a helpful assistant for students in their academics in various subjects."

# print(sel_language,sel_model,sel_temp,instruction)

# st.caption("this is choice by user")
def show_previous_chats(session_id):
    trnsl_chat_lis=[]
    if session_id_wo_runn in st.session_state:
        for msg in st.session_state[session_id_wo_runn][:]: #msg-> [role:, content]
            with st.chat_message(msg["role"]):
                if msg["content"] is not None:
                    if msg["role"]=="user":
                        message_to_app = HumanMessage(content=msg["content"])
                    else:
                        message_to_app = AIMessage(content=msg["content"])
                    st.markdown(msg["content"])
                    trnsl_chat_lis.append(message_to_app)

def chatbot(input_txt):
        st.chat_message('user').write(input_txt)
        st.session_state[session_id_wo_runn].append({"role":"user", "content":input_txt})
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):
                # print(f"Instruction desc: {prompt_inst(instruction,sel_language)}")
                response=chain_with_history.invoke(
                {"input":input_txt, "instruction_desc":instruction_desc,"sel_language":sel_language},
                {"configurable": {"session_id": session_id_runn}}
                )
                st.markdown(response.content)
                message = {"role":"assistant","content":response.content}
                st.session_state[session_id_wo_runn].append(message)
        st.write("\n***\n")
#to store in mmemory messagr with runnabels. other method is thru langgraph
def get_session_id(session_id:str) -> BaseChatMessageHistory:
    if session_id not in st.session_state:
        st.session_state[session_id]=InMemoryChatMessageHistory()
    return st.session_state[session_id]
#prepare groq chat api  model/client
if st.secrets["GROQ_API_KEY"]!="":
    groq_api_key=st.secrets["GROQ_API_KEY"]
else:
    groq_api_key=""
# print("groq key:...",{groq_api_key})
chat_groq=ChatGroq(
    api_key=st.secrets["GROQ_API_KEY"],
    model=sel_model,
    temperature=sel_temp
)

#updated version of llmchain
template = ChatPromptTemplate([
    ("system","Talk in {sel_language}. Instruction: {instruction_desc}"),
	 MessagesPlaceholder(variable_name=session_id_runn),
    ("human","{input}"),
])
chain = template | chat_groq
chain_with_history=RunnableWithMessageHistory(
                                chain,
                                get_session_id,
                                input_messages_key="input",
                                history_messages_key=session_id_runn
                                )
if session_id_runn not in st.session_state and session_id_wo_runn not in st.session_state: #runnbale vs without runnable
    # print(f"{session_id_runn} session id is not initialised. intialising...")
    with st.spinner("Initializing the bot..."):
            # initial_msg=conversation.predict(input="",trnsl_chat_history=[])
            initial_msg=chain_with_history.invoke( #when you invoke, you store. automatically with runnab;les
                {"input":"How can I utilise you? Briefly list out","instruction_desc":instruction_desc,"sel_language":sel_language}, #How can I utilise you? Briefly list out
                config={"configurable": {"session_id": session_id_runn}}
            )
            st.session_state[session_id_wo_runn]=[{"role":"assistant", "content":initial_msg.content}] #no need to add this in history

input_txt=st.chat_input("Input text")
if session_id_runn in st.session_state and session_id_wo_runn in st.session_state:
    # print("showing prev chats...")
    show_previous_chats(session_id_wo_runn)
    if input_txt:
        chatbot(input_txt)


