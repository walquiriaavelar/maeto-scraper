import sqlite3
from pathlib import Path

DB_PATH = Path("data/produtos.db")


def listar_produtos():
    if not DB_PATH.exists():
        print("Banco de dados não encontrado.")
        return

    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            sku,
            titulo,
            preco,
            preco_pix,
            numero_parcelas,
            valor_parcela,
            url
        FROM produtos
        ORDER BY titulo
    """)

    produtos = cursor.fetchall()

    print(f"Total de produtos cadastrados: {len(produtos)}\n")

    for produto in produtos:
        print("-" * 80)
        print(f"SKU: {produto['sku']}")
        print(f"Título: {produto['titulo']}")
        print(f"Preço: R$ {produto['preco']}")
        print(f"Preço PIX: R$ {produto['preco_pix']}")
        print(f"Parcelas: {produto['numero_parcelas']}x de R$ {produto['valor_parcela']}")
        print(f"URL: {produto['url']}")

    conexao.close()


if __name__ == "__main__":
    listar_produtos()