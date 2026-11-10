import streamlit as st
import numpy as np
import os
import sys

# Add the src folder to the Python path so internal imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

import pandas as pd
from src.core.link import OpticalLinkSystem
from src.modules.optimizer import LinkOptimizer
from src.modules.fault_detection import FaultDetector
from src.ai.assistant import AIAssistant
from src.ml.modulation_classifier import ModulationClassifierML

st.set_page_config(page_title="Optical Comm Simulator", layout="wide")

st.sidebar.title("Optical Communication Simulator")
page = st.sidebar.radio("Navigation", [
    "Home",
    "End-to-End Link Designer",
    "Link Optimizer",
    "Machine Learning Classifier",
    "AI Assistant",
    "Documentation"
])

if page == "Home":
    st.title("Optical Communication End-to-End System Simulator")
    st.markdown("""
    Welcome to the Optical Communication Simulator! 
    This application simulates an end-to-end optical link including Laser transmission, Digital Modulation, Fiber propagation, EDFA amplification, and Receiver signal recovery.
    
    **Navigate using the sidebar to explore different modules.**
    """)

elif page == "End-to-End Link Designer":
    st.title("End-to-End Link Designer")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("Link Configuration")
        tx_power = st.slider("Tx Power (dBm)", -10.0, 20.0, 0.0)
        mod = st.selectbox("Modulation Format", ["OOK", "BPSK", "QPSK", "16-QAM"])
        length = st.number_input("Fiber Length (km)", 10.0, 200.0, 50.0)
        attenuation = st.number_input("Attenuation (dB/km)", 0.1, 0.5, 0.2)
        edfa_enabled = st.checkbox("Enable EDFA Amplifier")
        edfa_gain = st.slider("EDFA Small Signal Gain (dB)", 10.0, 30.0, 20.0) if edfa_enabled else 20.0
        
        simulate_btn = st.button("Simulate Link", type="primary")

    with col2:
        st.header("Simulation Results")
        if simulate_btn:
            config = {
                "tx_power_dbm": tx_power,
                "modulation": mod,
                "fiber_length_km": length,
                "attenuation_db_km": attenuation,
                "edfa_enabled": edfa_enabled,
                "edfa_gain_db": edfa_gain,
                "n_bits": 50000
            }
            
            sys = OpticalLinkSystem(config)
            results = sys.simulate()
            
            # Store in session state for AI Assistant
            st.session_state['latest_results'] = results
            st.session_state['latest_config'] = config
            
            if results["link_status"] == "PASS":
                st.success(f"Link Status: {results['link_status']}")
            else:
                st.error(f"Link Status: {results['link_status']}")
                
            metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
            metrics_col1.metric("Received Power", f"{results['rx_power_dbm']:.2f} dBm")
            metrics_col2.metric("Link Margin", f"{results['link_margin_db']:.2f} dB")
            metrics_col3.metric("Bit Error Rate (BER)", f"{results['ber']:.2e}")
            
            st.subheader("Fault Diagnostics")
            faults = FaultDetector.diagnose(results, config)
            if not faults:
                st.info("No critical faults detected.")
            else:
                for f in faults:
                    st.warning(f"**{f['fault']} ({f['severity']})**: {f['action']}")

elif page == "Link Optimizer":
    st.title("Link Optimizer")
    st.write("Find the optimal (lowest power/cost) configuration that passes the BER threshold.")
    if st.button("Run Optimization"):
        with st.spinner("Searching configuration space..."):
            best = LinkOptimizer.optimize({"fiber_length_km": 50.0, "target_ber": 1e-3})
            if best["status"] == "SUCCESS":
                st.success("Optimal Configuration Found!")
                st.json(best["config"])
                st.write("Estimated BER:", best["results"]["ber"])
            else:
                st.error("Optimization failed. No feasible configuration.")

elif page == "Machine Learning Classifier":
    st.title("ML Modulation Classifier")
    st.write("Demonstration of a Random Forest classifying noisy modulation schemes.")
    if st.button("Train & Evaluate Model"):
        with st.spinner("Generating synthetic data and training Random Forest..."):
            ml = ModulationClassifierML()
            metrics = ml.train_and_evaluate()
            st.success("Model Trained Successfully!")
            st.metric("Test Accuracy", f"{metrics['accuracy']*100:.2f} %")

elif page == "AI Assistant":
    st.title("Gemini Optical Communication Assistant")
    st.write("Ask the AI to explain the physics and results of your latest simulation.")
    
    api_key = st.text_input("Enter Gemini API Key (or leave blank if set in environment)", type="password")
    user_q = st.text_input("Ask a question (e.g., 'Why is my BER high?'):")
    
    if st.button("Ask Assistant"):
        results = st.session_state.get('latest_results', "No simulation run yet.")
        config = st.session_state.get('latest_config', "")
        
        # Set API key for this run if provided
        if api_key: os.environ["GEMINI_API_KEY"] = api_key
        
        assistant = AIAssistant()
        with st.spinner("Analyzing results..."):
            explanation = assistant.explain({"config": config, "results": results}, user_q)
            st.markdown(explanation)

elif page == "Documentation":
    st.title("Documentation")
    st.markdown("""
    ### Assumptions & Limitations
    * **Laser:** Simplified rate equations using linear gain.
    * **Fiber:** Chromatic dispersion is modelled as linear pulse broadening.
    * **Receiver:** Assumes perfect phase synchronization for coherent formats (BPSK, QPSK, 16-QAM).
    * **AI:** The AI serves purely as an explainer and does not perform the physics calculations.
    """)
