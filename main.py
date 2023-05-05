import streamlit as st
import numpy as np
st.set_page_config(layout='wide')
if "load_state" not in st.session_state:
    st.session_state.load_state = False
if "calc" not in st.session_state:
    st.session_state.calc = False


# Função para criar a matriz do sistema
def criar_matriz(tamanho):
    matriz = np.zeros((tamanho, tamanho + 1))

    colunas = st.columns(tamanho+1)

    for i in range(tamanho):
        for j in range(tamanho):
            while True:
                try:
                    valor = colunas[j].number_input(f"Digite o coeficiente a[{i+1}][{j+1}]: ", key=f"a{i}{j}", step=1)
                    break
                except ValueError:
                    print("Valor inválido. Digite novamente.")
            matriz[i][j] = valor
        while True:
            try:
                valor_independente = colunas[tamanho].number_input(f"Digite o termo independente b[{i + 1}]: ", key=f"b{i}", step=1)
                break
            except ValueError:
                print("Valor inválido. Digite novamente.")
        matriz[i][-1] = valor_independente
    return matriz


# Função para exibir a matriz do sistema
def exibir_matriz(matriz):
    num_linhas = len(matriz)
    num_colunas = len(matriz[0])

    for i in range(num_linhas):
        cols = st.columns(num_colunas + 1)
        for j in range(num_colunas-1):
            cols[j].write(str(matriz[i][j]))
        cols[-1].write(str(matriz[i][num_colunas - 1]))


# Função para escalonar a matriz do sistema
def eliminacao_gauss(matriz):
    tamanho = matriz.shape[0]
    for i in range(tamanho):
        if matriz[i][i] == 0:
            # Troca de linha caso o pivô seja zero
            for k in range(i + 1, tamanho):
                if matriz[k][i] != 0:
                    matriz[[i, k]] = matriz[[k, i]]
                    break
        fator = matriz[i][i]
        matriz[i] /= fator
        for j in range(i + 1, tamanho):
            fator = matriz[j][i]
            matriz[j] -= fator * matriz[i]
    return matriz


# Função para resolver o sistema linear
def resolver_sistema(matriz):
    tamanho = matriz.shape[0]
    solucao = np.zeros(tamanho)
    for i in range(tamanho - 1, -1, -1):
        soma = np.dot(matriz[i][i+1:-1], solucao[i+1:])
        solucao[i] = (matriz[i][-1] - soma) / matriz[i][i]
    return solucao

# Programa principal
st.title("Resolução de sistema linear por eliminação de Gauss")
tamanho = st.number_input("Digite o tamanho do sistema linear:", min_value=2, max_value=10, step=1, value=3)
if st.button('Criar') or st.session_state.load_state:
    st.session_state.load_state = True
    matriz = criar_matriz(tamanho)
    st.write("Sistema original:")
    exibir_matriz(matriz)
    if st.button("Calcular") or st.session_state.calc:
        st.session_state.calc = True
        matriz_escalonada = eliminacao_gauss(matriz)
        st.write("Sistema escalonado:")
        exibir_matriz(matriz_escalonada)
        solucao = resolver_sistema(matriz_escalonada)
        st.write("Solução:")
        for i in range(tamanho):
            st.write(f"x{i + 1}: {round(solucao[i], 2)}")
        st.write([round(x, 2) for x in solucao])
