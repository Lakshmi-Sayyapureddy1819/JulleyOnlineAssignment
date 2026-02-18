
import os
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Get Backend URL from environment or default to localhost
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Drone Intel Dashboard", layout="wide")
st.title("Drone Intelligence System - India")

tab1, tab2, tab3 = st.tabs(["AI Chatbot", "Analytics & Calculators", "Compliance & Finder"])

with tab1:
    st.header("Chat with the Assistant")
    user_msg = st.chat_input("Ask about Drone Rules 2021 or ROI...")
    if user_msg:
        try:
            response = requests.post(f"{BACKEND_URL}/chat", json={"prompt": user_msg})
            if response.status_code == 200:
                res = response.json()
                with st.chat_message("assistant"):
                    st.write(res.get('answer', "No answer received."))
                    st.caption(f"Sources: {res.get('sources', [])}")
            else:
                st.error(f"Error {response.status_code}: {response.text}")
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
                response = requests.get(f"{BACKEND_URL}/calculate/roi?inv={inv}&rev={rev}")
                if response.status_code == 200:
                    st.json(response.json())
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
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
        # --- Header and Toggle ---
        st.header("⚖️ Regulation Checker")
        debug_mode = st.toggle("Enable Debug Mode", value=False)

        with st.container(border=True):
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                w = st.number_input("Drone Weight (kg)", min_value=0.0, value=1.5, step=0.1)
            with col_b:
                z = st.selectbox("Airspace Zone", ["Green", "Yellow", "Red"])
            with col_c:
                alt = st.slider("Altitude (ft)", 0, 1000, 100)

        if st.button("Check Compliance"):
            try:
                # 1. Make the request
                req_params = {"weight_kg": w, "zone": z, "altitude_ft": alt}
                response = requests.get(f"{BACKEND_URL}/tools/regulation-check", params=req_params)
                
                # Store debug info
                st.session_state['debug_url'] = response.url
                try:
                    st.session_state['debug_json'] = response.json()
                except:
                    st.session_state['debug_json'] = {"error": "Could not parse JSON"}
                
                if response.status_code == 200:
                    st.session_state['compliance_result'] = response.json()
                    
                    # Fetch PDF for download button
                    res = response.json()
                    pdf_params = {
                        "weight": w, "zone": z, "alt": alt, 
                        "category": res.get('drone_category', 'Unknown Category'), 
                        "status": res.get('flight_status', 'Unknown Status')
                    }
                    pdf_response = requests.get(f"{BACKEND_URL}/tools/download-report", params=pdf_params)

                    if pdf_response.status_code == 200:
                        st.session_state['compliance_pdf'] = pdf_response.content
                    else:
                        st.session_state['compliance_pdf'] = None
                        st.error("Could not generate PDF. Check backend logs.")

                else:
                    st.error(f"Backend Error: {response.status_code}. Make sure api/main.py is running.")
            except requests.exceptions.ConnectionError:
                st.error("API connection failed. Is the backend running?")

        # Display results from session state
        if debug_mode and 'debug_json' in st.session_state:
            st.write("---")
            st.write(f"**Requesting:** `{st.session_state.get('debug_url', '')}`")
            st.write("**Raw Backend Response:**")
            st.json(st.session_state['debug_json'])
            st.write("---")

        if 'compliance_result' in st.session_state:
            res = st.session_state['compliance_result']
            
            # Use .get() to provide a fallback and avoid KeyError
            flight_status = res.get('flight_status', 'Unknown Status')
            category = res.get('drone_category', 'Unknown Category')
            remarks = res.get('remarks', [])

            st.subheader(f"Status: {flight_status}")
            st.info(f"Category: **{category}**")
            for r in remarks:
                st.warning(r)
            
            if 'compliance_pdf' in st.session_state and st.session_state['compliance_pdf']:
                st.download_button(
                    label="📥 Download PDF Report",
                    data=st.session_state['compliance_pdf'],
                    file_name="Drone_Report.pdf",
                    mime="application/pdf"
                )

    with col2:
        st.subheader("Drone Finder")
        category = st.selectbox("Category", ["All", "Nano", "Micro", "Small", "Medium", "Large"])
        budget = st.slider("Budget (INR)", 100000, 2000000, 500000)
        endurance = st.slider("Min Endurance (mins)", 10, 120, 30)
        if st.button("Find Drones"):
            params = {}
            if category != "All":
                params["category"] = category
            params["budget"] = budget
            params["endurance"] = endurance
            
            # Ensure this URL matches your FastAPI address
            response = requests.get(f"{BACKEND_URL}/tools/find-drones", params=params)
            
            if response.status_code == 200:
                drones = response.json()
                if isinstance(drones, list) and len(drones) > 0:
                    st.write(f"Found {len(drones)} drones:")
                    st.table(drones) # Displays the data in a clean table
                else:
                    st.warning("No drones found in the database.")
            else:
                st.error("Failed to connect to the drone database.")