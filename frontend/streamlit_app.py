import streamlit as st
import requests

st.set_page_config(page_title="ODM Assistant", layout="centered")
st.title("🤖 OpenDroneMap AI Assistant")

question = st.text_input("Ask a question about OpenDroneMap")

if st.button("Submit") and question:
    with st.spinner("Thinking..."):
        response = requests.post("http://127.0.0.1:8000/ask", json={"question": question})
        if response.status_code == 200:
            data = response.json()
            st.success(data["answer"])
            st.markdown("#### 🔍 Sources")
            for src in data["sources"]:
                st.code(src)
        else:
            st.error("Failed to get response from backend.")
