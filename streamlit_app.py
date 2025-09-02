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

def get_tube_fiber_color(number):
    """Retourne la couleur selon le modulo 12 pour tubes et fibres"""
    colors = [
        '#dc2626',  # rouge
        '#2563eb',  # bleu  
        '#16a34a',  # vert
        '#eab308',  # jaune
        '#9333ea',  # violet
        '#ffffff',  # blanc
        '#ea580c',  # orange
        '#6b7280',  # gris
        '#92400e',  # marron
        '#000000',  # noir
        '#0891b2',  # turquoise
        '#ec4899'   # rose
    ]
    
    if not number or number == '' or pd.isna(number):
        return '#9ca3af'  # gris par défaut
    
    try:
        num = int(float(str(number)))
        if num <= 0:
            return '#9ca3af'
        index = (num - 1) % 12
        return colors[index]
    except:
        return '#9ca3af'

def get_text_color(bg_color):
    """Retourne noir ou blanc selon la couleur de fond"""
    if bg_color in ['#ffffff', '#eab308']:  # blanc et jaune
        return '#000000'
    return '#ffffff'

def extract_route_segments(row):
    """Extrait les segments de route d'une ligne avec détection automatique"""
    segments = []
    
    # Détecter automatiquement tous les segments jusqu'à la dernière colonne "STOCKEE"
    current_index = 9  # Commencer à la colonne 9 comme avant
    segment_number = 1
    
    while current_index < len(row):
        # Chercher un câble à cette position
        if current_index < len(row) and row.iloc[current_index] and pd.notna(row.iloc[current_index]) and str(row.iloc[current_index]).strip():
            cable = str(row.iloc[current_index]).strip()
            capacite = str(row.iloc[current_index + 2]).strip() if current_index + 2 < len(row) and pd.notna(row.iloc[current_index + 2]) else ''
            tube = str(row.iloc[current_index + 3]).strip() if current_index + 3 < len(row) and pd.notna(row.iloc[current_index + 3]) else ''
            fibre = str(row.iloc[current_index + 4]).strip() if current_index + 4 < len(row) and pd.notna(row.iloc[current_index + 4]) else ''
            boite = str(row.iloc[current_index + 5]).strip() if current_index + 5 < len(row) and pd.notna(row.iloc[current_index + 5]) else ''
            
            # Chercher l'état dans les colonnes suivantes (jusqu'à 10 colonnes après)
            etat = ''
            for i in range(current_index + 6, min(current_index + 16, len(row))):
                if i < len(row) and pd.notna(row.iloc[i]):
                    cell_value = str(row.iloc[i]).strip().upper()
                    if cell_value in ['STOCKEE', 'EN PASSAGE', 'EPISSUREE', 'OK', 'NOK']:
                        etat = cell_value
                        break
            
            segment = {
                'title': f'Segment {segment_number}',
                'cable': cable,
                'capacite': capacite,
                'tube': tube,
                'fibre': fibre,
                'boite': boite,
                'etat': etat
            }
            segments.append(segment)
            
            segment_number += 1
            current_index += 9  # Passer au segment suivant (approximation)
        else:
            current_index += 1
        
        # Limite de sécurité pour éviter boucle infinie
        if segment_number > 10:
            break
    
    return segments

def get_pbo_tube_fiber(row):
    """Récupère le tube et fibre du PBO extrémité (premier segment)"""
    if len(row) > 12 and pd.notna(row.iloc[12]):  # Tube première position
        tube = str(row.iloc[12]).strip()
    else:
        tube = ''
        
    if len(row) > 13 and pd.notna(row.iloc[13]):  # Fibre première position  
        fibre = str(row.iloc[13]).strip()
    else:
        fibre = ''
    
    return tube, fibre

def display_segment(segment, index):
    """Affiche un segment de route sans titre"""
    
    col1, col2, col3 = st.columns([3, 2, 2])
    
    with col1:
        if segment['cable']:
            cable_capacite = f"{segment['cable']}_{segment['capacite']}" if segment['capacite'] else segment['cable']
            st.metric("🔌 Câble_Capacité", cable_capacite[:30] + "..." if len(cable_capacite) > 30 else cable_capacite)
        if segment['boite']:
            st.metric("📦 Boîte", str(segment['boite'])[:20] + "..." if len(str(segment['boite'])) > 20 else str(segment['boite']))
    
    with col2:
        # Tube et Fibre collés ensemble avec couleurs
        if segment['tube'] or segment['fibre']:
            tube_num = segment['tube'] if segment['tube'] else ''
            fibre_num = segment['fibre'] if segment['fibre'] else ''
            
            if tube_num and fibre_num:
                try:
                    tube_int = int(float(tube_num))
                    fibre_int = int(float(fibre_num))
                    
                    tube_color = get_tube_fiber_color(tube_int)
                    tube_text_color = get_text_color(tube_color)
                    fibre_color = get_tube_fiber_color(fibre_int)  
                    fibre_text_color = get_text_color(fibre_color)
                    
                    st.markdown(f"""
                    <div style="margin-bottom: 1rem;">
                        <div style="font-size: 0.75rem; color: #6b7280; margin-bottom: 0.25rem; font-weight: 500;">🔧💡 Tube-Fibre</div>
                        <div style="display: flex; gap: 0.25rem; align-items: center;">
                            <div style="
                                background-color: {tube_color}; 
                                color: {tube_text_color}; 
                                padding: 0.5rem 0.75rem; 
                                border-radius: 0.5rem; 
                                font-weight: bold; 
                                font-size: 0.875rem;
                                border: 2px solid {tube_color};
                                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                            ">T{tube_int}</div>
                            <div style="
                                background-color: {fibre_color}; 
                                color: {fibre_text_color}; 
                                padding: 0.5rem 0.75rem; 
                                border-radius: 0.5rem; 
                                font-weight: bold; 
                                font-size: 0.875rem;
                                border: 2px solid {fibre_color};
                                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                            ">F{fibre_int}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                except ValueError:
                    st.metric("🔧💡 Tube-Fibre", f"T{tube_num}F{fibre_num}")
            elif tube_num:
                try:
                    tube_int = int(float(tube_num))
                    tube_color = get_tube_fiber_color(tube_int)
                    tube_text_color = get_text_color(tube_color)
                    
                    st.markdown(f"""
                    <div style="margin-bottom: 1rem;">
                        <div style="font-size: 0.75rem; color: #6b7280; margin-bottom: 0.25rem; font-weight: 500;">🔧 Tube</div>
                        <div style="
                            background-color: {tube_color}; 
                            color: {tube_text_color}; 
                            padding: 0.5rem 0.75rem; 
                            border-radius: 0.5rem; 
                            font-weight: bold; 
                            font-size: 0.875rem;
                            display: inline-block;
                            border: 2px solid {tube_color};
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        ">T{tube_int}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                except ValueError:
                    st.metric("🔧 Tube", f"T{tube_num}")
            elif fibre_num:
                try:
                    fibre_int = int(float(fibre_num))
                    fibre_color = get_tube_fiber_color(fibre_int)
                    fibre_text_color = get_text_color(fibre_color)
                    
                    st.markdown(f"""
                    <div style="margin-bottom: 1rem;">
                        <div style="font-size: 0.75rem; color: #6b7280; margin-bottom: 0.25rem; font-weight: 500;">💡 Fibre</div>
                        <div style="
                            background-color: {fibre_color}; 
                            color: {fibre_text_color}; 
                            padding: 0.5rem 0.75rem; 
                            border-radius: 0.5rem; 
                            font-weight: bold; 
                            font-size: 0.875rem;
                            display: inline-block;
                            border: 2px solid {fibre_color};
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        ">F{fibre_int}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                except ValueError:
                    st.metric("💡 Fibre", f"F{fibre_num}")
            
    with col3:
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
            # Charger le fichier Excel avec gestion d'erreurs améliorée
            try:
                # Essayer d'abord avec openpyxl (pour .xlsx)
                df = pd.read_excel(uploaded_file, engine='openpyxl')
            except Exception as e1:
                try:
                    # Fallback sur xlrd (pour .xls)
                    df = pd.read_excel(uploaded_file, engine='xlrd')
                except Exception as e2:
                    try:
                        # Dernière tentative sans spécifier d'engine
                        df = pd.read_excel(uploaded_file)
                    except Exception as e3:
                        st.error(f"❌ Impossible de lire le fichier Excel: {str(e3)}")
                        st.info("💡 Vérifiez que votre fichier est un Excel valide (.xlsx ou .xls)")
                        return
            
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
                            
                            # Formater l'identifiant: Tiroir + P + pos + tube + fibre du PBO extrémité
                            tiroir = str(row.iloc[0]) if len(row) > 0 and pd.notna(row.iloc[0]) else "N/A"
                            pos = str(row.iloc[1]) if len(row) > 1 and pd.notna(row.iloc[1]) else "N/A"
                            
                            # Récupérer tube et fibre du PBO extrémité  
                            pbo_tube, pbo_fibre = get_pbo_tube_fiber(row)
                            
                            # Construire l'identifiant
                            base_id = f"{tiroir}P{pos}"
                            if pbo_tube and pbo_fibre:
                                try:
                                    tube_int = int(float(pbo_tube))
                                    fibre_int = int(float(pbo_fibre))
                                    full_id = f"{base_id} - T{tube_int}F{fibre_int}"
                                except ValueError:
                                    full_id = f"{base_id} - T{pbo_tube}F{pbo_fibre}"
                            elif pbo_tube:
                                try:
                                    tube_int = int(float(pbo_tube))
                                    full_id = f"{base_id} - T{tube_int}"
                                except ValueError:
                                    full_id = f"{base_id} - T{pbo_tube}"
                            elif pbo_fibre:
                                try:
                                    fibre_int = int(float(pbo_fibre))
                                    full_id = f"{base_id} - F{fibre_int}"
                                except ValueError:
                                    full_id = f"{base_id} - F{pbo_fibre}"
                            else:
                                full_id = base_id
                            
                            with st.expander(f"📍 {full_id}"):
                                
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
