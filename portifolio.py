import streamlit as st

## CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Thiago P.Borges | Data & Business Solutions",
    page_icon="📊",
    layout="wide"
)

# Remove a margem padrão do app
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.write(f"**Olá, empresário(a) !**")
    st.caption("✅ Estou disponível para novos projetos")
    
    st.divider()
    
    # Área de Login
    st.header("🔒 Área do Cliente")
    st.info("Acesse seu projeto abaixo.")

    if "nome_usuario" not in st.session_state:
        st.session_state["nome_usuario"] = "Visitante"
    
    if st.session_state["nome_usuario"] == "Visitante":
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar no Sistema"):

            users = st.secrets["usuarios"]
    
    
            if usuario in users and users[usuario] == senha:
                st.session_state["nome_usuario"] = usuario
                st.success(f"Bem-vindo, {usuario.capitalize()}!")
                st.balloons()
            else:
                st.error("Acesso restrito a clientes ativos.")
                st.caption("Quer ter seu próprio acesso? Fale comigo.")

    st.divider()

col_whats, col_linked = st.sidebar.columns(2)

numero_whatsapp = "5519992814477"
mensagem_ola = "Olá Thiago! Vi seu portfólio e gostaria de saber mais."

link_whatsapp = f"https://wa.me/{numero_whatsapp}?text={mensagem_ola.replace(' ', '%20')}"

with col_whats:
        ## BOTÃO WHATSAPP
        st.markdown(f"""
        <a href="{link_whatsapp}" target="_blank" style="text-decoration: none;">
        <button style="
            width: 100%;
            background-color: #25D366; 
            color: white; 
            border: none; 
            padding: 8px 0px; 
            font-size: 14px; 
            border-radius: 5px; 
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: sans-serif;
            font-weight: bold;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="18" height="18" style="margin-right: 5px;">
            WhatsApp
        </button>
        </a>
        """, unsafe_allow_html=True)

with col_linked:
        ## BOTÃO LINKEDIN
        link_linkedin = "https://www.linkedin.com/in/thiagopborges/"
        st.markdown(f"""
        <a href="{link_linkedin}" target="_blank" style="text-decoration: none;">
            <button style="
                width: 100%;
                background-color: #0077B5;
                color: white;
                padding: 8px 0px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                display: flex;
                justify-content: center;
                align-items: center;
                font-family: sans-serif;
                font-weight: bold;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" width="18" height="18" style="margin-right: 5px;">
                LinkedIn
            </button>
        </a>
        """, unsafe_allow_html=True)

# --- INTRODUÇÃO DA PÁGINA ---

with st.container(border=True):

    espaco, intro2,espaco, foto3 = st.columns([0.01,9,1,3.4])

    with intro2:
            st.title("Transformando dados em eficiência.")
            
            # SUBTÍTULO COM DESTAQUE DE COR (Badge Nativo)
            st.markdown("### 🎓 Administração | 💻 Análise de Dados")
            st.write("")
            
            # AQUI ESTÁ A MUDANÇA DO TEXTO "TRAVAR PLANILHAS"
            # Usamos um visual de "Citação" ou "Destaque"
            st.markdown("""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #000000;'>
                <p style='font-size: 18px; margin: 0; color: #31333F;'>
                <b>"Não sou apenas um Analista de Dados, sou um Administrador com o domínio da tecnologia."</b><br>
                <span style='font-size: 16px; color: #555;'>
                Combino a visão estratégica de negócios com a precisão técnica da programação para eliminar ineficiências.
                </span>
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.write("#####")

            col_m1, col_m2, col_m3, = st.columns(3)

            with col_m1:
                st.metric(label="Foco Principal", value="ROI & Lucro", delta="Resultado")
            with col_m2:
                st.metric(label="Projetos", value="360º do Negócio", delta="Exclusivo")
            with col_m3:
                st.metric(label="Primeiro Passo", value="Diagnóstico Grátis",delta="Agendar Agora")

    with foto3:

        st.image(image="Utilities/Foto.png",width=300, output_format="PNG")

    st.write("")

st.write("")

# --- ESTILO DAS ABAS (CSS) ---
st.markdown("""
<style>
    /* Aumenta o tamanho da fonte do rótulo das abas */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 25px; /* Tamanho da fonte */
        font-weight: bold; /* Deixa em negrito (opcional) */
    }
""", unsafe_allow_html=True)

# --- CORPO DA PÁGINA ---
tab_sobre, tab_servicos, tab_portfolio = st.tabs(["🙋🏻‍♂️ Sobre Mim", "🛠️ O que eu faço", "📊 Meus Projetos"])

with tab_sobre:
    col_texto,esp1,col_skills1,esp2, col_skills2 = st.columns([4,0.2,2,0.2,2])

    with col_texto:
        st.markdown("")
        st.markdown("### 🚀 Onde Negócios e Dados se Encontram")
        st.markdown("")
        st.info("""
        "Não sou apenas um Analista de Dados, sou um Administrador com o domínio da tecnologia."
        """)
        st.markdown("######")
        st.markdown("""
        Enquanto muitos focam apenas no código, meu foco está no **:green-background[Resultado ao seu negócio]**. 
        Identifico onde sua operação perde tempo e dinheiro (gargalos) e construo a solução técnica exata para resolver isso.
        
        Combino a visão estratégica de negócios com uma gama de habilidades técnicas robustas para transformar planilhas manuais 
        e processos lentos em **:green-background[dashboards de decisão e automações inteligentes]**.
        """)

with col_skills1:
        st.markdown("")
        # --- BLOCO 1: TECNOLOGIA
        st.markdown("### 🛠️ Tecnologias")
        
        st.write("**PYTHON**")
        st.progress(80)
        
        st.write("**POWER BI & DAX**")
        st.progress(90)
        
        st.write("**SQL & BANCO DE DADOS**")
        st.progress(85)
        
        st.write("**EXCEL AVANÇADO**")
        st.progress(95)

with col_skills2:

    st.markdown("")
    st.markdown("### 💼 Domínio de Negócio")

    st.write("")

    # --- BLOCO 1: VISUALIZAÇÃO & BI (O que o chefe vê) ---
    with st.expander("📊 **Análise de dados**"):
        # --- BLOCO 1: VISUALIZAÇÃO & BI (O que o chefe vê) ---
        with st.expander("📊 **Business Intelligence**"):
            st.markdown("""
            Transformação de dados brutos em narrativa de negócio (**Data Storytelling**):
            
            * 🎨 **Dashboards Estratégicos:** Criação de painéis interativos para monitoramento de OKRs e KPIs de ativos, com foco em UX/UI para facilitar a leitura executiva.
            * 🧠 **Modelagem Avançada:** Domínio de **DAX** e **Linguagem M (Power Query)** para tratamento de dados complexos e relacionamento entre múltiplas tabelas fatos/dimensão.
            * 📈 **Excel Avançado:** Uso de Power Pivot e Macros (VBA) para modelagens financeiras rápidas e cenários de *What-If*.
            """)

        # --- AUTOMAÇÃO & PRODUTIVIDADE ---
        with st.expander("⚙️ **Automação de Processos**"):
            st.markdown("""
            Redução de trabalho manual para foco em análise estratégica (**RPA**):
            
            * 🤖 **Power Automate:** Criação de fluxos para coleta automática de dados, envio de alertas de anomalias e atualização de bases sem intervenção humana.
            * 📱 **Power Apps:** Desenvolvimento de interfaces (formulários) para entrada de dados em campo, garantindo padronização e governança na origem.
            """)

        # --- BLOCO 2: ENGENHARIA & MANIPULAÇÃO (O trabalho pesado) ---
        with st.expander("🐍 **Engenharia de Dados**"):
            st.markdown("""
            Garantia da integridade e disponibilidade da informação (**ETL**):
            * 🧹 **Saneamento de Dados (Pandas/NumPy):** Scripts em Python para limpeza de bases cadastrais, identificando duplicidades e erros de preenchimento.
            * 🗄️ **Consultas Estruturadas (SQL):** Extração de dados via *queries* otimizadas (JOINS, CTEs, Window Functions) para alimentar os relatórios de gestão.
            * 🔗 **Integração de Fontes:** Consolidação de dados vindos de diversas origens (SAP, Planilhas, Sistemas Legados) em uma única fonte da verdade.
            """)
    
    st.write("")

    # --- ADMINISTRAÇÃO ---
    with st.expander("🎓 **Administração & Processos**"):
        st.markdown("""
        Aplicação da visão sistêmica para conectar tecnologia e negócio:
        
        * 🔄 **Mapeamento de Processos:** Identificação de gargalos em fluxos de trabalho para propor automações com Power Automate/Python.
        * 🎯 **Gestão por Indicadores:** Definição e acompanhamento de KPIs e OKRs para garantir o alinhamento entre a operação e a estratégia da empresa.
        * 🏢 **Visão Organizacional:** Entendimento da interdependência entre áreas (Financeiro, Operações e TI) para liderar projetos transversais.
        """)

    st.write("")

    # --- FINANÇAS ---
    with st.expander("💰 **Contabilidade & Finanças**"):
        st.markdown("""
        Foco na integridade dos dados financeiros para suporte à decisão:
        
        * 📉 **Análise de Demonstrativos:** Leitura e interpretação de DRE e Fluxo de Caixa para diagnóstico de saúde financeira e eficiência operacional.
        * ⚖️ **Conciliação Físico-Contábil:** Cruzamento de bases de dados para garantir que o inventário físico reflita o Balanço Patrimonial.
        * 💵 **Gestão Orçamentária:** Classificação correta de custos (CAPEX vs OPEX) e monitoramento de desvios (Orçado x Realizado).
        """)

    st.write("")

    # --- GESTÃO DE ATIVOS ---
    with st.expander("⚡ **Gestão de Ativos**"):
        st.markdown("""
        Transformo dados físicos e contábeis em **estratégia financeira**:
        
        * 📊 **Inteligência Visual (Power BI):** Desenvolvimento de dashboards para consolidar indicadores de performance (OKRs) e métricas de capitalização, acelerando em até 70% o acesso à informação.
        * ⚙️ **Automação de Processos (Python/Power Apps/Automate):** Implantação de RPA para consolidação de indicadores e redução de retrabalho operacional, garantindo a integridade dos dados na ponta.
        * 🐍 **Conciliação Avançada (Python & SQL):** Scripts para cruzamento de grandes bases de dados e conciliação de receita operacional, apoiando a tomada de decisão.
        """)

with tab_servicos:
    st.markdown("")
    st.markdown("### 💼 Como posso impulsionar seu negócio?")
    st.markdown("")
    
    col_a, col_b = st.columns(2)
    
    # --- CARD 1: AUTOMAÇÃO ---
    with col_a:
        with st.container(border=True):
            st.markdown("### 🤖 Automação de Rotinas")
            st.markdown("*:grey[- Pare de desperdiçar talento humano com trabalho de robô.]*")

            st.write("""
            :blue-background[Crio scripts que executam tarefas repetitivas automaticamente, sem erros.]
            """)

            st.divider()
            
            st.write("""
            **Principais aplicações:**
            - ✅ **Financeiro:** Baixar e organizar Notas Fiscais (XML/PDF).
            - ✅ **Comercial:** Disparo automático por e-mail/WhatsApp.
            - ✅ **Sistêmico:** Preencher formulários em sistemas.
            - ✅ **Mercado:** Monitoramento de preços da concorrência na internet (Web Scraping).
            """)
            
            st.markdown("")
            
            with st.popover("🛠️ Ver Tecnologias Utilizadas"):
                st.markdown("**Python** (Pandas, Selenium, Playwright)")
                st.markdown("**Power Automate** (Fluxos Cloud/Desktop)")
                st.markdown("**Power Automate** (Integração com Office 365)")

    # --- CARD 2: B.I. & DASHBOARDS ---
    with col_b:
        with st.container(border=True):
            st.markdown("### 📊 Inteligência de Dados (B.I.)")
            st.markdown("*:grey[Transforme planilhas gigantes em decisões de 1 minuto.]*")

            st.write("""
            :blue-background[Desenvolvo painéis visuais que mostram a saúde do seu negócio em tempo real.]
            """)

            st.divider()
            
            st.write("""
            **Principais aplicações:**
            - ✅ **Gestão Financeira:** (DRE, Fluxo de Caixa, Inadimplência).
            - ✅ **Comercial:** (Metas, Comissões, Churn).
            - ✅ **Operacional:** (Estoque, Logística, Produção).
            - ✅ **Simulação:** Cenários de "E se?" (E se eu aumentar o preço em 5%?).
            """)
            
            st.markdown("")
            
            with st.popover("🛠️ Ver Tecnologias Utilizadas"):
                st.markdown("**Power BI** (DAX avançado, Power Query)")
                st.markdown("**Streamlit** (Dashboards Web Customizados)")
                st.markdown("**SQL** (Modelagem de Dados e ETL)")

    st.markdown("")
    st.write("##### 💡 :yellow-background[**Dica:** Não sabe qual você precisa? Geralmente começamos organizando os dados (Automação) para depois visualizá-los (B.I.).]")


with tab_portfolio:
    st.write("")
    st.markdown("### 🧩 Projetos em Destaque")
    st.write("Interaja com as ferramentas reais que desenvolvi para resolver problemas de negócio.")
    st.markdown("---")

    # --- PROJETO 1: DETECTOR DE VIPS (RFM) ---
    with st.container(border=True):
        col_img, col_info = st.columns([1, 2])
        
        with col_img:
            # Colocar aqui um GIF do projeto funcionando
            # Por enquanto, usamos um ícone gigante ou uma imagem estática
            st.markdown("## 💎") 
            # st.image("caminho_do_gif.gif") <--- Futuro
        
        with col_info:
            st.subheader("Detector de Oportunidades (RFM)")
            st.markdown("""
            **Foco:** Marketing e Vendas | **Tecnologia:** Python + Pandas
            
            Ferramenta que segmenta sua base de clientes automaticamente.
            Descubra quem são seus **VIPs**, quem está **Em Risco** e gere textos de recuperação para WhatsApp com IA.
            """)
            
            # O BOTÃO PARA A PÁGINA
            st.page_link("pages/1_💎_Detector_de_VIPs.py", label=":blue-background[***Testar Ferramenta Agora***]", icon="🚀")