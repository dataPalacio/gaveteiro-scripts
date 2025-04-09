from database.manager import DatabaseManager
from typing import List

class DocumentController:
    def __init__(self, db_path: str):
        self.db = DatabaseManager(db_path)

    def adicionar_documento(self, titulo: str, descricao: str, tags: List[str]):
        self.db.adicionar_documento(titulo, descricao, tags)

    def listar_documentos(self):
        return self.db.obter_documentos()

    def excluir_documento(self, doc_id: int):
        self.db.excluir_documento(doc_id)

    def fechar(self):
        self.db.fechar_conexao()
