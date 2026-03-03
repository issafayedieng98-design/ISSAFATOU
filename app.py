import streamlit as st
import json
import os
import uuid
from datetime import datetime

# ==========================================
# 1. CONFIGURATION ET DESIGN HAUTE LISIBILITÉ
# ==========================================
st.set_page_config(page_title="Issa & Fatou Planner", page_icon="💍", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Fond noir profond */
    .stApp {
        background-color: #0B0E14;
    }

    /* -------------------------------------- */
    /* NOUVEAU DASHBOARD : GROS CHIFFRES !    */
    /* -------------------------------------- */
    .dash-card {
        background-color: #1E1E2E;
        padding: 25px 15px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }
    .dash-title { font-size: 16px; font-weight: 600; color: #FFFFFF; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
    .dash-sub { font-size: 16px; color: #ADB5BD; font-weight: 500; margin-top: 5px; }
    
    /* Tailles et couleurs des gros chiffres */
    .dash-val-or { font-size: 38px; font-weight: 800; color: #F1C40F; line-height: 1.1; }
    .dash-val-vert { font-size: 38px; font-weight: 800; color: #2ECC71; line-height: 1.1; }
    .dash-val-orange { font-size: 38px; font-weight: 800; color: #E67E22; line-height: 1.1; }
    .dash-val-bleu { font-size: 40px; font-weight: 800; color: #3498DB; line-height: 1.1; text-shadow: 0px 0px 10px rgba(52,152,219,0.5); }

    /* -------------------------------------- */
    /* Cartes des listes en dessous           */
    /* -------------------------------------- */
    .solid-card {
        background-color: #1E1E2E !important; 
        color: #FFFFFF !important; 
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .accent-mar { border-left: 8px solid #F1C40F; } 
    .accent-mai { border-left: 8px solid #2ECC71; } 
    .accent-crs { border-left: 8px solid #E67E22; } 
    .accent-vac { border-left: 8px solid #1ABC9C; } 
    .accent-inv { border-left: 8px solid #3498DB; } 

    .prix-grand { font-size: 24px; font-weight: bold; }
    .prix-petit { font-size: 14px; color: #CCCCCC; }
    
    .text-or { color: #F1C40F; }
    .text-vert { color: #2ECC71; }
    .text-orange { color: #E67E22; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. MOTEUR DE DONNÉES
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
    now = datetime.now().strftime("%d/%m/%Y à %H:%M")
    st.session_state.db["last_edit"] = f"{now} par {st.session_state.current_user}"
    save_json(DB_FILE, st.session_state.db)

def format_money(fcfa_amount):
    euro = f"{(fcfa_amount / TAUX_EURO):,.2f} €".replace(",", " ")
    fcfa = f"{int(fcfa_amount):,} FCFA".replace(",", " ")
    return euro, fcfa

# ==========================================
# 3. ÉCRAN DE CONNEXION
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<br><br><h1 style='text-align: center; color: #F1C40F; font-size: 3em;'>💍 Portail Issa & Fatou</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2em; color: #CCCCCC;'>Connectez-vous pour organiser votre nouvelle vie</p><br>", unsafe_allow_html=True)
    
    col1, col_centre, col3 = st.columns([1, 1.5, 1])
    with col_centre:
        tab_login, tab_register = st.tabs(["🔐 Se Connecter", "📝 Créer un compte"])
        
        with tab_login:
            email = st.text_input("Adresse Email")
            pwd = st.text_input("Mot de passe", type="password")
            if st.button("ACCÉDER AU DASHBOARD", use_container_width=True):
                if email in st.session_state.users and st.session_state.users[email] == pwd:
                    st.session_state.logged_in = True
                    st.session_state.current_user = email
                    st.rerun()
                else:
                    st.error("Email ou mot de passe incorrect.")
                    
        with tab_register:
            new_email = st.text_input("Nouvelle Adresse Email")
            new_pwd = st.text_input("Créer un Mot de passe", type="password")
            if st.button("CRÉER MON COMPTE", use_container_width=True):
                if new_email and new_pwd:
                    if new_email in st.session_state.users:
                        st.error("Ce compte existe déjà.")
                    else:
                        st.session_state.users[new_email] = new_pwd
                        save_json(USERS_FILE, st.session_state.users)
                        st.success("Compte créé avec succès !")
                else:
                    st.warning("Veuillez remplir tous les champs.")

# ==========================================
# 4. APPLICATION PRINCIPALE
# ==========================================
else:
    # --- HEADER ---
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h1 style='color: #F1C40F;'>👑 Planificateur — Issa & Fatou</h1>", unsafe_allow_html=True)
    with col2:
        st.info(f"👤 Connecté : **{st.session_state.current_user}**\n\n⏱️ Modif : {st.session_state.db.get('last_edit', 'Inconnue')}")
        if st.button("🚪 Déconnexion", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # --- CALCULS DASHBOARD ---
    tot_mar = sum(item["prix"] for item in st.session_state.db["mariage"])
    tot_mai = sum(item["prix"] for item in st.session_state.db["maison"])
    tot_crs = sum(item["prix"] for item in st.session_state.db["courses"])
    tot_gen = tot_mar + tot_mai + tot_crs

    mar_e, mar_f = format_money(tot_mar)
    mai_e, mai_f = format_money(tot_mai)
    crs_e, crs_f = format_money(tot_crs)
    gen_e, gen_f = format_money(tot_gen)

    # --- AFFICHAGE DASHBOARD XXL ---
    st.write("") 
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(f"""
        <div class='dash-card' style='border-top: 4px solid #F1C40F;'>
            <div class='dash-title'>💍 MARIAGE</div>
            <div class='dash-val-or'>{mar_e}</div>
            <div class='dash-sub'>{mar_f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class='dash-card' style='border-top: 4px solid #2ECC71;'>
            <div class='dash-title'>🏠 MAISON</div>
            <div class='dash-val-vert'>{mai_e}</div>
            <div class='dash-sub'>{mai_f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class='dash-card' style='border-top: 4px solid #E67E22;'>
            <div class='dash-title'>🛒 COURSES</div>
            <div class='dash-val-orange'>{crs_e}</div>
            <div class='dash-sub'>{crs_f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class='dash-card' style='border-top: 4px solid #3498DB; background-color: #161A25;'>
            <div class='dash-title'>📊 TOTAL GLOBAL</div>
            <div class='dash-val-bleu'>{gen_e}</div>
            <div class='dash-sub'>{gen_f}</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("") 

    # --- ONGLETS ---
    tab1, tab2, tab3, tab4 = st.tabs(["💍 MARIAGE & INVITÉS", "🏠 MAISON & MEUBLES", "🛒 COURSES DU MOIS", "🌴 VACANCES"])

    # ---------------------------------------------------------
    # ONGLET 1 : MARIAGE
    # ---------------------------------------------------------
    with tab1:
        sub1, sub2 = st.tabs(["💰 Dépenses Mariage", "👥 Liste des Invités"])
        
        with sub1:
            with st.form("form_mar", clear_on_submit=True):
                ca, cb, cc, cd, ce = st.columns([3, 2, 2, 1, 2])
                nom = ca.text_input("Dépense (Robe, Traiteur...)")
                cat = cb.selectbox("Catégorie", ["Habits", "Alliances", "Traiteur", "Décoration", "Lieu", "Autre"])
                prix = cc.number_input("Montant", min_value=0.0, step=10.0)
                devise = cd.selectbox("Devise", ["€", "FCFA"])
                submit = ce.form_submit_button("Ajouter la dépense")
                
                if submit and nom and prix > 0:
                    prix_final = prix * TAUX_EURO if devise == "€" else prix
                    st.session_state.db["mariage"].append({"id": str(uuid.uuid4()), "nom": nom, "cat": cat, "prix": prix_final})
                    save_db()
                    st.rerun()

            for item in st.session_state.db["mariage"]:
                col_item, col_btn = st.columns([6, 1])
                euro, fcfa = format_money(item["prix"])
                with col_item:
                    st.markdown(f"""
                    <div class='solid-card accent-mar'>
                        <div><span style='color: #F1C40F; font-weight: bold;'>[{item['cat']}]</span> &nbsp; <span style='font-size: 18px;'>{item['nom']}</span></div>
                        <div style='text-align: right;'><span class='prix-grand text-or'>{euro}</span><br><span class='prix-petit'>{fcfa}</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_btn:
                    if st.session_state.delete_confirm == item["id"]:
                        cy, cn = st.columns(2)
                        if cy.button("✅", key=f"ym_{item['id']}"):
                            st.session_state.db["mariage"] = [i for i in st.session_state.db["mariage"] if i["id"] != item["id"]]
                            st.session_state.delete_confirm = None
                            save_db()
                            st.rerun()
                        if cn.button("❌", key=f"nm_{item['id']}"):
                            st.session_state.delete_confirm = None
                            st.rerun()
                    else:
                        if st.button("🗑️", key=f"delm_{item['id']}"):
                            st.session_state.delete_confirm = item["id"]
                            st.rerun()
                    
        with sub2:
            with st.form("form_inv", clear_on_submit=True):
                ca, cb, cc = st.columns([4, 3, 2])
                nom_inv = ca.text_input("Nom complet de l'invité")
                camp = cb.selectbox("Camp", ["Famille Issa", "Famille Fatou", "Amis Communs"])
                if cc.form_submit_button("Ajouter l'invité") and nom_inv:
                    st.session_state.db["invites"].append({"id": str(uuid.uuid4()), "nom": nom_inv, "camp": camp})
                    save_db()
                    st.rerun()
            
            for item in st.session_state.db["invites"]:
                col_item, col_btn = st.columns([6, 1])
                with col_item:
                    st.markdown(f"""
                    <div class='solid-card accent-inv'>
                        <div><span style='color: #3498DB; font-weight: bold;'>{item['camp']}</span></div>
                        <div style='font-size: 18px;'>👤 {item['nom']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_btn:
                    if st.session_state.delete_confirm == item["id"]:
                        cy, cn = st.columns(2)
                        if cy.button("✅", key=f"yi_{item['id']}"):
                            st.session_state.db["invites"] = [i for i in st.session_state.db["invites"] if i["id"] != item["id"]]
                            st.session_state.delete_confirm = None
                            save_db()
                            st.rerun()
                        if cn.button("❌", key=f"ni_{item['id']}"):
                            st.session_state.delete_confirm = None
                            st.rerun()
                    else:
                        if st.button("🗑️", key=f"deli_{item['id']}"):
                            st.session_state.delete_confirm = item["id"]
                            st.rerun()

    # ---------------------------------------------------------
    # ONGLET 2 : MAISON
    # ---------------------------------------------------------
    with tab2:
        with st.form("form_mai", clear_on_submit=True):
            ca, cc, cd, ce = st.columns([4, 2, 1, 2])
            nom = ca.text_input("Meuble, Loyer, Équipement...")
            prix = cc.number_input("Montant", min_value=0.0, step=10.0)
            devise = cd.selectbox("Devise ", ["€", "FCFA"])
            submit = ce.form_submit_button("Ajouter à la Maison")
            
            if submit and nom and prix > 0:
                prix_final = prix * TAUX_EURO if devise == "€" else prix
                st.session_state.db["maison"].append({"id": str(uuid.uuid4()), "nom": nom, "prix": prix_final})
                save_db()
                st.rerun()

        for item in st.session_state.db["maison"]:
            col_item, col_btn = st.columns([6, 1])
            euro, fcfa = format_money(item["prix"])
            with col_item:
                st.markdown(f"""
                <div class='solid-card accent-mai'>
                    <div style='font-size: 18px;'>🛋️ {item['nom']}</div>
                    <div style='text-align: right;'><span class='prix-grand text-vert'>{euro}</span><br><span class='prix-petit'>{fcfa}</span></div>
                </div>
                """, unsafe_allow_html=True)
            with col_btn:
                if st.session_state.delete_confirm == item["id"]:
                    cy, cn = st.columns(2)
                    if cy.button("✅", key=f"yh_{item['id']}"):
                        st.session_state.db["maison"] = [i for i in st.session_state.db["maison"] if i["id"] != item["id"]]
                        st.session_state.delete_confirm = None
                        save_db()
                        st.rerun()
                    if cn.button("❌", key=f"nh_{item['id']}"):
                        st.session_state.delete_confirm = None
                        st.rerun()
                else:
                    if st.button("🗑️", key=f"delh_{item['id']}"):
                        st.session_state.delete_confirm = item["id"]
                        st.rerun()

    # ---------------------------------------------------------
    # ONGLET 3 : COURSES
    # ---------------------------------------------------------
    with tab3:
        with st.form("form_crs", clear_on_submit=True):
            ca, cc, cd, ce = st.columns([4, 2, 1, 2])
            nom = ca.text_input("Course (Riz, Huile, Viande...)")
            prix = cc.number_input("Montant", min_value=0.0, step=10.0)
            devise = cd.selectbox("Devise  ", ["€", "FCFA"])
            submit = ce.form_submit_button("Ajouter la course")
            
            if submit and nom and prix > 0:
                prix_final = prix * TAUX_EURO if devise == "€" else prix
                st.session_state.db["courses"].append({"id": str(uuid.uuid4()), "nom": nom, "prix": prix_final})
                save_db()
                st.rerun()

        for item in st.session_state.db["courses"]:
            col_item, col_btn = st.columns([6, 1])
            euro, fcfa = format_money(item["prix"])
            with col_item:
                st.markdown(f"""
                <div class='solid-card accent-crs'>
                    <div style='font-size: 18px;'>🛒 {item['nom']}</div>
                    <div style='text-align: right;'><span class='prix-grand text-orange'>{euro}</span><br><span class='prix-petit'>{fcfa}</span></div>
                </div>
                """, unsafe_allow_html=True)
            with col_btn:
                if st.session_state.delete_confirm == item["id"]:
                    cy, cn = st.columns(2)
                    if cy.button("✅", key=f"yc_{item['id']}"):
                        st.session_state.db["courses"] = [i for i in st.session_state.db["courses"] if i["id"] != item["id"]]
                        st.session_state.delete_confirm = None
                        save_db()
                        st.rerun()
                    if cn.button("❌", key=f"nc_{item['id']}"):
                        st.session_state.delete_confirm = None
                        st.rerun()
                else:
                    if st.button("🗑️", key=f"delc_{item['id']}"):
                        st.session_state.delete_confirm = item["id"]
                        st.rerun()

    # ---------------------------------------------------------
    # ONGLET 4 : VACANCES
    # ---------------------------------------------------------
    with tab4:
        with st.form("form_vac", clear_on_submit=True):
            ca, ce = st.columns([4, 1])
            nom = ca.text_input("Activité (Safari, Plage, Dîner...)")
            submit = ce.form_submit_button("Planifier")
            
            if submit and nom:
                st.session_state.db["vacances"].append({"id": str(uuid.uuid4()), "nom": nom})
                save_db()
                st.rerun()

        for item in st.session_state.db["vacances"]:
            col_item, col_btn = st.columns([6, 1])
            with col_item:
                st.markdown(f"""
                <div class='solid-card accent-vac'>
                    <div style='font-size: 18px;'>✈️ {item['nom']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col_btn:
                if st.session_state.delete_confirm == item["id"]:
                    cy, cn = st.columns(2)
                    if cy.button("✅", key=f"yv_{item['id']}"):
                        st.session_state.db["vacances"] = [i for i in st.session_state.db["vacances"] if i["id"] != item["id"]]
                        st.session_state.delete_confirm = None
                        save_db()
                        st.rerun()
                    if cn.button("❌", key=f"nv_{item['id']}"):
                        st.session_state.delete_confirm = None
                        st.rerun()
                else:
                    if st.button("🗑️", key=f"delv_{item['id']}"):
                        st.session_state.delete_confirm = item["id"]
                        st.rerun()
