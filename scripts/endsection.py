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
    st.link_button(
        label="📘 Ver guia da Teoria da Mudança",
        url="https://planapp.gov.pt/wp-content/uploads/2023/09/PlanAPP_2023_GuiaTdM.pdf",
        type="primary",
        help="Clique para abrir o guia Teoria da Mudança",
        use_container_width=True
    )

    # Botão 2: Acompanhe o PlanAPP
    st.link_button(
        label="🫶 Acompanhe o PlanAPP",
        url="https://linktr.ee/planapp",
        type="primary",
        help="Acompanhar o PlanAPP nas redes que prefere",
        use_container_width=True
    )
    st.divider()

    # Restart button
    if st.button("Reiniciar", key="end_restart"):
        st.session_state.current_section = 0
        st.rerun()
