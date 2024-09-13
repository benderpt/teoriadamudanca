import streamlit as st
import os
import sys
import json
from streamlit_lottie import st_lottie


def render_single_choice_question(section):
    """
    Renderiza uma pergunta de escolha única e lida com as respostas dos usuários.
    
    Esta função exibe uma pergunta de escolha única, processa a entrada do usuário e fornece feedback.
    """
    st.write(section["question"])
    options = section.get("options", [])
    
    feedback_placeholder = st.empty()

    if not st.session_state.get("response_submitted", False):
        selected_option = st.radio("Selecione uma opção", options)

        if selected_option:
            if st.button(section.get("button_text", "Responder"), type="primary"):
                st.session_state.response_submitted = True
                st.session_state.selected_option = selected_option
                st.experimental_rerun()  # Força uma nova execução para atualizar o estado

    if st.session_state.get("response_submitted", False):
        selected_option = st.session_state.get("selected_option", "")
        explanation = section["explanations"].get(selected_option, "")
        correct = selected_option in section["answer"]
        
        if correct:
            feedback_placeholder.success(f"Escolha: **{selected_option}**\n\n**Correto**. {explanation}")
            st.toast("🎉 Parabéns, você acertou!", icon="🔥")
        else:
            feedback_placeholder.error(f"Escolha: **{selected_option}**\n\n**Incorreto**. {explanation}")


        # Adicionar colunas para botões
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(section.get("button_answer", "Continuar"), type="primary", use_container_width=True):
                st.session_state.current_section += 1
                st.session_state.response_submitted = False
                st.experimental_rerun()
        if not correct:
            with col2:
                if st.button("Tentar novamente", use_container_width=True):
                    st.session_state.response_submitted = False
                    st.experimental_rerun()  # Atualizar a página
        if st.session_state.current_section > 0:
            with col3:
                if st.button("Voltar atrás", use_container_width=True):
                    st.session_state.current_section -= 1
                    st.session_state.response_submitted = False
                    st.experimental_rerun()


def render_multiple_choice_question(section):
    """
    Renderiza uma pergunta de múltipla escolha e lida com as respostas dos usuários.
    
    Esta função exibe uma pergunta de múltipla escolha, processa a entrada do usuário e fornece feedback.
    """
    st.write(section["question_multiple"])
    options = section.get("options", [])
    
    feedback_placeholder = st.empty()

    if not st.session_state.get("response_submitted", False):
        selected_options = st.multiselect(
            "Selecione uma ou mais opções", options, placeholder="Selecione uma opção", key="multiselect"
        )

        if selected_options:
            if st.button(section.get("button_text", "Responder"), type="primary"):
                st.session_state.response_submitted = True
                st.session_state.selected_options = selected_options
                st.experimental_rerun()  # Força uma nova execução para atualizar o estado

    if st.session_state.get("response_submitted", False):
        selected_options = st.session_state.get("selected_options", [])
        correct_count = 0  # Contador de respostas corretas
        incorrect_count = 0  # Contador de respostas incorretas

        for option in selected_options:
            explanation = section["explanations"].get(option, "")
            if option in section["answer"]:
                st.success(f"**{option}**\n\n**Correto**. {explanation}")
                correct_count += 1  # Incrementar contador de respostas corretas
            else:
                st.error(f"**{option}**\n\n**Incorreto**. {explanation}")
                incorrect_count += 1  # Incrementar contador de respostas incorretas

        # Fornecer feedback geral
        all_correct = correct_count == len(section["answer"]) and incorrect_count == 0
        if all_correct:
            feedback_placeholder.success("Todas as respostas estão corretas!")
            st.toast("🎉 Parabéns, você acertou!", icon="🔥")
        elif correct_count > 0 and incorrect_count > 0:
            feedback_placeholder.warning("Algumas respostas estão corretas, mas também há respostas incorretas.")
        elif correct_count == 1 and incorrect_count == 0:
            feedback_placeholder.warning("Resposta correta, mas ainda incompleta.")
        elif correct_count > 1 and correct_count < len(section["answer"]) and incorrect_count == 0:
            feedback_placeholder.warning("Respostas corretas, mas incompletas.")
        else:
            feedback_placeholder.error("Há respostas incorretas.")
        
        # Adicionar colunas para botões
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(section.get("button_answer", "Continuar"), type="primary", use_container_width=True):
                st.session_state.current_section += 1
                st.session_state.response_submitted = False
                st.experimental_rerun()
        if not all_correct:
            with col2:
                if st.button("Tentar novamente", use_container_width=True):
                    st.session_state.response_submitted = False
                    st.experimental_rerun()  # Atualizar a página
        if st.session_state.current_section > 0:
            with col3:
                if st.button("Voltar atrás", use_container_width=True):
                    st.session_state.current_section -= 1
                    st.session_state.response_submitted = False
                    st.experimental_rerun()


def render_question_content(section):
    """
    Renderiza uma seção de perguntas e lida com as respostas dos usuários com base no tipo de pergunta.

    Esta função delega a renderização e o tratamento de respostas para a função de pergunta de escolha única ou múltipla apropriada com base no conteúdo da seção.
    """
    if "question_multiple" in section:
        render_multiple_choice_question(section)
    elif "question" in section:
        render_single_choice_question(section)

def render_static_content(section):
    """
    Renderiza conteúdo estático, incluindo título, imagem e texto.

    Esta função exibe um título, uma imagem se existir e texto formatado da seção fornecida.
    """
    if "title" in section:
        st.markdown(f"<h3 style='text-align: center;'>{section['title']}</h3>", unsafe_allow_html=True)
    if "image_path" in section and os.path.exists(section["image_path"]):
        st.image(section["image_path"])
    if "lottie" in section and os.path.exists(section["lottie"]):
        with open(section["lottie"], 'r') as f:
            lottie_animation = json.load(f)
        st_lottie(lottie_animation)
    st.divider()
    if "text" in section:
        st.markdown(section["text"].replace("\n", "  \n"))

def render_script_content(section):
    """
    Executa um script se estiver presente na seção.

    Esta função importa dinamicamente e executa um script Python especificado na seção.
    """
    if "script_path" in section:
        script_path = section["script_path"]
        script_dir, script_name = os.path.split(script_path)
        script_module_name = script_name.replace('.py', '')

        # Adicionar o diretório do script ao caminho do sistema
        sys.path.append(script_dir)

        # Ler e executar o script
        with open(script_path) as f:
            code = f.read()
            exec(code, globals())

        st.divider()
        st.write(section["explanations"])

def render_navigation_buttons(section):
    """
    Renderiza botões de navegação para mover entre as seções.

    Esta função exibe botões para continuar para a próxima seção ou voltar à seção anterior.
    """
    if "button_text" in section:
        if st.session_state.current_section > 0:
            st.subheader('', divider='rainbow')
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(section["button_text"], type="primary", use_container_width=True):
                    st.session_state.current_section += 1
                    st.rerun()
            col2 = st.empty()
            with col3:
                if st.button("Voltar atrás", use_container_width=True):
                    st.session_state.current_section -= 1
                    st.rerun()
        else:
            if st.button(section["button_text"], type="primary", use_container_width=True):
                st.session_state.current_section += 1
                st.rerun()

def load_quiz_data(file_path):
    """
    Carrega dados do questionário a partir de um arquivo JSON.

    Args:
        file_path (str): Caminho para o arquivo JSON contendo os dados do questionário.

    Returns:
        dict: Dados JSON analisados como um dicionário.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
