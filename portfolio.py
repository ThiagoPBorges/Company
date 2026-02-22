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
        background-image: radial-gradient(#d1d5db 0.4px, transparent 1px); /* Pontos um pouco mais visíveis para o vidro funcionar */
        background-size: 24px 24px; 
    }

    /* 2. BARRA LATERAL (SIDEBAR) - Sombra Elegante */
    [data-testid="stSidebar"] {
        background-color: #0000000 !important; 
        /* 5px para a direita, 30px de difusão, cor preta com 20% de opacidade */
        box-shadow: 2px 0 30px rgba(0,0,0,0.3) !important;
        border-right: 1px solid #e5e7eb;
    }

    /* 3. CARTÕES DE VIDRO (GLASSMORPHISM) */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        /* Fundo Branco com 70% de opacidade (Aumentei um pouco para garantir leitura) */
        background-color: rgba(255, 255, 255, 0.7) !important; 
        
        /* O Desfoque do vidro */
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        
        /* Borda fina e semi-transparente */
        border: 1px solid rgba(255, 255, 255, 0.6) !important;
        border-radius: 12px !important;
        
        /* Sombra difusa para elevar o cartão */
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05) !important;
    }

    /* 4. TIPOGRAFIA */
    h1, h2, h3 {
        color: #111827 !important; 
        letter-spacing: -0.5px;
    }
    
    p, li, .stMarkdown {
        color: #1f2937 !important; /* Cinza escuro (quase preto) é mais elegante que #000000 */
    }
    
    /* 5. CABEÇALHO TRANSPARENTE */
    [data-testid="stHeader"] {
        background: transparent;
    }
</style>
"""

st.markdown(page_style, unsafe_allow_html=True)

# Update memory depends where user click
def idioma(pt,en):
    if st.session_state.get('idioma', 'PT') == 'PT':
        return pt
    else:
        return en

# ----- SIDEBAR -----
with st.sidebar:
    
    # Create button to alternate EN-PT
    escolha = st.radio(
        "Idioma / Language", 
        ['PT - 🇧🇷', 'EN - 🇺🇸'], 
        horizontal=True,
        label_visibility="collapsed"
    )
    # Save on memory EN-PT
    if 'PT' in escolha:
        st.session_state['idioma'] = 'PT'
    else:
        st.session_state['idioma'] = 'EN'
   
    st.markdown("")
    st.markdown("")
    st.markdown("")


    st.write(
        idioma("**Olá, empresário(a) !**",
               "**Hello, business owner !**"))
    st.caption(
        idioma("✅ Estou disponível para novos projetos",
        "✅ I'm available for new projects"))
        
    st.divider()
    
    # Login Area
    st.header(idioma("🔒 Área do Cliente","🔒 Client Area"))
    st.badge(idioma("Acesse seu projeto abaixo.","Access your project below.")
             , color="grey")

    if "nome_usuario" not in st.session_state:
        st.session_state["nome_usuario"] = "Visitante"
    
    if st.session_state["nome_usuario"] == "Visitante":
        btn_user = st.text_input(idioma("Usuário", "Username"))
        btn_password = st.text_input(idioma("Senha", "Password"), type="password")

        if st.button(idioma("Entrar no Sistema", "Login")):

            users = st.secrets["usuarios"]
    
            if btn_user in users and users[btn_user] == btn_password:
                st.session_state["nome_usuario"] = btn_user
                
                st.success(idioma(f"Bem-vindo, {btn_user.capitalize()}!", f"Welcome, {btn_user.capitalize()}!"))
                st.balloons()
            else:
                st.error(idioma("Acesso restrito a clientes ativos.", "Access restricted to active clients."))
                st.caption(idioma("Quer ter seu próprio acesso? Fale comigo.", "Want your own access? Contact me."))

    st.divider()


    # Contacts area
    col_whats, col_linked = st.columns(2)

    num_whatsapp = "5519992814477"
    message_hello = idioma(
        "Olá Thiago! Vi seu portfólio de Dados e Automação e gostaria de discutir uma oportunidade/projeto.",
        "Hello Thiago! I saw your portfolio of Data and Automation and would like to discuss an opportunity/project."
    )


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

## ----- SELF INTRODUCTION -----

with st.container(border=True):

    whitespace, intro, whitespace2, photo = st.columns([0.01,9,1,3.4])

    with intro:
            st.title(idioma("Transformando dados em eficiência", "Transforming data into efficiency"))

            st.markdown(f"""</h1>
            <p style='color: #666; font-size: 18px; margin-top: 5px;'>
                {idioma('🎓 Administração | 💻 Análise de Dados | 🧾 Finanças', '🎓 Adminstration | 💻 Data Analysis | 🧾 Finance')}
            </p>
            """,
            unsafe_allow_html=True)

            st.write("")
            
            main_txt = idioma(
                "Não sou apenas um Analista de Dados, sou um Administrador com o domínio da tecnologia.",
                "I'm not just a Data Analyst, I'm a Business Administrator with mastery of technology."
            )

            comp_txt = idioma(
                "Combino a visão estratégica de negócios com a precisão técnica da programação para eliminar ineficiências.",
                "I combine the strategic business vision with the technical precision of programming to eliminate inefficiencies."
            )

            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #000000;'>
                <p style='font-size: 18px; margin: 0; color: #31333F;'>
                    <b>"{main_txt}"</b><br>
                    <span style='font-size: 16px; color: #555;'>
                        {comp_txt}
                    </span>
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.write("#####")

            col_m1, col_m2, col_m3 = st.columns(3)

            with col_m1:
                with st.container(border=True):
                    st.markdown(idioma("### 🎯 Foco", "### 🎯 Focus"))
                    st.caption(idioma("Resultado mensurável", "Measurable result"))
                    st.markdown("")

            with col_m2:
                with st.container(border=True):
                    st.markdown(idioma("### 🧭 Escopo", "### 🧭 Scope"))
                    st.caption(idioma("Do Operacional ao Estratégico", "From Operational to Strategic"))
                    st.markdown("")

            with col_m3:
                with st.container(border=True):
                    st.markdown(idioma("### 🚀 Próximo Passo", "### 🚀 Next Step"))
                    st.link_button(idioma("📅 Agendar Avaliação", "📅 Schedule Evaluation"),link_whatsapp)

    with photo:
        year_birth = date(2003, 11, 12)
        today = date.today()
        age = today.year - year_birth.year - ((today.month, today.day) < (year_birth.month, year_birth.day))

        st.image(image="Utilities/Foto.png",width=300, output_format="PNG")
        st.markdown(f"""
        <div style="text-align: center; margin-top: 2px;">
            <p style="font-weight: bold; font-size: 18px; margin-bottom: 2px;">Thiago Prochnow Borges</p>
            <p style="color: #666; font-size: 14px;"> {age} {idioma('anos', 'years')} | Campinas - SP</p>
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
tab_sobre, tab_servicos, tab_portfolio = st.tabs(idioma(["🙋🏻‍♂️ Sobre Mim", "🛠️ Soluções", "📊 Portifólio"], ["🙋🏻‍♂️ About Me", "🛠️ Solutions", "📊 Portfolio"]))

with tab_sobre:
    col_text,esp1,col_skills1,esp2, col_skills2 = st.columns([4,0.2,2,0.2,2.9])

    with col_text:
        st.markdown("")
        with st.container(border=True):
            st.markdown(idioma("### Onde Negócios e Dados se Encontram", "### Where Business and Data Meet"))
            st.markdown("")

            st.markdown(idioma(
                """
                Atuo na lacuna entre a Gestão e a TI. Meu objetivo é garantir que cada dado coletado se traduza em **:green-background[Vantagem Competitiva]** para o seu negócio.
                Não entrego apenas "códigos funcionando", entrego processos otimizados que se pagam pelo tempo e recursos economizados.

                Combino a visão estratégica de negócios com uma gama de habilidades técnicas robustas para transformar planilhas manuais 
                e processos lentos em **:green-background[dashboards de decisão e automações inteligentes]**.

                Seja reestruturando processos falhos ou implementando inovação, meu compromisso é com a **entrega de valor contínuo**. 
                Desenvolvo soluções escaláveis que funcionam no mundo real, permitindo que sua equipe pare de apagar incêndios operacionais e foque no que realmente importa: **:green-background[o Core Business]**.
                """,
                """
                I bridge the gap between Management and IT. My goal is to ensure that every piece of data collected translates into a **:green-background[Competitive Advantage]** for your business.
                I don't just deliver "working code", I deliver optimized processes that pay for themselves through saved time and resources.

                I combine a strategic business vision with a robust set of technical skills to transform manual spreadsheets 
                and slow processes into **:green-background[decision-making dashboards and smart automations]**.

                Whether restructuring flawed processes or implementing innovation, my commitment is to **continuous value delivery**. 
                I develop scalable solutions that work in the real world, allowing your team to stop putting out operational fires and focus on what truly matters: **:green-background[the Core Business]**.
                """
            ))

with col_skills1:
        st.markdown("")
        with st.container(border=True):
            # --- BLOCK 1: TECHNOLOGY ---
            st.markdown(idioma("### 🛠️ Tecnologias","### 🛠️ Technologies"))
            
            st.write("**PYTHON**")
            st.progress(80)
            
            st.write("**POWER BI & DAX**")
            st.progress(90)
            
            st.write(idioma("**SQL & BANCO DE DADOS**", "**SQL & DATABASE**"))
            st.progress(85)
            
            st.write(idioma("**EXCEL AVANÇADO**", "**EXCEL ADVANCED**"))
            st.progress(95)

            st.markdown("####")

with col_skills2:
        st.markdown("")
        with st.container(border=True):
            st.markdown("### 💼 Domínio de Negócio")

            st.markdown("")

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
            st.write("###")
            

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

    st.markdown("######")
    st.info("**Dica:** Não sabe por onde começar? Geralmente organizamos os dados (**Automação**) para depois visualizá-los (**B.I.**).", icon="💡")
    st.markdown("######")


with tab_portfolio:
    st.write("")
    st.header("🧩 Projetos em Destaque")
    st.markdown("Aqui estão algumas soluções de automação e análise de dados que desenvolvi.")

    # --- CARD PROJECT 1 ---
    with st.container(border=True):
        col_imagem, col_texto = st.columns([1, 2])
        
        with col_imagem:
            st.video(
            'Utilities/Video Project 2.mp4',
            format="video/mp4", 
            start_time=0, 
            autoplay=True,
            muted=True,
            loop=True
        )
            
        with col_texto:
            st.subheader("💎 Detector de Oportunidades (CRM Automático)")
            st.write("**O que é:** Um sistema de segmentação RFM que transforma extratos de vendas em perfis de clientes (VIPs, Em Risco, etc).")
            st.write("**Tecnologias:** Python, Pandas, Streamlit, Integração com WhatsApp Web.")
            
            with st.container(border=True):
                st.page_link("pages/1_detector_vips.py", label="Testar Aplicativo", icon="▶️")