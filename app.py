import streamlit as st
import pandas as pd
import requests
import os
import base64

# --- 1. CONFIGURAÇÕES GERAIS ---
st.set_page_config(page_title="Maura | Produção Pro", layout="wide", page_icon="🕯️")

# --- 2. SUPABASE ---
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

# --- 3. DESIGN LIMPO ---
st.markdown("""
<style>
header { visibility: hidden !important; height: 0px !important; }
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
.stApp { background-color: #f4ecd8 !important; }
.caixa-login-estilizada { border: 2px solid #002b5b !important; border-radius: 12px !important; padding: 25px !important; background-color: #fdfbf7 !important; }
div[data-testid="stForm"] { border: 2px solid #002b5b !important; border-radius: 12px !important; padding: 25px !important; background-color: #fdfbf7 !important; }
</style>
""", unsafe_allow_html=True)

# --- 4. LOGIN ---
if "autenticado" not in st.session_state: st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    _, col_l2, _ = st.columns([1, 1.2, 1])
    with col_l2:
        if os.path.exists("logo.png"): st.image("logo.png", width=210)
        st.markdown('<div class="caixa-login-estilizada">', unsafe_allow_html=True)
        st.subheader("Área de Login")
        u = st.text_input("Utilizador", key="u")
        p = st.text_input("Palavra-passe", type="password", key="p")
        if st.button("ENTRAR NO PAINEL"):
            if u == "lunara2026" and p == "220415F&M":
                st.session_state["autenticado"] = True
                st.rerun()
            else: st.error("Credenciais incorretas.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 5. ÁREA PRIVADA ---
st.title("LUNARA | Gestão de Moldes")
if st.sidebar.button("🔒 Sair do Painel"):
    st.session_state["autenticado"] = False
    st.rerun()

# Lógica de Carregamento
linhas = []
res = requests.get(f"{SUPABASE_URL}/rest/v1/moldes?select=*&order=id.desc", headers=HEADERS)
if res.status_code == 200: linhas = res.json()

col1, col2 = st.columns([1, 1.4], gap="large")

with col1:
    with st.form("formulario_molde", clear_on_submit=True):
        molde = st.text_input("Nome do Molde")
        tipo = st.radio("Material:", ["Gesso", "Cera", "Gesso + Cera"], horizontal=True)
        v_total = st.number_input("Volume (ml)", min_value=0.0, step=10.0)
        submetido = st.form_submit_button("ADICIONAR")
    
    if submetido:
        # Lógica de cálculo simplificada para garantir funcionamento
        gramas = v_total * 0.89 if tipo != "Gesso" else 0
        custo = ((v_total * 0.5) * 0.00749 if tipo != "Cera" else 0) + ((gramas * 17.50) / 2000 if tipo != "Gesso" else 0) + 0.50
        dados = {"molde": molde, "tipo": tipo, "valor_final": f"{custo*3:.2f}€"}
        requests.post(f"{SUPABASE_URL}/rest/v1/moldes", json=dados, headers=HEADERS)
        st.rerun()

with col2:
    if linhas:
        df = pd.DataFrame(linhas)
        st.dataframe(df, use_container_width=True)
