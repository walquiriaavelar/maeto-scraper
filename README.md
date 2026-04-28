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

- `app.py` — arquivo principal da aplicação.
- `scraper.py` — responsável pela busca e extração dos dados do site.
- `database.py` — responsável pela conexão, criação da tabela e salvamento no SQLite.
- `create_database.py` — script para criar o banco de dados.
- `consultar_produtos.py` — script para consultar os produtos salvos.
- `requirements.txt` — dependências do projeto.
- `README.md` — documentação do projeto.
- `.gitignore` — arquivos ignorados pelo Git.
- `data/` — pasta onde o banco SQLite é gerado localmente.

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

O campo `sku` foi definido como chave primária para garantir que cada produto seja único no banco. Caso uma nova busca retorne um produto já cadastrado, a aplicação atualiza os dados existentes em vez de criar um registro duplicado.

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
