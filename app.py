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
div.stButton > button[key="btn_eliminar_direto"] { width: 100%; background-color: #c0392b !important; color: white !important; border-radius: 6px !important; height: 3.2em; font-weight: bold !important; border: none !important; }

/* Botão LOGIN */
div.stButton > button[key="btn_login"] { background-color: #002b5b !important; color: white !important; font-weight: bold !important; width: 100%; height: 3em; border-radius: 6px !important; }
</style>
""", unsafe_allow_html=True)

# --- SISTEMA DE CONTROLO DE LOGIN ---
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    # Ecrã de Login Centralizado
    st.write("")
    st.write("")
    col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
    
    with col_l2:
        st.markdown("""
        <div style='background-color: #002b5b; padding: 20px; border-radius: 12px; border-bottom: 4px solid #cfa134; text-align: center; margin-bottom: 20px;'>
            <h2 style='color: #f4ecd8; margin: 0; font-family: sans-serif;'>💎 Acesso Restrito</h2>
            <p style='color: #cfa134; margin: 5px 0 0 0;'>Introduza as suas credenciais Lunara</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("form_login"):
            usuario_input = st.text_input("Utilizador")
            senha_input = st.text_input("Palavra-passe", type="password")
            botao_entrar = st.form_submit_button("ENTRAR NO PAINEL", key="btn_login")
            
            if botao_entrar:
                # Altera aqui os teus dados de acesso se quiseres algo mais complexo:
                if usuario_input == "lunara2026" and senha_input == "220415F&M":
                    st.session_state["autenticado"] = True
                    st.rerun()
                else:
                    st.error("Credenciais incorretas. Tente novamente.")
    st.stop() # Bloqueia o resto do código se não estiver logado

# =====================================================================
# --- A PARTIR DAQUI SÓ ENTRA QUEM FIZER LOGIN COM SUCESSO ---
# =====================================================================

# Cabeçalho da Lunara
st.markdown("""
<div style='background-color: #002b5b; padding: 25px; border-radius: 12px; margin-bottom: 25px; border-bottom: 6px solid #cfa134; box-shadow: 0 4px 10px rgba(0,0,0,0.1);'>
    <div style='float: right;'>
        <form action='javascript:void(0);'></form>
    </div>
    <h1 style='color: #f4ecd8; margin: 0; font-family: "Helvetica Neue", sans-serif; font-weight: 700; text-align: center;'>GESTÃO DE MOLDES: GESSO & CERA</h1>
    <p style='color: #cfa134; margin: 6px 0 0 0; font-size: 1.1rem; font-weight: 500; text-align: center;'>Área Protegida • Clique diretamente numa linha da tabela para Editar ou Apagar</p>
</div>
""", unsafe_allow_html=True)

# Botão de Log Out discreto no topo lateral direito
if st.sidebar.button("🔒 Sair do Painel (Log Out)"):
    st.session_state["autenticado"] = False
    st.rerun()

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

col1, col2 = st.columns([1, 1.4], gap="large")

with col1:
    st.markdown("<h3 style='color: #002b5b; font-family: sans-serif; border-left: 5px solid #cfa134; padding-left: 10px;'>📋 Formulário de Trabalho</h3>", unsafe_allow_html=True)
    
    with st.form("formulario_molde", clear_on_submit=True):
        molde = st.text_input("Nome do Molde", placeholder="Ex: Jarra Tulipa")
        tipo_producao = st.radio("Selecione o Material:", ["Gesso", "Cera", "Gesso + Cera"], horizontal=True)
        v_total = st.number_input("Volume Total (ml)", min_value=0.0, step=10.0, value=None, placeholder="Introduza o volume total...")
        
        recipiente = "Não se aplica"
        if tipo_producao in ["Cera", "Gesso + Cera"]:
            recipiente = st.radio("Tipo de Recipiente para a Cera:", ["Molde", "Sem Tampa"], horizontal=True)
            
        st.write("---")
        extra = st.number_input("Material Extra (€)", min_value=0.0, value=0.50, step=0.10)
        mult = st.number_input("Multiplicador Mão de Obra (x)", min_value=1.0, value=3.0, step=0.5)
        
        submetido = st.form_submit_button("ADICIONAR NOVO REGISTO", key="btn_adicionar")

if submetido:
    if molde and v_total is not None and v_total > 0:
        gramas_cera = v_total * 0.89 if (tipo_producao in ["Cera", "Gesso + Cera"] and recipiente == "Molde") else (v_total * 0.86 if tipo_producao in ["Cera", "Gesso + Cera"] else 0.0)

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
        nome_final_molde = f"{molde} ({recipiente})" if recipiente != "Não se aplica" else molde
        
        dados_novos = {
            "molde": nome_final_molde, "tipo": tipo_producao, 
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

with col2:
    st.markdown("<h3 style='color: #002b5b; font-family: sans-serif; border-left: 5px solid #002b5b; padding-left: 10px;'>📊 Histórico de Produção</h3>", unsafe_allow_html=True)
    
    dados_selecionados = None
    if conexao_ok:
        if linhas:
            df = pd.DataFrame(linhas)
            df_visual = df[["molde", "tipo", "agua", "gesso", "cera", "custo_mat", "valor_final"]]
            df_visual.columns = ["Molde (Recipiente)", "Tipo", "Água", "Gesso", "Cera Calculada", "Custo Mat.", "PREÇO FINAL"]
            
            selecao = st.dataframe(
                df_visual, 
                use_container_width=True, 
                hide_index=True,
                selection_mode="single-row",
                on_select="rerun"
            )
            
            linhas_clicadas = selecao.get("selection", {}).get("rows", [])
            if linhas_clicadas:
                index_clicado = linhas_clicadas[0]
                dados_selecionados = linhas[index_clicado]
            
            st.write("")
            
            if dados_selecionados:
                st.markdown(f"<div style='background-color: #002b5b; padding: 10px; border-radius: 6px; color: white; font-weight: bold;'>⚙️ A Gerir: {dados_selecionados['molde']}</div>", unsafe_allow_html=True)
                
                with st.expander("📝 Editar ou Apagar o Molde Selecionado", expanded=True):
                    c_ed1, c_ed2 = st.columns(2)
                    with c_ed1:
                        novo_nome = st.text_input("Corrigir Nome", value=dados_selecionados["molde"])
                        novo_tipo = st.selectbox("Mudar Material", ["Gesso", "Cera", "Gesso + Cera"], index=["Gesso", "Cera", "Gesso + Cera"].index(dados_selecionados["tipo"]))
                        novo_vol = st.number_input("Introduzir Novo Volume (ml)", min_value=1.0, step=10.0, value=200.0)
                    
                    with c_ed2:
                        tipo_rec = "Sem Tampa" if "Sem Tampa" in novo_nome else "Molde"
                        g_cera_ed = novo_vol * 0.89 if tipo_rec == "Molde" else novo_vol * 0.86
                        
                        if novo_tipo == "Cera":
                            ag_ed, ge_ed, c_ge_ed = 0.0, 0.0, 0.0
                            c_ce_ed = (g_cera_ed * 17.50) / 2000
                        elif novo_tipo == "Gesso":
                            ag_ed = novo_vol / 2
                            ge_ed = ag_ed * 2.5
                            c_ge_ed = (ge_ed * 7.49) / 1000
                            g_cera_ed, c_ce_ed = 0.0, 0.0
                        else:
                            ag_ed = novo_vol / 2
                            ge_ed = ag_ed * 2.5
                            c_ge_ed = (ge_ed * 7.49) / 1000
                            c_ce_ed = (g_cera_ed * 17.50) / 2000
                        
                        c_total_ed = c_ge_ed + c_ce_ed + 0.50
                        v_final_ed = c_total_ed * 3.0
                        st.info(f"Novos Valores Calculados:\n- Custo: {c_total_ed:.2f}€\n- Preço Final: {v_final_ed:.2f}€")
                    
                    b_col1, b_col2 = st.columns(2)
                    with b_col1:
                        if st.button("GUARDAR ALTERAÇÕES", key="btn_guardar_edicao"):
                            dados_atualizados = {
                                "molde": novo_nome, "tipo": novo_tipo,
                                "agua": f"{ag_ed:.0f}g", "gesso": f"{ge_ed:.0f}g", "cera": f"{g_cera_ed:.0f}g",
                                "custo_mat": f"{c_total_ed:.2f}€", "valor_final": f"{v_final_ed:.2f}€"
                            }
                            try:
                                res_put = requests.patch(f"{SUPABASE_URL}/rest/v1/moldes?id=eq.{dados_selecionados['id']}", json=dados_atualizados, headers=HEADERS)
                                if res_put.status_code in [200, 204]:
                                    st.success("Atualizado!")
                                    st.rerun()
                            except:
                                st.rerun()
                    
                    with b_col2:
                        if st.button("ELIMINAR ESTE REGISTO", key="btn_eliminar_direto"):
                            try:
                                res_del = requests.delete(f"{SUPABASE_URL}/rest/v1/moldes?id=eq.{dados_selecionados['id']}", headers=HEADERS)
                                if res_del.status_code in [200, 204]:
                                    st.success("Eliminado!")
                                    st.rerun()
                            except:
                                st.rerun()
            else:
                st.info("💡 Clique numa linha da tabela para gerir os dados.")
        else:
            st.info("A base de dados está vazia.")
    else:
        st.error("Não foi possível ligar à nuvem.")
