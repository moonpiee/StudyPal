import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory,InMemoryChatMessageHistory
import json, toml

session_id_runn="runn_chat_history1"
session_id_wo_runn="wo_runn_chat_history1"
st.title("Study Pal🌱📚💪")
st.header("Tutor Me📚👨‍🏫")
cols= st.columns(4)
with cols[3]:
    adv_opt=st.toggle("More Options")
    if adv_opt:
     sel_temp = st.slider("Temperature",0.0,1.0,0.0)
     st.session_state["sel_temp"]=sel_temp
     st.session_state["groq_api_key"]=st.text_input("Your Groq API Key",type="password")
     
languages=["Select a Language","English","Telugu","Hindi","Malayalam","Marathi","Bengali","Kannada"]
instructions_lis=["Tutor Me","Teacher Pal","Translate","Learn Language","Communicate","Surprise Me","Tell Me Why","Tongue Twister","Humor Me","Story Time", "More Fun Games","Inspire Me"]
instruction = instructions_lis[0]
def get_default_models():
    if 'models_data' not in st.secrets:
        st.error("You need to set the default models in the secrets.")
        st.stop()
    config = toml.load('.streamlit/secrets.toml')
    # Parse the JSON string
    models_data = json.loads(config['models_data'])
    select_map={}
    # models_data=st.secrets["models_data"]
    for model in models_data["data"]:
         model_name=f"{model["id"]} (Owned by {model["owned_by"]})"
         select_map[model_name]=model["id"]
    default_llm=models_data["data"][11]["id"] #can be customised
    return select_map,default_llm
if "sel_temp" not in st.session_state:
    st.session_state["sel_temp"]=0
if "groq_api_key" not in st.session_state:
    if "GROQ_API_KEY" in st.secrets:
        st.session_state["groq_api_key"]=st.secrets["GROQ_API_KEY"]
# default_llm=models_data["data"][11]["id"] #can be customised
select_map,default_llm=get_default_models()
llms_map={'Select an LLM':None}
llms_map.update(select_map)
sel_language = st.selectbox(label="Your Language?",options=languages,index=languages.index(st.session_state["sel_language"]) if "sel_language" in st.session_state else 0)
st.session_state["sel_language"]=sel_language
# print(llms_map)
if st.session_state["sel_language"] != "Your Language?":
     sel_language=st.session_state["sel_language"]
     if 'sel_model' not in st.session_state.keys():
        sel_model = st.selectbox("Select a Model", llms_map.keys())
        if sel_model and llms_map[sel_model] is not None:
            if "sel_model" in st.session_state.keys():
                st.session_state["sel_model"]=None
            st.session_state["sel_model"]=llms_map[sel_model]  
if "sel_model" in st.session_state.keys():
     cur_llm=st.session_state["sel_model"]
     st.caption(f"You are using {instruction} on {cur_llm}")
     chat_groq=ChatGroq(
     api_key=st.session_state["groq_api_key"],
     model=cur_llm,
     temperature=st.session_state["sel_temp"]
     )
else:
     chat_groq=ChatGroq(
     api_key=st.session_state["groq_api_key"],
     model=default_llm,
     temperature=st.session_state["sel_temp"]
     )
# print("clinet: ",chat_groq)
sel_language=st.session_state["sel_language"]

cur_llm=st.session_state["sel_model"] if "sel_model" in st.session_state else default_llm
# print("chosen llm, language",cur_llm,sel_language)

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
                {"input":"What can you do? Briefly list out in simple format","instruction_desc":instruction_desc,"sel_language":sel_language}, #How can I utilise you? Briefly list out
                config={"configurable": {"session_id": session_id_runn}}
            )
            st.session_state[session_id_wo_runn]=[{"role":"assistant", "content":initial_msg.content}] #no need to add this in history

input_txt=st.chat_input("Input text")
if session_id_runn in st.session_state and session_id_wo_runn in st.session_state:
    # print("showing prev chats...")
    show_previous_chats(session_id_wo_runn)
    if input_txt:
        chatbot(input_txt)


