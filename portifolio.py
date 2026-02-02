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
    st.write(f"**Olá visitante!**")
    st.caption("✅ Disponível para novos projetos")
    
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
    st.write("Aqui você conta sua história de estudante de Adm que virou Data Analyst.")

with tab_servicos:
    st.header("Soluções para o seu Negócio")
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Automação de Processos")
        st.write("Transformo tarefas manuais repetitivas em scripts automáticos.")
        st.markdown("- **Exemplo:** Baixar notas fiscais, atualizar planilhas, enviar e-mails.")
    with col_b:
        st.subheader("Business Intelligence")
        st.write("Dashboards interativos para você parar de decidir no 'achismo'.")
        st.markdown("- **Exemplo:** Acompanhamento de metas, fluxo de caixa, DRE gerencial.")

with tab_portfolio:
    st.info("Em construção: Aqui entrarão os meus projetos exemplo.")