import streamlit as st
import pandas as pd
import requests

# --- CONFIGURAÇÕES TÉCNICAS (CONECTANDO AOS SECRETS DO STREAMLIT) ---
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except:
    # Caso os secrets ainda estejam a carregar, usa o plano B temporário
    SUPABASE_URL = "https://bkawgiunbbyukdbjywyx.supabase.co"
    SUPABASE_KEY = "sb_publishable_yCx2VN23E4Ar0YE1r-XTDQ_LoqYi9H9"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# --- CONFIGURAÇÃO DA PÁGINA (ESTÉTICA) ---
st.set_page_config(page_title="Maura | Produção", layout="wide", page_icon="💎")

# CSS Personalizado Avançado para forçar as cores institucionais
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        background-color: #002b5b !important;
        color: white !important;
        border-radius: 8px !important;
        height: 3em;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(0,43,91,0.2);
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        background-color: #d4af37 !important;
        color: #002b5b !important;
        box-shadow: 0 4px 12px rgba(212,175,55,0.4);
    }
    div[data-testid="stForm"] {
        border: none !important;
        border-radius: 15px !important;
        padding: 30px !important;
        background-color: white !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05) !important;
    }
    div[data-baseweb="input"] {
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Cabeçalho Premium
st.markdown("""
    <div style='background-color: #002b5b; padding: 25px; border-radius: 12px; margin-bottom: 25px; border-left: 8px solid #d4af37;'>
        <h1 style='color: white; margin: 0; font-family: \"Helvetica Neue\", sans-serif; font-weight: 700;'>💎 Maura — Gestão de Produção</h1>
        <p style='color: #d4af37; margin: 5px 0 0 0; font-size: 1.1rem; font-weight: 500;'>Calculadora de Custos e Receitas Sincronizada em Tempo Real</p>
    </div>
    """, unsafe_allow_html=True)

# Criar duas colunas
col1, col2 = st.columns([1, 1.5], gap="large")

with col1:
    st.markdown("<h3 style='color: #002b5b; font-family: sans-serif;'>📋 Novo Registo</h3>", unsafe_allow_html=True)
    with st.form("formulario_molde", clear_on_submit=True):
        molde = st.text_input("Nome do Molde", placeholder="Ex: Jarra Tulipa")
        v_total = st.number_input("Volume Total (ml)", min_value=0.0, step=10.0)
        
        c1, c2 = st.columns(2)
        with c1:
            leva_cera = st.checkbox("Incluir Cera?")
        with c2:
            gramas_cera = st.number_input("Cera (g)", min_value=0.0, step=5.0)
            
        st.write("---")
        extra = st.number_input("Material Extra (€)", min_value=0.0, value=0.50, step=0.10)
        mult = st.number_input("Multiplicador Mão de Obra (x)", min_value=1.0, value=3.0, step=0.5)
        
        submetido = st.form_submit_button("CALCULAR E GUARDAR")

if submetido:
    if molde and v_total > 0:
        agua = v_total / 2
        gesso = agua * 2.5
        custo_gesso = (gesso * 7.49) / 1000
        custo_cera = (gramas_cera * 17.50) / 2000 if leva_cera else 0.0
        custo_total_mat = custo_gesso + custo_cera + extra
        valor_final = custo_total_mat * mult
        tipo = "Gesso + Cera" if leva_cera else "Gesso"
        
        dados_novos = {
            "molde": molde, "tipo": tipo, "agua": f"{agua}g", 
            "gesso": f"{gesso}g", "cera": f"{gramas_cera}g", 
            "custo_mat": f"{custo_total_mat:.2f}€", "valor_final": f"{valor_final:.2f}€"
        }
        
        try:
            res = requests.post(f"{SUPABASE_URL}/rest/v1/moldes", json=dados_novos, headers=HEADERS)
            if res.status_code in [200, 201, 204]:
                st.success(f"Registo '{molde}' sincronizado!")
                st.rerun()
            else:
                st.error(f"Erro ao guardar no servidor (Código {res.status_code})")
        except:
            st.rerun()

with col2:
    st.markdown("<h3 style='color: #002b5b; font-family: sans-serif;'>📊 Histórico de Produção</h3>", unsafe_allow_html=True)
    try:
        response_get = requests.get(f"{SUPABASE_URL}/rest/v1/moldes?select=*&order=id.desc", headers=HEADERS)
        if response_get.status_code == 200:
            linhas = response_get.json()
            if linhas:
                df = pd.DataFrame(linhas)
                df_visual = df[["molde", "tipo", "agua", "gesso", "cera", "custo_mat", "valor_final"]]
                df_visual.columns = ["Molde", "Tipo", "Água", "Gesso", "Cera", "Custo Mat.", "PREÇO FINAL"]
                
                st.dataframe(df_visual, use_container_width=True, hide_index=True)
                
                st.write("")
                with st.expander("🗑️ Opções de Gestão (Eliminar Registo)"):
                    lista_moldes = list(set([i["molde"] for i in linhas if "molde" in i]))
                    molde_apagar = st.selectbox("Selecione o molde a remover:", lista_moldes)
                    
                    if st.button("CONFIRMAR ELIMINAÇÃO PERMANENTE"):
                        res_del = requests.delete(f"{SUPABASE_URL}/rest/v1/moldes?molde=eq.{molde_apagar}", headers=HEADERS)
                        if res_del.status_code in [200, 204]:
                            st.rerun()
            else:
                st.info("A base de dados está vazia. Adicione o seu primeiro molde à esquerda.")
        else:
            st.error(f"O banco de dados recusou o acesso (Erro {response_get.status_code}). Verifique se os Secrets estão bem salvos.")
    except:
        st.error("Não foi possível estabelecer ligação com a nuvem.")
