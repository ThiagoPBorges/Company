import streamlit as st
from datetime import date

## ----- PAGE CONFIGURATION -----
st.set_page_config(
    page_title="Thiago P.Borges | Data Solutions",
    page_icon="📊",
    layout="wide"
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

# ----- PAGE DESIGN -----
page_style = """
<style>
    /* 1. FUNDO GERAL (Grade Fantasma Suave) */
    [data-testid="stAppViewContainer"] {
        background-color: #fafafa; /* Fundo base: Branco "Off-White" */
        background-image: radial-gradient(#e5e7eb 1px, transparent 1px); /* Pontos cinza muito claro */
        background-size: 24px 24px; /* Espaçamento generoso */
    }

    /* 2. A Barra Lateral (Sidebar) Totalmente Branca */
    [data-testid="stSidebar"] {
        background-color: #00000;
        box-shadow: 2px 0 5px rgba(0,0,0,0.05); /* Sombra sutil para separar do fundo */
        border-right: 1px solid #e0e0e0;
    }

    /* 3. CARTÕES (Containers) - Efeito "Levitação Suave" */
    /* Fundo branco puro sobre o off-white cria contraste elegante */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background-color: #ffffff !important;
        border: 1px solid #f0f0f0 !important; /* Borda ultra-suave */
        border-radius: 12px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.01), 0 2px 4px -1px rgba(0, 0, 0, 0.01) !important; /* Sombra quase imperceptível */
    }

    /* 4. TIPOGRAFIA (Cinza Chumbo em vez de Preto Puro) */
    /* Isso cansa menos a vista e parece mais premium */
    h1, h2, h3 {
        color: #111827 !important; 
        letter-spacing: -0.5px; /* Deixa os títulos mais "apertadinhos" e modernos */
    }
    
    p, li, .stMarkdown {
        color: #000000 !important;
    }
    
    /* 5. AJUSTE FINO NO CABEÇALHO (Transparente) */
    [data-testid="stHeader"] {
        background: transparent;
    }
</style>
"""

st.markdown(page_style, unsafe_allow_html=True)

# ----- SIDEBAR -----
with st.sidebar:
    st.write("")
    st.write(f"**Olá, empresário(a) !**")
    st.caption("✅ Estou disponível para novos projetos")
    
    st.divider()
    
    # Login Area
    st.header("🔒 Área do Cliente")
    st.badge("Acesse seu projeto abaixo.", color="grey")

    if "nome_usuario" not in st.session_state:
        st.session_state["nome_usuario"] = "Visitante"
    
    if st.session_state["nome_usuario"] == "Visitante":
        btn_user = st.text_input("Usuário")
        btn_password = st.text_input("Senha", type="password")

        if st.button("Entrar no Sistema"):

            users = st.secrets["usuarios"]
    
            if btn_user in users and users[btn_user] == btn_password:
                st.session_state["nome_usuario"] = btn_user
                st.success(f"Bem-vindo, {btn_user.capitalize()}!")
                st.balloons()
            else:
                st.error("Acesso restrito a clientes ativos.")
                st.caption("Quer ter seu próprio acesso? Fale comigo.")

    st.divider()


    # Contacts area
    col_whats, col_linked = st.columns(2)

    num_whatsapp = "5519992814477"
    message_hello = "Olá Thiago! Vi seu portfólio de Dados e Automação e gostaria de discutir uma oportunidade/projeto."

    with col_whats:
            # Button Whatsapp
            link_whatsapp = f"https://wa.me/{num_whatsapp}?text={message_hello.replace(' ', '%20')}"
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
            # Button Linkedin
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
    
    st.divider()

    # Feedback area
    st.text("Deixe sua opinião/sugestão")
    sentiment_mapping = ["1", "2", "3", "4", "5"]
    selected = st.feedback("stars")
    if selected is not None:
        st.markdown(f"Você selecionou {sentiment_mapping[selected]} estrela(s).")

## ----- SELF INTRODUCTION -----

with st.container(border=True):

    whitespace, intro, whitespace2, photo = st.columns([0.01,9,1,3.4])

    with intro:
            st.title("Transformando dados em eficiência")
            
            st.markdown("""
            </h1>
            <p style='color: #666; font-size: 18px; margin-top: 5px;'>
                🎓 Administração | 💻 Análise de Dados | 🧾 Finanças
            </p>
            """, unsafe_allow_html=True)

            st.write("")
            
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

            col_m1, col_m2, col_m3 = st.columns(3)

            with col_m1:
                with st.container(border=True):
                    st.markdown("### 🎯 Foco")
                    st.caption("- Resultado mensurável")
                    st.markdown("")

            with col_m2:
                with st.container(border=True):
                    st.markdown("### 🧭 Escopo")
                    st.caption("- Do Operacional ao Estratégico")
                    st.markdown("")

            with col_m3:
                with st.container(border=True):
                    st.markdown("### 🚀 Próximo Passo")
                    st.link_button("📅 Agendar Diagnóstico", link_whatsapp)

    with photo:
        year_birth = date(2003, 11, 12)
        today = date.today()
        age = today.year - year_birth.year - ((today.month, today.day) < (year_birth.month, year_birth.day))

        st.image(image="Utilities/Foto.png",width=300, output_format="PNG")
        st.markdown(f"""
        <div style="text-align: center; margin-top: 2px;">
            <p style="font-weight: bold; font-size: 18px; margin-bottom: 2px;">Thiago Prochnow Borges</p>
            <p style="color: #666; font-size: 14px;"> {age} anos | Campinas - SP</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

st.write("")

# Increase the font size of the tab labels
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 25px; /* Tamanho da fonte */
        font-weight: bold; /* Deixa em negrito (opcional) */
    }
""", unsafe_allow_html=True)


## ----- TABS -----
tab_sobre, tab_servicos, tab_portfolio = st.tabs(["🙋🏻‍♂️ Sobre Mim", "🛠️ Soluções", "📊 Portifólio"])

with tab_sobre:
    col_text,esp1,col_skills1,esp2, col_skills2 = st.columns([4,0.2,2,0.2,2])

    with col_text:
        st.markdown("")
        with st.container(border=True):
            st.markdown("### Onde Negócios e Dados se Encontram")
            st.markdown("")

            st.markdown("""
            Atuo na lacuna entre a Gestão e a TI. Meu objetivo é garantir que cada dado coletado se traduza em **:green-background[Vantagem Competitiva]** para o seu negócio.
            Não entrego apenas "códigos funcionando", entrego processos otimizados que se pagam pelo tempo e recursos economizados.

            Combino a visão estratégica de negócios com uma gama de habilidades técnicas robustas para transformar planilhas manuais 
            e processos lentos em **:green-background[dashboards de decisão e automações inteligentes]**.

            Seja reestruturando processos falhos ou implementando inovação, meu compromisso é com a **entrega de valor contínuo**. 
            Desenvolvo soluções escaláveis que funcionam no mundo real, permitindo que sua equipe pare de apagar incêndios operacionais e foque no que realmente importa: **:green-background[o Core Business]**.
            """)

with col_skills1:
        st.markdown("")
        with st.container(border=True):
            # --- BLOCK 1: TECHNOLOGY ---
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
        with st.container(border=True):
            st.markdown("### 💼 Domínio de Negócio")

            st.write("")

            # --- BLOCK 2: Visualization & BI ---
            with st.expander("📊 **Análise de dados**"):
                with st.expander("📊 **Business Intelligence**"):
                    st.markdown("""
                    Transformação de dados brutos em narrativa de negócio (**Data Storytelling**):
                    
                    * 🎨 **Dashboards Estratégicos:** Criação de painéis interativos para monitoramento de OKRs e KPIs, com foco em UX/UI para facilitar a leitura executiva.
                    * 🧠 **Modelagem Avançada:** Domínio de **DAX** e **Linguagem M (Power Query)** para tratamento de dados complexos e relacionamento entre múltiplas tabelas fatos/dimensão.
                    * 📈 **Excel Avançado:** Uso de fórmulas e Macros (VBA) para modelagens financeiras rápidas.
                    """)

                # --- AUTOMATION & PRODUCTIVITY ---
                with st.expander("⚙️ **Automação de Processos**"):
                    st.markdown("""
                    Redução de trabalho manual para foco em análise estratégica (**RPA**):
                                
                    * 🐍 **Python Scripting:** Desenvolvimento de robôs para tarefas de alta complexidade, como **Web Scraping** (coleta de dados na web), leitura de PDFs e manipulação de arquivos em massa.
                    * 🤖 **Power Automate:** Criação de fluxos para coleta automática de dados, envio de alertas de anomalias e atualização de bases sem intervenção humana.
                    * 📱 **Power Apps:** Desenvolvimento de interfaces (formulários) para entrada de dados em campo, garantindo padronização e governança na origem.
                    """)

                # --- BLOCK 3: ENGINEER & MANIPULATION ---
                with st.expander("🐍 **Engenharia de Dados**"):
                    st.markdown("""
                    Garantia da integridade e disponibilidade da informação (**ETL**):
                    * 🧹 **Saneamento de Dados (Pandas/NumPy):** Scripts em Python para limpeza de bases cadastrais, identificando duplicidades e erros de preenchimento.
                    * 🗄️ **Consultas Estruturadas (SQL):** Extração de dados via *queries* otimizadas (JOINS, CTEs, Window Functions) para alimentar os relatórios de gestão.
                    * 🔗 **Integração de Fontes:** Consolidação de dados vindos de diversas origens (SAP, Planilhas, Sistemas Legados) em uma única fonte da verdade.
                    """)
            
            st.write("")

            # --- ADMINISTRATION ---
            with st.expander("🎓 **Administração & Processos**"):
                st.markdown("""
                Aplicação da visão sistêmica para conectar tecnologia e negócio:
                
                * 🔄 **Mapeamento de Processos:** Identificação de gargalos em fluxos de trabalho para propor automações com Power Automate/Python.
                * 🎯 **Gestão por Indicadores:** Definição e acompanhamento de KPIs e OKRs para garantir o alinhamento entre a operação e a estratégia da empresa.
                * 🏢 **Visão Organizacional:** Entendimento da interdependência entre áreas (Financeiro, Operações e TI) para liderar projetos transversais.
                """)

            st.write("")

            # --- FINANCE ---
            with st.expander("💰 **Contabilidade & Finanças**"):
                st.markdown("""
                Foco na integridade dos dados financeiros para suporte à decisão:
                
                * 📉 **Análise de Demonstrativos:** Leitura e interpretação de DRE e Fluxo de Caixa para diagnóstico de saúde financeira e eficiência operacional.
                * ⚖️ **Conciliação Físico-Contábil:** Cruzamento de bases de dados para garantir que o inventário físico reflita o Balanço Patrimonial.
                * 💵 **Gestão Orçamentária:** Classificação correta de custos (CAPEX vs OPEX) e monitoramento de desvios (Orçado x Realizado).
                """)

            st.write("")

            # --- ASSET MANAGEMENT ---
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
    
    # --- CARD 1: AUTOMATION ---
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
                st.markdown("**Power Apps** (Integração com Office 365)")

    # --- CARD 2: B.I. & DASHBOARDS ---
    with col_b:
        with st.container(border=True):
            st.markdown("### 📊 Inteligência de Dados (B.I.)")
            st.markdown("*:grey[- Transforme planilhas gigantes em decisões de 1 minuto.]*")

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

    # --- PROJETO 1: VIPS DETECTOR (RFM) ---
    with st.container(border=True):
        col_img, col_info = st.columns([1, 2])
        
        with col_img:
            st.image("Utilities\Detector de VIPs.png", use_container_width=True)
        
        with col_info:
            st.subheader("Detector de Oportunidades (RFM)")
            st.markdown("""
            **Foco:** Marketing e Vendas | **Tecnologia:** Python + Pandas
            
            Ferramenta que segmenta sua base de clientes automaticamente.
            Descubra quem são seus **VIPs**, quem está **Em Risco** e gere textos de recuperação para WhatsApp com IA.
            """)
            
            # O BOTÃO PARA A PÁGINA
            st.page_link("pages/1_💎_Detector_de_VIPs.py", label=":blue-background[***Testar Ferramenta Agora***]", icon="🚀")