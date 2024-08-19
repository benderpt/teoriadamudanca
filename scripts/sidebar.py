# scripts/components.py
import streamlit as st
import os

def configure_sidebar():
    """Configura a sidebar do Streamlit."""
    logo_path = "content/Assets/logos/logo.png"
    icon_path = "content/Assets/logos/logo.png"
    
    # Verifica se os arquivos existem
    if os.path.exists(logo_path) and os.path.exists(icon_path):
        st.logo(logo_path, icon_image=icon_path)
    else:
        st.error("Logotipo ou ícone não encontrados.")

    st.sidebar.title("Microlearning Teoria da mudança")
    st.sidebar.divider()
    st.sidebar.subheader("Objetivos 🎯")
    st.sidebar.markdown("""Compreender a metodologia da teoria da mudança nas seguintes dimensões: \n
    - O que é
    - Para que serve
    - A quem pode servir
    - Em que fases pode ser útil
    """)
    st.sidebar.divider()

    # Botão 1: Ver guia de avaliabilidade
    st.sidebar.link_button(
        label="📘 Ver guia de avaliabilidade",
        url="https://planapp.gov.pt/wp-content/uploads/2023/09/PlanAPP_2023_GuiaTdM.pdf",
        type="primary",
        help="Clique para abrir o guia de avaliabilidade",
        use_container_width=True
    )

    # Botão 2: Acompanhe o PlanAPP
    st.sidebar.link_button(
        label="🫶 Acompanhe o PlanAPP",
        url="https://linktr.ee/planapp",
        type="primary",
        help="Acompanhar o PlanAPP nas redes que prefere",
        use_container_width=True
    )

    st.sidebar.divider()
    # Botão para reiniciar
    if st.sidebar.button("Voltar ao início"):
        st.session_state.current_section = 0
        st.rerun()

