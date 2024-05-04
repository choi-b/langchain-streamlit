#Make sure to pip install the required dependencies

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

#Initialize our chat history variable
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] #initialize it as an empty array

st.set_page_config(page_title="Streaming Bot", page_icon="🤖")

st.title("Streaming Bot")

#Get response from the language model
def get_response(query, chat_history):
    template = """
        You are a helpful assistant. Answer the following questions considering the history of the conversation:

        Chat history: {chat_history}

        User question: {user_question}
        """
    #initialize our prompt from this template
    prompt = ChatPromptTemplate.from_template(template)

    #our language model from OpenAI
    llm = ChatOpenAI()

    #lastly, add a string output parser
    chain = prompt | llm | StrOutputParser
    
    #this will return a generator
    return chain.stream({
        "chat_history": chat_history,
        "user_question": query
    })
     


#Conversation
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)

#User Input - where the user adds an input (initialize the entire chat interface)
user_query = st.chat_input("Your message")
if user_query is not None and user_query !="":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        ai_response = st.write_stream(get_response(user_query, st.session_state.chat_history))
        #Running the generator inside the write_stream emthod
    st.session_state.chat_history.append(AIMessage(content=ai_response))
