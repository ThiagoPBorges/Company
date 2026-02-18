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
    arquivo_upload = st.file_uploader("Suba sua planilha de vendas (Excel/CSV/TXT)", type=['xls', 'xlsb', 'xlsm', 'csv', 'txt'])
    
    st.markdown("---")
    
    usar_exemplo = st.checkbox("Não tem dados? Usar Exemplo", value=False)

# --- LÓGICA DE CARREGAMENTO ---
df = None

if arquivo_upload:
    try:
        if arquivo_upload.name.endswith('.csv'):
            df = pd.read_csv(arquivo_upload)
        elif arquivo_upload.name.endswith('.xlsx') or arquivo_upload.name.endswith('.xls') or arquivo_upload.name.endswith('.xlsb') or arquivo_upload.name.endswith('.xlsm'):
            df = pd.read_excel(arquivo_upload)
        elif arquivo_upload.name.endswith('.txt'):
            df = pd.read_csv(arquivo_upload, sep='\t')
        else:
            st.error("Formato de arquivo não suportado.")
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

# ... (Seu código anterior de carga do df continua igual)

st.markdown("---")
st.subheader("⚙️ Mapeamento de Vendas")
st.info("Indique as colunas do seu extrato de vendas para que o sistema calcule o perfil de cada cliente.")

col1, col2, col3 = st.columns(3)

with col1:
    col_id = st.selectbox("Coluna de ID/NOME do Cliente", df.columns, index=0)
    
with col2:
    col_data = st.selectbox("Coluna da DATA da Venda", df.columns, index=1)
    
with col3:
    col_valor = st.selectbox("Coluna do VALOR da Venda (R$)", df.columns, index=2)

# --- CÁLCULO ---
if st.button("🚀 Processar e Calcular RFM", type="primary"):
    with st.spinner("Analisando todas as vendas..."):
        time.sleep(5)
        
        try:
            # Tratamento de Datas
            df[col_data] = pd.to_datetime(df[col_data], errors='coerce')
            
            # Data de referência (Dia seguinte à última venda da planilha)
            ultima_venda = df[col_data].max() + pd.Timedelta(days=1)
            
            # GROUPBY
            df_rfm = df.groupby(col_id).agg({
                # Recência: Hoje - Máxima Data
                col_data: lambda x: (ultima_venda - x.max()).days,
                # Frequência: Contagem de linhas
                col_id: 'count',  
                # Monetário: Soma dos valores                              
                col_valor: 'sum'                                
            }).rename(columns={
                col_data: 'Recencia',
                col_id: 'Frequencia',
                col_valor: 'Monetario'
            }).reset_index()
            
            # Exibição do Resultado
            st.success("✅ Cálculo realizado com sucesso!")
            st.markdown("### 📊 Tabela RFM Calculada")
            st.caption(f"Transformamos {len(df)} vendas em {len(df_rfm)} clientes únicos.")
            
            st.dataframe(df_rfm, hide_index=True, use_container_width=True)
            
            # Dica para o usuário entender o que aconteceu
            with st.expander("ℹ️ Como esse cálculo foi feito?"):
                st.write(f"""
                O sistema agrupou as vendas por **{col_id}**:
                - **Recência:** Calculada subtraindo a última compra encontrada da data {ultima_venda.date()}.
                - **Frequência:** Contamos quantas vezes o cliente apareceu na planilha.
                - **Monetário:** Somamos todos os valores da coluna **{col_valor}**.
                """)

            # Salva no session_state para não perder se clicar em outro lugar
            st.session_state['df_rfm'] = df_rfm
            
        except Exception as e:
            st.error(f"Erro no cálculo: {e}. Verifique se as colunas selecionadas contêm números e datas válidos.")
    # --- ETAPA 3: SEGMENTAÇÃO (Dar notas de 1 a 5) ---

    # Verifica se o cálculo RFM já foi feito e está na memória
    if 'df_rfm' in st.session_state:
        df_rfm = st.session_state['df_rfm']
        
        st.divider()
        st.subheader("🏆 Segmentação de Clientes")
        st.info("Agora vamos dar notas de 1 a 5 para cada cliente comparando eles entre si.")

        # CRIANDO AS NOTAS (SCORES)
        # Usamos rank(pct=True) para saber em qual % o cliente está (0 a 100%)
        # Depois multiplicamos por 5 para ter uma nota de 1 a 5
        
        # R (Recência): Lógica INVERSA (Quanto menor o dias, MAIOR a nota)
        df_rfm['R_Score'] = 5 - (df_rfm['Recencia'].rank(pct=True, method='first') * 5).astype(int)
        
        # F (Frequência): Lógica DIRETA (Quanto mais, melhor)
        df_rfm['F_Score'] = (df_rfm['Frequencia'].rank(pct=True, method='first') * 5).astype(int) + 1
        
        # M (Monetário): Lógica DIRETA (Quanto mais, melhor)
        df_rfm['M_Score'] = (df_rfm['Monetario'].rank(pct=True, method='first') * 5).astype(int) + 1
        
        # Ajuste fino: O rank pode gerar nota 6 em casos raros de borda, garantimos o teto 5
        df_rfm['F_Score'] = df_rfm['F_Score'].apply(lambda x: 5 if x > 5 else x)
        df_rfm['M_Score'] = df_rfm['M_Score'].apply(lambda x: 5 if x > 5 else x)

        # CRIA O "SCORE FINAL" (Ex: "555" é o cliente perfeito)
        # Somamos R + F + M para ter uma "Média Geral"
        df_rfm['Score_Geral'] = df_rfm[['R_Score', 'F_Score', 'M_Score']].mean(axis=1)
        
        # DEFININDO OS SEGMENTOS (A Regra de Negócio)
        def definir_segmento(row):
            r = row['R_Score']
            f = row['F_Score']
            m = row['M_Score']
            media = row['Score_Geral']
            
            # Regras Clássicas de RFM
            if r >= 4 and f >= 4 and m >= 4:
                return "💎 Campeão"
            elif r >= 3 and f >= 3:
                return "😊 Leal"
            elif r >= 4 and f <= 2:
                return "🆕 Novo Promissor"
            elif r <= 2 and f >= 4:
                return "⚠️ Em Risco"
            elif r <= 2 and f <= 2:
                return "💤 Hibernando/Perdido"
            else:
                return "🤔 Precisa de Atenção"

        df_rfm['Segmento'] = df_rfm.apply(definir_segmento, axis=1)

        # --- MOSTRAR O RESULTADO ---
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("### 🕵️ Visão Detalhada")
            # Mostra as colunas principais ordenadas pelos melhores clientes
            st.dataframe(
                df_rfm[['Score_Geral', 'Segmento', 'Recencia', 'Frequencia', 'Monetario']].sort_values('Score_Geral', ascending=False),
                use_container_width=True
            )
            
        with col2:
            st.write("### 📊 Distribuição")
            # Conta quantos clientes tem em cada grupo
            contagem = df_rfm['Segmento'].value_counts()
            st.bar_chart(contagem)
            
        # Atualiza o session_state com a tabela completa
        st.session_state['df_rfm_final'] = df_rfm