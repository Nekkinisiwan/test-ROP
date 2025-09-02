def get_pbo_tube_fiber(row, df):
    """Récupère le tube et fibre du PBO extrémité (premier segment) par nom de colonne"""
    
    # Chercher les premières colonnes tube et fibre
    tube_names = ['tube', 'Tube', 'TUBE']
    fibre_names = ['fibre', 'Fibre', 'FIBRE', 'fiber', 'Fiber']
    
    tube = ''
    fibre = ''
    
    # Trouver la première colonne tube
    for col in df.columns:
        col_lower = col.lower().strip()
        for tube_name in tube_names:
            if tube_name.lower() in col_lower:
                if col in row.index and pd.notna(row[col]):
                    tube = str(row[col]).strip()
                    break
        if tube:
            break
    
    # Trouver la première colonne fibre
    for col in df.columns:
        col_lower = col.lower().strip()
        for fibre_name in fibre_names:
            if fibre_name.lower() in col_lower:
                if col in row.index and pd.notna(row[col]):
                    fibre = str(row[col]).strip()
                    break
        if fibre:
            break
    
    return tube, fibre# app.py - Application Route Optique avec Streamlit
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# Configuration de la page
st.set_page_config(
    page_title="Route Optique ICT",
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

def find_column_by_name(df, possible_names):
    """Trouve une colonne par ses noms possibles (case insensitive)"""
    df_columns = [col.lower().strip() for col in df.columns]
    
    for name in possible_names:
        name_lower = name.lower().strip()
        for i, col in enumerate(df_columns):
            if name_lower in col or col in name_lower:
                return df.columns[i]  # Retourne le nom original
    return None

def extract_route_segments(row, df):
    """Extrait les segments de route d'une ligne en se basant sur les noms d'entêtes"""
    segments = []
    
    # Définir les noms possibles pour chaque type de colonne
    cable_names = ['cable', 'câble', 'Cable', 'Câble', 'CABLE', 'CÂBLE']
    capacite_names = ['capacité', 'capacite', 'Capacité', 'Capacite', 'CAPACITÉ', 'CAPACITE', 'capacity']
    tube_names = ['tube', 'Tube', 'TUBE']
    fibre_names = ['fibre', 'Fibre', 'FIBRE', 'fiber', 'Fiber']
    etat_names = ['etat', 'état', 'Etat', 'État', 'ETAT', 'ÉTAT', 'state', 'State', 'STATUS', 'status']
    
    # Identifier toutes les colonnes de chaque type
    cable_cols = []
    capacite_cols = []
    tube_cols = []
    fibre_cols = []
    etat_cols = []
    
    for col in df.columns:
        col_lower = col.lower().strip()
        
        # Vérifier si c'est une colonne câble
        for cable_name in cable_names:
            if cable_name.lower() in col_lower:
                cable_cols.append(col)
                break
                
        # Vérifier si c'est une colonne capacité
        for cap_name in capacite_names:
            if cap_name.lower() in col_lower:
                capacite_cols.append(col)
                break
                
        # Vérifier si c'est une colonne tube
        for tube_name in tube_names:
            if tube_name.lower() in col_lower:
                tube_cols.append(col)
                break
                
        # Vérifier si c'est une colonne fibre
        for fibre_name in fibre_names:
            if fibre_name.lower() in col_lower:
                fibre_cols.append(col)
                break
                
        # Vérifier si c'est une colonne état
        for etat_name in etat_names:
            if etat_name.lower() in col_lower:
                etat_cols.append(col)
                break
    
    # Créer des segments basés sur le nombre de colonnes trouvées
    max_segments = max(len(cable_cols), len(capacite_cols), len(tube_cols), len(fibre_cols), len(etat_cols))
    
    for i in range(max_segments):
        cable = ''
        capacite = ''
        tube = ''
        fibre = ''
        etat = ''
        
        # Récupérer les valeurs pour chaque segment
        if i < len(cable_cols) and cable_cols[i] in row.index:
            cable = str(row[cable_cols[i]]).strip() if pd.notna(row[cable_cols[i]]) else ''
            
        if i < len(capacite_cols) and capacite_cols[i] in row.index:
            capacite = str(row[capacite_cols[i]]).strip() if pd.notna(row[capacite_cols[i]]) else ''
            
        if i < len(tube_cols) and tube_cols[i] in row.index:
            tube = str(row[tube_cols[i]]).strip() if pd.notna(row[tube_cols[i]]) else ''
            
        if i < len(fibre_cols) and fibre_cols[i] in row.index:
            fibre = str(row[fibre_cols[i]]).strip() if pd.notna(row[fibre_cols[i]]) else ''
            
        if i < len(etat_cols) and etat_cols[i] in row.index:
            etat_val = str(row[etat_cols[i]]).strip().upper() if pd.notna(row[etat_cols[i]]) else ''
            if etat_val in ['STOCKEE', 'EN PASSAGE', 'EPISSUREE', 'OK', 'NOK']:
                etat = etat_val
        
        # Créer un segment s'il y a au moins une valeur
        if any([cable, capacite, tube, fibre, etat]):
            segment = {
                'title': f'Segment {i + 1}',
                'cable': cable,
                'capacite': capacite,
                'tube': tube,
                'fibre': fibre,
                'boite': '',  # Pas utilisé dans la vue condensée
                'etat': etat
            }
            segments.append(segment)
    
    return segments

def get_tiroir_pos(row, df):
    """Récupère tiroir et position par nom de colonne ou position par défaut"""
    
    # Chercher par noms de colonnes d'abord
    tiroir_names = ['tiroir', 'Tiroir', 'TIROIR', 'drawer']
    pos_names = ['pos', 'Pos', 'POS', 'position', 'Position', 'POSITION']
    
    tiroir = ''
    pos = ''
    
    # Chercher tiroir par nom
    for col in df.columns:
        col_lower = col.lower().strip()
        for tiroir_name in tiroir_names:
            if tiroir_name.lower() in col_lower:
                if col in row.index and pd.notna(row[col]):
                    tiroir = str(row[col]).strip()
                    break
        if tiroir:
            break
    
    # Chercher position par nom  
    for col in df.columns:
        col_lower = col.lower().strip()
        for pos_name in pos_names:
            if pos_name.lower() in col_lower:
                if col in row.index and pd.notna(row[col]):
                    pos = str(row[col]).strip()
                    break
        if pos:
            break
    
    # Fallback sur les premières colonnes si pas trouvé par nom
    if not tiroir and len(row) > 0 and pd.notna(row.iloc[0]):
        tiroir = str(row.iloc[0]).strip()
        
    if not pos and len(row) > 1 and pd.notna(row.iloc[1]):
        pos = str(row.iloc[1]).strip()
    
    return tiroir, pos
    """Récupère le tube et fibre du PBO extrémité (premier segment) par nom de colonne"""
    
    # Chercher les premières colonnes tube et fibre
    tube_names = ['tube', 'Tube', 'TUBE']
    fibre_names = ['fibre', 'Fibre', 'FIBRE', 'fiber', 'Fiber']
    
    tube = ''
    fibre = ''
    
    # Trouver la première colonne tube
    for col in df.columns:
        col_lower = col.lower().strip()
        for tube_name in tube_names:
            if tube_name.lower() in col_lower:
                if col in row.index and pd.notna(row[col]):
                    tube = str(row[col]).strip()
                    break
        if tube:
            break
    
    # Trouver la première colonne fibre
    for col in df.columns:
        col_lower = col.lower().strip()
        for fibre_name in fibre_names:
            if fibre_name.lower() in col_lower:
                if col in row.index and pd.notna(row[col]):
                    fibre = str(row[col]).strip()
                    break
        if fibre:
            break
    
    return tube, fibre

def display_segment(segment, index):
    """Affiche un segment de route condensé sans icônes"""
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Tube et Fibre collés ensemble avec couleurs + État à côté
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
                    
                    # Affichage tube-fibre + état sur la même ligne
                    tube_fibre_html = f"""
                    <div style="display: flex; gap: 0.5rem; align-items: center; margin-bottom: 1rem;">
                        <div style="display: flex; gap: 0.25rem;">
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
                    """
                    
                    # Ajouter l'état à côté si disponible
                    if segment['etat']:
                        status_class = get_status_class(segment['etat'])
                        if 'success' in status_class:
                            status_bg = '#dcfce7'
                            status_color = '#166534'
                        elif 'warning' in status_class:
                            status_bg = '#fef3c7'  
                            status_color = '#92400e'
                        elif 'error' in status_class:
                            status_bg = '#fee2e2'
                            status_color = '#dc2626'
                        else:
                            status_bg = '#f3f4f6'
                            status_color = '#374151'
                            
                        tube_fibre_html += f"""
                        <div style="
                            background-color: {status_bg}; 
                            color: {status_color}; 
                            padding: 0.5rem 0.75rem; 
                            border-radius: 0.5rem; 
                            font-weight: 600; 
                            font-size: 0.75rem;
                            text-transform: uppercase;
                            border: 2px solid {status_bg};
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        ">{segment['etat']}</div>
                        """
                    
                    tube_fibre_html += "</div>"
                    st.markdown(tube_fibre_html, unsafe_allow_html=True)
                    
                except ValueError:
                    # Fallback si conversion échoue
                    fallback_html = f'<div style="font-weight: bold; margin-bottom: 1rem;">T{tube_num}F{fibre_num}'
                    if segment['etat']:
                        fallback_html += f' - {segment["etat"]}'
                    fallback_html += '</div>'
                    st.markdown(fallback_html, unsafe_allow_html=True)
                    
            elif tube_num:
                try:
                    tube_int = int(float(tube_num))
                    tube_color = get_tube_fiber_color(tube_int)
                    tube_text_color = get_text_color(tube_color)
                    
                    tube_html = f"""
                    <div style="display: flex; gap: 0.5rem; align-items: center; margin-bottom: 1rem;">
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
                    """
                    
                    if segment['etat']:
                        status_class = get_status_class(segment['etat'])
                        if 'success' in status_class:
                            status_bg = '#dcfce7'
                            status_color = '#166534'
                        elif 'warning' in status_class:
                            status_bg = '#fef3c7'  
                            status_color = '#92400e'
                        elif 'error' in status_class:
                            status_bg = '#fee2e2'
                            status_color = '#dc2626'
                        else:
                            status_bg = '#f3f4f6'
                            status_color = '#374151'
                            
                        tube_html += f"""
                        <div style="
                            background-color: {status_bg}; 
                            color: {status_color}; 
                            padding: 0.5rem 0.75rem; 
                            border-radius: 0.5rem; 
                            font-weight: 600; 
                            font-size: 0.75rem;
                            text-transform: uppercase;
                            border: 2px solid {status_bg};
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        ">{segment['etat']}</div>
                        """
                    
                    tube_html += "</div>"
                    st.markdown(tube_html, unsafe_allow_html=True)
                    
                except ValueError:
                    fallback = f'T{tube_num}'
                    if segment['etat']:
                        fallback += f' - {segment["etat"]}'
                    st.markdown(f'<div style="font-weight: bold; margin-bottom: 1rem;">{fallback}</div>', unsafe_allow_html=True)
                    
            elif fibre_num:
                try:
                    fibre_int = int(float(fibre_num))
                    fibre_color = get_tube_fiber_color(fibre_int)
                    fibre_text_color = get_text_color(fibre_color)
                    
                    fibre_html = f"""
                    <div style="display: flex; gap: 0.5rem; align-items: center; margin-bottom: 1rem;">
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
                    """
                    
                    if segment['etat']:
                        status_class = get_status_class(segment['etat'])
                        if 'success' in status_class:
                            status_bg = '#dcfce7'
                            status_color = '#166534'
                        elif 'warning' in status_class:
                            status_bg = '#fef3c7'  
                            status_color = '#92400e'
                        elif 'error' in status_class:
                            status_bg = '#fee2e2'
                            status_color = '#dc2626'
                        else:
                            status_bg = '#f3f4f6'
                            status_color = '#374151'
                            
                        fibre_html += f"""
                        <div style="
                            background-color: {status_bg}; 
                            color: {status_color}; 
                            padding: 0.5rem 0.75rem; 
                            border-radius: 0.5rem; 
                            font-weight: 600; 
                            font-size: 0.75rem;
                            text-transform: uppercase;
                            border: 2px solid {status_bg};
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        ">{segment['etat']}</div>
                        """
                    
                    fibre_html += "</div>"
                    st.markdown(fibre_html, unsafe_allow_html=True)
                    
                except ValueError:
                    fallback = f'F{fibre_num}'
                    if segment['etat']:
                        fallback += f' - {segment["etat"]}'
                    st.markdown(f'<div style="font-weight: bold; margin-bottom: 1rem;">{fallback}</div>', unsafe_allow_html=True)
            
            elif segment['etat']:
                # Si seulement l'état est disponible
                status_class = get_status_class(segment['etat'])
                st.markdown(f'<span class="{status_class}">{segment["etat"]}</span>', unsafe_allow_html=True)
                
    with col2:
        # Capacité en entier seulement
        if segment['capacite']:
            try:
                capacite_int = int(float(segment['capacite']))
                st.metric("Capacité", capacite_int)
            except ValueError:
                st.metric("Capacité", segment['capacite'])

# Interface principale
def main():
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="color: #1e40af; margin-bottom: 0;">🔌 Route Optique ICT</h1>
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
            
            # Afficher les colonnes détectées pour la route
            st.markdown("**🔍 Colonnes détectées pour les routes :**")
            col1, col2, col3, col4 = st.columns(4)
            
            # Détecter les colonnes par type
            tiroir_cols = []
            pos_cols = []
            cable_cols = []
            capacite_cols = []
            tube_cols = []
            fibre_cols = []
            etat_cols = []
            
            tiroir_names = ['tiroir', 'drawer']
            pos_names = ['pos', 'position']
            cable_names = ['cable', 'câble']
            capacite_names = ['capacité', 'capacite', 'capacity']
            tube_names = ['tube']
            fibre_names = ['fibre', 'fiber']
            etat_names = ['etat', 'état', 'state', 'status']
            
            for col in df.columns:
                col_lower = col.lower().strip()
                
                if any(name in col_lower for name in tiroir_names):
                    tiroir_cols.append(col)
                elif any(name in col_lower for name in pos_names):
                    pos_cols.append(col)
                elif any(name in col_lower for name in cable_names):
                    cable_cols.append(col)
                elif any(name in col_lower for name in capacite_names):
                    capacite_cols.append(col)
                elif any(name in col_lower for name in tube_names):
                    tube_cols.append(col)
                elif any(name in col_lower for name in fibre_names):
                    fibre_cols.append(col)
                elif any(name in col_lower for name in etat_names):
                    etat_cols.append(col)
            
            with col1:
                if tiroir_cols:
                    st.success(f"🏠 Tiroir: {len(tiroir_cols)} col(s)")
                    for col in tiroir_cols[:2]:
                        st.caption(f"• {col}")
                else:
                    st.info("ℹ️ Tiroir: Col 1 (défaut)")
                    
                if tube_cols:
                    st.success(f"🔧 Tube: {len(tube_cols)} col(s)")
                    for col in tube_cols[:2]:
                        st.caption(f"• {col}")
                else:
                    st.warning("⚠️ Aucune colonne tube")
            
            with col2:
                if pos_cols:
                    st.success(f"📍 Position: {len(pos_cols)} col(s)")
                    for col in pos_cols[:2]:
                        st.caption(f"• {col}")
                else:
                    st.info("ℹ️ Position: Col 2 (défaut)")
                    
                if fibre_cols:
                    st.success(f"💡 Fibre: {len(fibre_cols)} col(s)")
                    for col in fibre_cols[:2]:
                        st.caption(f"• {col}")
                else:
                    st.warning("⚠️ Aucune colonne fibre")
            
            with col3:
                if cable_cols:
                    st.success(f"🔌 Câble: {len(cable_cols)} col(s)")
                    for col in cable_cols[:2]:
                        st.caption(f"• {col}")
                else:
                    st.warning("⚠️ Aucune colonne câble")
                    
                if etat_cols:
                    st.success(f"📊 État: {len(etat_cols)} col(s)")
                    for col in etat_cols[:2]:
                        st.caption(f"• {col}")
                else:
                    st.warning("⚠️ Aucune colonne état")
                    
            with col4:
                if capacite_cols:
                    st.success(f"⚡ Capacité: {len(capacite_cols)} col(s)")
                    for col in capacite_cols[:2]:
                        st.caption(f"• {col}")
                else:
                    st.warning("⚠️ Aucune colonne capacité")
            
            st.markdown("---")
            
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
            
            # Afficher quelques informations sur le fichier
            st.caption(f"📁 Fichier: {uploaded_file.name} | Lignes: {len(df)} | Colonnes: {len(df.columns)}")
            
            # Bouton pour voir toutes les colonnes
            if st.checkbox("🔍 Voir toutes les colonnes du fichier"):
                st.markdown("**📋 Toutes les colonnes disponibles :**")
                cols_text = ", ".join([f"`{col}`" for col in df.columns])
                st.markdown(cols_text)
            
            st.markdown("---")
            
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
                            pbo_tube, pbo_fibre = get_pbo_tube_fiber(row, df)
                            
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

