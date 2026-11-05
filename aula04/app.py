"""Dashboard de Livros: app Streamlit.

Para rodar (com o ambiente virtual ativado):  streamlit run aula04/app.py
"""

import streamlit as st

import dados


def calcular_preco_medio(livros):
    """Soma os preços de todos os livros e divide pelo total."""
    soma = 0
    for livro in livros:
        soma = soma + livro["preco"]
    return soma / len(livros)


def contar_cinco_estrelas(livros):
    """Conta quantos livros têm a nota máxima."""
    quantidade = 0
    for livro in livros:
        if livro["nota"] == 5:
            quantidade = quantidade + 1
    return quantidade


def classificar_preco(preco):
    """Classifica um preço em libras em uma faixa de texto."""
    if preco < 20:
        return "Barato"
    elif preco <= 40:
        return "Médio"
    else:
        return "Caro"


def contar_por_faixa(livros):
    """Conta quantos livros existem em cada faixa de preço: {"Caro": 403, ...}"""
    contagem = {}
    for livro in livros:
        faixa = classificar_preco(livro["preco"])
        if faixa in contagem:
            contagem[faixa] = contagem[faixa] + 1
        else:
            contagem[faixa] = 1
    return contagem


def montar_tabela(livros):
    """Prepara as linhas que aparecem na tabela, com nomes de coluna amigáveis."""
    tabela = []
    for livro in livros:
        linha = {
            "Título": livro["titulo"],
            "Categoria": livro["categoria"],
            "Nota": "⭐" * livro["nota"],
            "Preço": f"£ {livro['preco']:.2f}",
            "Faixa": classificar_preco(livro["preco"]),
        }
        tabela.append(linha)
    return tabela

def montar_tabela_favoritos(favoritos):
    """Prepara as linhas que aparecem na tabela, com nomes de coluna amigáveis."""
    tabela = []
    for titulo, favorito in favoritos.items():
        linha = {
            "Título": titulo["titulo"],
            "Preço": f"£ {favorito['preco']:.2f}",
            "Status": favorito["status"],
            "Comentário": favorito["comentario"]
        }
        tabela.append(linha)
    return tabela


def buscar_por_titulo(livros, busca):
    """Devolve só os livros cujo título contém o texto buscado."""
    resultado = []
    for livro in livros:
        # Compara tudo em minúsculas: "harry" encontra "Harry Potter"
        if busca.lower() in livro["titulo"].lower():
            resultado.append(livro)
    return resultado


def listar_categorias(livros):
    """Devolve as categorias dos livros, sem repetição e em ordem alfabética."""
    categorias = []
    for livro in livros:
        if livro["categoria"] not in categorias:
            categorias.append(livro["categoria"])
    categorias.sort()
    return categorias


def filtrar_por_categoria(livros, categoria):
    """Devolve só os livros da categoria escolhida. Com "Todas", devolve todos."""
    if categoria == "Todas":
        return livros
    resultado = []
    for livro in livros:
        if livro["categoria"] == categoria:
            resultado.append(livro)
    return resultado

def listar_titulos(livros):
    titulos = []
    for livro in livros:
        titulos.append(livro["titulo"])

def main():
    st.set_page_config(page_title="Dashboard de Livros", page_icon="📚", layout="wide")
    st.title("📚 Dashboard de Livros")

    livros = dados.carregar_livros()

    with aba_catalogo():
        mostrar_catalogo(livros)

    with aba_favoritos():
        mostrar_favoritos(livros)

def somar_favoritos(favoritos):
    soma = 0
    for favorito in favoritos.values():
        soma = soma + favorito["preco"]
    return soma

def mostrar_favoritos():
    favoritos = dados.carregar_favoritos()

    if len(favoritos) <= 0:
        st.warning("Nenhum favorio foi adicionado")
        return
    
    col1, col2 = st.columns(2)
    col1.metric("Favoritos", len(favoritos))
    col2.metric("Valor Total", somar_favoritos(favoritos))





def mostrar_catalogo(livros):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de livros", len(livros))
    col2.metric("Preço médio", f"£{round(calcular_preco_medio(livros), 2)}")
    col3.metric("Livros com 5 estrelas", contar_cinco_estrelas(livros))

    mais_caro = dados.encontrar_mais_caro(livros)
    col4.metric("Livro mais caro", f"£{mais_caro["preco"]}")
    col4.caption(mais_caro["titulo"])

    col_busca, col_categoria = st.columns(2)
    busca = col_busca.text_input("🔎 Buscar pelo título")
    categoria = col_categoria.selectbox("📂 Categoria", ["Todas"] + listar_categorias(livros))

    # Cada filtro recebe o resultado do anterior
    encontrados = filtrar_por_categoria(livros, categoria)
    encontrados = buscar_por_titulo(encontrados, busca)

    if len(encontrados) == 0:
        st.warning("Nenhum livro encontrado.")
    else:
        st.caption(f"{len(encontrados)} livros encontrados")
        st.dataframe(montar_tabela(encontrados), hide_index=True, width="stretch")

        titulos_livros = listar_titulos(livros)
        titulo_selecionado = st.selectbox("Escolhe um livro", titulos_livros)

        livro_favorito = buscar_por_titulo(livros, titulo_selecionado)
        if st.button("Inserir Favorito"):
            ## Criar o arquivo
            ## Incluir p cabeçalho
            ## Incluir o dado do livro
            dados.salvar_favoritos(livro_favorito[0])
            st.success(f'O livro{titulo_selecionado}" foi inserido na lista de favoritos.')


if __name__ == "__main__":
    main()
