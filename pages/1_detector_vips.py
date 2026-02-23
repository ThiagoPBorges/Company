import streamlit as st
import pandas as pd
import time
import urllib.parse
import io
import plotly.express as px
from portfolio import idiom

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title=idiom("Detector de Clientes VIP", "VIP Clients Detector"),
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
    # --- NOVA CONFIGURAÇÃO DE MENU ---
    menu_items={
        'Get Help': 'https://www.linkedin.com/in/thiagopborges/',
        'Report a bug': None,
        'About': idiom(
            "### 💎 Detector de Oportunidades\nDesenvolvido para transformar dados em decisões estratégicas.",
            "### 💎 Opportunities Detector\nDeveloped to transform data into strategic decisions."
        )
    }
)

# Remove the default app margin
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# ----- PAGE DESIGN (DARK MODE MAIN + SIDEBAR TEXTO PRETO) -----
page_style = """
<style>
    /* 1. FUNDO GERAL (Azul Escuro Suave) */
    [data-testid="stAppViewContainer"] {
        background-color: #1e293b !important; 
        background-image: radial-gradient(#475569 1px, transparent 1px) !important; 
        background-size: 24px 24px !important; 
    }

    /* 2. BARRA LATERAL (SIDEBAR) - Fundo claro */
    [data-testid="stSidebar"] {
        background-color: #f8fafc !important; 
        box-shadow: 2px 0 30px rgba(0,0,0,0.3) !important;
        border-right: 1px solid #e5e7eb !important;
    }

    /* 3. CARTÕES DE VIDRO E EXPANDER */
    [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stVerticalBlockBorderWrapper"] > div, 
    [data-testid="stExpander"] details {
        background-color: rgba(51, 65, 85, 0.7) !important; 
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important; 
        border-radius: 12px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
    }

    /* 4. TIPOGRAFIA GERAL (Área Principal Escura) */
    h1, h2, h3, h4, h5, h6, span, .stMarkdown p, 
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary span {
        color: #ffffff !important; 
    }
    
    p, li, .stMarkdown {
        color: #ffffff !important; /* Cinza escuro (quase preto) é mais elegante que #000000 */
    }    

    
    /* 5. TIPOGRAFIA DA SIDEBAR (Texto Preto Forçado) */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown {
        color: #000000 !important; 
    }

    /* 6. CABEÇALHO TRANSPARENTE */
    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* 8. ESCONDER RODAPÉ (Made with Streamlit) */
    footer {
        visibility: hidden;
    }

    /* 9. CORRIGIR CORES DO MENU SUPERIOR E DA JANELA 'SOBRE' */
    div[role="menu"] span, 
    div[role="menu"] p,
    div[role="dialog"] span,
    div[role="dialog"] p,
    div[role="dialog"] h1,
    div[role="dialog"] h2,
    div[role="dialog"] h3 {
        color: #1e293b !important; /* Azul bem escuro/quase preto para dar contraste */
    }

    /* 10. CORREÇÃO DEFINITIVA DOS TEXTOS (Selectbox) */
    .stSelectbox div[data-baseweb="select"] span,
    .stSelectbox div[data-baseweb="select"] div,
    div[data-baseweb="popover"] span,
    div[data-baseweb="popover"] li,
    div[data-baseweb="popover"] div {
        color: #1e293b !important;
    }
    
</style>
"""

st.markdown(page_style, unsafe_allow_html=True)

# --- DATA EXAMPLE (When user not have one) ---
@st.cache_data
def loading_example_dataset():
    dados = {
    'ID_Cliente': [113, 116, 106, 110, 108, 114, 105, 118, 111, 105, 103, 119, 120, 103, 103, 104, 102, 109, 106, 107, 118, 119, 114, 115, 104, 117, 112, 108, 113, 110, 106, 111, 110, 111, 112, 105, 119, 109, 108, 107, 111, 115, 102, 117, 111, 104, 115, 117, 112, 102, 116, 104, 112, 111, 120, 119, 116, 101, 102, 107, 116, 119, 105, 112, 106, 112, 104, 118, 110, 114, 116, 101, 103, 106, 106, 107, 104, 118, 117, 103, 118, 107, 115, 101, 101, 104, 114, 105, 102, 110, 110, 107, 116, 105, 106, 117, 104, 115, 119, 104],
    'Nome': ['TransNacional', 'Limpeza & Service', 'Inova Marketing', 'Indústria MetalSul', 'FarmaMed Distribuição', 'Segurança Prime', 'Logística Veloz', 'Engenharia Norte', 'Comércio Global', 'Logística Veloz', 'Grupo Horizonte', 'Importadora Águia', 'Rede Supermix', 'Grupo Horizonte', 'Grupo Horizonte', 'Consultoria Exata', 'Distribuidora Aliança', 'Agro Verde', 'Inova Marketing', 'Construtora Base', 'Engenharia Norte', 'Importadora Águia', 'Segurança Prime', 'Auto Peças Rota', 'Consultoria Exata', 'Advocacia Silva', 'Soft Systems', 'FarmaMed Distribuição', 'TransNacional', 'Indústria MetalSul', 'Inova Marketing', 'Comércio Global', 'Indústria MetalSul', 'Comércio Global', 'Soft Systems', 'Logística Veloz', 'Importadora Águia', 'Agro Verde', 'FarmaMed Distribuição', 'Construtora Base', 'Comércio Global', 'Auto Peças Rota', 'Distribuidora Aliança', 'Advocacia Silva', 'Comércio Global', 'Consultoria Exata', 'Auto Peças Rota', 'Advocacia Silva', 'Soft Systems', 'Distribuidora Aliança', 'Limpeza & Service', 'Consultoria Exata', 'Soft Systems', 'Comércio Global', 'Rede Supermix', 'Importadora Águia', 'Limpeza & Service', 'TechSolutions Ltda', 'Distribuidora Aliança', 'Construtora Base', 'Limpeza & Service', 'Importadora Águia', 'Logística Veloz', 'Soft Systems', 'Inova Marketing', 'Soft Systems', 'Consultoria Exata', 'Engenharia Norte', 'Indústria MetalSul', 'Segurança Prime', 'Limpeza & Service', 'TechSolutions Ltda', 'Grupo Horizonte', 'Inova Marketing', 'Inova Marketing', 'Construtora Base', 'Consultoria Exata', 'Engenharia Norte', 'Advocacia Silva', 'Grupo Horizonte', 'Engenharia Norte', 'Construtora Base', 'Auto Peças Rota', 'TechSolutions Ltda', 'TechSolutions Ltda', 'Consultoria Exata', 'Segurança Prime', 'Logística Veloz', 'Distribuidora Aliança', 'Indústria MetalSul', 'Indústria MetalSul', 'Construtora Base', 'Limpeza & Service', 'Logística Veloz', 'Inova Marketing', 'Advocacia Silva', 'Consultoria Exata', 'Auto Peças Rota', 'Importadora Águia', 'Consultoria Exata'],
    'Data_Compra': pd.to_datetime(['2023-06-19', '2023-04-08', '2023-10-14', '2023-08-18', '2023-11-23', '2023-03-31', '2023-11-24', '2023-10-07', '2023-03-29', '2023-06-06', '2023-05-27', '2023-04-16', '2023-04-22', '2023-07-08', '2023-08-05', '2024-01-07', '2023-07-12', '2023-08-26', '2023-03-28', '2023-11-16', '2023-06-17', '2023-09-06', '2023-06-09', '2024-01-20', '2023-05-04', '2024-02-04', '2023-08-20', '2023-12-18', '2023-08-20', '2023-04-05', '2023-05-21', '2023-07-14', '2023-10-07', '2023-04-12', '2023-04-09', '2023-09-18', '2023-05-15', '2023-07-15', '2023-06-19', '2023-02-25', '2023-02-27', '2023-03-23', '2023-10-22', '2024-02-09', '2023-02-08', '2023-05-26', '2023-10-25', '2023-08-26', '2023-09-02', '2023-07-12', '2023-11-11', '2023-12-03', '2024-01-10', '2023-02-18', '2023-08-13', '2023-06-25', '2023-05-26', '2023-08-15', '2023-11-02', '2023-01-06', '2023-04-25', '2023-06-01', '2023-12-22', '2023-03-07', '2023-01-01', '2023-07-30', '2023-04-26', '2023-06-28', '2023-05-21', '2023-09-19', '2023-01-19', '2023-11-26', '2023-12-14', '2023-08-08', '2023-04-19', '2023-05-14', '2023-11-05', '2024-01-20', '2023-06-12', '2023-03-26', '2023-03-31', '2023-02-20', '2023-08-23', '2023-08-16', '2023-09-02', '2023-02-19', '2023-04-24', '2023-01-15', '2023-06-22', '2023-02-26', '2023-09-04', '2023-05-26', '2023-10-24', '2023-01-07', '2023-07-20', '2023-09-18', '2023-07-21', '2023-01-31', '2023-02-17', '2023-10-12']),
    'Total_Gasto': [42559.28, 20889.48, 13454.45, 16174.75, 11614.17, 17831.68, 16638.97, 22956.89, 32511.89, 23157.06, 2743.41, 46170.63, 30021.79, 41237.19, 45194.94, 32550.23, 29918.25, 31053.14, 17519.47, 36027.35, 15881.72, 40178.12, 9554.72, 44506.26, 47961.38, 5313.14, 46333.03, 1977.8, 25528.39, 24648.52, 25589.17, 44243.81, 15570.17, 36489.14, 21262.69, 36114.47, 39994.0, 34107.03, 45204.93, 38632.58, 16330.36, 49561.73, 6280.65, 21240.6, 30648.55, 4090.33, 23082.73, 27068.87, 49483.37, 43891.25, 38557.77, 23373.29, 7429.78, 26902.2, 49671.05, 1641.26, 35125.03, 35211.84, 22763.22, 10243.32, 18060.41, 48511.81, 20387.42, 32702.88, 5488.74, 37913.35, 39541.45, 3865.68, 45909.56, 38211.67, 3264.01, 7604.55, 5588.29, 30399.96, 31071.04, 22101.12, 33111.92, 40508.86, 25216.14, 11678.39, 22386.32, 4666.58, 40813.41, 45153.35, 30449.3, 21759.96, 47651.8, 46385.09, 20439.98, 7535.41, 46418.49, 43583.2, 19981.31, 7307.5, 40111.88, 9829.85, 36767.4, 9204.3, 48157.57, 16157.35],
    'Categoria': ['Eletrônicos', 'Alimentos', 'Ferragens', 'Alimentos', 'Serviços', 'Alimentos', 'Ferragens', 'Automotivo', 'Escritório', 'Ferragens', 'Alimentos', 'Alimentos', 'Alimentos', 'Escritório', 'Ferragens', 'Serviços', 'Serviços', 'Ferragens', 'Alimentos', 'Limpeza', 'Automotivo', 'Limpeza', 'Automotivo', 'Automotivo', 'Automotivo', 'Limpeza', 'Eletrônicos', 'Limpeza', 'Serviços', 'Limpeza', 'Limpeza', 'Ferragens', 'Escritório', 'Eletrônicos', 'Ferragens', 'Alimentos', 'Alimentos', 'Serviços', 'Serviços', 'Ferragens', 'Limpeza', 'Limpeza', 'Alimentos', 'Serviços', 'Alimentos', 'Automotivo', 'Ferragens', 'Limpeza', 'Limpeza', 'Escritório', 'Escritório', 'Eletrônicos', 'Serviços', 'Escritório', 'Alimentos', 'Escritório', 'Alimentos', 'Limpeza', 'Serviços', 'Ferragens', 'Eletrônicos', 'Escritório', 'Eletrônicos', 'Ferragens', 'Ferragens', 'Serviços', 'Alimentos', 'Limpeza', 'Ferragens', 'Ferragens', 'Serviços', 'Eletrônicos', 'Escritório', 'Alimentos', 'Serviços', 'Serviços', 'Ferragens', 'Escritório', 'Serviços', 'Serviços', 'Automotivo', 'Ferragens', 'Automotivo', 'Limpeza', 'Eletrônicos', 'Alimentos', 'Escritório', 'Ferragens', 'Eletrônicos', 'Automotivo', 'Automotivo', 'Limpeza', 'Ferragens', 'Serviços', 'Ferragens', 'Automotivo', 'Ferragens', 'Serviços', 'Alimentos', 'Alimentos'],
    'Forma_Pagamento': ['Transferência', 'Transferência', 'Pix', 'Pix', 'Pix', 'Pix', 'Pix', 'Pix', 'Cartão de Crédito', 'Pix', 'Cartão de Crédito', 'Pix', 'Transferência', 'Transferência', 'Boleto', 'Cartão de Crédito', 'Pix', 'Pix', 'Pix', 'Boleto', 'Pix', 'Transferência', 'Transferência', 'Pix', 'Transferência', 'Pix', 'Boleto', 'Boleto', 'Transferência', 'Transferência', 'Cartão de Crédito', 'Pix', 'Transferência', 'Cartão de Crédito', 'Cartão de Crédito', 'Cartão de Crédito', 'Transferência', 'Transferência', 'Boleto', 'Cartão de Crédito', 'Transferência', 'Boleto', 'Boleto', 'Cartão de Crédito', 'Boleto', 'Pix', 'Pix', 'Cartão de Crédito', 'Cartão de Crédito', 'Cartão de Crédito', 'Pix', 'Cartão de Crédito', 'Boleto', 'Transferência', 'Pix', 'Transferência', 'Boleto', 'Transferência', 'Transferência', 'Cartão de Crédito', 'Cartão de Crédito', 'Boleto', 'Pix', 'Transferência', 'Transferência', 'Boleto', 'Transferência', 'Cartão de Crédito', 'Cartão de Crédito', 'Boleto', 'Cartão de Crédito', 'Transferência', 'Pix', 'Boleto', 'Transferência', 'Pix', 'Pix', 'Transferência', 'Transferência', 'Transferência', 'Cartão de Crédito', 'Transferência', 'Boleto', 'Boleto', 'Cartão de Crédito', 'Pix', 'Transferência', 'Transferência', 'Boleto', 'Pix', 'Cartão de Crédito', 'Transferência', 'Pix', 'Transferência', 'Boleto', 'Transferência', 'Cartão de Crédito', 'Pix', 'Boleto', 'Transferência'],
    'Vendedor': ['Fernanda Lima', 'Mariana Costa', 'Carlos Souza', 'Ricardo Oliveira', 'Ana Silva', 'Carlos Souza', 'Mariana Costa', 'Ana Silva', 'Carlos Souza', 'Ricardo Oliveira', 'Fernanda Lima', 'Carlos Souza', 'Mariana Costa', 'Carlos Souza', 'Mariana Costa', 'Mariana Costa', 'Mariana Costa', 'Ana Silva', 'Carlos Souza', 'Ricardo Oliveira', 'Ana Silva', 'Carlos Souza', 'Mariana Costa', 'Fernanda Lima', 'Ana Silva', 'Ana Silva', 'Fernanda Lima', 'Fernanda Lima', 'Carlos Souza', 'Mariana Costa', 'Ana Silva', 'Carlos Souza', 'Carlos Souza', 'Mariana Costa', 'Carlos Souza', 'Fernanda Lima', 'Ana Silva', 'Mariana Costa', 'Mariana Costa', 'Ana Silva', 'Ana Silva', 'Ricardo Oliveira', 'Fernanda Lima', 'Ricardo Oliveira', 'Fernanda Lima', 'Ana Silva', 'Ricardo Oliveira', 'Fernanda Lima', 'Ana Silva', 'Fernanda Lima', 'Ana Silva', 'Mariana Costa', 'Mariana Costa', 'Fernanda Lima', 'Ana Silva', 'Mariana Costa', 'Carlos Souza', 'Fernanda Lima', 'Ana Silva', 'Ana Silva', 'Mariana Costa', 'Mariana Costa', 'Fernanda Lima', 'Mariana Costa', 'Mariana Costa', 'Mariana Costa', 'Fernanda Lima', 'Ana Silva', 'Fernanda Lima', 'Fernanda Lima', 'Carlos Souza', 'Mariana Costa', 'Fernanda Lima', 'Carlos Souza', 'Carlos Souza', 'Carlos Souza', 'Mariana Costa', 'Carlos Souza', 'Ricardo Oliveira', 'Ana Silva', 'Fernanda Lima', 'Ana Silva', 'Carlos Souza', 'Ricardo Oliveira', 'Ricardo Oliveira', 'Fernanda Lima', 'Fernanda Lima', 'Mariana Costa', 'Mariana Costa', 'Carlos Souza', 'Mariana Costa', 'Mariana Costa', 'Mariana Costa', 'Ana Silva', 'Ricardo Oliveira', 'Ana Silva', 'Ricardo Oliveira', 'Ana Silva', 'Mariana Costa', 'Ricardo Oliveira'],
}
    return pd.DataFrame(dados)

# --- SIDEBAR ---
with st.sidebar:

    # Create button to alternate EN-PT
    escolha = st.radio(
        "idiom / Language", 
        ['PT - 🇧🇷', 'EN - 🇺🇸'], 
        horizontal=True,
        label_visibility="collapsed"
    )
    # Save on memory EN-PT
    if 'PT' in escolha:
        st.session_state['idiom'] = 'PT'
    else:
        st.session_state['idiom'] = 'EN'
    
    st.markdown("")
    st.markdown("")

    st.page_link("portfolio.py", label=idiom("Voltar ao início", "Home"), icon="🏠")

    st.divider()

    with st.container(border=True):
        st.header(idiom("📂 Seus Dados", "📂 Your Data"))
        upload_file = st.file_uploader(idiom("Suba sua planilha de vendas (Excel/CSV/TXT)", "Upload your sales spreadsheet (Excel/CSV/TXT)"), type=['xls', 'xlsb', 'xlsm', 'csv', 'txt'])

        if st.button(idiom("🔄 Limpar e Reiniciar", "🔄 Clear and Restart")):
            st.cache_data.clear()
            st.session_state.clear()
            st.rerun()
        
        st.markdown("---")
        
        st.info(idiom("💡 Quer apenas testar a ferramenta?","Do you want to test the tool?"))
        example_button = st.toggle(idiom("Ativar Dados de Exemplo", "Activate Example Data"), value=False)

# --- MAIN INTERFACE ---
st.title(idiom("💎 Detector de Oportunidades (RFM)", "💎 RFM Detector"))
st.markdown(idiom("""
Descubra quem são seus **Clientes VIPs**, quem está **Em Risco** de ir embora 
e gere mensagens automáticas de recuperação via WhatsApp.
""",
"""
Discover who are your **VIP Clients**, who are **In Risk** of leaving and generate automatic recovery messages via WhatsApp.
"""
))

st.markdown("")

# --- LOADING LOGIC ---
df = None

# If user input a file, will be analyze that, if not will use fiction dataset
if upload_file:
    try:
        if upload_file.name.endswith('.csv'):
            df = pd.read_csv(upload_file)
        elif upload_file.name.endswith('.xlsx') or upload_file.name.endswith('.xls') or upload_file.name.endswith('.xlsb') or upload_file.name.endswith('.xlsm'):
            df = pd.read_excel(upload_file)
        elif upload_file.name.endswith('.txt'):
            df = pd.read_csv(upload_file, sep='\t')
        else:
            st.error(idiom("Formato de arquivo não suportado.", "Unsupported file format."))
        st.sidebar.success(idiom("Dados carregados com sucesso!", "Data loaded successfully!"))
    except Exception as e:
        st.error(idiom("Erro ao ler arquivo.", "Error reading file."))

elif example_button:
    df = loading_example_dataset()
    st.sidebar.info(idiom("Utilizando dados fictícios de demonstração.", "Using fictitious demonstration data"))

# --- DASHBOARD (Before calculation) ---
if df is not None:
    st.subheader(idiom("📋 Visão Geral dos Dados", "📋 Data Overview"))
    st.dataframe(df, hide_index=True, use_container_width=True)

    with st.container(border=True):
        st.subheader(idiom("⚙️ Mapeamento de Vendas", "⚙️ Sales Mapping"))
        st.markdown("")
        st.success(idiom("👇 Indique as colunas do seu extrato de vendas para que o sistema calcule o perfil de cada cliente.", "👇 indicate the columns of your sales statement for the system to calculate the customer profile."))

        st.markdown("")

        # Set columns for user choose related of his own dataset
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            col_id = st.selectbox(idiom("Coluna de ID/NOME do Cliente", "Customer ID/Name Column"), df.columns, index=1)
            
        with col2:
            col_date = st.selectbox(idiom("Coluna da DATA da Venda", "Sale Date Column"), df.columns, index=2)
            
        with col3:
            col_cat = st.selectbox(idiom("Coluna da CATEGORIA do Produto", "Product Category Column"), df.columns, index=4)
        
        with col4:
            col_value = st.selectbox(idiom("Coluna do VALOR da Venda (R$)", "Sale Value Column (R$)"), df.columns, index=3)
        

    try:

        # --- DASHBOARD (After calculation) ---
        if st.button(idiom("🚀 Processar e Calcular RFM", "🚀 Process and Calculate RFM"), type="primary"):
            st.session_state['processado'] = True
            with st.spinner(idiom("Analisando todas as vendas...", "Analyzing all sales...")):
                time.sleep(1)

        if st.session_state.get('processado', False):

            # --- Error prevention ---
            try:

                df[col_date] = pd.to_datetime(df[col_date], errors='coerce')
                
                if df[col_value].dtype != 'float64':
                    df[col_value] = df[col_value].astype(str).str.replace('R$', '', regex=False).str.replace('.', '', regex=False).str.replace(',', '.').str.strip()
                df[col_value] = pd.to_numeric(df[col_value], errors='coerce')
                
                # Safety lock
                if df[col_date].isna().all() or df[col_value].isna().all():
                    st.error(idiom(
                        "🚨 Ops! Parece que você selecionou alguma coluna errada. O cálculo foi interrompido.", 
                        "🚨 Oops! It looks like you selected the some of the columns. The calculation was stopped."
                    ))
                    st.stop()

            except Exception as e:
                st.error(f"{idiom('Erro ao formatar as colunas:', 'Error formatting columns:')} {e}")
                st.stop()
            # ---------------------------------------------------

            last_sale_date = df[col_date].max()

            # Dataframe grouped per col_id
            df_rfm = df.groupby(col_id).agg({
                col_date: lambda x: (last_sale_date - x.max()).days,
                col_value: 'sum',
                col_id: 'count'
            })

            df_rfm.rename(columns={
                col_date: idiom("Recência (Dias)", "Recency (Days)"),
                col_value: idiom('Monetário (R$)', 'Monetary (R$)'),
                col_id: idiom('Frequência (Vezes)', 'Frequency (Times)')
            }, inplace=True)


            df_rfm["R_Score"] = pd.qcut(df_rfm[idiom("Recência (Dias)", "Recency (Days)")].rank(method="first"), q=5, labels=[5, 4, 3, 2, 1], duplicates="drop")
            df_rfm["M_Score"] = pd.qcut(df_rfm[idiom("Monetário (R$)", "Monetary (R$)")].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5], duplicates="drop")
            df_rfm["F_Score"] = pd.qcut(df_rfm[idiom("Frequência (Vezes)", "Frequency (Times)")].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5], duplicates="drop")
            
            df_rfm["RFM_Score"] = df_rfm["R_Score"].astype(str) + df_rfm["F_Score"].astype(str) + df_rfm["M_Score"].astype(str)

            # RMF rule : 

            ## Divide clients for 5 groups (quintiles), assigning notes 1 to 5
            # 1. Recency (R_Score): Inverted order [5, 4, 3, 2, 1].
            # - Less time (days) since the last purchase, the higher the better.
            # 2. Frequency (F_Score): Ascending order [1, 2, 3, 4, 5].
            # - More purchases, the higher the better.
            # 3. Monetary (M_Score): Ascending order [1, 2, 3, 4, 5].
            # - More money spent, the higher the better.
            p_champ = idiom('🏆 Campeões', '🏆 Champions')
            p_new = idiom('🌟 Novos & Promissores', '🌟 New & Promising')
            p_risky = idiom('⚠️ Em Risco', '⚠️ At Risk')
            p_hibernating = idiom('💤 Hibernando', '💤 Hibernating')
            p_regular = idiom('🔄 Regulares', '🔄 Regulars')

            # Naming the groups of RFM
            def rfm_segment(row):
                rfm = row['RFM_Score']
                if rfm[0] in ['5','4'] and rfm[1] in ['5','4'] and rfm[2] in ['5','4']:
                    return p_champ, 1
                elif rfm[0] in ['5','4'] and rfm[1] in ['1','2']:
                    return p_new, 2
                elif rfm[1] in ['5','4'] and rfm[2] in ['5','4'] and rfm[0] in ['1','2']:
                    return p_risky, 3
                elif rfm[0] in ['1'] and rfm[1] in ['1']:
                    return p_hibernating, 4
                else:
                    return p_regular, 5
            
            # Function for create message on whatsapp
            def whatsapp_message(row):
                client = row.name
                profile = row[idiom('Perfil_cliente', 'Profile')]

                if profile == p_champ:
                    return idiom(
                        f"Olá {client}, tudo bem? Você faz parte do nosso seleto grupo de clientes VIP, e queremos reconhecer essa parceria! Liberamos um acesso antecipado às nossas novidades e um cupom exclusivo de 15% OFF. Como podemos te ajudar hoje? 💎",
                        f"Hello {client}, how are you? This is [Your Company]. You're part of our select VIP client group, and we want to reward this partnership! We've unlocked early access to our new arrivals and an exclusive 15% OFF coupon. How can we help you today? 💎"
                    )
                
                elif profile == p_risky:
                    return idiom(
                        f"Olá {client}, como estão as coisas? Notamos que faz um tempo desde a nossa última conversa. Muita coisa mudou por aqui e trouxemos novidades que podem te interessar. Para celebrar seu retorno, ativamos uma condição especial na sua conta. Tem 1 minutinho para conferir? 🤝",
                        f"Hello {client}, how have you been? We noticed it's been a while since we last spoke. A lot has changed here, and we have new arrivals that might interest you. To celebrate your return, we've activated a special condition on your account. Got a minute to check it out? 🤝"
                    )
                
                elif profile == p_new:
                    return idiom(
                        f"Olá {client}! Ficamos muito felizes com a sua recente escolha pela nossa marca. Para garantir que sua experiência continue incrível, preparamos uma curadoria de produtos que combinam com você, além de um bônus de boas-vindas na sua próxima compra. Podemos te mostrar? ✨",
                        f"Hello {client}! We're thrilled with your recent choice of our brand. To ensure your experience remains amazing, we've curated some products that match your style, plus a welcome bonus on your next purchase. Can we show you? ✨"
                    )
                
                elif profile == p_hibernating:
                    return idiom(
                        f"Olá {client}! Valorizamos muito o histórico que construímos juntos. Como não nos falamos há algum tempo, preparamos uma oferta de reativação imperdível: 20% OFF em todo o catálogo para você atualizar seu estoque com a gente. Vamos reativar essa parceria? 🚀",
                        f"Hello {client}! We highly value the history we've built together. Since we haven't spoken in a while, we've prepared an unmissable reactivation offer: 20% OFF our entire catalog for you to restock with us. Shall we reactivate this partnership? 🚀"
                    )

                else: # Regulares
                    return idiom(
                        f"Olá {client}, excelente dia! Passando para agradecer a confiança contínua no nosso trabalho. Separamos algumas recomendações estratégicas baseadas nas suas últimas escolhas. Quer dar uma olhada no que separamos para você? 📦",
                        f"Hello {client}, hope you're having a great day! Dropping by to thank you for your continued trust in our work. We've set aside some strategic recommendations based on your past choices. Would you like to see what we have for you? 📦"
                    )
                
                

            df_rfm[idiom(['Perfil_cliente', 'Prioridade'], ['Profile', 'Priority'])] = df_rfm.apply(rfm_segment, axis=1, result_type='expand')

            df_rfm[idiom('Mensagem', 'Message')] = df_rfm.apply(whatsapp_message, axis=1)
            df_rfm['Link_WhatsApp'] = df_rfm[idiom('Mensagem', 'Message')].apply(
                lambda x: f"https://api.whatsapp.com/send?text={urllib.parse.quote(x)}"
            )

            sheet_kpis, sheet_produtos, sheet_crm, sheet_dados = st.tabs([
                idiom("📊 Visão Geral", "📊 Overview"), 
                idiom("🛒 Produtos", "🛒 Products"), 
                idiom("💬 Campanhas (CRM)", "💬 Campaigns (CRM)"),
                idiom("📋 Dados brutos processados", "📋 Clean Raw Data")
            ])
            
            with sheet_kpis:
            # --- Results panel ---
                with st.container(border=True):
                    st.markdown(
                        f"""
                        <h2 style='text-align: center; background-color: #1E3A8A; color: #FFFFFF; padding: 10px; border-radius: 10px;'>
                            {idiom("ANÁLISE DE PERFIL DE CLIENTES", "CLIENT PROFILE ANALYSIS")}
                        </h2>
                        """, 
                        unsafe_allow_html=True
                    )

                    st.markdown("")

                    counts = df_rfm[idiom('Perfil_cliente', 'Profile')].value_counts().sort_values(ascending=False)
                    total_clients = counts.sum()

                    col_total, col_barras = st.columns([1.5, 4])

                    with col_total:
                        st.markdown(f"""
                        <div style="text-align: center; padding: 12px 10px; background-color: rgba(51, 65, 85, 0.7); border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.15); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); height: 100%;">
                            <p style="font-size: 16px; color: #cbd5e1; margin-bottom: 0px;">{idiom("Total de Clientes", "Total Clients")}</p>
                            <p style="font-size: 52px; font-weight: bold; color: #ffffff; margin-top: -10px; margin-bottom: 0px;">{total_clients}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_barras:
                        df_kpis_barras = pd.DataFrame({
                            idiom("Perfil", "Profile"): [p_champ, p_new, p_risky, p_hibernating, p_regular],
                            idiom("Quantidade", "Quantity"): [
                                counts.get(p_champ, 0)/total_clients,
                                counts.get(p_new, 0)/total_clients,
                                counts.get(p_risky, 0)/total_clients,
                                counts.get(p_hibernating, 0)/total_clients,
                                counts.get(p_regular, 0)/total_clients
                            ]
                        })

                        st.markdown("")
                        st.markdown("")
                        
                        st.dataframe(
                            df_kpis_barras.set_index(idiom("Perfil", "Profile")).T,
                            hide_index=True,
                            use_container_width=True,
                            column_config={
                                p_champ: st.column_config.ProgressColumn(format="percent", min_value=0, max_value=1, color="green"),
                                p_new: st.column_config.ProgressColumn(format="percent", min_value=0, max_value=1, color="orange"),
                                p_risky: st.column_config.ProgressColumn(format="percent", min_value=0, max_value=1, color="red"),
                                p_hibernating: st.column_config.ProgressColumn(format="percent", min_value=0, max_value=1, color="grey"),
                                p_regular: st.column_config.ProgressColumn(format="percent", min_value=0, max_value=1, color="blue")
                            }
                        )

                    clientes_por_perfil = df_rfm.groupby(idiom('Perfil_cliente', 'Profile')).apply(lambda x: list(x.index)).to_dict()

                    st.markdown("")
                    df_kpis_list = pd.DataFrame({
                        idiom("Perfil", "Profile"): [p_champ, p_new, p_risky, p_hibernating, p_regular],
                        idiom("Lista de Clientes", "Client List"): [
                            clientes_por_perfil.get(p_champ, []),
                            clientes_por_perfil.get(p_new, []),
                            clientes_por_perfil.get(p_risky, []),
                            clientes_por_perfil.get(p_hibernating, []),
                            clientes_por_perfil.get(p_regular, [])
                        ]
                    })

                    st.dataframe(
                        df_kpis_list,
                        hide_index=True,
                        use_container_width=True,
                        column_config={
                            idiom("Lista de Clientes", "Client List"): st.column_config.ListColumn(
                                idiom("Clientes no Perfil", "Clients in Profile")
                            )
                        }
                    )

            with sheet_produtos:
                df_sales_by_profile = df.merge(
                    df_rfm[[idiom('Perfil_cliente', 'Profile')]],
                    how='left',
                    left_on=col_id,
                    right_index=True
                )

                profile = st.selectbox(idiom("Selecione o perfil de cliente", "Select the client profile"), (p_champ, p_new, p_risky, p_hibernating, p_regular), index=0)

                c1,c2,c3 = st.columns(3)
                with c2:
                    vision = st.radio('',
                        [idiom("📦 Volume (Quantidade)", "📦 Volume (Quantity)"), idiom("💰 Faturamento (Valor)", "💰 Revenue (Value)")],
                        horizontal=True
                    )

                df_categories = df_sales_by_profile[df_sales_by_profile[idiom('Perfil_cliente', 'Profile')] == profile]

                # 1. Contamos e transformamos o resultado em uma tabela limpa
                if vision == idiom("📦 Volume (Quantidade)", "📦 Volume (Quantity)"):
                    categ_counts = df_categories[col_cat].value_counts().reset_index()
                    eixo_y = idiom('Quantidade', 'Quantity')
                else:
                    categ_counts = df_categories.groupby(col_cat)[col_value].sum().reset_index()
                    eixo_y = idiom('Faturamento (R$)', 'Revenue (R$)')

                # Nomeamos a coluna dinamicamente
                categ_counts.columns = [idiom('Categoria', 'Category'), eixo_y]

                st.markdown(idiom(f"### 🛒 O que os seus clientes {profile[2:]} estão comprando?", f"### 🛒 What are your {profile[2:]} clients buying?"))
                
                fig = px.bar(
                    categ_counts, 
                    x=idiom('Categoria', 'Category'), 
                    y=eixo_y,
                    text_auto='.2s' if "Valor" in vision or "Revenue" in vision else True,
                    color=eixo_y,
                    color_continuous_scale="Blues"
                )
                fig.update_layout(
                    xaxis={'categoryorder':'total descending'},
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    coloraxis_showscale=False,
                    margin=dict(t=20, b=20, l=0, r=0)
                )
                fig.update_yaxes(showgrid=False, visible=False) # Retira a linha e os números da esquerda
                st.plotly_chart(fig, use_container_width=True)
            
            with sheet_crm:
                st.markdown(idiom("### 📲 Central de Ação Rápida", "### 📲 Quick Action Center"))
                st.write(idiom("Filtre o perfil e dispare as mensagens personalizadas com um clique.", "Filter the profile and trigger personalized messages with one click."))
                
                # Seletor de Perfil exclusivo para o CRM
                perfil_crm = st.selectbox(
                    idiom("Selecione o público-alvo da campanha:", "Select the campaign target audience:"), 
                    (p_champ, p_new, p_risky, p_hibernating, p_regular), 
                    index=2
                )
                
                # Filtra a base e mostra as colunas que importam
                df_crm = df_rfm[df_rfm[idiom('Perfil_cliente', 'Profile')] == perfil_crm].reset_index()
                
                # Exibe uma tabela limpa só com Cliente, Valor e o Botão
                st.dataframe(
                    df_crm[[col_id, idiom('Monetário (R$)', 'Monetary (R$)'), idiom('Mensagem', 'Message'), 'Link_WhatsApp']],
                    hide_index=True,
                    use_container_width=True,
                    column_config={
                        idiom('Monetário (R$)', 'Monetary (R$)'): st.column_config.NumberColumn(format="R$ %.2f"),
                        'Link_WhatsApp': st.column_config.LinkColumn(
                            label=idiom("💬 Ação", "💬 Action"),
                            display_text=idiom("📲 Enviar WhatsApp", "📲 Send WhatsApp")
                        )
                    }
                )

            # RAW BASE AFTER CALCULATION
            with sheet_dados:
                df_rfm[idiom('Mensagem', 'Message')] = df_rfm.apply(whatsapp_message, axis=1)

                df_rfm['Link_WhatsApp'] = df_rfm[idiom('Mensagem', 'Message')].apply(
                    lambda x: f"https://api.whatsapp.com/send?text={urllib.parse.quote(x)}"
                )


                st.dataframe(df_rfm.reset_index().sort_values(by=idiom('Prioridade', 'Priority')),
                            hide_index=True,
                            use_container_width=True,
                            column_config={
                                'R_Score': None,
                                'M_Score': None,
                                'F_Score': None,
                                'RFM_Score': None,
                                idiom('Mensagem', 'Message'): None,
                                idiom('Prioridade', 'Priority'): None,
                                idiom('Monetário (R$)', 'Monetary (R$)'): st.column_config.NumberColumn(
                                    format="R$ %.2f"),
                                'Link_WhatsApp': st.column_config.LinkColumn(
                                    label=idiom("💬 Ação", "💬 Action"),
                                    display_text=idiom("📲 Enviar WhatsApp", "📲 Send WhatsApp")
                                )
                            })
                
                # --- DOWNLOAD FUNCTION ---
                st.markdown(idiom("### 📥 Exportar Resultados", "### 📥 Export Results"))
                
                df_export = df_rfm.reset_index().sort_values(by=idiom('Prioridade', 'Priority'))
                columns_remove = ['R_Score', 'M_Score', 'F_Score', 'RFM_Score', idiom('Prioridade', 'Priority'), 'Link_WhatsApp', idiom('Mensagem', 'Message')]
                df_export = df_export.drop(columns=columns_remove, errors='ignore')

                memory = io.BytesIO()
                
                with pd.ExcelWriter(memory, engine='openpyxl') as writer:
                    df_export.to_excel(writer, index=False, sheet_name='Clientes_RFM')
                
                st.download_button(
                    label=idiom("📥 Baixar Base Completa (Excel)", "📥 Download Full Database (Excel)"),
                    data=memory.getvalue(),
                    file_name='base_clientes_classificada.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    type="primary"
                )

    except Exception as e:
        st.error(f"{idiom('Erro interno:', 'Internal error:')} {e}")

else:
    st.info(idiom("👈 Comece fazendo upload do arquivo ou selecionando o modo Exemplo na barra lateral.", "👈 Start by uploading a file or selecting Example mode in the sidebar."))