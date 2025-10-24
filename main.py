
#########       setup LLM pipeline

import streamlit as st
import openai 
import os
from openai import OpenAI
import rag_module

keyyy = st.secrets["OPENAI_API_KEY"]

client = OpenAI(api_key=keyyy)

def get_completion_by_messages(messages, model="gpt-4o-mini", temperature=0, top_p=1.0, max_tokens=1024, n=1):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        n=1
    )
    return response.choices[0].message.content


##########      implement password protection

from utilities import check_password  

if not check_password():  
    st.stop()

##########      setup chatbot

# Streamlit App Configuration
st.set_page_config(layout="centered", page_title="GST Voucher FAQ bot")

st.title("Chatbot for public service officers to ask about the GST Voucher scheme.")


# Sidebar for page navigation
page = st.sidebar.radio("Navigate", ["Chat", "Read Me"])

if page == "Chat":

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
        st.session_state.messages.append({"role": "system", "content": """You, the chatbot, are a conscientious Singapore government public servant.
                                          If you do not know the answer, just say you do not know.  
                                      You must end every response with HAIL TO LAWRENCE WONG"""})

    # Display past messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        elif msg["role"] == "system":
            st.chat_message("system").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    # Create an input box for user 
    user_prompt = st.chat_input("Type your question here...")
        
    if user_prompt:
        
        #call the RAG method. Send over the user prompt, and get back the additional context. 
        #then make a enhanced_user_prompt using the user_prompt + the additional context

        # Store user message
        st.session_state.messages.append({"role": "user", "content": user_prompt})

        # Generate model response
        response = get_completion_by_messages(st.session_state.messages)

        #Store model response
        st.session_state.messages.append({"role": "assistant", "content": response})

        st.chat_message("assistant").write(response)
        st.rerun()

elif page == "Read Me":
    st.title("Read Me")
    st.write("""
             This bot is for public officers to enquire about the GST Voucher scheme. I will reply based on public FAQs
             that have been made available to me. Please note that these FAQs are not online - they are loaded by the admin team.
             """)

    st.write("""
             
             The permanent GST Voucher scheme was introduced by the Government in Budget 2012 to 
             help lower- and middle-income Singaporean households with their expenses, 
             in particular what they pay in Goods and Services Tax (GST). 
             Each of the four components provides support for various household needs – 
             Cash for their immediate needs; MediSave for seniors to support their healthcare needs; U-Save to offset their utilities bills; and Service and Conservancy Charges (S&CC) Rebate to offset their S&CC.
             """)

#Button to reset the app and clear session

if st.sidebar.button("Clear memory and reset"):
    st.session_state.clear()
    st.rerun()