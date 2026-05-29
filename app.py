import streamlit as st
import pandas as pd
import requests

# --- CONFIGURAÇÕES TÉCNICAS (CONECTANDO AOS SECRETS DO STREAMLIT) ---
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except:
    SUPABASE_URL = "https://bkawgiunbbyukdbjywyx.supabase.co"
    SUPABASE_KEY = "sb_publishable_yCx2VN23E4Ar0YE1r-XTDQ_LoqYi9H9"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# --- CONFIGURAÇÃO DA PÁGINA (ESTÉTICA PC) ---
st.set_page_config(page_title="Maura | Produção Pro", layout="wide", page_icon="💎")

# --- DESIGN PERSONALIZADO (BEGE, DOURADO, VERDE, AZUL E VERMELHO) ---
st.markdown("""
    <style>
    .stApp { background-color: #f4ecd8 !important; }
    div[data-testid="stWidgetLabel"] p { color: #002b5b !important; font-weight: bold !important; }
    div[data-baseweb="input"], div[data-baseweb="number-input"] { border: 2px solid #cfa134 !important; border-radius: 6px !important; background-color: white !important; }
    div[data-testid="stForm"] { border: 2px solid #002b5b !important; border-radius: 12px !important; padding: 25px !important; background-color: #fdfbf7 !important; box-shadow: 0 6px 15px rgba(0,0,0,0.05) !important; }
    
    /* Botão ADICIONAR (Verde) */
    div.stButton > button[key="btn_adicionar"] { width: 100%; background-color: #27ae60 !important; color: white !important; border-radius: 6px !important; height: 3.2em; font-weight: bold !important; border: none !important; }
    
    /* Botão GUARDAR EDIÇÃO (Azul) */
    div.stButton > button[key="btn_guardar_edicao"] { width: 100%; background-color: #2980b9 !important; color: white !important; border-radius: 6px !important; height: 3.2em; font-weight: bold !important; border: none !important; }
    
    /* Botão ELIMINAR (Vermelho) */
    div[data-testid="stExpander"] button { background-color: #c0392b !important; color: white !important; border-radius: 6px !important; font-weight: bold !important; border: none !important; width: 100%; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# Cabeçalho Institucional
st.markdown("""
    <div style='background-color: #002b5b; padding: 25px; border-radius: 12px; margin-bottom: 25px; border-bottom: 6px solid #cfa134; box-shadow: 0 4px 10px rgba(0,0,0,0.1);'>
        <h1 style='color: #f4ecd8; margin: 0; font-family: \"Helvetica Neue\", sans-serif; font-weight: 700; text-align: center;'>GESTÃO DE MOLDES: GESSO & CERA</h1>
        <p style='color: #cfa134; margin: 6px 0 0 0; font-size: 1.1rem; font-weight: 50
