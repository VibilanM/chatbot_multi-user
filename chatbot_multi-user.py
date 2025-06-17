from openai import OpenAI
import os
#from dotenv import load_dotenv
import streamlit as st
import sys
import requests
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=5000, limit=None, key="chatrefresh")

#load_dotenv() #loading env file

character_deepseek = "You are a funny AI assistant that is supposed to interact with multiple users and AIs. The name before the colon at the starting of each message is the username. Keep track of the usernames and respond to whichever user has asked you the question, while also analysing all users' opinions on the subject. Remember, Gemini is your rival AI model. You are always competing with it."
character_gemini = "You are a funny AI assistant that is supposed to interact with multiple users and AIs. The name before the colon at the starting of each message is the username. Keep track of the usernames and respond to whichever user has asked you the question, while also analysing all users' opinions on the subject. Remember, Deepseek is your rival AI model. You are always competing with it."
character_qwen = "You are a funny AI assistant that is supposed to interact with multiple users and AIs. The name before the colon at the starting of each message is the username. Keep track of the usernames and respond to whichever user has asked you the question, while also analysing all users' opinions on the subject. Remember, Gemini is your rival AI model, while you're friends with the Deepseek AI model. So you're always biased towards Deepseek but competing with Gemini for fun."

#OpenAI init
openai_key = st.secrets["OPENAI_API_KEY"]
headers_openai = {
    "Authorization": f"Bearer {openai_key}",
    "Content-Type": "application/json"}

#Supabase init
supabase_url = "https://lnvhxrbompjbmfdekbha.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxudmh4cmJvbXBqYm1mZGVrYmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDkzNzI4MTksImV4cCI6MjA2NDk0ODgxOX0.AHxed6baGIfcK3JWaOH0Aa2-bPULn_LseuVQ_fS2hMs"

headers_supabase = {
    "apikey": supabase_key,
    "Authorization": f"Bearer {supabase_key}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

st.title("Hi. How can I help you?")

if "username" not in st.session_state:
    st.session_state.username = ""

if st.session_state.username == "":
    st.session_state.username = st.text_input("USERNAME:")

username = st.session_state.username

history = requests.get(f"{supabase_url}/rest/v1/chat_history?select=*&order=timestamp.asc", headers = headers_supabase).json()
for i in history:
    with st.chat_message(i["role"]):
        load_history = i["username"] + ": " + i["content"]
        st.markdown(load_history)

if username:
    user_input = st.chat_input("Ask anything.")

    if user_input:
        requests.post(f"{supabase_url}/rest/v1/chat_history", headers = headers_supabase, json = {
            "username": username,
            "role": "user",
            "content": user_input})

        with st.chat_message("user"):
            load_user = f"{username}: {user_input}"
            st.markdown(load_user)

        if "@deepseek" in user_input.lower():
            messages = [{"role": "system", "content": character_deepseek}]
            for msg in history:
                load_append_1 = msg["username"] + ": " + msg["content"]
                messages.append({"role": msg["role"], "content": load_append_1})

            deepseek_response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers = headers_openai, json = {
                "model": "deepseek/deepseek-chat-v3-0324:free",
                "messages": messages}).json()["choices"][0]["message"]["content"]

            requests.post(f"{supabase_url}/rest/v1/chat_history", headers = headers_supabase, json = {
                "username": "Deepseek",
                "role": "assistant",
                "content": deepseek_response})

            with st.chat_message("assistant"):
                load_ai = f"Deepseek: {deepseek_response}"
                st.markdown(load_ai)

        if "@gemini" in user_input.lower():
            messages = [{"role": "system", "content": character_gemini}]
            for msg in history:
                load_append_2 = msg["username"] + ": " + msg["content"]
                messages.append({"role": msg["role"], "content": load_append_2})

            gemini_response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers = headers_openai, json = {
                "model": "google/gemini-2.0-flash-exp:free",
                "messages": messages}).json()["choices"][0]["message"]["content"]

            requests.post(f"{supabase_url}/rest/v1/chat_history", headers = headers_supabase, json = {
                "username": "Gemini",
                "role": "assistant",
                "content": gemini_response})

            with st.chat_message("assistant"):
                load_ai = f"Gemini: {gemini_response}"
                st.markdown(load_ai)

        if "@qwen" in user_input.lower():
            messages = [{"role": "system", "content": character_qwen}]
            for msg in history:
                load_append_3 = msg["username"] + ": " + msg["content"]
                messages.append({"role": msg["role"], "content": load_append_3})

            qwen_response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers = headers_openai, json = {
                "model": "qwen/qwen3-14b:free",
                "messages": messages}).json()["choices"][0]["message"]["content"]

            requests.post(f"{supabase_url}/rest/v1/chat_history", headers = headers_supabase, json = {
                "username": "Qwen",
                "role": "assistant",
                "content": qwen_response})

            with st.chat_message("assistant"):
                load_ai = f"Qwen: {qwen_response}"
                st.markdown(load_ai)
