import streamlit as st
import pandas as pd
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Detector de Clientes VIP",
    page_icon="💎",
    layout="wide"
)

# --- FUNÇÕES DE CARREGAMENTO (ETL) ---
@st.cache_data
def carregar_dados_exemplo():
    # Cria um DataFrame falso na memória para demonstração
    dados = {
        'ID_Cliente': [101, 102, 103, 104, 105, 106, 107, 108],
        'Nome': ['Padaria do João', 'Mercado Silva', 'Oficina Top', 'Dona Maria', 'Pedro Tech', 'Ana Modas', 'Bar do Zé', 'Loja 10'],
        'Data_Ultima_Compra': pd.to_datetime(['2024-02-01', '2023-11-15', '2024-01-20', '2023-05-10', '2024-02-03', '2023-12-01', '2024-01-30', '2023-08-20']),
        'Total_Gasto': [5000, 1200, 8500, 150, 12000, 3000, 450, 800],
        'Frequencia_Compras': [12, 3, 20, 1, 25, 5, 2, 2]
    }
    return pd.DataFrame(dados)

# --- INTERFACE PRINCIPAL ---
st.title("💎 Detector de Oportunidades (RFM)")
st.markdown("""
Descubra quem são seus **Clientes VIPs**, quem está **Em Risco** de ir embora 
e gere mensagens automáticas de recuperação via WhatsApp.
""")

st.divider()

# --- SIDEBAR (CONTROLES) ---
with st.sidebar:
    st.header("📂 Seus Dados")
    arquivo_upload = st.file_uploader("Suba sua planilha de vendas (Excel/CSV)", type=['xlsx', 'csv'])
    
    st.markdown("---")
    
    usar_exemplo = st.checkbox("Não tem dados? Usar Exemplo", value=False)

# --- LÓGICA DE CARREGAMENTO ---
df = None

if arquivo_upload:
    try:
        if arquivo_upload.name.endswith('.csv'):
            df = pd.read_csv(arquivo_upload)
        else:
            df = pd.read_excel(arquivo_upload)
        st.sidebar.success("Dados carregados com sucesso!")
    except Exception as e:
        st.error(f"Erro ao ler arquivo: {e}")

elif usar_exemplo:
    df = carregar_dados_exemplo()
    st.sidebar.info("Utilizando dados fictícios de demonstração.")

# --- O DASHBOARD (SÓ APARECE SE TIVER DADOS) ---
if df is not None:
    # Mostra um "cheiro" dos dados
    st.subheader("📋 Visão Geral dos Dados")
    st.dataframe(df.head(), use_container_width=True)
    
    st.info("👆 Se você está vendo a tabela acima, a Etapa 1 (Conexão) funcionou!")
    
    # AQUI ENTRARÁ O CÁLCULO RFM E A IA DEPOIS
    
else:
    # Tela de "Venda" quando não tem nada carregado
    st.info("👈 Comece fazendo upload do arquivo ou selecionando o modo Exemplo na barra lateral.")