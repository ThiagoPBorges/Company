import streamlit as st
import pdfplumber
import re
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import seaborn as sns
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
import cv2
import numpy as np
import base64
import spacy
import requests
from bs4 import BeautifulSoup
import os
from portfolio import idiom


# --------- EXECUTION & CONFIG ---------


# Define local system is Wisdows (Use machine path), or Linux (Use ST.Cloud)
if os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    poppler_path = r'C:\Program Files\poppler-25.12.0\Library\bin'
else:
    pytesseract.pytesseract.tesseract_cmd = 'tesseract'
    poppler_path = None


st.set_page_config(page_title="ATS Analyzer",
                   page_icon="📑",
                   layout="wide",
                   initial_sidebar_state="expanded"
                   )


# CSS for Branding
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { color: #007bff; font-weight: bold; }
    [data-testid="stPills"] div[role="listitem"] { background-color: #e8f0fe; border: 1px solid #007bff; }
    div[data-testid="metric-container"] { background-color: #ffffff; border: 1px solid #e0e0e0; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)


# --------- NLP ENGINE ---------

nlp = spacy.load("pt_core_news_sm")

# --------- FUNCTIONS ---------

def clean_text(txt):
    '''
    Intelligent cleaning of text: PoS Tagging + Lematization (Reduce words to their root - EX : Analists to Analyst) + Filter of numbers
    '''
    # Process text with Spacy
    doc = nlp(txt.lower())
    pos_allowed = ["NOUN", "ADJ", "PROPN"]
    words = [word.lemma_ for word in doc # Return to root
             if word.pos_ in pos_allowed # Only types of examples
             and not word.is_stop # Filters and retains only meaningful words
             and not word.is_punct # Remove punctuation
             and not any(char.isdigit() for char in word.text) #Remove numbers
             and len(word.text) > 2]
   
    return " ".join(words) # Put it all together


def extrair_entidades(txt):
    doc = nlp(txt.lower())
    entities = {"Tecnologias/Org": [], "Datas/Tempo": [], "Locais": []}
    for ent in doc.ents:
        if ent.label_ == "ORG": entities["Tecnologias/Org"].append(ent.text)
        elif ent.label_ == "LOC": entities["Locais"].append(ent.text)
        elif ent.label_ == "MISC": entities["Tecnologias/Org"].append(ent.text)

    return entities


def categorizar_skills(keywords_list, area):
    categorias = {"Hard Skills": 0, "Soft Skills": 0, "Business": 0}
    doc = nlp(" ".join(keywords_list))

    # Dicionários de "pesos extras" por área
    expertise_map = {
        "Tecnologia / Dados": ['python', 'sql', 'bi', 'cloud', 'devops', 'machine'],
        "Saúde": ['clínico', 'paciente', 'diagnóstico', 'terapia', 'exame'],
        "Engenharia": ['autocad', 'projeto', 'norma', 'estrutural', 'obra'],
        "Vendas / Marketing": ['crm', 'funil', 'conversão', 'leads', 'venda']
    }

    extra_terms = expertise_map.get(area, [])

    for token in doc:
        t_low = token.text.lower()
        # Hard Skills: Nomes Próprios ou termos da área escolhida
        if token.pos_ == "PROPN" or any(term in t_low for term in extra_terms):
            categorias["Hard Skills"] += 2
        # Soft Skills: Adjetivos (comunicativo, ágil, etc)
        elif token.pos_ == "ADJ":
            categorias["Soft Skills"] += 1
        # Business: O restante dos substantivos comuns
        else:
            categorias["Business"] += 1
           
    return categorias



def plot_radar(categorias):
    labels, values = list(categorias.keys()), list(categorias.values())
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    values += values[:1]; angles += angles[:1]
    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='#007bff', alpha=0.25)
    ax.plot(angles, values, color='#007bff', linewidth=2)
    ax.set_yticklabels([]); ax.set_xticks(angles[:-1]); ax.set_xticklabels(labels)

    return fig



def gerar_dicas_ouro(missing_words, area):
    dicas = []

    # Processamos as palavras que faltam para entender a categoria
    doc_missing = nlp(" ".join(missing_words))
    hard_missing = [token.text for token in doc_missing if token.pos_ == "PROPN"][:3]
    soft_missing = [token.text for token in doc_missing if token.pos_ == "ADJ"][:2]

    # Dica de Hard Skill
    if hard_missing:
        termos = ", ".join(hard_missing)
        dicas.append(f"🎯 **Hard Skill:** Adicione uma seção de 'Projetos e Ferramentas' e mencione explicitamente sua experiência ou estudos em: **{termos}**.")

    # Dica de Soft Skill / Atitude
    if soft_missing:
        termos = " e ".join(soft_missing)
        dicas.append(f"💡 **Diferencial:** No seu resumo profissional, utilize palavras como **'{termos}'** para demonstrar alinhamento com a cultura da vaga.")

    # Dica Estratégica baseada na Área

    if area == "Tecnologia / Dados":
        dicas.append("🚀 **Estratégia:** Foque em descrever resultados quantitativos, como 'Redução de X% no tempo de processamento' ou 'Aumento de eficiência em Y%'.")
    else:
        dicas.append("📈 **Estratégia:** Certifique-se de que os processos e resultados mencionados no seu currículo utilizam o vocabulário específico desta descrição de vaga.")

    return dicas


# --------- MAIN INTERFACE ---------

with st.sidebar:
    escolha = st.radio("Language", ['PT - 🇧🇷', 'EN - 🇺🇸'], horizontal=True, label_visibility="collapsed")
    st.session_state['idiom'] = 'PT' if 'PT' in escolha else 'EN'
    st.page_link("portfolio.py", label=idiom("Home", "Home"), icon="🏠")

    st.divider()

    area_atuacao = st.selectbox(
        idiom("Área de Atuação", "Area of Expertise"),
        ["Geral / Admin", "Tecnologia / Dados", "Saúde", "Engenharia", "Vendas / Marketing"]
    )

job_input = st.text_area(idiom("Cole a descrição...", "Paste description..."), max_chars=10000)

file_input = st.file_uploader(idiom("Upload do Currículo", "Upload Resume"), type=["pdf","jpg","png","jpeg"])

# --- PROCESSAMENTO E OUTPUT ---

if file_input and job_input:
    with st.spinner(idiom("Analisando perfil...", "Analyzing profile...")):
        # OCR e Extração
        if file_input.name.lower().endswith(".pdf"):
            with pdfplumber.open(file_input) as pdf_doc:
                raw_text = " ".join([p.extract_text() for p in pdf_doc.pages if p.extract_text()])
            if not raw_text.strip():
                images = convert_from_bytes(file_input.getvalue(), poppler_path=poppler_path)
                raw_text = " ".join([pytesseract.image_to_string(np.array(img), lang='por+eng') for img in images])
        else:
            raw_text = pytesseract.image_to_string(np.array(Image.open(file_input)), lang='por+eng')

        # Inteligência
        resume_clean, job_clean = clean_text(raw_text), clean_text(job_input)
        vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform([resume_clean, job_clean])
        score = cosine_similarity(tfidf_matrix)[0][1]
        
        entidades = extrair_entidades(raw_text)
        keywords_found = set(resume_clean.split()).intersection(set(job_clean.split()))
        cat_data = categorizar_skills(keywords_found, area_atuacao)
        missing_words = sorted(list(set(job_clean.split()) - set(resume_clean.split())))

        # DASHBOARD
        st.divider()
        m1, m2, m3 = st.columns(3)
        m1.metric(idiom("Índice de Match", "Match Index"), f"{(score * 100):.2f}%")
        m2.metric(idiom("Skills Detectadas", "Detected Skills"), len(keywords_found))
        m3.metric(idiom("Gaps", "Gaps"), len(missing_words))

        c_radar, c_ner = st.columns([1, 1.5], gap="medium")
        with c_radar:
            with st.container(border=True):
                st.write(f"**{idiom('Equilíbrio de Perfil', 'Skill Balance')}**")
                st.pyplot(plot_radar(cat_data))
        
        with c_ner:
            with st.container(border=True):
                st.write(f"**{idiom('Mapeamento de IA (NER)', 'AI Mapping')}**")
                n1, n2, n3 = st.columns(3)
                n1.write(f"🏢 **Tech**\n" + "\n".join([f"- {i}" for i in list(set(entidades["Tecnologias/Org"]))[:5]]))
                n2.write(f"📍 **Locais**\n" + "\n".join([f"- {i}" for i in list(set(entidades["Locais"]))[:3]]))
                n3.write(f"📅 **Datas**\n" + "\n".join([f"- {i}" for i in list(set(entidades["Datas/Tempo"]))[:3]]))

        # INSIGHTS
        st.markdown("### ✨ " + idiom("Dicas de Ouro", "Golden Tips"))
        dicas = gerar_dicas_ouro(missing_words, area_atuacao)
        d_col1, d_col2, d_col3 = st.columns(3)
        d_col1.success(dicas[0]); d_col2.success(dicas[1]); d_col3.info(dicas[2])

        # AUDITORIA
        with st.expander(idiom("🔍 Detalhes Técnicos e Keywords", "🔍 Technical Details")):
            k1, k2 = st.columns(2)
            k1.write("**Found:**"); k1.pills("F", list(keywords_found), label_visibility="collapsed")
            k2.write("**Missing:**"); k2.pills("F", missing_words, label_visibility="collapsed")
            col_res, col_job = st.columns(2)
            with col_res:
                st.caption("Resume (Cleaned)")
                st.info(resume_clean)
            with col_job:
                st.caption("Job (Cleaned)")
                st.success(job_clean)