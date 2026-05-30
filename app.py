import streamlit as st
import pandas as pd
import requests
import os
import base64

# --- CONFIGURAÇÕES DA BASE DE DADOS (SUPABASE) ---
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

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Maura | Produção Pro", layout="wide", page_icon="🕯️")

# --- DESIGN PERSONALIZADO ---
st.markdown("""
<style>
header { visibility: hidden !important; height: 0px !important; }
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
div[data-testid="stDecoration"] { display: none !important; }
.stApp { background-color: #f4ecd8 !important; }

div[data-testid="stWidgetLabel"] p, label[data-testid="stWidgetLabel"] p { 
    color: #000000 !important; font-weight: 600 !important; font-size: 1.1rem !important; margin-bottom: 6px !important;
}

div[data-baseweb="input"], div[data-baseweb="number-input"] { 
    border: 2px solid #cfa134 !important; border-radius: 6px !important; background-color: white !important; 
}

.caixa-login-estilizada {
    border: 2px solid #002b5b !important; border-radius: 12px !important; padding: 25px !important; 
    background-color: #fdfbf7 !important; box-shadow: 0 6px 15px rgba(0,0,0,0.05) !important; margin-bottom: 25px !important;
}

.logo-login-box { display: flex; justify-content: center; align-items: center; width: 100%; margin-bottom: 25px !important; margin-top: 10px; }

div.stButton > button { 
    background-color: #002b5b !important; color: #ffffff !important; font-weight: bold !important;
    font-size: 1.05rem !important; text-transform: uppercase !important; letter-spacing: 1px !important;
    width: 240px !important; height: 46px !important; border-radius: 6px !important; border: none !important;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1) !important;
}

div[data-testid="stColumn"] div[data-testid="stForm"] { 
    border: 2px solid #002b5b !important; border-radius: 12px !important; padding: 25px !important; 
    background-color: #fdfbf7 !important; box-shadow: 0 6px 15px rgba(0,0,0,0.05) !important; 
}
</style>
""", unsafe_allow_html=True)

# --- SISTEMA DE CONTROLO DE LOGIN ---
if "autenticado" not in st.session_state: st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    _, col_l2, _ = st.columns([1, 1.2, 1])
    with col_l2:
        if os.path.exists("logo.png"):
            with open("logo.png", "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            st.markdown(f"<div class='logo-login-box'><img src='data:image/png;base64,{encoded}' style='width: 210px;'></div>", unsafe_allow_html=True)
        
        st.markdown('<div class="caixa-login-estilizada">', unsafe_allow_html=True)
        st.subheader("Área de Login")
        u = st.text_input("Utilizador", key="input_user")
        p = st.text_input("Palavra-passe", type="password", key="input_pass")
        
        if st.button("ENTRAR NO PAINEL"):
            if u == "lunara2026" and p == "220415F&M":
                st.session_state["autenticado"] = True
                st.rerun()
            else: st.error("Credenciais incorretas.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- ÁREA PRIVADA ---
if os.path.exists("logo.png"):
    col_h1, col_h2 = st.columns([1, 6.5])
    with col_h1: st.image("logo.png", width=85)
    with col_h2: st.markdown("<div style='background-color: #002b5b; padding: 14px; border-radius: 12px; border-bottom: 6px solid #cfa134; text-align: center;'><h1 style='color: #f4ecd8;'>LUNARA | GESTÃO DE MOLDES</h1></div>", unsafe_allow_html=True)

if st.sidebar.button("🔒 Sair do Painel"):
    st.session_state["autenticado"] = False
    st.rerun()

# --- LÓGICA DE DADOS ---
linhas = []
try:
    res = requests.get(f"{SUPABASE_URL}/rest/v1/moldes?select=*&order=id.desc", headers=HEADERS)
    if res.status_code == 200: linhas = res.json()
except: pass

col1, col2 = st.columns([1, 1.4], gap="large")

with col1:
    with st.form("formulario_molde", clear_on_submit=True):
        molde = st.text_input("Nome do Molde")
        tipo = st.radio("Material:", ["Gesso", "Cera", "Gesso + Cera"], horizontal=True)
        v = st.number_input("Volume (ml)", min_value=0.0, step=10.0)
        sub = st.form_submit_button("ADICIONAR")
    
    if sub:
        # Lógica original de cálculo
        gramas = v * 0.89 if tipo != "Gesso" else 0
        custo = ((v * 0.5) * 0.00749 if tipo != "Cera" else 0) + ((gramas * 17.50) / 2000 if tipo != "Gesso" else 0) + 0.50
        requests.post(f"{SUPABASE_URL}/rest/v1/moldes", json={"molde": molde, "tipo": tipo, "valor_final": f"{custo*3:.2f}€"}, headers=HEADERS)
        st.rerun()

with col2:
    if linhas: st.dataframe(pd.DataFrame(linhas), use_container_width=True)
