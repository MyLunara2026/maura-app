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

# --- CONFIGURAÇÃO DA PÁGINA (ESTÉTICA) ---
st.set_page_config(page_title="Maura | Produção Pro", layout="wide", page_icon="💎")

# --- DESIGN PERSONALIZADO (CORES DA TUA APLICAÇÃO: BEGE, DOURADO, VERDE E VERMELHO) ---
st.markdown("""
    <style>
    /* Fundo da aplicação em Bege Suave */
    .stApp { 
        background-color: #f4ecd8 !important; 
    }
    
    /* Customização dos Inputs (Caixas de texto e números) */
    div[data-testid="stWidgetLabel"] p {
        color: #002b5b !important;
        font-weight: bold !important;
    }
    div[data-baseweb="input"], div[data-baseweb="number-input"] {
        border: 2px solid #cfa134 !important;
        border-radius: 6px !important;
        background-color: white !important;
    }
    
    /* Bloco do Formulário Esquerdo */
    div[data-testid="stForm"] {
        border: 2px solid #002b5b !important;
        border-radius: 12px !important;
        padding: 25px !important;
        background-color: #fdfbf7 !important;
        box-shadow: 0 6px 15px rgba(0,0,0,0.05) !important;
    }
    
    /* BOTÃO VERDE: CALCULAR E GUARDAR */
    div.stButton > button:first-child {
        width: 100%;
        background-color: #27ae60 !important;
        color: white !important;
        border-radius: 6px !important;
        height: 3.2em;
        font-weight: bold !important;
        font-size: 1.05rem !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(39,174,96,0.2);
        transition: all 0.2s ease;
    }
    div.stButton > button:first-child:hover { 
        background-color: #1e7e43 !important;
        box-shadow: 0 4px 12px rgba(39,174,96,0.4);
        transform: translateY(-1px);
    }
    
    /* BOTÃO VERMELHO: CONFIRMAR ELIMINAÇÃO (Dentro do Expander) */
    div[data-testid="stExpander"] button {
        background-color: #c0392b !important;
        color: white !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        border: none !important;
    }
    div[data-testid="stExpander"] button:hover {
        background-color: #a93226 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Cabeçalho Institucional (Azul Escuro e Ouro)
st.markdown("""
    <div style='background-color: #002b5b; padding: 25px; border-radius: 12px; margin-bottom: 25px; border-bottom: 6px solid #cfa134; box-shadow: 0 4px 10px rgba(0,0,0,0.1);'>
        <h1 style='color: #f4ecd8; margin: 0; font-family: \"Helvetica Neue\", sans-serif; font-weight: 700; text-align: center; letter-spacing: 1px;'>GESTÃO DE MOLDES: GESSO & CERA</h1>
        <p style='color: #cfa134; margin: 6px 0 0 0; font-size: 1.1rem; font-weight: 500; text-align: center;'>Calculadora de Custos e Receitas Sincronizada em Tempo Real</p>
    </div>
    """, unsafe_allow_html=True)

# Criar as duas colunas principais
col1, col2 = st.columns([1, 1.4], gap="large")

with col1:
    st.markdown("<h3 style='color: #002b5b; font-family: sans-serif; border-left: 5px solid #cfa134; padding-left: 10px;'>📋 Novo Registo</h3>", unsafe_allow_html=True)
    with st.form("formulario_molde", clear_on_submit=True):
        molde = st.text_input("Nome do Molde", placeholder="Ex: Jarra Tulipa")
        v_total = st.number_input("Volume Total (ml)", min_value=0.0, step=10.0)
        
        c1, c2 = st.columns(2)
        with c1:
            st.write("")
            st.write("")
            leva_cera = st.checkbox("Incluir Cera?")
        with c2:
            gramas_cera = st.number_input("Cera (g)", min_value=0.0, step=5.0)
            
        st.write("---")
        extra = st.number_input("Material Extra (€)", min_value=0.0, value=0.50, step=0.10)
        mult = st.number_input("Multiplicador Mão de Obra (x)", min_value=1.0, value=3.0, step=0.5)
        
        submetido = st.form_submit_button("ADICIONAR & GUARDAR NA NUVEM")

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
    st.markdown("<h3 style='color: #002b5b; font-family: sans-serif; border-left: 5px solid #002b5b; padding-left: 10px;'>📊 Histórico de Produção</h3>", unsafe_allow_html=True)
    try:
        response_get = requests.get(f"{SUPABASE_URL}/rest/v1/moldes?select=*&order=id.desc", headers=HEADERS)
        if response_get.status_code == 200:
            linhas = response_get.json()
            if linhas:
                df = pd.DataFrame(linhas)
                df_visual = df[["molde", "tipo", "agua", "gesso", "cera", "custo_mat", "valor_final"]]
                df_visual.columns = ["Molde", "Tipo", "Água", "Gesso", "Cera", "Custo Mat.", "PREÇO FINAL"]
                
                # Exibe a tabela adaptada ao tamanho da coluna
                st.dataframe(df_visual, use_container_width=True, hide_index=True)
                
                st.write("")
                with st.expander("🗑️ Opções de Gestão (Eliminar Registo de Forma Permanente)"):
                    lista_moldes = list(set([i["molde"] for i in linhas if "molde" in i]))
                    molde_apagar = st.selectbox("Selecione o molde a remover da base de dados:", lista_moldes)
                    
                    if st.button("ELIMINAR REGISTO SELECIONADO"):
                        res_del = requests.delete(f"{SUPABASE_URL}/rest/v1/moldes?molde=eq.{molde_apagar}", headers=HEADERS)
                        if res_del.status_code in [200, 204]:
                            st.rerun()
            else:
                st.info("A base de dados está vazia. Adicione o seu primeiro molde à esquerda.")
        else:
            st.error(f"O banco de dados recusou o acesso (Erro {response_get.status_code}).")
    except:
        st.error("Não foi possível estabelecer ligação com a nuvem.")
