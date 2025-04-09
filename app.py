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

            # Controle de edição por sessão
            if f"editando_{doc_id}" not in st.session_state:
                st.session_state[f"editando_{doc_id}"] = False

            if not st.session_state[f"editando_{doc_id}"]:
                if st.button(f"✏️ Editar '{titulo}'", key=f"editar_{doc_id}"):
                    st.session_state[f"editando_{doc_id}"] = True
            else:
                novo_titulo = st.text_input("Novo Título", value=titulo, key=f"titulo_{doc_id}")
                nova_descricao = st.text_area("Nova Descrição", value=descricao, key=f"desc_{doc_id}")
                novas_tags = st.text_input("Novas Tags (separadas por vírgula)", value=", ".join(tags), key=f"tags_{doc_id}")

                if st.button("Salvar Alterações", key=f"salvar_{doc_id}"):
                    controller.excluir_documento(doc_id)
                    controller.adicionar_documento(novo_titulo, nova_descricao, novas_tags.split(','))
                    st.success("Documento atualizado com sucesso.")
                    st.session_state[f"editando_{doc_id}"] = False
                    st.experimental_rerun()

                if st.button("Cancelar", key=f"cancelar_{doc_id}"):
                    st.session_state[f"editando_{doc_id}"] = False

elif escolha == "Excluir":
    st.subheader("Excluir Documento")
    documentos = controller.listar_documentos()
    opcoes = {f"{titulo} (ID: {doc_id})": doc_id for doc_id, titulo, _, _ in documentos}
    selecao = st.selectbox("Selecione um documento", list(opcoes.keys()))
    if st.button("Excluir"):
        controller.excluir_documento(opcoes[selecao])
        st.success("Documento excluído com sucesso.")

controller.fechar()
