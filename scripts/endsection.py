import streamlit as st
from streamlit_lottie import st_lottie
import json

# Load Lottie animation
def load_lottie(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def render_end_section():

    # Display Lottie animation
    lottie_animation = load_lottie("content/Assets/endsection.json")
    st_lottie(lottie_animation, height=300)
    

    
    st.markdown(f"""
        <div style="text-align: center;">
            <h3> 🎓Parabéns! Concluiu a sessão de microlearning sobre a Teoria da Mudança. 🎓</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # Botão 1: Ver guia de avaliabilidade
    if st.button("📘 Ver guia de avaliabilidade", use_container_width=True, type="primary", help="Clique para abrir o guia de avaliabilidade"):
        st.markdown("[Abra o guia](https://planapp.gov.pt/wp-content/uploads/2023/09/PlanAPP_2023_GuiaTdM.pdf)")

    # Botão 2: Acompanhe o PlanAPP
    if st.button("🫶 Acompanhe o PlanAPP", use_container_width=True, type="primary", help="Acompanhar o PlanAPP nas redes que prefere"):
        st.markdown("[Siga o PlanAPP](https://linktr.ee/planapp)")
    
    st.markdown("---")

    # Restart button
    if st.button("Reiniciar", key="end_restart"):
        st.session_state.current_section = 0
        st.rerun()
