import streamlit as st
from portfolio import idiom
import pdfplumber
import pandas as pd
import re


# --- PAGE CONFIGURATION ---

st.set_page_config(
    page_title="ATS Analyzer",
    page_icon="📑",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# --- FUNCTIONS ---

def pdf(summary):

    complet_text = ""

    # Open file and create a [list] of pages
    with pdfplumber.open(summary) as pdf_doc:
        # Travels each page of [list] of pages
        for page in pdf_doc.pages:
            extract = page.extract_text()
            if extract:
                complet_text += extract
    return complet_text


def clean_text(txt):

    stopwords = ['de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'com']

    text = txt.lower()
    # keep letters (with accents), numbers, and spaces.
    cleaned = re.sub(r'[^\w\s]', '', text).replace('_', '')
    cleaned = ' '.join([word for word in cleaned.split() if word not in stopwords])
    
    return cleaned


# --- INPUT ---

job_description = st.text_area(
    "Put the job description here",
    max_chars=10000
)

pdf_input = st.file_uploader(
    "Upload a PDF file",
    type=["pdf"]
)


if st.button("Submit", type="primary"):
    if pdf_input is not None:
        result = pdf(pdf_input)
        if not result:
            st.warning("The PDF file is empty")
        if not job_description:
            st.warning("Please enter the job description")

        else:
            st.header("Extracted text:", divider="grey")

            col1, col2 = st.columns(2)

            with col1:
                with st.container(border=True):
                    st.subheader("Summary PDF")
                    st.write(clean_text(result))
            with col2:
                with st.container(border=True):
                    st.subheader("Job Description")
                    st.write(clean_text(job_description))



