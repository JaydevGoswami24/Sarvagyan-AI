import streamlit as st
import os
import requests

# Set page config
st.set_page_config(page_title="Sarvagyan AI", layout="centered")

st.markdown("## 🤖 Welcome to Sarvagyan AI")
st.markdown("Ask anything, select response level:")

# Mode selection (Beginner, Professional, Expert)
mode = st.selectbox("Select Mode", ["Beginner", "Professional", "Expert"])

# Prompt input
prompt = st.text_area("📝 Your Question", placeholder="e.g. What is the capital of India?")

# Call Together API (Qwen model)
def get_qwen_reply(prompt, mode):
    api_url = "https://api.together.xyz/v1/chat/completions"
    api_key = os.getenv("TOGETHER_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_prompt = f"Answer as a {mode} in a structured and professional manner."

    data = {
        "model": "Qwen1.5-14B-Chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Error: {response.status_code} - {response.text}"

# Submit button
if st.button("🔍 Get Answer"):
    if not prompt.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            reply = get_qwen_reply(prompt, mode)
            st.markdown("### 💬 Sarvagyan AI Says:")
            st.write(reply)
