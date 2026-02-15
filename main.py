import streamlit as st
import requests

st.set_page_config(page_title="Drone Intelligence System", layout="wide")

st.title("🚁 Drone Intelligence System for India")

query = st.text_input("Ask about Drone Rules, Specs, or Calculations:")

if st.button("Submit"):
    if query:
        # Connect to FastAPI backend
        # response = requests.post("http://api:8000/chat", json={"query": query})
        # st.write(response.json())
        st.info(f"Backend processing: {query}")