import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("data/produtos.db")


def conectar():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            sku TEXT PRIMARY KEY,
            titulo TEXT NOT NULL,
            preco REAL,
            preco_pix REAL,
            valor_parcela REAL,
            numero_parcelas INTEGER,
            informacoes_tecnicas TEXT,
            url TEXT,
            data_atualizacao TEXT
        )
    """)

    conexao.commit()
    conexao.close()


def salvar_ou_atualizar_produto(produto):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO produtos (
            sku,
            titulo,
            preco,
            preco_pix,
            valor_parcela,
            numero_parcelas,
            informacoes_tecnicas,
            url,
            data_atualizacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(sku) DO UPDATE SET
            titulo = excluded.titulo,
            preco = excluded.preco,
            preco_pix = excluded.preco_pix,
            valor_parcela = excluded.valor_parcela,
            numero_parcelas = excluded.numero_parcelas,
            informacoes_tecnicas = excluded.informacoes_tecnicas,
            url = excluded.url,
            data_atualizacao = excluded.data_atualizacao
    """, (
        produto["sku"],
        produto["titulo"],
        produto["preco"],
        produto["preco_pix"],
        produto["valor_parcela"],
        produto["numero_parcelas"],
        produto["informacoes_tecnicas"],
        produto["url"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conexao.commit()
    conexao.close()