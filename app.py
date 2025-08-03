import streamlit as st
import requests
import os

st.set_page_config(page_title="Sarvagyan AI", layout="centered")

st.markdown("## 🤖 Sarvagyan AI – Powered by Mixtral via Groq")
st.markdown("Structured professional assistant with Beginner / Professional / Expert response levels.")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

level = st.radio("Select Response Mode", ["Beginner", "Professional", "Expert"], horizontal=True)
question = st.text_input("Ask your question:", placeholder="e.g. What is the capital of India?")

if st.button("Ask Sarvagyan") and question:
    if not GROQ_API_KEY:
        st.error("GROQ_API_KEY not set. Please add it in Render environment variables.")
    else:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "mixtral-8x7b-32768",
            "messages": [
                {
                    "role": "system",
                    "content": f"You are Sarvagyan AI, a highly professional chatbot that gives structured responses in {level} style using Indian context wherever possible.",
                },
                {
                    "role": "user",
                    "content": question,
                },
            ],
        }
        try:
            res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
            res.raise_for_status()
            reply = res.json()["choices"][0]["message"]["content"]
            st.markdown("### 📘 Answer")
            st.write(reply)
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")