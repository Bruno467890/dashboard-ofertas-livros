"""Dashboard de Livros: app Streamlit.
"""

import streamlit as st
import dados

st.set_page_config(layout="wide")
st.title("📚 Dashboard de Livros")
st.write("Se você está vendo esta página, o seu ambiente está pronto! 🎉")

col1, col2, col3 = st.columns(3)

livros = dados.ler_livros()
qtd_livros = len(livros)
media_preco = dados.calcular_preco_medio(livros)
cinco_estrelas = dados.contar_cinco_estrelas(livros)

col1.metric("Total de Livros", qtd_livros)
col2.metric("Preço médio", f"£{media_preco:.2f}")
col3.metric("Qtd. livros 5 estrelas", cinco_estrelas)

st.dataframe(livros)