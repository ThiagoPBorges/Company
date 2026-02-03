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
    st.write(f"**Olá, empresário!**")
    st.caption("✅ Estou disponível para novos projetos")
    
    st.divider()
    
    # Área de Login
    st.header("🔒 Área do Cliente")
    st.info("Acesse seu projeto abaixo.")
    
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    ## CRIAR UM ESQUECI A SENHA
    
    if st.button("Entrar no Sistema"):
        if usuario == "demo" and senha == "1234":
            st.success("Logado na Demonstração!")
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

v1, intro2, foto3 = st.columns([0.5,4,2])

with intro2:
    st.title("Transformando dados em eficiência.")

    st.write("")

    st.markdown("### 🎓 Administração | 💻 Análise de dados")
    
    st.markdown("######")

    st.write("""
    **Pare de travar em planilhas.**
    
    Combino a **visão estratégica de um Administrador de Negócios** com o **poder técnico da análise de dados**
    """)

with foto3:

    st.image(image="Utilities/Foto.png",width=300, output_format="PNG")

st.divider()


# --- CORPO DA PÁGINA ---
tab_sobre,tab_servicos, tab_portfolio = st.tabs(["🙋‍♂️ Sobre Mim","🛠️ O que eu faço", "📈 Meus Projetos"])

with tab_sobre:
    col_texto,esp, col_skills = st.columns([3,0.1, 1])

    with col_texto:
        st.markdown("")
        st.markdown("### 🚀 Onde Negócios e Dados se Encontram")
        st.markdown("")
        st.info("""
        "Não sou apenas um Analista de Dados, sou um Administrador com o domínio da tecnologia."
        """)
        st.markdown("")
        st.markdown("""
        Enquanto muitos focam apenas no código, meu foco está no **:green-background[Resultado do seu negócio]**. 
        Identifico onde sua operação perde tempo e dinheiro (gargalos) e construo a solução técnica exata para resolver isso.
        
        Combino a visão estratégica de negócios com uma gama de habilidades técnicas robustas para transformar planilhas manuais 
        e processos lentos em **:green-background[dashboards de decisão e automações inteligentes]**.
        """)

        st.divider()

        c1, c2, c3 = st.columns(3)
        c1.markdown("<h5 style='text-align: center;'>✅ Visão Sistêmica</h5>", unsafe_allow_html=True)
        c2.markdown("<h5 style='text-align: center;'>✅ Comunicação Clara</h5>", unsafe_allow_html=True)
        c3.markdown("<h5 style='text-align: center;'>✅ Foco em ROI</h5>", unsafe_allow_html=True)

    with col_skills:
        st.markdown("")
        st.markdown("### 🛠️ Tecnologias")
        
        st.write("PYTHON")
        st.progress(80)
        
        st.write("POWER BI & DAX")
        st.progress(90)
        
        st.write("SQL & BANCO DE DADOS")
        st.progress(85)
        
        st.write("EXCEL AVANÇADO")
        st.progress(95)

        st.write("📈 Evoluindo constantemente em Data Science.")

with tab_servicos:
    st.markdown("## 💼 Como posso impulsionar seu negócio?")
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
    st.info("Em construção: Aqui entrarão os meus projetos exemplo.")