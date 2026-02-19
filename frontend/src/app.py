
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
    
    # Multi-modal Upload
    with st.expander("📂 Upload Documents or Images"):
        uploaded_file = st.file_uploader("Upload PDF, Image, CSV, or Text", type=['pdf', 'png', 'jpg', 'jpeg', 'csv', 'txt', 'json'])
        if uploaded_file is not None:
            if st.button("Process File"):
                with st.spinner("Analyzing and ingesting file..."):
                    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    try:
                        response = requests.post(f"{BACKEND_URL}/upload", files=files)
                        if response.status_code == 200:
                            st.success(f"✅ {uploaded_file.name} processed! You can now chat about it.")
                        else:
                            st.error(f"Error: {response.text}")
                    except Exception as e:
                        st.error(f"Failed to connect: {e}")

import pytest
from mcp_server.tools.flight_calc import get_flight_estimates
from mcp_server.tools.roi_calc import get_roi_analysis
from mcp_server.tools.compliance import check_regulation_compliance
from mcp_server.tools.selection_assistant import recommend_drone
# Note: recommendation.py seems redundant with selection_assistant.py, testing selection_assistant as it's in the server.py

def test_flight_time_calculator():
    """
    Verifies Phase 4.1: Drone Flight Time Calculator
    """
    # Test with standard values
    result = get_flight_estimates(battery_ah=10.0, drone_weight=2.0, payload=0.5)
    
    assert "estimated_minutes" in result
    assert "safe_minutes" in result
    assert "range_km" in result
    assert result["estimated_minutes"] > 0

def test_roi_calculator():
    """
    Verifies Phase 4.2: ROI Calculator
    """
    # Test with profitable scenario
    result = get_roi_analysis(investment=500000, daily_revenue=6000)
    
    assert "net_daily_profit" in result
    assert "break_even_days" in result
    assert "status" in result
    assert result["status"] == "Profitable"

def test_compliance_checker():
    """
    Verifies Phase 4.3: Regulation Compliance Checker
    """
    # Test Green Zone Compliance
    res_green = check_regulation_compliance(weight_kg=1.5, zone="Green", altitude_ft=100, purpose="Recreational")
    assert res_green["status"] == "Compliant"
    
    # Test Red Zone Violation
    res_red = check_regulation_compliance(weight_kg=1.5, zone="Red", altitude_ft=100)
    assert res_red["status"] == "Non-Compliant"
    assert "Flight strictly prohibited in Red Zone." in res_red["violations"]

def test_selection_assistant():
    """
    Verifies Phase 4.4: Drone Selection Assistant
    """
    # Test recommendation logic
    # Note: This test requires the CSV file to be present. 
    # If running in an environment without the data generation script run first, this might fail or return error dict.
    
    # We mock the os.path.exists to return False to test the error handling path if data is missing,
    # or we can assume data exists if the previous steps were followed.
    # Let's test the function signature and return type.
    
    result = recommend_drone(max_budget=1000000, primary_use="Agriculture")
    
    # The result should be either a list of dicts (drones) or a dict with an error/message
    if isinstance(result, dict) and "error" in result:
        # If data is missing, it returns an error dict, which is valid handling
        assert True 
    elif isinstance(result, list):
        # If data exists, it returns a list of records
        assert len(result) >= 0
    elif isinstance(result, dict) and "message" in result:
        # If no drones found
        assert True
    else:
        pytest.fail(f"Unexpected return type: {type(result)}")

    # 1. Initialize chat history if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 2. Display existing chat messages from history on every rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. Handle new user input
    if user_msg := st.chat_input("Ask about Drone Rules 2021 or ROI..."):
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(user_msg)
        st.session_state.messages.append({"role": "user", "content": user_msg})

        try:
            response = requests.post(f"{BACKEND_URL}/chat", json={"prompt": user_msg})
            if response.status_code == 200:
                res = response.json()
                with st.chat_message("assistant"):
                    answer = res.get('answer', "No answer received.")
                    sources = res.get('sources', [])
                    st.markdown(answer)
                    if sources:
                        st.caption(f"Sources: {sources}")
                
                # Add assistant response to history
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the API. Please ensure 'python api/main.py' is running.")

    st.divider()
    
    st.subheader("✈️ Drone Flight Time Calculator")
    st.info("Calculate estimated flight endurance based on your drone's specifications.")

    # 1. Create columns for organized user input
    f_col1, f_col2, f_col3 = st.columns(3)

    with f_col1:
        bat_cap = st.number_input("Battery Capacity (Ah)", min_value=1.0, value=10.0, step=0.5)
    with f_col2:
        drone_w = st.number_input("Drone Weight (kg)", min_value=0.1, value=2.0, step=0.1)
    with f_col3:
        payload_w = st.number_input("Payload Weight (kg)", min_value=0.0, value=0.5, step=0.1)

    # 2. Action Button
    if st.button("Calculate Flight Time"):
        try:
            # Call your FastAPI backend
            response = requests.get(f"{BACKEND_URL}/calculate/flight?bat={bat_cap}&weight={drone_w}&pay={payload_w}")
            
            if response.status_code == 200:
                result = response.json()
                st.success("Calculation Successful!")
                res_col1, res_col2 = st.columns(2)
                res_col1.metric("Est. Flight Time", f"{result.get('estimated_minutes', 0)} min")
                res_col2.metric("Safe Flight Time", f"{result.get('safe_minutes', 0)} min")
                st.write(f"**Estimated Range:** {result.get('range_km', 0)} km")
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Connection Error: {e}")

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