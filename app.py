import streamlit as st
import json
import os
import uuid
from datetime import datetime

# ==========================================
# 1. DESIGN UNIVERSEL (COMPATIBLE SAFARI/IPHONE)
# ==========================================
st.set_page_config(page_title="Issa & Fatou Planner", page_icon="💍", layout="wide")

# CSS simplifié sans imports complexes pour éviter les blocages Safari
st.markdown("""
<style>
    /* Fond sombre simple et efficace */
    .stApp {
        background-color: #0E1117;
    }

    /* Cartes unies (pas de transparence pour Safari) */
    .solid-card {
        background-color: #1A1C23;
        color: #FFFFFF;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border: 1px solid #30363D;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Dashboard XXL ultra-lisible */
    .dash-box {
        background-color: #1A1C23;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border-bottom: 5px solid #30363D;
    }
    .big-num { font-size: 32px; font-weight: bold; margin: 10px 0; }
    .sub-num { font-size: 14px; color: #8B949E; }
    
    /* Couleurs fixes */
    .color-or { color: #F1C40F; }
    .color-vert { color: #2ECC71; }
    .color-orange { color: #E67E22; }
    .color-bleu { color: #58A6FF; }

    /* Corrections pour Safari */
    div[data-testid="stMetricValue"] { font-size: 28px !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOGIQUE DE DONNÉES
# ==========================================
TAUX_EURO = 655.957
DB_FILE = "issafatou_web_data.json"
USERS_FILE = "users_web_db.json"

def load_json(file, default):
    if os.path.exists(file):
        try:
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return default
    return default

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

if "db" not in st.session_state:
    st.session_state.db = load_json(DB_FILE, {"mariage": [], "maison": [], "courses": [], "invites": [], "vacances": [], "last_edit": "Jamais"})
if "users" not in st.session_state:
    st.session_state.users = load_json(USERS_FILE, {})
if "delete_confirm" not in st.session_state:
    st.session_state.delete_confirm = None

def save_db():
    now = datetime.now().strftime("%d/%m %H:%M")
    st.session_state.db["last_edit"] = f"{now} par {st.session_state.current_user}"
    save_json(DB_FILE, st.session_state.db)

def format_money(fcfa_amount):
    euro = f"{(fcfa_amount / TAUX_EURO):,.2f} €".replace(",", " ")
    fcfa = f"{int(fcfa_amount):,} F".replace(",", " ")
    return euro, fcfa

# ==========================================
# 3. INTERFACE DE CONNEXION
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #F1C40F;'>💍 Issa & Fatou Planner</h1>", unsafe_allow_html=True)
    col1, col_c, col2 = st.columns([1, 2, 1])
    with col_c:
        choice = st.radio("Action", ["Connexion", "Inscription"], horizontal=True)
        email = st.text_input("Email")
        pwd = st.text_input("Mot de passe", type="password")
        if st.button("Valider", use_container_width=True):
            if choice == "Connexion":
                if email in st.session_state.users and st.session_state.users[email] == pwd:
                    st.session_state.logged_in = True
                    st.session_state.current_user = email
                    st.rerun()
                else: st.error("Erreur email/pass")
            else:
                st.session_state.users[email] = pwd
                save_json(USERS_FILE, st.session_state.users)
                st.success("Compte créé !")

# ==========================================
# 4. DASHBOARD & ONGLETS
# ==========================================
else:
    st.write(f"👤 {st.session_state.current_user} | ⏱️ {st.session_state.db['last_edit']}")
    if st.button("Déconnexion"):
        st.session_state.logged_in = False
        st.rerun()

    # Calculs
    t_mar = sum(i["prix"] for i in st.session_state.db["mariage"])
    t_mai = sum(i["prix"] for i in st.session_state.db["maison"])
    t_crs = sum(i["prix"] for i in st.session_state.db["courses"])
    t_gen = t_mar + t_mai + t_crs

    # Dashboard XXL
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f"<div class='dash-box'><p>💍 MARIAGE</p><p class='big-num color-or'>{format_money(t_mar)[0]}</p><p class='sub-num'>{format_money(t_mar)[1]}</p></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='dash-box'><p>🏠 MAISON</p><p class='big-num color-vert'>{format_money(t_mai)[0]}</p><p class='sub-num'>{format_money(t_mai)[1]}</p></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='dash-box'><p>🛒 COURSES</p><p class='big-num color-orange'>{format_money(t_crs)[0]}</p><p class='sub-num'>{format_money(t_crs)[1]}</p></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='dash-box'><p>📊 TOTAL</p><p class='big-num color-bleu'>{format_money(t_gen)[0]}</p><p class='sub-num'>{format_money(t_gen)[1]}</p></div>", unsafe_allow_html=True)

    tabs = st.tabs(["💍 MARIAGE", "🏠 MAISON", "🛒 COURSES", "👥 INVITÉS"])

    # Logique simplifiée pour les onglets (exemple Mariage)
    with tabs[0]:
        with st.form("f_mar", clear_on_submit=True):
            col_a, col_b, col_c = st.columns([3, 2, 1])
            n = col_a.text_input("Objet")
            p = col_b.number_input("Prix", step=1.0)
            d = col_c.selectbox("Devise", ["€", "F"])
            if st.form_submit_button("Ajouter"):
                p_f = p * TAUX_EURO if d == "€" else p
                st.session_state.db["mariage"].append({"id": str(uuid.uuid4()), "nom": n, "prix": p_f})
                save_db(); st.rerun()
        
        for item in st.session_state.db["mariage"]:
            e, f = format_money(item['prix'])
            st.markdown(f"<div class='solid-card' style='border-left: 5px solid #F1C40F;'><div>{item['nom']}</div><div><b>{e}</b><br><small>{f}</small></div></div>", unsafe_allow_html=True)
            if st.button("Effacer", key=item['id']):
                st.session_state.db["mariage"] = [i for i in st.session_state.db["mariage"] if i["id"] != item["id"]]
                save_db(); st.rerun()

    # (Le reste des onglets suit la même logique simplifiée)
