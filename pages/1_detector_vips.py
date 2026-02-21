import streamlit as st
import pandas as pd
import time
import urllib.parse

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Detector de Clientes VIP",
    page_icon="💎",
    layout="wide"
)

# --- FUNÇÕES DE CARREGAMENTO (ETL) ---
@st.cache_data
def carregar_dados_exemplo():
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

# --- DASHBOARD ---
if df is not None:
    st.subheader("📋 Visão Geral dos Dados")
    st.dataframe(df, hide_index=True, use_container_width=True)
    
    # AQUI ENTRARÁ O CÁLCULO RFM E A IA DEPOIS

    st.markdown("---")
    st.subheader("⚙️ Mapeamento de Vendas")
    st.markdown("")
    st.info("Indique as colunas do seu extrato de vendas para que o sistema calcule o perfil de cada cliente.")

    st.markdown("")
    st.markdown("")

    col1, col2, col3 = st.columns(3)

    with col1:
        col_id = st.selectbox("Coluna de ID/NOME do Cliente", df.columns, index=1)
        
    with col2:
        col_data = st.selectbox("Coluna da DATA da Venda", df.columns, index=2)
        
    with col3:
        col_valor = st.selectbox("Coluna do VALOR da Venda (R$)", df.columns, index=3)

    st.markdown("#####")

    try:

        # --- CALCULATION ---
        if st.button("🚀 Processar e Calcular RFM", type="primary"):
            with st.spinner("Analisando todas as vendas..."):
                time.sleep(7)

            st.divider()

            last_sale_date = df[col_data].max()

            df_rfm = df.groupby(col_id).agg({
                col_data: lambda x: (last_sale_date - x.max()).days,
                col_valor: 'sum',
                col_id: 'count'
            })

            df_rfm.rename(columns={
                col_data: 'Recência (Dias)',
                col_valor: 'Monetário (R$)',
                col_id: 'Frequência (Vezes)'
            }, inplace=True)

            df_rfm["R_Score"] = pd.qcut(df_rfm["Recência (Dias)"].rank(method="first"), q=5, labels=[5, 4, 3, 2, 1], duplicates="drop")
            df_rfm["M_Score"] = pd.qcut(df_rfm["Monetário (R$)"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5], duplicates="drop")
            df_rfm["F_Score"] = pd.qcut(df_rfm["Frequência (Vezes)"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5], duplicates="drop")
            
            df_rfm["RFM_Score"] = df_rfm["R_Score"].astype(str) + df_rfm["F_Score"].astype(str) + df_rfm["M_Score"].astype(str)

            def rfm_segment(row):

                rfm = row['RFM_Score']

                if rfm[0] in ['5','4'] and rfm[1] in ['5','4'] and rfm[2] in ['5','4']:
                    return '🏆 Campeões', 1

                elif rfm[0] in ['5','4'] and rfm[1] in ['1','2']:
                    return '🌟 Novos & Promissores', 2

                elif rfm[1] in ['5','4'] and rfm[2] in ['5','4'] and rfm[0] in ['1','2']:
                    return '⚠️ Em Risco' , 3

                elif rfm[0] in ['1'] and rfm[1] in ['1']:
                    return '💤 Hibernando', 4

                else:
                    return '🔄 Regulares', 5
                
            df_rfm[['Perfil_cliente', 'Prioridade']] = df_rfm.apply(rfm_segment, axis=1, result_type='expand')

            
            with st.container(border=True):
                st.markdown(
                    """
                    <h2 style='text-align: center; background-color: #1E3A8A; color: #FFFFFF; padding: 10px; border-radius: 10px;'>
                        ANÁLISE DE PERFIL DE CLIENTES
                    </h2>
                    """, 
                    unsafe_allow_html=True
                )
                st.markdown("")

                counts = df_rfm['Perfil_cliente'].value_counts()
                total_clientes = counts.sum()

                df_kpis = pd.DataFrame({
                    "Perfil": ["Total_clientes", "🏆 Campeões", "🌟 Novos & Promissores", "⚠️ Em Risco", "💤 Hibernando", "🔄 Regulares"],
                    "Quantidade": [
                        total_clientes,
                        counts.get('🏆 Campeões', 0)/total_clientes,
                        counts.get('🌟 Novos & Promissores', 0)/total_clientes,
                        counts.get('⚠️ Em Risco', 0)/total_clientes,
                        counts.get('💤 Hibernando', 0)/total_clientes,
                        counts.get('🔄 Regulares', 0)/total_clientes
                    ]
                })

                st.dataframe(
                    df_kpis.set_index("Perfil").T,
                    use_container_width=True,
                    column_config={
                        'Total_clientes': st.column_config.ProgressColumn(format="%d", min_value=0, max_value=int(total_clientes), color="grey"),
                        "🏆 Campeões": st.column_config.ProgressColumn(format="percent", min_value=0, max_value=1, color="green"),
                        "🌟 Novos & Promissores": st.column_config.ProgressColumn(format="percent", min_value=0, max_value=1, color="orange"),
                        "⚠️ Em Risco": st.column_config.ProgressColumn(format="percent", min_value=0, max_value=1, color="auto"),
                        "💤 Hibernando": st.column_config.ProgressColumn(format="percent", min_value=0, max_value=1, color="grey"),
                        "🔄 Regulares": st.column_config.ProgressColumn(format="percent", min_value=0, max_value=1, color="blue")
                    }
                )

                clientes_por_perfil = df_rfm.groupby('Perfil_cliente').apply(lambda x: list(x.index)).to_dict()

                # 2. Criamos a tabela vertical completa
                df_kpis_list = pd.DataFrame({
                    "Perfil": ["🏆 Campeões", "🌟 Novos & Promissores", "⚠️ Em Risco", "💤 Hibernando", "🔄 Regulares"],
                    "Lista de Clientes": [
                        clientes_por_perfil.get('🏆 Campeões', []),
                        clientes_por_perfil.get('🌟 Novos & Promissores', []),
                        clientes_por_perfil.get('⚠️ Em Risco', []),
                        clientes_por_perfil.get('💤 Hibernando', []),
                        clientes_por_perfil.get('🔄 Regulares', [])
                    ]
                })

                st.dataframe(
                    df_kpis_list,
                    hide_index=True,
                    use_container_width=True,
                    column_config={
                        "Lista de Clientes": st.column_config.ListColumn(
                            "Clientes no Perfil"
                        )
                    }
                )

    
            def whatsapp_message(row):

                client = row.name
                profile = row['Perfil_cliente']

                if profile == '🏆 Campeões':
                    return f"Olá {client}! Tudo bem? Vimos que você é um dos nossos melhores clientes. Como agradecimento, geramos um cupom de 15% OFF para sua próxima compra! 🎁"
                
                elif profile == '⚠️ Em Risco':
                    return f"Olá {client}! Faz um tempinho que não nos vemos. Sentimos sua falta! Chegaram novidades por aqui, quer dar uma olhada? 👀"
                
                elif profile == '🌟 Novos & Promissores':
                    return f"Olá {client}! Foi muito bom ter você com a gente recentemente. Preparamos algumas recomendações especiais que são a sua cara. Vem ver! ✨"
                
                elif profile == '💤 Hibernando':
                    return f"Oi {client}, sumido! Saudade de ver você por aqui. Para celebrar sua volta, liberamos um desconto exclusivo de 20% em todo o site. Aproveite! 🚀"

                else:
                    # Commom message for regular clients
                    return f"Olá {client}, confira nossas ofertas da semana!"
                
            df_rfm['Mensagem'] = df_rfm.apply(whatsapp_message, axis=1)

            # Transforma o texto em um link clicável do WhatsApp
            df_rfm['Link_WhatsApp'] = df_rfm['Mensagem'].apply(
                lambda x: f"https://api.whatsapp.com/send?text={urllib.parse.quote(x)}"
            )

            with st.expander("📋 Detalhamento (Base Completa)"):
                st.dataframe(df_rfm.reset_index().sort_values(by='Prioridade'),
                            hide_index=True,
                            use_container_width=True,
                            column_config={
                                'R_Score': None,
                                'M_Score': None,
                                'F_Score': None,
                                'RFM_Score': None,
                                'Mensagem': None,
                                'Prioridade': None,
                                # --- A MÁGICA AQUI ---
                                'Link_WhatsApp': st.column_config.LinkColumn(
                                    label="💬 Ação",
                                    display_text="📲 Enviar WhatsApp"
                                )
                            })
                
    
    # --- FUNÇÃO DE DOWNLOAD ---
            st.markdown("### 📥 Exportar Resultados")
            
            # Preparamos o DataFrame para exportação (resetando o index para o nome aparecer como coluna)
            df_export = df_rfm.reset_index().sort_values(by='Prioridade')
            
            # Removemos as colunas de notas que o usuário final não precisa ver
            colunas_para_remover = ['R_Score', 'M_Score', 'F_Score', 'RFM_Score', 'Prioridade']
            df_export = df_export.drop(columns=colunas_para_remover, errors='ignore')

            # Convertendo para CSV (O .encode('utf-8') garante que acentos fiquem corretos)
            csv = df_export.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="📥 Baixar Base Completa (CSV)",
                data=csv,
                file_name='base_clientes_classificada.csv',
                mime='text/csv',
                type="primary"
            )



    except Exception as e:
        st.error("Por favor, verifique o direcionamento da colunas")


else:
    st.info("👈 Comece fazendo upload do arquivo ou selecionando o modo Exemplo na barra lateral.")