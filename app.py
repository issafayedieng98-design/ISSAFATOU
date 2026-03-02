import streamlit as st
from datetime import date
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Notre Mariage au Sénégal 🇸🇳", layout="wide")

# Barre latérale pour la navigation
st.sidebar.title("Menu Principal")
page = st.sidebar.radio("Aller vers :", ["🏠 Dashboard", "💍 Mariage (CCAM & Dossier)", "🌍 Voyage au Sénégal"])

# --- SECTION DASHBOARD ---
if page == "🏠 Dashboard":
    st.title("🇸🇳 Notre Aventure : Mariage & Sénégal")
    
    # Calcul du compte à rebours (Exemple : 15 Décembre 2026)
    date_mariage = date(2026, 12, 15)
    jours_restants = (date_mariage - date.today()).days
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Jours avant le grand OUI", value=f"{jours_restants} jours")
    with col2:
        st.info("💡 Conseil du jour : Vérifiez la validité de vos passeports !")

    st.image("https://images.unsplash.com/photo-1598450844431-238209e87ae3", caption="Bientôt Dakar...")

# --- SECTION MARIAGE ---
elif page == "💍 Mariage (CCAM & Dossier)":
    st.title("💍 Organisation du Mariage")
    
    st.subheader("Check-list Documents CCAM")
    docs = {
        "Document": ["Acte de naissance ( < 3 mois)", "Preuve de nationalité", "Justificatif de domicile", "Questionnaire Consulaire"],
        "Lui": [False, False, False, False],
        "Elle": [False, False, False, False]
    }
    df_docs = pd.DataFrame(docs)
    st.data_editor(df_docs, use_container_width=True) # Permet de cocher en direct

    st.subheader("Budget Mariage")
    st.text_input("Budget Total Estimé (€)", value="5000")

# --- SECTION VOYAGE ---
elif page == "🌍 Voyage au Sénégal":
    st.title("🌍 Planification du Voyage")
    
    st.tabs(["📍 Itinéraire", "✈️ Billets & Logements", "🎒 Sac à dos"])
    
    with st.expander("Voir l'itinéraire prévu"):
        st.write("""
        1. **Dakar** : Arrivée et dépôt du dossier à l'ambassade.
        2. **Lac Rose** : Détente et balade en pirogue.
        3. **Casamance** : Nature sauvage pour la lune de miel.
        """)