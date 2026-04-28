import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote_plus
import unicodedata
from difflib import SequenceMatcher

BASE_URL = "https://www.lojamaeto.com"


def limpar_texto(texto):
    return re.sub(r"\s+", " ", texto).strip()

def limpar_texto(texto):
    return re.sub(r"\s+", " ", texto).strip()


def normalizar_busca(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def palavra_parecida(palavra, referencia):
    for item in referencia.split():
        similaridade = SequenceMatcher(None, palavra, item).ratio()

        if similaridade >= 0.80:
            return True

    return False


def produto_combina_com_termo(termo, referencia):
    termo_normalizado = normalizar_busca(termo)
    referencia_normalizada = normalizar_busca(referencia)

    if termo_normalizado in referencia_normalizada:
        return True

    palavras = [
        palavra for palavra in termo_normalizado.split()
        if len(palavra) >= 3
    ]

    if not palavras:
        return False

    encontradas = 0

    for palavra in palavras:
        if palavra in referencia_normalizada or palavra_parecida(palavra, referencia_normalizada):
            encontradas += 1

    percentual = encontradas / len(palavras)

    return percentual >= 0.60


def converter_preco(valor):
    if not valor:
        return None

    valor = valor.replace("R$", "")
    valor = valor.replace(".", "")
    valor = valor.replace(",", ".")
    valor = re.sub(r"[^\d.]", "", valor)

    try:
        return float(valor)
    except ValueError:
        return None


def obter_soup(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }

    resposta = requests.get(url, headers=headers, timeout=20)
    resposta.raise_for_status()

    return BeautifulSoup(resposta.text, "html.parser")


def extrair_sku(titulo_completo):
    match = re.search(r"Cód\.\s*([A-Za-z0-9\-]+)", titulo_completo, re.IGNORECASE)

    if match:
        return match.group(1)

    return None


def extrair_titulo(titulo_completo):
    return re.sub(
        r"\s*\(\s*Cód\.\s*[A-Za-z0-9\-]+\s*\)\s*",
        "",
        titulo_completo
    ).strip()


def extrair_informacoes_tecnicas(texto):
    linhas = [linha.strip() for linha in texto.splitlines() if linha.strip()]

    chaves_tecnicas = [
        "Marca",
        "Formato anatômico",
        "Dimensões",
        "Temperatura",
        "Material",
        "Instalação",
        "Vida Útil",
        "Garantia"
    ]

    paradas = [
        "Você também deve gostar",
        "Produtos relacionados",
        "Avaliações",
        "Descrição do Produto",
        "Informações do Produto"
    ]

    informacoes = []
    capturando = False

    i = 0
    while i < len(linhas):
        linha = linhas[i]

        if "Informações Técnicas" in linha:
            capturando = True
            i += 1
            continue

        if capturando and any(parada in linha for parada in paradas):
            break

        if capturando:
            if linha in chaves_tecnicas and i + 1 < len(linhas):
                chave = linha
                valor = linhas[i + 1]

                if valor not in chaves_tecnicas:
                    informacoes.append(f"{chave}: {valor}")
                    i += 2
                    continue

        i += 1

    return "\n".join(informacoes)


def extrair_preco(texto):
    match = re.search(r"R\$\s*[\d\.,]+\s*\(\d+% de desconto\)", texto)

    if match:
        preco = re.search(r"R\$\s*[\d\.,]+", match.group())
        return converter_preco(preco.group()) if preco else None

    linhas = [linha.strip() for linha in texto.splitlines() if linha.strip()]

    for linha in linhas:
        if linha.startswith("R$") and "pix" not in linha.lower():
            return converter_preco(linha)

    return None


def extrair_preco_pix(texto):
    match = re.search(r"Pix\s*R\$\s*[\d\.,]+", texto, re.IGNORECASE)

    if match:
        preco = re.search(r"R\$\s*[\d\.,]+", match.group())
        return converter_preco(preco.group()) if preco else None

    return None


def extrair_parcelas(texto):
    match = re.search(r"(\d+)x\s+de\s+R\$\s*[\d\.,]+", texto, re.IGNORECASE)

    if not match:
        return None, None

    numero_parcelas = int(match.group(1))

    valor_match = re.search(r"R\$\s*[\d\.,]+", match.group())
    valor_parcela = converter_preco(valor_match.group()) if valor_match else None

    return numero_parcelas, valor_parcela


def extrair_produto(url):
    soup = obter_soup(url)
    texto = soup.get_text("\n")

    h1 = soup.find("h1")

    if not h1:
        return None

    titulo_completo = limpar_texto(h1.get_text(" "))
    sku = extrair_sku(titulo_completo)

    if not sku:
        return None

    titulo = extrair_titulo(titulo_completo)
    preco = extrair_preco(texto)
    preco_pix = extrair_preco_pix(texto)
    numero_parcelas, valor_parcela = extrair_parcelas(texto)
    informacoes_tecnicas = extrair_informacoes_tecnicas(texto)

    return {
        "sku": sku,
        "titulo": titulo,
        "preco": preco,
        "preco_pix": preco_pix,
        "valor_parcela": valor_parcela,
        "numero_parcelas": numero_parcelas,
        "informacoes_tecnicas": informacoes_tecnicas,
        "url": url
    }


def buscar_links_produtos(termo):
    termo_url = quote_plus(termo)

    urls_busca = [
        f"{BASE_URL}/search/?q={termo_url}",
        f"{BASE_URL}/search/"
    ]

    links = []

    for url_busca in urls_busca:
        soup = obter_soup(url_busca)

        for link in soup.find_all("a", href=True):
            href = link["href"]
            texto_link = limpar_texto(link.get_text(" "))

            url_completa = urljoin(BASE_URL, href)

            if BASE_URL not in url_completa:
                continue

            if any(x in url_completa for x in [
                "/blog",
                "/search",
                "/login",
                "/carrinho",
                "/checkout",
                "/conta",
                "/politica",
                "/sobre",
                "whatsapp",
                "facebook",
                "instagram",
                "youtube",
                "tiktok"
            ]):
                continue

            if not texto_link:
                continue

            referencia = f"{texto_link} {url_completa}"

            if not produto_combina_com_termo(termo, referencia):
                continue

            if url_completa not in links:
                links.append(url_completa)

    return links


def buscar_produtos(termo, limite=20):
    links = buscar_links_produtos(termo)

    produtos = []

    for url in links[:limite]:
        try:
            produto = extrair_produto(url)

            if produto:
                produtos.append(produto)
                print(f"Produto encontrado: {produto['titulo']}")

        except Exception as erro:
            print(f"Erro ao processar {url}: {erro}")

    return produtos