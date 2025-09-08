
# app_final_v3.py - Application Route Optique avec Streamlit - Version complète et stylisée
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import base64
import re

# Configuration de la page
st.set_page_config(
    page_title="Route Optique ICT",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Fonctions Utilitaires ---

def get_base64_of_bin_file(bin_file):
    """Convertit un fichier binaire en base64 pour l'affichage d'images locales."""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

# CSS intégré directement dans le code Python
css = """
/* Import Google Fonts */
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap");

/* Variables CSS */
:root {
    --primary-color: #2563eb;
    --primary-light: #3b82f6;
    --primary-dark: #1d4ed8;
    --secondary-color: #64748b;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --error-color: #ef4444;
    --orange-color: #ea580c;
    --purple-color: #9333ea;
    --background-light: #f8fafc;
    --background-white: #ffffff;
    --text-primary: #1e293b;
    --text-secondary: #64748b;
    --border-color: #e2e8f0;
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    --radius-sm: 0.375rem;
    --radius-md: 0.5rem;
    --radius-lg: 0.75rem;
    --radius-xl: 1rem;
}

/* Reset et base */
.main > div {
    max-width: 1400px;
    padding-top: 1rem;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Header amélioré avec logo */
.app-header {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
    padding: 2rem;
    border-radius: var(--radius-xl);
    margin-bottom: 2rem;
    color: white;
    text-align: center;
    box-shadow: var(--shadow-lg);
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2rem;
}

.app-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
    opacity: 0.3;
}

.logo-container {
    position: relative;
    z-index: 2;
    flex-shrink: 0;
}

.logo-container img {
    height: 80px;
    width: auto;
    filter: brightness(0) invert(1);
}

.header-content {
    position: relative;
    z-index: 2;
    text-align: left;
}

.app-header h1 {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    position: relative;
    z-index: 1;
}

.app-header p {
    font-size: 1.125rem;
    opacity: 0.9;
    margin-top: 0;
    position: relative;
    z-index: 1;
}

/* Cards et containers */
.upload-container {
    background: var(--background-white);
    padding: 2rem;
    border-radius: var(--radius-lg);
    border: 2px dashed var(--border-color);
    margin-bottom: 2rem;
    transition: all 0.3s ease;
    box-shadow: var(--shadow-sm);
}

.upload-container:hover {
    border-color: var(--primary-light);
    box-shadow: var(--shadow-md);
}

.search-container {
    background: var(--background-white);
    padding: 1.5rem;
    border-radius: var(--radius-lg);
    margin-bottom: 2rem;
    box-shadow: var(--shadow-md);
    border: 1px solid var(--border-color);
}

/* Segment condensé avec éléments colorés */
.segment-condensed {
    background: var(--background-white);
    padding: 1rem 1.5rem;
    border-radius: var(--radius-md);
    margin: 0.5rem 0;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border-color);
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: all 0.3s ease;
    flex-wrap: wrap;
}

.segment-condensed:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-1px);
}

.cable-name-condensed {
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text-primary);
    flex-shrink: 0;
}

.elements-group {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
}

/* Tube et fibre condensés avec couleurs */
.tube-badge-condensed, .fiber-badge-condensed, .boite-badge-condensed {
    padding: 0.375rem 0.75rem;
    border-radius: var(--radius-sm);
    font-weight: 700;
    font-size: 0.8rem;
    border: 2px solid;
    min-width: 2.5rem;
    text-align: center;
    box-shadow: var(--shadow-sm);
    transition: all 0.3s ease;
}

.tube-badge-condensed:hover, .fiber-badge-condensed:hover, .boite-badge-condensed:hover {
    transform: scale(1.05);
    box-shadow: var(--shadow-md);
}

.boite-badge-condensed {
    background-color: #f3f4f6;
    color: #374151;
    border-color: #9ca3af;
}
	
.k7-badge-condensed {
    background-color: #000000;
    color: #ffffff;
    padding: 0.375rem 0.75rem;
    border-radius: var(--radius-sm);
    font-weight: 700;
    font-size: 0.8rem;
    border: 2px solid;
    min-width: 2.5rem;
    text-align: center;
    box-shadow: var(--shadow-sm);
    transition: all 0.3s ease;
}

.k7-badge-condensed:hover {
    transform: scale(1.05);
    box-shadow: var(--shadow-md);
}

/* Badge pour nombre de prises */
.prises-badge {
    background: linear-gradient(135deg, #dbeafe 0%, #93c5fd 100%);
    color: #1e3a8a;
    padding: 0.5rem 1rem;
    border-radius: var(--radius-md);
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    box-shadow: var(--shadow-sm);
    border: 1px solid #3b82f6;
    margin-left: 1rem;
}
	
/* Status badges personnalisés */
.status-epissuree {
    background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%);
    color: #9a3412;
    padding: 0.375rem 0.75rem;
    border-radius: var(--radius-sm);
    font-size: 0.75rem;
    font-weight: 600;
    border: 1px solid var(--orange-color);
    box-shadow: var(--shadow-sm);
    text-transform: uppercase;
    letter-spacing: 0.025em;
    flex-shrink: 0;
}

.status-en-passage {
    background: linear-gradient(135deg, #e9d5ff 0%, #d8b4fe 100%);
    color: #6b21a8;
    padding: 0.375rem 0.75rem;
    border-radius: var(--radius-sm);
    font-size: 0.75rem;
    font-weight: 600;
    border: 1px solid var(--purple-color);
    box-shadow: var(--shadow-sm);
    text-transform: uppercase;
    letter-spacing: 0.025em;
    flex-shrink: 0;
}

.status-stockee {
    background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
    color: #166534;
    padding: 0.375rem 0.75rem;
    border-radius: var(--radius-sm);
    font-size: 0.75rem;
    font-weight: 600;
    border: 1px solid var(--success-color);
    box-shadow: var(--shadow-sm);
    text-transform: uppercase;
    letter-spacing: 0.025em;
    flex-shrink: 0;
}

.status-ok {
    background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
    color: #166534;
    padding: 0.375rem 0.75rem;
    border-radius: var(--radius-sm);
    font-size: 0.75rem;
    font-weight: 600;
    border: 1px solid var(--success-color);
    box-shadow: var(--shadow-sm);
    text-transform: uppercase;
    letter-spacing: 0.025em;
    flex-shrink: 0;
}

.status-nok {
    background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
    color: #dc2626;
    padding: 0.375rem 0.75rem;
    border-radius: var(--radius-sm);
    font-size: 0.75rem;
    font-weight: 600;
    border: 1px solid var(--error-color);
    box-shadow: var(--shadow-sm);
    text-transform: uppercase;
    letter-spacing: 0.025em;
    flex-shrink: 0;
}

/* Boutons améliorés */
.stButton > button {
    width: 100%;
    border-radius: var(--radius-md);
    border: none;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    transition: all 0.3s ease;
    box-shadow: var(--shadow-sm);
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
}

/* Metrics améliorés */
.metric-container {
    background: var(--background-light);
    padding: 1rem;
    border-radius: var(--radius-md);
    text-align: center;
    border: 1px solid var(--border-color);
}

.metric-label {
    font-size: 0.875rem;
    color: var(--text-secondary);
    font-weight: 500;
    margin-bottom: 0.25rem;
}

.metric-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
}

/* Input amélioré */
.stTextInput > div > div > input {
    border-radius: var(--radius-md);
    border: 2px solid var(--border-color);
    padding: 0.75rem;
    font-size: 1rem;
    transition: all 0.3s ease;
}

.stTextInput > div > div > input:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.fade-in {
    animation: fadeIn 0.5s ease-out;
}

/* Responsive */
@media (max-width: 768px) {
    .app-header {
        flex-direction: column;
        text-align: center;
    }
    
    .app-header h1 {
        font-size: 2rem;
    }
    
    .logo-container img {
        height: 60px;
    }
    
    .segment-condensed {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.75rem;
    }
    
    .cable-name-condensed {
        width: 100%;
        text-align: center;
    }
    
    .elements-group {
        justify-content: center;
        width: 100%;
    }
}

/* Style pour les zones de téléchargement */
.stFileUploader {
    border: 2px dashed var(--primary-color); /* Bordure bleue */
    border-radius: var(--radius-lg);
    padding: 20px;
    text-align: center;
    transition: all 0.3s ease-in-out;
}

.stFileUploader:hover {
    border-color: var(--primary-light); /* Bleu plus foncé au survol */
    box-shadow: 0 0 15px rgba(30, 144, 255, 0.3); /* Ombre légère */
}

/* Pour cacher le texte par défaut de Streamlit et ajouter le vôtre */
.stFileUploader > div > div > p:first-child {
    display: none;
}

/* Style pour le bouton 'Browse files' */
.stFileUploader button {
    background-color: var(--primary-color); /* Couleur du thème */
    color: white;
    border-radius: var(--radius-md);
    padding: 10px 20px;
    border: none;
    cursor: pointer;
}

.stFileUploader button:hover {
    background-color: var(--primary-dark);
}

/* Style pour le message d'avertissement */
.stAlert {
    background-color: #FFFACD; /* Jaune pâle */
    border-left: 5px solid #FFD700; /* Bordure jaune */
    border-radius: var(--radius-md);
    padding: 10px;
    margin-top: 20px;
}

.stAlert > div > div > p {
    color: #8B8B00; /* Texte marron-jaune */
}

/* Style pour les radio buttons */
div[data-baseweb="radio"] label {
    background-color: #E0E0E0; /* Gris clair */
    border-radius: var(--radius-md);
    padding: 8px 15px;
    margin-right: 10px;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
}

div[data-baseweb="radio"] label:hover {
    background-color: #D0D0D0;
}

div[data-baseweb="radio"] input:checked + div {
    background-color: var(--primary-color); /* Couleur primaire */
    color: white;
}

/* Style pour le bouton de recherche */
.stButton button {
    background-color: var(--primary-color); /* Couleur primaire */
    color: white;
    border-radius: var(--radius-md);
    padding: 10px 20px;
    border: none;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
}

.stButton button:hover {
    background-color: var(--primary-dark);
}

/* Style pour les expanders (éléments de liste détaillés) */
.stExpander {
    border: 1px solid var(--border-color); /* Gris clair */
    border-radius: var(--radius-md);
    margin-bottom: 10px;
    box-shadow: var(--shadow-sm);
}

.stExpander > div > div > div > p {
    font-weight: bold;
    color: var(--primary-color); /* Texte bleu pour le titre de l'expander */
}

/* Style pour les cartes d'en-tête de section (Tiroir, Position) */
.st-emotion-cache-1r6dm1c {
    /* Cible le conteneur de st.columns pour appliquer un style aux cartes */
    display: flex;
    justify-content: space-around;
    margin-bottom: 20px;
}

.st-emotion-cache-1r6dm1c > div > div > div {
    /* Cible les divs générés par st.markdown pour les cartes */
    flex: 1;
    margin: 0 10px;
}

/* Style pour chaque étape de route */
.route-step-card {
    background-color: var(--background-white);
    border-radius: var(--radius-md);
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: var(--shadow-md);
    display: flex;
    flex-direction: column;
    gap: 10px;
    border: 1px solid var(--border-color);
}
"""
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# --- Fonctions de Traitement des Données (Mises en Cache) ---

@st.cache_data
def get_all_unique_values(df):
    """Extrait toutes les valeurs uniques du DataFrame pour l'autocomplétion."""
    all_values = set()
    for col in df.columns:
        unique_vals = df[col].dropna().astype(str).unique()
        all_values.update(unique_vals)
    return sorted([val for val in all_values if val.strip() != ''])

@st.cache_data
def extract_boite_names_from_rop_df(df):
    """Extrait les noms de boîtes uniques des colonnes 'Boîte' du DataFrame ROP."""
    boite_names = set()
    boite_column_names = ['boite', 'boîte', 'Boite', 'Boîte', 'BOITE', 'BOÎTE'] # Noms de colonnes à rechercher
    for col_idx in range(df.shape[1]): # Itérer sur les indices de colonnes
        # Vérifier si la première cellule de la colonne correspond à un nom de boîte
        if pd.notna(df.iloc[0, col_idx]) and str(df.iloc[0, col_idx]).lower().strip() in boite_column_names:
            # Extraire les valeurs de cette colonne (en ignorant l'en-tête)
            unique_vals = df.iloc[1:, col_idx].dropna().astype(str).unique()
            boite_names.update([val.strip() for val in unique_vals if val.strip()])
    return sorted(list(boite_names))

@st.cache_data
def extract_stban_boite_names_from_df(df):
    """Extrait tous les noms de boîtes uniques depuis le DataFrame STBAN."""
    boite_names = set()
    boite_column_names = ['boite', 'boîte', 'Boite', 'Boîte', 'BOITE', 'BOÎTE', 'box', 'Box']
    for col in df.columns:
        col_lower = col.lower().strip()
        if any(boite_name.lower() in col_lower for boite_name in boite_column_names):
            unique_vals = df[col].dropna().astype(str).unique()
            boite_names.update([val.strip() for val in unique_vals if val.strip()])
            break
    return sorted(list(boite_names))

@st.cache_data
def identify_columns(columns_list):
    """Identifie les colonnes PRISE et PTO une seule fois."""
    prise_col, pto_col = None, None
    for col in columns_list:
        col_upper = col.upper()
        if not prise_col and 'REF_PBO_PRISE' in col_upper:
            prise_col = col
        elif not pto_col and 'REF_PBO_PTO' in col_upper:
            pto_col = col
        if prise_col and pto_col:
            break
    return prise_col, pto_col

@st.cache_data
def prepare_stban_for_search(_stban_df, prise_col, pto_col):
    """Prépare le DataFrame STBAN une seule fois avec les colonnes en majuscules."""
    if _stban_df is None or not prise_col or not pto_col:
        return None
    return pd.DataFrame({
        'PRISE_UPPER': _stban_df[prise_col].fillna('').astype(str).str.strip().str.upper(),
        'PTO_UPPER': _stban_df[pto_col].fillna('').astype(str).str.strip().str.upper()
    })

@st.cache_data
def calculate_prises_count_optimized(_optimized_df, boite_name):
    """Version optimisée du calcul des prises avec DataFrame pré-traité."""
    if _optimized_df is None or not boite_name:
        return None
    boite_name_clean = str(boite_name).strip().upper()
    prise_array = _optimized_df['PRISE_UPPER'].values
    pto_array = _optimized_df['PTO_UPPER'].values
    is_prise = (prise_array == boite_name_clean)
    is_pto = (pto_array == boite_name_clean)
    pto_not_empty = (pto_array != '')
    count_prise = np.sum(is_prise)
    count_pto_only = np.sum(is_pto & ~is_prise)
    count_prise_autre_pto = np.sum(is_prise & pto_not_empty & ~is_pto)
    return max(int(count_prise), int(count_prise + count_pto_only - count_prise_autre_pto))

def calculate_prises_count(stban_df, boite_name):
    """Fonction principale pour calculer le nombre de prises pour une boîte."""
    if stban_df is None or not boite_name:
        return None
    prise_col, pto_col = identify_columns(list(stban_df.columns))
    if not prise_col or not pto_col:
        st.warning("Colonnes 'REF_PBO_PRISE' ou 'REF_PBO_PTO' introuvables dans le fichier STBAN.")
        return None
    optimized_df = prepare_stban_for_search(stban_df, prise_col, pto_col)
    return calculate_prises_count_optimized(optimized_df, boite_name)

# --- Fonctions d'Affichage ---

def get_tiroir_pos(row, rop_df):
    """Extrait le tiroir et la position d'une ligne de ROP."""
    tiroir = None
    pos = None
    for i, val in enumerate(row):
        if pd.isna(val): continue
        val_str = str(val).strip()
        if "TIROIR" in val_str.upper():
            tiroir = val_str
        if "POSITION" in val_str.upper():
            pos = val_str
    return tiroir, pos

def get_pbo_tube_fiber(row, rop_df):
    """Extrait les informations PBO, tube et fibre d'une ligne de ROP."""
    pbo_tube = None
    pbo_fiber = None
    # Cette fonction est un placeholder, à adapter selon la structure réelle de vos données
    # Par exemple, si PBO_TUBE et PBO_FIBRE sont des colonnes spécifiques
    # Ou si elles sont extraites de manière plus complexe à partir de la ligne
    return pbo_tube, pbo_fiber

def get_status_class(text):
    """Retourne la classe CSS appropriée en fonction du statut."""
    text_lower = str(text).lower()
    if 'epissure' in text_lower:
        return 'status-epissuree'
    if 'passage' in text_lower:
        return 'status-en-passage'
    if 'stockee' in text_lower:
        return 'status-stockee'
    if 'ok' in text_lower:
        return 'status-ok'
    if 'nok' in text_lower:
        return 'status-nok'
    return ''

def get_color_from_text(text):
    """Assigne une couleur basée sur le texte (TUBE, FIBRE)."""
    text = str(text).upper()
    if text.startswith('T'):
        return '#3b82f6'  # Blue
    elif text.startswith('F'):
        return '#10b981'  # Green
    return '#64748b'  # Gray

@st.cache_data
def extract_route_segments(row):
    """Extrait les segments de route d'une ligne du DataFrame."""
    segments = []
    for item in row.dropna():
        item_str = str(item).strip()
        if not item_str: continue

        # Regex pour capturer le nom du câble, la longueur du segment et la longueur cumulée
        # Ex: TE2-CA-0000101_72F0 / 10ml (10ml)
        cable_match = re.match(r'([A-Z0-9\-]+_\d+F\d*)\s*/\s*(\d+ml)\s*\((\d+ml)\)', item_str)
        if cable_match:
            cable_name, segment_length, cumulative_length = cable_match.groups()
            remaining_text = item_str[cable_match.end():].strip()
            parts = [p.strip() for p in remaining_text.split(',') if p.strip()]
            segments.append({
                'type': 'cable',
                'name': cable_name,
                'segment_length': segment_length,
                'cumulative_length': cumulative_length,
                'details': parts
            })
        else:
            # Si ce n'est pas un câble, c'est un point de passage (boîte, tiroir, position, etc.)
            segments.append({
                'type': 'point',
                'name': item_str
            })
    return segments

@st.cache_data
def calculate_cumulative_lengths(df):
    """Calcule les longueurs cumulées pour chaque segment de route."""
    # Cette fonction est un placeholder si le calcul est déjà fait dans le fichier.
    # Si le fichier ROP ne contient pas de longueurs cumulées, cette fonction les calculerait.
    # Pour l'instant, elle retourne le DataFrame tel quel, car les longueurs cumulées sont extraites directement.
    return df

def display_segment_condensed_with_colors(segment):
    """Affiche un segment de route de manière condensée avec des badges colorés."""
    if segment['type'] == 'cable':
        cable_name = segment['name']
        segment_length = segment['segment_length']
        details = segment['details']

        elements_html = f'<div class="cable-name-condensed">{cable_name} ({segment_length})</div>'
        status_html = ''
        elements_group = ''

        for part in details:
            status_class = get_status_class(part)
            if status_class:
                status_html += f'<div class="{status_class}">{part}</div>'
            else:
                color = get_color_from_text(part)
                badge_class = 'boite-badge-condensed' if 'BPE' in part or 'CAS' in part else 'tube-badge-condensed'
                elements_group += f'<span class="{badge_class}" style="background-color: {color}20; color: {color}; border-color: {color};">{part}</span>'
        
        if elements_group:
            elements_html += f'<div class="elements-group">{elements_group}</div>'

        st.markdown(f'<div class="segment-condensed fade-in">{elements_html}{status_html}</div>', unsafe_allow_html=True)

    elif segment['type'] == 'point':
        point_name = segment['name']
        # Gérer l'affichage des points comme Tiroir, Position, etc.
        if 'Tiroir' in point_name or 'Position' in point_name:
            # Ces éléments sont gérés séparément dans display_detailed_route
            pass
        else:
            # Pour les autres points, on peut les afficher comme un badge simple
            st.markdown(f'<div class="segment-condensed fade-in"><span class="boite-badge-condensed">{point_name}</span></div>', unsafe_allow_html=True)

def display_detailed_route(row, rop_df):
    """Affiche la route détaillée pour une ligne de résultat, en utilisant les fonctions réintégrées."""
    tiroir, pos = get_tiroir_pos(row, rop_df)
    pbo_tube, pbo_fiber = get_pbo_tube_fiber(row, rop_df) # Cette fonction est un placeholder, à adapter si nécessaire

    # Extraire le base_id (première valeur non-NaN de la ligne qui n'est ni Tiroir ni Position)
    base_id = None
    for item in row.dropna():
        item_str = str(item)
        if "TIROIR" not in item_str.upper() and "POSITION" not in item_str.upper():
            base_id = item_str
            break

    if base_id:
        st.markdown(f"<h3>ROP pour <span class=\"search-term-highlight\">{base_id}</span></h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if tiroir:
            st.markdown(f"<div class=\"metric-container\"><div class=\"metric-label\">Tiroir</div><div class=\"metric-value\">{tiroir.split(":")[-1].strip()}</div></div>", unsafe_allow_html=True)
    with col2:
        if pos:
            st.markdown(f"<div class=\"metric-container\"><div class=\"metric-label\">Position</div><div class=\"metric-value\">{pos.split(":")[-1].strip()}</div></div>", unsafe_allow_html=True)
    
    st.markdown("<h4>🗺️ Route Détaillée</h4>", unsafe_allow_html=True)

    segments = extract_route_segments(row)
    if segments:
        cumulative_lengths = calculate_cumulative_lengths(segments)
        for i, segment in enumerate(segments):
            cumul = cumulative_lengths[i] if i < len(cumulative_lengths) else None
            display_segment_condensed_with_colors(segment)
    else:
        st.info("ℹ️ Pas de détails de route disponibles")


# --- Interface Utilisateur (UI) ---

# En-tête de l'application
logo_base64 = "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"
logo_html = f'<img src="data:image/png;base64,{logo_base64}" alt="Logo ICT">' if logo_base64 else ''

st.markdown(f'''
<div class="app-header">
    <div class="logo-container">{logo_html}</div>
    <div class="header-content">
        <h1>Route Optique ICT</h1>
        <p>Analyse avancée des infrastructures optiques</p>
    </div>
</div>
''', unsafe_allow_html=True)

# Initialisation de l'état de session
if 'route_optique_df' not in st.session_state: st.session_state.route_optique_df = None
if 'stban_df' not in st.session_state: st.session_state.stban_df = None
if 'all_unique_values' not in st.session_state: st.session_state.all_unique_values = []
if 'boite_names' not in st.session_state: st.session_state.boite_names = []
if 'stban_processed' not in st.session_state: st.session_state.stban_processed = False

# Section de téléchargement des fichiers
st.markdown('## 📂 Charger vos fichiers')
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("<h5>Fichier Excel Route Optique (.xlsx, .xls)</h5>", unsafe_allow_html=True)
            uploaded_route_optique = st.file_uploader("Glissez-déposez ou cliquez pour charger", type=['xlsx', 'xls'], key="route_optique_uploader", label_visibility="collapsed")
            if uploaded_route_optique:
                st.session_state.route_optique_df = pd.read_excel(uploaded_route_optique, header=None)
                st.success("Fichier Route Optique chargé !")
    with col2:
        with st.container(border=True):
            st.markdown("<h5>Fichier Excel STBAN (optionnel)</h5>", unsafe_allow_html=True)
            uploaded_stban = st.file_uploader("Glissez-déposez ou cliquez pour charger", type=['xlsx', 'xls'], key="stban_uploader", label_visibility="collapsed")
            if uploaded_stban:
                st.session_state.stban_df = pd.read_excel(uploaded_stban)
                st.success("Fichier STBAN chargé !")

# Logique principale de l'application
if st.session_state.route_optique_df is None:
    st.warning("Veuillez charger un fichier Excel Route Optique pour commencer l'analyse.")
else:
    df = st.session_state.route_optique_df
    if not st.session_state.all_unique_values:
        st.session_state.all_unique_values = get_all_unique_values(df)
    # La liste des noms de boîtes est toujours extraite du fichier ROP si disponible
    # Le fichier STBAN est utilisé pour enrichir cette liste si présent
    if not st.session_state.boite_names or (st.session_state.stban_df is not None and not st.session_state.get("stban_processed", False)):
        # Initialiser boite_names avec les valeurs du fichier ROP
        st.session_state.boite_names = extract_boite_names_from_rop_df(df)
        if st.session_state.stban_df is not None:
            # Si le fichier STBAN est chargé, ajouter ses noms de boîtes et supprimer les doublons
            st.session_state.boite_names.extend(extract_stban_boite_names_from_df(st.session_state.stban_df))
            st.session_state.boite_names = sorted(list(set(st.session_state.boite_names)))
            st.session_state.stban_processed = True # Marquer que le STBAN a été traité pour les noms de boîtes
        

    with st.container(border=True):
        st.markdown('## 🔍 Recherche avec autocomplétion')
        search_term = ''
        if st.session_state.route_optique_df is not None:
            st.markdown("<h5>Recherche par boîte</h5>", unsafe_allow_html=True)
            search_query = st.text_input("Saisissez une partie du nom de la boîte ou sélectionnez dans la liste", key="boite_text_input", label_visibility="collapsed")
            
            # Filtrer les suggestions en fonction de la saisie
            if search_query:
                filtered_boite_names = [name for name in st.session_state.boite_names if search_query.lower() in name.lower()]
            else:
                filtered_boite_names = st.session_state.boite_names

            # Utiliser un selectbox pour la sélection avec les options filtrées
            # Si la liste filtrée est vide, afficher un message
            if not filtered_boite_names:
                st.info("Aucune boîte correspondante trouvée.")
                search_term = None # Pas de terme de recherche si aucune correspondance
            else:
                search_term = st.selectbox("Sélectionnez une boîte", filtered_boite_names, key="boite_selectbox", label_visibility="collapsed")

            if st.session_state.stban_df is None:
                st.info("Le fichier STBAN n'est pas chargé. Le calcul du nombre de prises ne sera pas disponible.")
        else:
            st.info("Veuillez charger un fichier Excel Route Optique pour activer la recherche.")
            search_term = st.selectbox("Sélectionnez une boîte", ["Veuillez charger un fichier ROP"], key="boite_selectbox", label_visibility="collapsed", disabled=True)

        # La recherche se déclenche automatiquement si un terme est sélectionné ou saisi
        if search_term: # Condition pour lancer la recherche
            st.markdown(f'### Résultats pour : <span class="search-term-highlight">{search_term}</span>', unsafe_allow_html=True)

            # Affichage du nombre de prises
            if st.session_state.stban_df is not None: # Le calcul des prises est toujours lié à la recherche par boîte
                with st.spinner("Calcul du nombre de prises..."):
                    prises_count = calculate_prises_count(st.session_state.stban_df, search_term)
                if prises_count is not None:
                    st.markdown(f'<div class="prises-badge">🔌 Nombre de prises : <strong>{prises_count}</strong></div>', unsafe_allow_html=True)
            
            # Recherche des ROPs
            # Recherche des ROPs
            # Recherche de la colonne contenant la valeur sélectionnée et application de la condition 'STOCKEE'
            mask = df == search_term
            exclude_cols = [col for col in df.columns.astype(str) if "EXTREMI" in col]
            column_indices = np.where(mask.any(axis=0) & ~exclude_cols)[0]

            if len(column_indices) > 0:
                col_index = column_indices[0]
                matching_rows = df[(df.iloc[:, col_index] == search_term) &
                                   (df.iloc[:, col_index + 3] == "STOCKEE")]
            else:
                matching_rows = pd.DataFrame()

            if not matching_rows.empty:
                st.success(f"{len(matching_rows)} ROP trouvée(s).")
                for index, row in matching_rows.iterrows():
                    # Tenter d'extraire le base_id pour le titre de l'expander
                    # Le base_id est souvent la première valeur non-NaN de la ligne
                    base_id_for_expander = row.dropna().iloc[0] if not row.dropna().empty else 'Détails'
                    expander_title = f"ROP {index + 1} - {base_id_for_expander}"
                    with st.expander(expander_title):
                        display_detailed_route(row, st.session_state.route_optique_df)
            else:
                st.warning("Aucun résultat trouvé pour votre recherche.")


