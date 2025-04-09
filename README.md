
# Documentação Manager (Streamlit)

Gerencie documentos com descrição e tags em uma interface web simples, utilizando Streamlit.

## Funcionalidades

- Adição de documentos com descrição e tags
- Listagem de documentos com visualização Markdown
- Exclusão de documentos
- Visualização via interface Streamlit
- Banco de dados SQLite com estrutura normalizada

## Executando localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Estrutura do Projeto

```
DocumentacaoManagerStreamlit/
├── app.py                  # Interface principal Streamlit (View)
├── controller/
│   └── controller.py       # Controller da aplicação
├── database/
│   └── manager.py          # Acesso ao banco de dados (Model)
├── prog_documentacao/
│   └── documentacao.db     # Banco de dados SQLite
├── requirements.txt        # Dependências do projeto
└── README.md               # Instruções do projeto
```
