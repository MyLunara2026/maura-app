import streamlit as st
import pandas as pd
import requests

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
st.set_page_config(page_title="Maura | Produção Pro", layout="wide", page_icon="💎")

# --- DESIGN PERSONALIZADO EM BEGE, AZUL E OURO ---
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

# Cabeçalho da Lunara
st.markdown("""
<div style='background-color: #002b5b; padding: 25px; border-radius: 12px; margin-bottom: 25px; border-bottom: 6px solid #cfa134; box-shadow: 0 4px 10px rgba(0,0,0,0.1);'>
    <h1 style='color: #f4ecd8; margin: 0; font-family: "Helvetica Neue", sans-serif; font-weight: 700; text-align: center;'>GESTÃO DE MOLDES: GESSO & CERA</h1>
    <p style='color: #cfa134; margin: 6px 0 0 0; font-size: 1.1rem; font-weight: 500; text-align: center;'>Calculadora de Custos e Receitas Sincronizada em Tempo Real</p>
</div>
""", unsafe_allow_html=True)

# --- CARREGAR DADOS HISTÓRICOS ---
linhas = []
conexao_ok = False
try:
    response_get = requests.get(f"{SUPABASE_URL}/rest/v1/moldes?select=*&order=id.desc", headers=HEADERS)
    if response_get.status_code == 200:
        linhas = response_get.json()
        conexao_ok = True
except:
    conexao_ok = False

# Layout em duas colunas para Computador
col1, col2 = st.columns([1, 1.4], gap="large")

with col1:
    st.markdown("<h3 style='color: #002b5b; font-family: sans-serif; border-left: 5px solid #cfa134; padding-left: 10px;'>📋 Formulário de Trabalho</h3>", unsafe_allow_html=True)
    
    with st.form("formulario_molde", clear_on_submit=True):
        molde = st.text_input("Nome do Molde", placeholder="Ex: Jarra Tulipa")
        
        # Os 3 botões redondos horizontais que pediste
        tipo_producao = st.radio("Selecione o Material:", ["Gesso", "Cera", "Gesso + Cera"], horizontal=True)
        
        # Caixas numéricas limpas sem o "0.00" inicial
        v_total = st.number_input("Volume Total (ml)", min_value=0.0, step=10.0, value=None, placeholder="Introduza o volume total...")
        
        gramas_cera = 0.0
        if tipo_producao in ["Cera", "Gesso + Cera"]:
            gramas_cera_input = st.number_input("Peso da Cera (g)", min_value=0.0, step=5.0, value=None, placeholder="Introduza as gramas de cera...")
            if gramas_cera_input is not None:
                gramas_cera = gramas_cera_input
            
        st.write("---")
        extra = st.number_input("Material Extra (€)", min_value=0.0, value=0.50, step=0.10)
        mult = st.number_input("Multiplicador Mão de Obra (x)", min_value=1.0, value=3.0, step=0.5)
        
        submetido = st.form_submit_button("ADICIONAR", key="btn_adicionar")

if submetido:
    if molde and v_total is not None and v_total > 0:
        if tipo_producao == "Cera":
            agua, gesso, custo_gesso = 0.0, 0.0, 0.0
            custo_cera = (gramas_cera * 17.50) / 2000
        elif tipo_producao == "Gesso":
            agua = v_total / 2
            gesso = agua * 2.5
            custo_gesso = (gesso * 7.49) / 1000
            custo_cera = 0.0
        else:
            agua = v_total / 2
            gesso = agua * 2.5
            custo_gesso = (gesso * 7.49) / 1000
            custo_cera = (gramas_cera * 17.50) / 2000
            
        custo_total_mat = custo_gesso + custo_cera + extra
        valor_final = custo_total_mat * mult
        
        dados_novos = {
            "molde": molde, "tipo": tipo_producao, 
            "agua": f"{agua:.0f}g", "gesso": f"{gesso:.0f}g", "cera": f"{gramas_cera:.0f}g", 
            "custo_mat": f"{custo_total_mat:.2f}€", "valor_final": f"{valor_final:.2f}€"
        }
        try:
            res = requests.post(f"{SUPABASE_URL}/rest/v1/moldes", json=dados_novos, headers=HEADERS)
            if res.status_code in [200, 201, 204]:
                st.success(f"Molde '{molde}' adicionado!")
                st.rerun()
        except:
            st.rerun()
    else:
        st.warning("Preencha o Nome do Molde e o Volume antes de avançar.")

with col2:
    st.markdown("<h3 style='color: #002b5b; font-family: sans-serif; border-left: 5px solid #002b5b; padding-left: 10px;'>📊 Histórico de Production</h3>", unsafe_allow_html=True)
    
    if conexao_ok:
        if linhas:
            df = pd.DataFrame(linhas)
            df_visual = df[["molde", "tipo", "agua", "gesso", "cera", "custo_mat", "valor_final"]]
            df_visual.columns = ["Molde", "Tipo", "Água", "Gesso", "Cera", "Custo Mat.", "PREÇO FINAL"]
            st.dataframe(df_visual, use_container_width=True, hide_index=True)
            
            st.write("")
            # --- PAINEL DE EDIÇÃO ---
            with st.expander("📝 Opções de Gestão: Editar Dados Existentes"):
                lista_moldes_edit = list(set([i["molde"] for i in linhas if "molde" in i]))
                molde_escolhido = st.selectbox("Selecione o molde que quer alterar:", lista_moldes_edit)
                dados_atuais = next((item for item in linhas if item["molde"] == molde_escolhido), None)
                
                if dados_atuais:
                    c_ed1, c_ed2 = st.columns(2)
                    with c_ed1:
                        novo_nome = st.text_input("Corrigir Nome do Molde", value=dados_atuais["molde"])
                        novo_tipo = st.selectbox("Mudar Tipo", ["Gesso", "Cera", "Gesso + Cera"], index=["Gesso", "Cera", "Gesso + Cera"].index(dados_atuais["tipo"]))
                    with c_ed2:
                        novo_custo = st.text_input("Corrigir Custo Mat. (€)", value=dados_atuais["custo_mat"])
                        novo_preco = st.text_input("Corrigir Preço Final (€)", value=dados_atuais["valor_final"])
                    
                    if st.button("GUARDAR ALTERAÇÕES", key="btn_guardar_edicao"):
                        dados_atualizados = {"molde": novo_nome, "tipo": novo_tipo, "custo_mat": novo_custo, "valor_final": novo_preco}
                        try:
                            res_put = requests.patch(f"{SUPABASE_URL}/rest/v1/moldes?id=eq.{dados_atuais['id']}", json=dados_atualizados, headers=HEADERS)
                            if res_put.status_code in [200, 204]:
                                st.success("Atualizado com sucesso!")
                                st.rerun()
                        except:
                            st.rerun()
            
            # --- PAINEL DE ELIMINAÇÃO ---
            with st.expander("🗑️ Opções de Gestão: Eliminar Registos"):
                lista_moldes_del = list(set([i["molde"] for i in linhas if "molde" in i]))
                molde_apagar = st.selectbox("Selecione o molde a remover:", lista_moldes_del)
                if st.button("ELIMINAR REGISTO SELECIONADO"):
                    try:
                        res_del = requests.delete(f"{SUPABASE_URL}/rest/v1/moldes?molde=eq.{molde_apagar}", headers=HEADERS)
                        if res_del.status_code in [200, 204]:
                            st.rerun()
                    except:
                        st.rerun()
        else:
            st.info("A base de dados está vazia.")
    else:
        st.error("Não foi possível ligar à nuvem.")
