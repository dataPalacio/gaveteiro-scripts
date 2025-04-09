import streamlit as st
import streamlit.components.v1 as components
from controller.controller import DocumentController

controller = DocumentController("prog_documentacao/documentacao.db")

st.title("Gerenciador de Documentações")

menu = ["Adicionar", "Visualizar", "Excluir"]
escolha = st.sidebar.selectbox("Menu", menu)

if escolha == "Adicionar":
    st.subheader("Adicionar Novo Documento")
    titulo = st.text_input("Título")
    descricao = st.text_area("Descrição (Markdown)")
    tags = st.text_input("Tags (separadas por vírgula)")
    if st.button("Salvar"):
        if titulo and descricao:
            controller.adicionar_documento(titulo, descricao, tags.split(','))
            st.success("Documento adicionado com sucesso!")
        else:
            st.error("Título e descrição são obrigatórios.")

elif escolha == "Visualizar":
    st.subheader("Lista de Documentos")
    documentos = controller.listar_documentos()
    for doc_id, titulo, descricao, tags in documentos:
        with st.expander(titulo):
            st.markdown(descricao)
            st.markdown(f"**Tags:** {', '.join(tags)}")

            # Botão copiar via HTML/JS
            components.html(f'''
                <textarea id="code_{doc_id}" style="display:none;">{descricao}</textarea>
                <button onclick="navigator.clipboard.writeText(document.getElementById('code_{doc_id}').value)">
                    📋 Copiar Descrição
                </button>
            ''', height=50)

elif escolha == "Excluir":
    st.subheader("Excluir Documento")
    documentos = controller.listar_documentos()
    opcoes = {f"{titulo} (ID: {doc_id})": doc_id for doc_id, titulo, _, _ in documentos}
    selecao = st.selectbox("Selecione um documento", list(opcoes.keys()))
    if st.button("Excluir"):
        controller.excluir_documento(opcoes[selecao])
        st.success("Documento excluído com sucesso.")

controller.fechar()
