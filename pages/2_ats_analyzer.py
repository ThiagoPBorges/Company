import streamlit as st
import pdfplumber
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import numpy as np
import spacy
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
import os
from portfolio import idiom

# --------- 1. INFRAESTRUTURA E CONFIGURAÇÕES ---------

# Detecção automática de ambiente (Local vs Nuvem)
if os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    poppler_path = r'C:\Program Files\poppler-25.12.0\Library\bin'
else:
    pytesseract.pytesseract.tesseract_cmd = 'tesseract'
    poppler_path = None

st.set_page_config(page_title="ATS Master | Pro", page_icon="🛡️", layout="wide")

# CSS Premium (Oculta elementos nativos do Streamlit e moderniza a UI)
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    h1, h2, h3 { color: #1e3a8a; font-family: 'Inter', sans-serif; }
    .step-card { background-color: #ffffff; padding: 25px; border-radius: 12px; border-left: 5px solid #2563eb; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    [data-testid="stPills"] div[role="listitem"] { background-color: #eff6ff; border: 1px solid #3b82f6; color: #1e40af; font-weight: 500; }
    </style>
    """, unsafe_allow_html=True)

# --------- 2. MOTORES DE INTELIGÊNCIA (NLP) ---------

@st.cache_resource
def load_nlp():
    return spacy.load("pt_core_news_sm")

nlp = load_nlp()

def extrair_tech_entities(txt):
    """Extrai tecnologias, softwares e jargões da área."""
    doc = nlp(txt)
    return list(set([ent.text.lower() for ent in doc.ents if ent.label_ in ["ORG", "MISC"]]))

def clean_text(txt):
    """Filtro semântico: lematização, remoção de stopwords, pontuação e números."""
    doc = nlp(txt.lower())
    pos_allowed = ["NOUN", "ADJ", "PROPN"]
    return [t.lemma_ for t in doc if t.pos_ in pos_allowed and not t.is_stop and not t.is_punct and not any(c.isdigit() for c in t.text) and len(t.text) > 2]

def plot_radar(categorias):
    """Gera o mapa visual de competências do candidato."""
    labels, values = list(categorias.keys()), list(categorias.values())
    num_vars = len(labels)
    
    # Previne erro se o gráfico estiver zerado
    if sum(values) == 0:
        values = [0.1, 0.1, 0.1]
        
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    values += values[:1]; angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='#2563eb', alpha=0.3)
    ax.plot(angles, values, color='#2563eb', linewidth=2)
    ax.set_xticks(angles[:-1]); ax.set_xticklabels(labels, fontsize=10, fontweight='bold', color='#334155')
    ax.set_yticklabels([])
    ax.spines['polar'].set_visible(False) # Deixa o gráfico mais limpo
    return fig

def gerar_card_premium(score_final, score_conteudo, score_tech, num_issues):
    """Gera o Card de Conversão SaaS usando HTML/CSS puro sem quebrar no Markdown."""
    sf, sc, st_tech = int(score_final * 100), int(score_conteudo * 100), int(score_tech * 100)
    
    def get_color(val):
        if val >= 75: return "#22c55e", "#dcfce7" # Verde
        if val >= 50: return "#f59e0b", "#fef3c7" # Laranja
        return "#ef4444", "#fee2e2"               # Vermelho

    color_sf, bg_sf = get_color(sf)
    color_sc, bg_sc = get_color(sc)
    color_st, bg_st = get_color(st_tech)

    # HTML formatado em uma única string sem recuos no início da linha
    html = (
        f'<div style="background-color: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); max-width: 400px; margin: 0 auto; font-family: \'Inter\', sans-serif;">'
        f'<h3 style="text-align: center; color: #334155; margin-bottom: 5px; font-weight: 500;">Score de Aderência</h3>'
        f'<h1 style="text-align: center; color: {color_sf}; font-size: 54px; font-weight: 800; margin: 0;">{sf}/100</h1>'
        f'<p style="text-align: center; color: #64748b; font-size: 14px; margin-top: 5px; margin-bottom: 25px;">{num_issues} Gaps Críticos Encontrados</p>'
        f'<hr style="border: none; border-top: 1px solid #f1f5f9; margin-bottom: 20px;">'
        
        f'<div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #f8fafc;">'
        f'<span style="color: #475569; font-weight: 600; font-size: 13px;">CONTEÚDO E SEMÂNTICA</span>'
        f'<div><span style="background-color: {bg_sc}; color: {color_sc}; padding: 4px 12px; border-radius: 12px; font-weight: 700; font-size: 14px;">{sc}%</span></div>'
        f'</div>'
        
        f'<div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #f8fafc;">'
        f'<span style="color: #475569; font-weight: 600; font-size: 13px;">HARD SKILLS (NER)</span>'
        f'<div><span style="background-color: {bg_st}; color: {color_st}; padding: 4px 12px; border-radius: 12px; font-weight: 700; font-size: 14px;">{st_tech}%</span></div>'
        f'</div>'
        
        f'<div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #f8fafc; opacity: 0.7;">'
        f'<span style="color: #475569; font-weight: 600; font-size: 13px;">MÉTRICAS E IMPACTO</span>'
        f'<div><span style="background-color: #f1f5f9; color: #94a3b8; padding: 4px 12px; border-radius: 12px; font-weight: 700; font-size: 14px;">??%</span><span style="margin-left: 8px;">🔒</span></div>'
        f'</div>'
        
        f'<div style="margin-top: 30px;">'
        f'<a href="#" style="display: block; text-align: center; text-decoration: none; width: 100%; padding: 16px 0; background-color: #2563eb; color: white; border-radius: 12px; font-size: 16px; font-weight: bold; box-sizing: border-box; box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4);">'
        f'Desbloquear Relatório Completo 🚀'
        f'</a>'
        f'</div>'
        f'</div>'
    )
    return html

# --------- 3. INTERFACE DE USUÁRIO (UI) ---------

st.title("🛡️ ATS Master Intelligence")
st.subheader("Transforme seu currículo em um imã de entrevistas validado por Inteligência Artificial.")

with st.sidebar:
    st.header("💎 Área do Candidato")
    area = st.selectbox("Seu Nicho Profissional", ["Tecnologia / Dados", "Administração", "Engenharia", "Vendas", "Saúde"])
    st.divider()
    st.info("Este motor simula a mesma triagem algorítmica utilizada pelas maiores plataformas de RH (Gupy, Workday, LinkedIn).")
    st.page_link("portfolio.py", label="Voltar ao Portfólio", icon="🏠")

col_vaga, col_cv = st.columns(2)
with col_vaga:
    with st.container(border=True):
        st.write("🎯 **Passo 1: A Vaga dos Sonhos**")
        job_input = st.text_area("Cole a descrição da vaga", height=150, help="Quanto mais completa a descrição, mais preciso será o diagnóstico.", label_visibility="collapsed")
with col_cv:
    with st.container(border=True):
        st.write("📄 **Passo 2: Seu Currículo**")
        file_input = st.file_uploader("Subir Currículo", type=["pdf", "jpg", "png"], label_visibility="collapsed")

# --------- 4. PROCESSAMENTO E DIAGNÓSTICO ---------

if file_input and job_input:
    with st.spinner("Analisando padrões semânticos e extraindo entidades..."):
        
        # Leitura de Arquivo Híbrida
        if file_input.name.lower().endswith(".pdf"):
            with pdfplumber.open(file_input) as pdf:
                raw_cv = " ".join([p.extract_text() for p in pdf.pages if p.extract_text()])
            if not raw_cv.strip():
                imgs = convert_from_bytes(file_input.getvalue(), poppler_path=poppler_path)
                raw_cv = " ".join([pytesseract.image_to_string(np.array(i), lang='por+eng') for i in imgs])
        else:
            raw_cv = pytesseract.image_to_string(np.array(Image.open(file_input)), lang='por+eng')

        # Limpeza e NLP
        cv_words, job_words = clean_text(raw_cv), clean_text(job_input)
        cv_clean, job_clean = " ".join(cv_words), " ".join(job_words)
        
        # Score de Contexto (TF-IDF)
        vectorizer = TfidfVectorizer(ngram_range=(1, 3))
        try:
            matrix = vectorizer.fit_transform([cv_clean, job_clean])
            score_text = cosine_similarity(matrix)[0][1]
        except ValueError:
            score_text = 0.0 # Previne erro se os textos forem muito curtos

        # Score de Hard Skills (NER)
        tech_job = extrair_tech_entities(job_input)
        tech_cv = extrair_tech_entities(raw_cv)
        match_tech = len(set(tech_job).intersection(set(tech_cv))) / len(tech_job) if tech_job else score_text
        
        # O Motor Ponderado
        final_score = (score_text * 0.6) + (match_tech * 0.4)
        missing_words = sorted(list(set(job_words) - set(cv_words)))

        # --- EXIBIÇÃO DE RESULTADOS PREMIUM ---
        st.divider()
        st.header("📋 Seu Diagnóstico de Performance")
        
        col_card, col_radar = st.columns([1.2, 1.5], gap="large")
        
        with col_card:
            # Exibe o Card SaaS HTML
            st.markdown(gerar_card_premium(final_score, score_text, match_tech, len(missing_words)), unsafe_allow_html=True)
            
        with col_radar:
            st.write("### 🧭 Mapa de Perfil (IA)")
            skills = {"Hard Skills": 0, "Soft Skills": 0, "Business": 0}
            for word in set(cv_words).intersection(set(job_words)):
                t = nlp(word)[0]
                if t.pos_ == "PROPN": skills["Hard Skills"] += 2
                elif t.pos_ == "ADJ": skills["Soft Skills"] += 1
                else: skills["Business"] += 1
            st.pyplot(plot_radar(skills))
            st.caption("O radar analisa se o recrutador te enxerga como um perfil puramente técnico, de negócios ou balanceado.")

        # --- PLANO DE AÇÃO (POR QUE PAGAR?) ---
        st.header("🛠️ Plano de Ação Direcionado", divider="grey")
        st.write("A inteligência artificial detectou que as seguintes otimizações podem dobrar suas chances de entrevista:")
        
        t1, t2 = st.columns(2)
        with t1:
            st.markdown(f"""
            <div class='step-card'>
                <h4 style="color: #1e40af; margin-top: 0;">✍️ Ajuste Semântico Imediato</h4>
                <p>O algoritmo eliminatório sentiu falta destas palavras essenciais:</p>
                <b>{', '.join(missing_words[:4])}</b>
                <p style="margin-top: 10px; font-size: 14px; color: #64748b;"><b>Como resolver:</b> Adicione estes exatos termos no seu resumo principal (sem usar sinônimos).</p>
            </div>
            """, unsafe_allow_html=True)
            
        with t2:
            st.markdown(f"""
            <div class='step-card'>
                <h4 style="color: #1e40af; margin-top: 0;">🔧 Validação de Stack Técnica</h4>
                <p>A vaga exige conhecimento explícito nestas ferramentas/organizações:</p>
                <b>{', '.join(tech_job[:3] if tech_job else ['Habilidades Específicas'])}</b>
                <p style="margin-top: 10px; font-size: 14px; color: #64748b;"><b>Como resolver:</b> Crie uma seção 'Ferramentas' e liste-as como substantivos próprios.</p>
            </div>
            """, unsafe_allow_html=True)

        # --- AUDITORIA DE CONFIANÇA ---
        with st.expander("🔍 Modo Desenvolvedor: Como a IA enxergou seu CV"):
            st.write("ATS não leem layouts bonitos, eles leem dados puros. Abaixo está a extração literal do seu documento:")
            st.code(cv_clean[:800] + "...")
            st.warning("Se o texto acima estiver misturado ou ilegível, o software do RH não conseguirá ler seu currículo. Use um formato mais simples.")

else:
    st.info("💡 Insira a descrição da vaga e faça o upload do seu currículo para liberar o motor de análise.")