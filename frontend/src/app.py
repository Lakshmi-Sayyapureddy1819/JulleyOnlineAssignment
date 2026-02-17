import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Drone Intel Dashboard", layout="wide")
st.title("Drone Intelligence System - India")

tab1, tab2, tab3 = st.tabs(["AI Chatbot", "Analytics & Calculators", "Compliance & Finder"])

with tab1:
    st.header("Chat with the Assistant")
    user_msg = st.chat_input("Ask about Drone Rules 2021 or ROI...")
    if user_msg:
        try:
            res = requests.post("http://localhost:8000/chat", json={"prompt": user_msg}).json()
            with st.chat_message("assistant"):
                st.write(res['answer'])
                st.caption(f"Sources: {res['sources']}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the API. Please ensure 'python api/main.py' is running.")

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("ROI Tool")
        inv = st.number_input("Investment", value=600000)
        rev = st.number_input("Daily Revenue", value=5000)
        if st.button("Analyze ROI"):
            try:
                data = requests.get(f"http://localhost:8000/calculate/roi?inv={inv}&rev={rev}").json()
                st.json(data)
            except requests.exceptions.ConnectionError:
                st.error("API connection failed. Is the backend running?")
    with col2:
        st.subheader("Synthetic Flight Data View")
        df = pd.read_csv("data/synthetic/flight_logs.csv")
        fig = px.scatter(df, x="altitude_ft", y="battery_drain_%", color="zone")
        st.plotly_chart(fig)

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Regulation Checker")
        weight = st.number_input("Drone Weight (kg)", 0.1, 150.0, 1.5)
        zone = st.selectbox("Airspace Zone", ["Green", "Yellow", "Red"])
        alt = st.number_input("Altitude (ft)", 0, 1000, 100)
        if st.button("Check Compliance"):
            try:
                res = requests.get(f"http://localhost:8000/check/compliance?weight={weight}&zone={zone}&alt={alt}").json()
                st.write(f"**Status:** {res['status']}")
                if res['violations']: st.error(f"Violations: {res['violations']}")
                if res['required_permits']: st.info(f"Permits: {res['required_permits']}")
            except requests.exceptions.ConnectionError:
                st.error("API connection failed. Is the backend running?")

    with col2:
        st.subheader("Drone Finder")
        budget = st.slider("Budget (INR)", 100000, 2000000, 500000)
        endurance = st.slider("Min Endurance (mins)", 10, 120, 30)
        if st.button("Find Drones"):
            try:
                res = requests.get(f"http://localhost:8000/recommend/drone?budget={budget}&endurance={endurance}").json()
                if "models" in res:
                    st.dataframe(res['models'])
                else:
                    st.write(res)
            except requests.exceptions.ConnectionError:
                st.error("API connection failed. Is the backend running?")