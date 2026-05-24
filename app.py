import streamlit as st
import pandas as pd
import requests

# --- CONFIGURAÇÕES TÉCNICAS (SUPABASE) ---
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

# CSS Personalizado para um visual "Premium"
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        background-color: #002b5b;
        color: white;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover { background-color: #004080; border: none; color: white; }
    div[data-testid="stForm"] {
        border: 1px solid #e0e0e0;
        border-radius: 15px;
        padding: 30px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    h1 { color: #002b5b; font-family: 'Helvetica Neue', sans-serif; }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #002b5b;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# Cabeçalho
st.title("💎 Maura — Gestão de Produção")
st.write("Calculadora de Custos e Receitas Sincronizada em Tempo Real.")

# Criar duas colunas: uma para o formulário e outra para a lista
col1, col2 = st.columns([1, 1.5], gap="large")

with col1:
    st.subheader("Novo Registo")
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
        
        requests.post(f"{SUPABASE_URL}/rest/v1/moldes", json=dados_novos, headers=HEADERS)
        st.success(f"Registo '{molde}' sincronizado!")
        st.rerun()

with col2:
    st.subheader("Histórico de Produção")
    try:
        response_get = requests.get(f"{SUPABASE_URL}/rest/v1/moldes?select=*&order=id.desc", headers=HEADERS)
        if response_get.status_code == 200:
            linhas = response_get.json()
            if linhas:
                df = pd.DataFrame(linhas)
                df_visual = df[["molde", "tipo", "agua", "gesso", "cera", "custo_mat", "valor_final"]]
                df_visual.columns = ["Molde", "Tipo", "Água", "Gesso", "Cera", "Custo Mat.", "PREÇO FINAL"]
                
                st.dataframe(df_visual, use_container_width=True, hide_index=True)
                
                # Botão discreto para apagar
                with st.expander("🗑️ Eliminar Registos"):
                    molde_apagar = st.selectbox("Escolha o molde para remover", [i["molde"] for i in linhas])
                    if st.button("CONFIRMAR ELIMINAÇÃO"):
                        requests.delete(f"{SUPABASE_URL}/rest/v1/moldes?molde=eq.{molde_apagar}", headers=HEADERS)
                        st.rerun()
            else:
                st.info("A base de dados está vazia. Comece por adicionar um molde.")
    except:
        st.error("Erro ao carregar dados da nuvem.")