# frontend/pages/analytics.py
import streamlit as st
from frontend.utils.api_client import get
import streamlit.components.v1 as components

def show():
    st.title("📈 Analytique")
    st.markdown("Indicateurs clés de performance, budget et équipe.")

    # Project selection
    project_id = st.number_input(
        "Sélectionnez le projet ID",
        min_value=1,
        value=1
    )

    # Fetch project KPIs from backend
    kpis = get(f"/analytics/project/{project_id}")
    if kpis:
        st.subheader(f"KPIs pour le projet: {kpis.get('project_name', 'N/A')}")
        st.write(f"- Progression moyenne: {kpis.get('average_progress', 0):.1f}%")
        st.write(f"- Budget total: ${kpis.get('budget_total', 0):,.2f}")
        st.write(f"- Budget dépensé: ${kpis.get('budget_spent', 0):,.2f}")
        st.write(f"- Marge actuelle: {kpis.get('current_margin', 0)}%")
    else:
        st.warning("Aucune donnée analytique trouvée pour ce projet.")

    # Fetch team performance
    team_perf = get("/analytics/team-performance")
    if team_perf:
        st.subheader("Performance de l'équipe")
        for member in team_perf:
            st.write(f"- {member['name']}: {member.get('performance', 0)}%")

    # Optional: Embed UserPanel TS component (if still needed)
    user_panel = components.declare_component(
        "user_panel",
        path="frontend/components/UserPanel/build"
    )
    user_panel(projectId=project_id)
