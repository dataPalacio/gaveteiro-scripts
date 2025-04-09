import sqlite3
from typing import List, Tuple

class DatabaseManager:
    def __init__(self, db_name: str = "prog_documentacao/documentacao.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documento_tags (
                documento_id INTEGER,
                tag_id INTEGER,
                FOREIGN KEY(documento_id) REFERENCES documentos(id),
                FOREIGN KEY(tag_id) REFERENCES tags(id),
                PRIMARY KEY (documento_id, tag_id)
            )
        """)
        self.conn.commit()

    def adicionar_documento(self, titulo: str, descricao: str, tags: List[str]):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO documentos (titulo, descricao) VALUES (?, ?)",
            (titulo, descricao)
        )
        doc_id = cursor.lastrowid
        for tag in tags:
            tag = tag.strip()
            cursor.execute("INSERT OR IGNORE INTO tags (nome) VALUES (?)", (tag,))
            cursor.execute("SELECT id FROM tags WHERE nome = ?", (tag,))
            tag_id = cursor.fetchone()[0]
            cursor.execute(
                "INSERT OR IGNORE INTO documento_tags (documento_id, tag_id) VALUES (?, ?)",
                (doc_id, tag_id)
            )
        self.conn.commit()

    def obter_documentos(self) -> List[Tuple[int, str, str, List[str]]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, titulo, descricao FROM documentos")
        documentos = cursor.fetchall()
        resultados = []
        for doc_id, titulo, descricao in documentos:
            cursor.execute("""
                SELECT tags.nome FROM tags
                JOIN documento_tags ON tags.id = documento_tags.tag_id
                WHERE documento_tags.documento_id = ?
            """, (doc_id,))
            tags = [row[0] for row in cursor.fetchall()]
            resultados.append((doc_id, titulo, descricao, tags))
        return resultados

    def excluir_documento(self, doc_id: int):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM documento_tags WHERE documento_id = ?", (doc_id,))
        cursor.execute("DELETE FROM documentos WHERE id = ?", (doc_id,))
        self.conn.commit()

    def fechar_conexao(self):
        self.conn.close()
