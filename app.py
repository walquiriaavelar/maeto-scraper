from database import criar_tabela, salvar_ou_atualizar_produto
from scraper import buscar_produtos


def main():
    criar_tabela()

    termo = input("Digite o termo de busca: ").strip()

    if not termo:
        print("Você precisa informar um termo de busca.")
        return

    print(f"\nBuscando produtos para: {termo}\n")

    produtos = buscar_produtos(termo)

    if not produtos:
        print("Nenhum produto encontrado.")
        return

    for produto in produtos:
        salvar_ou_atualizar_produto(produto)

    print(f"\nProcesso finalizado. {len(produtos)} produto(s) salvo(s)/atualizado(s) no banco.")


if __name__ == "__main__":
    main()