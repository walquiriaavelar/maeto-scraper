# Web Scraper Loja Maeto

Aplicação em Python para buscar produtos no site da Loja Maeto, extrair informações dos produtos encontrados e armazenar os dados em um banco SQLite3.

## Funcionalidades

- Busca de produtos por termo informado pelo usuário.
- Extração de dados de produtos encontrados.
- Armazenamento dos dados em banco SQLite3.
- Atualização automática caso o produto já exista no banco.
- Tratamento de conflitos pelo SKU: caso um produto já exista no banco, os dados são atualizados automaticamente em vez de serem duplicados.
- Uso do SKU como chave única para evitar duplicidade.

## Dados extraídos

Para cada produto encontrado, são armazenadas as seguintes informações:

- SKU
- Título do produto
- Preço
- Preço no PIX
- Valor da parcela
- Número de parcelas
- Informações técnicas
- URL do produto
- Data da última atualização

## Tecnologias utilizadas

- Python
- Requests
- BeautifulSoup
- SQLite3

## Estrutura do projeto

```text
maeto-scraper/
│
├── app.py
├── scraper.py
├── database.py
├── create_database.py
├── consultar_produtos.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── data/

## Modelagem do banco de dados

O banco de dados possui uma tabela chamada `produtos`.

| Campo | Tipo | Descrição |
|---|---|---|
| sku | TEXT | Chave primária do produto |
| titulo | TEXT | Nome do produto |
| preco | REAL | Preço principal do produto |
| preco_pix | REAL | Preço do produto no PIX |
| valor_parcela | REAL | Valor de cada parcela |
| numero_parcelas | INTEGER | Quantidade de parcelas |
| informacoes_tecnicas | TEXT | Informações técnicas do produto |
| url | TEXT | Link da página do produto |
| data_atualizacao | TEXT | Data e hora da última atualização |

## Como executar o projeto
1. Clonar o repositório
git clone URL_DO_REPOSITORIO
cd maeto-scraper

2. Criar o ambiente virtual
python -m venv venv

3. Ativar o ambiente virtual
source venv/Scripts/activate

4. Instalar as dependências
pip install -r requirements.txt

5. Criar o banco de dados
python create_database.py

6. Executar a busca de produtos
python app.py

Depois informe um termo de busca, por exemplo: assento

7. Consultar os produtos salvos
python consultar_produtos.py

Observação sobre o banco de dados

O arquivo produtos.db é gerado automaticamente dentro da pasta data/ ao executar o projeto.

Esse arquivo não é versionado no GitHub, pois está incluído no .gitignore.

Autor
Desenvolvido por Walquiria de Avelar Mourão.