# frontend/pages/analytics.py
# frontend/pages/analytics.py
import streamlit as st
import streamlit.components.v1 as components

def show():
    st.title("📈 Analytique")
    st.markdown("Indicateurs clés de performance, budget et équipe.")

    # Embed UserPanel TS component
    user_panel = components.declare_component(
        "user_panel",
        path="frontend/components/UserPanel/build"
    )
    user_panel()