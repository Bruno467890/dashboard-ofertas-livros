"""Leitura dos arquivos CSV do projeto.
"""

from pathlib import Path
import csv

# Pasta onde este arquivo .py está. Assim o programa encontra o CSV
# mesmo quando é executado a partir de outra pasta (como no Streamlit Cloud).
PASTA = Path(__file__).parent
CAMINHO_LIVROS = PASTA / "livros.csv"

def ler_livros():
    livros = []
    try:
       with open(CAMINHO_LIVROS, "r", encoding="utf-8") as arquivo:
           leitor = csv.DictReader(arquivo)
           for linha in leitor:
               livros.append(linha)
    except FileNotFoundError:
        print("Ocorreu algum erro na leitura do arquivo")
    except Exception as error:
        print("Algum erro aconteceu na leitura do arquivo", error)

    return livros

def ler_livros_v2():
    with open("livros.csv", "r", encoding="utf-8") as arquivo:
        print(arquivo.readline())

def calcular_preco_medio(livros):
    soma = 0
    for livro in livros:
        preco_original: str = livro["preco"]
        preco_original_limpo: str = preco_original.replace("£", "")
        preco_num: float = float(preco_original_limpo)
        soma += preco_num
    preco_medio = soma / len(livros)
    return preco_medio

def contar_cinco_estrelas(livros):
    contador: int = 0
    for livro in livros:
        nota_limpa: str = livro["nota"].lower().strip()
        if nota_limpa == "five":
            contador += 1
    return contador

def obter_preco_maior(livros):
    preco_original_maior: str = livros[0]["preco"]
    preco_original_limpo_maior: str = preco_original_maior.replace("£", "")
    preco_num_maior: float = float(preco_original_limpo_maior)
    for livro in livros:
        preco_original: str = livro["preco"]
        preco_original_limpo: str = preco_original.replace("£", "")
        preco_num: float = float(preco_original_limpo)
        if preco_num > preco_num_maior:
            preco_num_maior = preco_num
    return preco_num_maior

if __name__ == "__main__":
    livros = ler_livros()
    print(f"A quantidade de livros da coleção é de {len(livros)} livros.")
    calcular_preco_medio(livros)
    cinco_estrelas = contar_cinco_estrelas(livros)
    print(cinco_estrelas)