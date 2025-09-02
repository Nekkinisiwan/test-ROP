# app.py - Application Route Optique avec Streamlit
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# Configuration de la page
st.set_page_config(
    page_title="Route Optique Pro",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé pour mobile
st.markdown("""
<style>
    .main > div {
        max-width: 1200px;
        padding-top: 1rem;
    }
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        border: none;
        padding: 0.5rem;
        font-weight: 600;
    }
    .search-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        color: white;
    }
    .segment-card {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #3b82f6;
        margin: 0.5rem 0;
    }
    .status-success {
        background: #dcfce7;
        color: #166534;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-warning {
        background: #fef3c7;
        color: #92400e;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-error {
        background: #fee2e2;
        color: #dc2626;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        font-size: 0.8rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

def get_status_class(status):
    """Retourne la classe CSS selon le statut"""
    if not status:
        return "status-warning"
    status_upper = str(status).upper()
    if status_upper in ['STOCKEE', 'OK']:
        return "status-success"
    elif status_upper in ['EPISSUREE', 'EN PASSAGE']:
        return "status-warning"
    elif status_upper == 'NOK':
        return "status-error"
    return "status-warning"

def extract_route_segments(row):
    """Extrait les segments de route d'une ligne"""
    segments = []
    
    # Segment 1 (colonnes 9-17)
    if len(row) > 9 and pd.notna(row.iloc[9]):
        segment1 = {
            'title': '🔌 Segment 1',
            'cable': row.iloc[9] if len(row) > 9 else '',
            'capacite': row.iloc[11] if len(row) > 11 else '',
            'tube': row.iloc[12] if len(row) > 12 else '',
            'fibre': row.iloc[13] if len(row) > 13 else '',
            'boite': row.iloc[14] if len(row) > 14 else '',
            'etat': row.iloc[17] if len(row) > 17 else ''
        }
        segments.append(segment1)
    
    # Segment 2 (colonnes 18-26)  
    if len(row) > 18 and pd.notna(row.iloc[18]):
        segment2 = {
            'title': '⚡ Segment 2',
            'cable': row.iloc[18] if len(row) > 18 else '',
            'capacite': row.iloc[20] if len(row) > 20 else '',
            'tube': row.iloc[21] if len(row) > 21 else '',
            'fibre': row.iloc[22] if len(row) > 22 else '',
            'boite': row.iloc[23] if len(row) > 23 else '',
            'etat': row.iloc[26] if len(row) > 26 else ''
        }
        segments.append(segment2)
        
    return segments

def display_segment(segment, index):
    """Affiche un segment de route"""
    st.markdown(f"""
    <div class="segment-card">
        <h4>{segment['title']}</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if segment['cable']:
            st.metric("🔌 Câble", str(segment['cable'])[:20] + "..." if len(str(segment['cable'])) > 20 else str(segment['cable']))
        if segment['tube']:
            st.metric("🔧 Tube", segment['tube'])
    
    with col2:
        if segment['capacite']:
            st.metric("📊 Capacité", segment['capacite'])
        if segment['fibre']:
            st.metric("💡 Fibre", segment['fibre'])
            
    with col3:
        if segment['boite']:
            st.metric("📦 Boîte", str(segment['boite'])[:15] + "..." if len(str(segment['boite'])) > 15 else str(segment['boite']))
        if segment['etat']:
            status_class = get_status_class(segment['etat'])
            st.markdown(f'<span class="{status_class}">📍 {segment["etat"]}</span>', unsafe_allow_html=True)

# Interface principale
def main():
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="color: #1e40af; margin-bottom: 0;">🔌 Route Optique Pro</h1>
        <p style="color: #6b7280; margin-top: 0;">Analyse avancée des infrastructures optiques</p>
    </div>
    """, unsafe_allow_html=True)

    # Upload de fichier
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    st.markdown("### 📊 Charger votre fichier Excel")
    
    uploaded_file = st.file_uploader(
        "Sélectionnez un fichier Excel (.xlsx, .xls)",
        type=['xlsx', 'xls'],
        help="Glissez-déposez votre fichier ici ou cliquez pour parcourir"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file is not None:
        try:
            # Charger le fichier Excel
            if uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file, engine='openpyxl')
            else:
                df = pd.read_excel(uploaded_file, engine='xlrd')
            
            st.success(f"✅ Fichier chargé avec succès ! {len(df)} lignes trouvées.")
            
            # Interface de recherche
            st.markdown("### 🔍 Recherche Intelligente")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                search_term = st.text_input(
                    "",
                    placeholder="🔍 Saisir un code, référence, ou identifiant...",
                    help="Recherche dans toutes les colonnes du fichier"
                )
            
            with col2:
                search_button = st.button("🔍 Rechercher", type="primary")
            
            # Recherche
            if search_term or search_button:
                if search_term:
                    # Recherche dans toutes les colonnes
                    mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
                    results = df[mask]
                    
                    if len(results) > 0:
                        st.markdown(f"### 📋 {len(results)} résultat(s) trouvé(s)")
                        
                        # Afficher les résultats
                        for idx, (_, row) in enumerate(results.head(10).iterrows()):
                            with st.expander(f"📍 Ligne {row.name + 2} - {search_term} trouvé"):
                                
                                # Informations générales
                                col1, col2 = st.columns(2)
                                with col1:
                                    if len(row) > 0:
                                        st.metric("🏠 Tiroir", str(row.iloc[0]) if pd.notna(row.iloc[0]) else "N/A")
                                with col2:
                                    if len(row) > 1:
                                        st.metric("📍 Position", str(row.iloc[1]) if pd.notna(row.iloc[1]) else "N/A")
                                
                                # Extraire et afficher les segments
                                segments = extract_route_segments(row)
                                
                                if segments:
                                    st.markdown("#### 🗺️ Route Détaillée")
                                    for i, segment in enumerate(segments):
                                        display_segment(segment, i)
                                        if i < len(segments) - 1:
                                            st.markdown("---")
                                else:
                                    st.info("ℹ️ Aucun segment de route détaillé trouvé pour cette ligne")
                                    
                                    # Afficher les données brutes si pas de segments
                                    st.markdown("**📄 Données de la ligne :**")
                                    for i, value in enumerate(row):
                                        if pd.notna(value) and str(value).strip():
                                            col_name = df.columns[i] if i < len(df.columns) else f"Col {i+1}"
                                            st.text(f"{col_name}: {value}")
                        
                        if len(results) > 10:
                            st.info(f"ℹ️ Affichage des 10 premiers résultats sur {len(results)} trouvés")
                            
                    else:
                        st.warning(f"❌ Aucun résultat trouvé pour '{search_term}'")
                        st.info("💡 Essayez avec un terme de recherche différent ou plus court")
            
            # Aperçu des données (optionnel)
            with st.expander("👁️ Aperçu du fichier (premiers lignes)"):
                st.dataframe(df.head(), use_container_width=True)
                st.caption(f"Fichier: {uploaded_file.name} | Colonnes: {len(df.columns)} | Lignes: {len(df)}")
                
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement du fichier: {str(e)}")
            st.info("💡 Vérifiez que votre fichier Excel est valide et n'est pas protégé par mot de passe")

if __name__ == "__main__":
    main()
