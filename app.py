import streamlit as st
import requests
import collections
import random

st.set_page_config(page_title="IA Lotofácil Pessoal", page_icon="📊", layout="centered")
st.title("📊 Analisador de Tendências - Lotofácil")
st.write("Dados extraídos em tempo real via API alternativa estável.")

@st.cache_data(ttl=3600)
def buscar_dados_lotofacil():
    try:
        # Usando a API pública do Loterias API (focada em desenvolvedores)
        url_base = "https://herokuapp.com"
        response = requests.get(url_base, timeout=15)
        dados_completos = response.json()
        
        # Pega o último concurso da lista
        ultimo_registro = dados_completos[0]
        ultimo_concurso = int(ultimo_registro['concurso'])
        
        # Filtra e armazena os últimos 200 sorteios direto da lista recebida
        todos_sorteios = []
        for concurso in dados_completos[:200]:
            # Converte a lista de dezenas para números inteiros ordenados
            dezenas = sorted([int(x) for x in concurso['dezenas']])
            todos_sorteios.append(dezenas)
            
        return todos_sorteios, ultimo_concurso
    except Exception as e:
        st.error(f"Erro ao conectar com o servidor de dados: {e}")
        return None, None

historico_200, ultimo_num = buscar_dados_lotofacil()

if historico_200:
    st.success(f"Análise concluída com sucesso! Recorte: Últimos 200 concursos até o nº {ultimo_num}.")
    todos_numeros_sorteados = [num for sorteio in historico_200 for num in sorteio]
    contagem = collections.Counter(todos_numeros_sorteados)
    
    # Extrai o número da dezena puramente
    top_5_com_frequencia = contagem.most_common(5)
    as_5_mais = [item[0] for item in top_5_com_frequencia]
    
    todos_impares = [n for n in range(1, 26) if n % 2 != 0]
    todos_pares = [n for n in range(1, 26) if n % 2 == 0]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🔢 Divisão Fixa do Volante")
        st.write(f"**Ímpares:** `{str(todos_impares)[1:-1]}`")
        st.write(f"**Pares:** `{str(todos_pares)[1:-1]}`")
    with col2:
        st.markdown("### 🔥 As 5 Mais Sorteadas")
        for idx, (num, freq) in enumerate(top_5_com_frequencia):
            st.write(f"**{idx+1}º Lugar:** Dezena `{num:02d}` — {freq} vezes")

    st.markdown("---")
    st.subheader("🎲 Gerador Inteligente de Palpites")
    qtd_jogos = st.slider("Quantos cartões você quer gerar?", min_value=1, max_value=10, value=3)

    if st.button("Gerar Jogos Otimizados"):
        st.markdown("### 📝 Seus Cartões Prontos:")
        for i in range(qtd_jogos):
            # Garante que o jogo use a lista de inteiros das top dezenas
            jogo = list(as_5_mais)
            
            impares_fixos = [n for n in jogo if n % 2 != 0]
            pares_fixos = [n for n in jogo if n % 2 == 0]
            
            meta_impares = 8
            meta_pares = 7
            
            faltam_impares = meta_impares - len(impares_fixos)
            faltam_pares = meta_pares - len(pares_fixos)
            
            opcoes_impares = [n for n in todos_impares if n not in jogo]
            opcoes_pares = [n for n in todos_pares if n not in jogo]
            
            jogo.extend(random.sample(opcoes_impares, faltam_impares))
            jogo.extend(random.sample(opcoes_pares, faltam_pares))
            jogo.sort()
            
            jogo_formatado = " - ".join(f"{num:02d}" for num in jogo)
            st.info(f"**Jogo {i+1}:** {jogo_formatado}")
else:
    st.warning("Não foi possível carregar os dados. Aguarde um momento e recarregue a página.")
