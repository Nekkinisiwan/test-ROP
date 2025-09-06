# app_final_v3.py - Application Route Optique avec Streamlit - Version simplifiée
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import base64

# Configuration de la page
st.set_page_config(
    page_title="Route Optique ICT",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def get_base64_of_bin_file(bin_file):
    """Convertit un fichier binaire en base64"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# CSS personnalisé amélioré avec logo
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
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
</style>
""", unsafe_allow_html=True)

def get_all_unique_values(df):
    """Extrait toutes les valeurs uniques du DataFrame pour l'autocomplétion"""
    all_values = set()
    for col in df.columns:
        unique_vals = df[col].dropna().astype(str).unique()
        all_values.update(unique_vals)
    # Filtrer les valeurs vides et trier
    all_values = sorted([val for val in all_values if val.strip() != ''])
    return all_values

def extract_boite_names_from_df(df):
    """Extrait tous les noms de boîtes uniques depuis le DataFrame"""
    boite_names = set()
    
    # Définir les noms possibles pour les colonnes boîte
    boite_column_names = ['boite', 'boîte', 'Boite', 'Boîte', 'BOITE', 'BOÎTE', 'box', 'Box']
    
    for col in df.columns:
        col_lower = col.lower().strip()
        for boite_name in boite_column_names:
            if boite_name.lower() in col_lower:
                # Extraire les valeurs uniques de cette colonne
                unique_vals = df[col].dropna().astype(str).unique()
                boite_names.update([val.strip() for val in unique_vals if val.strip() != ''])
                break
    
    return sorted(list(boite_names))
	
# Mettre en cache les colonnes identifiées pour ne pas les rechercher à chaque fois
@st.cache_data
def identify_columns(columns_list):
    """Identifie les colonnes PRISE et PTO une seule fois"""
    prise_col = None
    pto_col = None
    
    for col in columns_list:
        col_upper = col.upper()
        if not prise_col and 'REF_PBO_PRISE' in col_upper:
            prise_col = col
        elif not pto_col and 'REF_PBO_PTO' in col_upper:
            pto_col = col
        
        if prise_col and pto_col:
            break
    
    return prise_col, pto_col

# Mettre en cache le DataFrame préparé
@st.cache_data
def prepare_stban_for_search(stban_df, prise_col, pto_col):
    """Prépare le DataFrame une seule fois avec les colonnes en majuscules"""
    if stban_df is None or not prise_col or not pto_col:
        return None
    
    # Créer un DataFrame optimisé avec seulement les colonnes nécessaires
    optimized_df = pd.DataFrame({
        'PRISE_UPPER': stban_df[prise_col].fillna('').astype(str).str.strip().str.upper(),
        'PTO_UPPER': stban_df[pto_col].fillna('').astype(str).str.strip().str.upper()
    })
    
    return optimized_df

# Mettre en cache les résultats de calcul
@st.cache_data
def calculate_prises_count_optimized(optimized_df, boite_name):
    """Version optimisée du calcul des prises avec DataFrame pré-traité"""
    if optimized_df is None or boite_name is None or boite_name == '':
        return None
    
    boite_name_clean = str(boite_name).strip().upper()
    
    # Utiliser des opérations vectorisées NumPy pour la vitesse
    import numpy as np
    
    prise_array = optimized_df['PRISE_UPPER'].values
    pto_array = optimized_df['PTO_UPPER'].values
    
    # Calculs vectorisés
    is_prise = (prise_array == boite_name_clean)
    is_pto = (pto_array == boite_name_clean)
    pto_not_empty = (pto_array != '')
    
    # 1. Dans PRISE
    count_prise = np.sum(is_prise)
    
    # 2. Dans PTO uniquement
    count_pto_only = np.sum(is_pto & ~is_prise)
    
    # 3. Dans PRISE avec autre PTO
    count_prise_autre_pto = np.sum(is_prise & pto_not_empty & ~is_pto)
    
    return int(count_prise + count_pto_only - count_prise_autre_pto)

# Fonction wrapper qui utilise le cache
def calculate_prises_count(stban_df, boite_name):
    """Fonction principale qui utilise les versions optimisées"""
    if stban_df is None:
        return None
    
    # Identifier les colonnes (mis en cache)
    prise_col, pto_col = identify_columns(list(stban_df.columns))
    
    if not prise_col or not pto_col:
        return None
    
    # Préparer le DataFrame (mis en cache)
    optimized_df = prepare_stban_for_search(stban_df, prise_col, pto_col)
    
    # Calculer (mis en cache)
    return calculate_prises_count_optimized(optimized_df, boite_name)

@st.cache_data(show_spinner=False)
def load_stban_file(file_content):
    """Charge le fichier STBAN avec mise en cache"""
    try:
        df = pd.read_excel(file_content, engine='openpyxl')
        return df
    except:
        try:
            df = pd.read_excel(file_content, engine='xlrd')
            return df
        except:
            return pd.read_excel(file_content)
			
def get_status_class_condensed(status):
    """Retourne la classe CSS selon le statut pour l'affichage condensé"""
    if not status:
        return "status-en-passage"
    status_upper = str(status).upper()
    if status_upper == 'STOCKEE':
        return "status-stockee"
    elif status_upper == 'EPISSUREE':
        return "status-epissuree"
    elif status_upper == 'EN PASSAGE':
        return "status-en-passage"
    elif status_upper == 'OK':
        return "status-ok"
    elif status_upper == 'NOK':
        return "status-nok"
    return "status-en-passage"

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
	longueur_names = ['longueur', 'Longueur', 'LONGUEUR', 'length', 'Length', 'lg', 'LG']
	tube_names = ['tube', 'Tube', 'TUBE']
	fibre_names = ['fibre', 'Fibre', 'FIBRE', 'fiber', 'Fiber']
	boite_names = ['boite', 'boîte', 'Boite', 'Boîte', 'BOITE', 'BOÎTE', 'box', 'Box']
	etat_names = ['etat', 'état', 'Etat', 'État', 'ETAT', 'ÉTAT', 'state', 'State', 'STATUS', 'status']
	k7_names = ['k7', 'K7', 'Cassette', 'CASSETTE', 'cassette']
	
	# Identifier toutes les colonnes de chaque type
	cable_cols = []
	capacite_cols = []
	longueur_cols = []
	tube_cols = []
	fibre_cols = []
	boite_cols = []
	etat_cols = []
	k7_cols = []
	
	# Vérifier si la colonne 3 (index 2) a pour nom "k7"
	ignore_col3_k7 = False
	if len(df.columns) > 2:  # S'assurer que la colonne 3 existe
		col3_name = df.columns[2].lower().strip()
		if col3_name == 'k7':
			ignore_col3_k7 = True
			
	for i, col in enumerate(df.columns[1:], start=1):  # Commencer à partir de la colonne 1 (index 1)
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
				
		# Vérifier si c'est une colonne longueur
		if 'totale' not in col_lower:
			for long_name in longueur_names:
				if long_name.lower() in col_lower:
					longueur_cols.append(col)
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
				
		# Vérifier si c'est une colonne boite
		for boite_name in boite_names:
			if boite_name.lower() in col_lower:
				boite_cols.append(col)
				break
				
		# Vérifier si c'est une colonne état
		for etat_name in etat_names:
			if etat_name.lower() in col_lower:
				etat_cols.append(col)
				break
		
		# Vérifier si c'est une colonne K7 - AVEC LOGIQUE SPÉCIALE
		for k7_name in k7_names:
			if k7_name.lower() in col_lower:
				# Si c'est la colonne 3 (index 2) ET que ignore_col3_k7 est True, ignorer
				if i == 2 and ignore_col3_k7:  # i=2 correspond à l'index 2 (colonne 3)
					continue  # Ignorer cette colonne K7
				else:
					k7_cols.append(col)  # Ajouter cette colonne K7
				break
				
	# Créer des segments basés sur le nombre de colonnes trouvées
	max_segments = max(len(cable_cols), len(capacite_cols), len(longueur_cols), 
					   len(tube_cols), len(fibre_cols), len(boite_cols), 
					   len(etat_cols), len(k7_cols))
	
	for i in range(max_segments):
		cable = ''
		capacite = ''
		longueur = ''
		tube = ''
		fibre = ''
		boite = ''
		etat = ''
		k7 = ''
		
		# Récupérer les valeurs pour chaque segment
		if i < len(cable_cols) and cable_cols[i] in row.index:
			cable = str(row[cable_cols[i]]).strip() if pd.notna(row[cable_cols[i]]) else ''
			
		if i < len(capacite_cols) and capacite_cols[i] in row.index:
			capacite = str(row[capacite_cols[i]]).strip() if pd.notna(row[capacite_cols[i]]) else ''
			
		if i < len(longueur_cols) and longueur_cols[i] in row.index:
			longueur = str(row[longueur_cols[i]]).strip() if pd.notna(row[longueur_cols[i]]) else ''
			
		if i < len(tube_cols) and tube_cols[i] in row.index:
			tube = str(row[tube_cols[i]]).strip() if pd.notna(row[tube_cols[i]]) else ''
			
		if i < len(fibre_cols) and fibre_cols[i] in row.index:
			fibre = str(row[fibre_cols[i]]).strip() if pd.notna(row[fibre_cols[i]]) else ''
			
		if i < len(boite_cols) and boite_cols[i] in row.index:
			boite = str(row[boite_cols[i]]).strip() if pd.notna(row[boite_cols[i]]) else ''
			
		if i < len(etat_cols) and etat_cols[i] in row.index:
			etat_val = str(row[etat_cols[i]]).strip().upper() if pd.notna(row[etat_cols[i]]) else ''
			if etat_val in ['STOCKEE', 'EN PASSAGE', 'EPISSUREE', 'OK', 'NOK']:
				etat = etat_val
		
		if i < len(k7_cols) and k7_cols[i] in row.index:
			k7 = str(row[k7_cols[i]]).strip() if pd.notna(row[k7_cols[i]]) else ''
			
		# Créer un segment s'il y a au moins une valeur
		if any([cable, capacite, longueur, tube, fibre, boite, etat, k7]):
			segment = {
				'title': f'Segment {i + 1}',
				'cable': cable,
				'capacite': capacite,
				'longueur': longueur,
				'tube': tube,
				'fibre': fibre,
				'boite': boite,
				'etat': etat,
				'k7': k7
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
	# for col in df.columns:
		# col_lower = col.lower().strip()
		# for tiroir_name in tiroir_names:
			# if tiroir_name.lower() in col_lower:
				# if col in row.index and pd.notna(row[col]):
					# tiroir = str(row[col]).strip()
					# break
		# if tiroir:
			# break
	tiroir = str(row[0]).strip()

	if len(tiroir) > 5 :
		tiroir = "TI" + str(tiroir[-9:][:2])
	tiroir = tiroir.replace('-', '')
	tiroir = tiroir.replace('_', '')
	
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
	# if not tiroir and len(row) > 0 and pd.notna(row.iloc[0]):
		# tiroir = str(row.iloc[0]).strip()
		
	# if not pos and len(row) > 1 and pd.notna(row.iloc[1]):
		# pos = str(row.iloc[1]).strip()

	return tiroir, pos

def get_pbo_tube_fiber(row, df):
    """Récupère le tube et fibre du PBO extrémité (DERNIÈRES informations trouvées) par nom de colonne"""
    
    # Chercher les DERNIÈRES colonnes tube et fibre
    tube_names = ['tube', 'Tube', 'TUBE']
    fibre_names = ['fibre', 'Fibre', 'FIBRE', 'fiber', 'Fiber']
    
    tube = ''
    fibre = ''
    
    # Trouver la DERNIÈRE colonne tube (parcourir en sens inverse)
    tube_cols = []
    for col in df.columns:
        col_lower = col.lower().strip()
        for tube_name in tube_names:
            if tube_name.lower() in col_lower:
                tube_cols.append(col)
                break
    
    # Prendre la dernière colonne tube trouvée
    for col in reversed(tube_cols):
        if col in row.index and pd.notna(row[col]) and str(row[col]).strip():
            tube = str(row[col]).strip()
            break
    
    # Trouver la DERNIÈRE colonne fibre (parcourir en sens inverse)
    fibre_cols = []
    for col in df.columns:
        col_lower = col.lower().strip()
        for fibre_name in fibre_names:
            if fibre_name.lower() in col_lower:
                fibre_cols.append(col)
                break
    
    # Prendre la dernière colonne fibre trouvée
    for col in reversed(fibre_cols):
        if col in row.index and pd.notna(row[col]) and str(row[col]).strip():
            fibre = str(row[col]).strip()
            break
    
    return tube, fibre

def format_cable_name_with_capacity_and_length(cable, capacite, longueur, cumul_longueur=None):
	"""Formate le nom du câble avec sa capacité FO et longueur ml selon le format demandé"""
	if not cable and not capacite and not longueur:
		return ""
	
	# Commencer par le nom du câble ou un nom par défaut
	if cable:
		result = cable
	else:
		result = "Cable"
	
	# Ajouter la capacité avec FO
	if capacite:
		try:
			cap_int = int(float(capacite))
			result += f"_{cap_int}FO"
		except ValueError:
			result += f"_{capacite}FO"
	
	# Ajouter la longueur avec ml
	if longueur:
		try:
			long_int = int(float(longueur))
			result += f" / {long_int}ml"
		except ValueError:
			result += f" / {longueur}ml"
	
	# Ajouter le cumul des longueurs entre parenthèses si fourni
	if cumul_longueur is not None:
		try:
			cumul_int = int(float(cumul_longueur))
			result += f" ({cumul_int}ml)"
		except ValueError:
			result += f" ({cumul_longueur}ml)"
			
	return result

def calculate_cumulative_lengths(segments):
	"""Calcule le cumul des longueurs pour chaque segment"""
	cumulative_lengths = []
	cumul = 0
	
	for segment in segments:
		longueur = segment.get('longueur', '')
		if longueur:
			try:
				long_value = float(longueur)
				cumul += long_value * 1.05
				cumulative_lengths.append(cumul)
			except ValueError:
				# Si la longueur n'est pas numérique, on garde le cumul précédent
				cumulative_lengths.append(cumul if cumul > 0 else None)
		else:
			# Pas de longueur pour ce segment
			cumulative_lengths.append(cumul if cumul > 0 else None)
	
	return cumulative_lengths
	
def display_segment_condensed_with_colors(segment, index, cumul_longueur=None):
	"""Affiche un segment de route en format condensé avec T et F colorés et boite : Cable_CapacityFO_Lengthml Boite T1 F1 STATUS"""
	
	# Construire le nom du câble avec capacité et longueur
	cable_name = format_cable_name_with_capacity_and_length(segment['cable'], segment['capacite'], segment['longueur'], cumul_longueur)
	
	# Construire les éléments HTML
	elements = []
	
	# 1. Nom du câble
	if cable_name:
		elements.append(f'<div class="cable-name-condensed">{cable_name}</div>')
	
	# 2. Groupe des autres éléments (boite, tube, fibre, statut)
	group_elements = []
	
	# 3. Boite
	if segment['boite']:
		group_elements.append(f'<div class="boite-badge-condensed">{segment["boite"]}</div>')
	
	# 4. Tube coloré
	if segment['tube']:
		try:
			tube_int = int(float(segment['tube']))
			tube_color = get_tube_fiber_color(tube_int)
			tube_text_color = get_text_color(tube_color)
			
			group_elements.append(
				f'<div class="tube-badge-condensed" style="background-color: {tube_color}; '
				f'color: {tube_text_color}; border-color: {tube_color};">T{tube_int}</div>'
			)
		except ValueError:
			group_elements.append(
				f'<div class="tube-badge-condensed" style="background-color: #9ca3af; '
				f'color: white; border-color: #9ca3af;">T{segment["tube"]}</div>'
			)
	
	# 5. Fibre colorée
	if segment['fibre']:
		try:
			fibre_int = int(float(segment['fibre']))
			fibre_color = get_tube_fiber_color(fibre_int)
			fibre_text_color = get_text_color(fibre_color)
			
			group_elements.append(
				f'<div class="fiber-badge-condensed" style="background-color: {fibre_color}; '
				f'color: {fibre_text_color}; border-color: {fibre_color};">F{fibre_int}</div>'
			)
		except ValueError:
			group_elements.append(
				f'<div class="fiber-badge-condensed" style="background-color: #9ca3af; '
				f'color: white; border-color: #9ca3af;">F{segment["fibre"]}</div>'
			)
	
	# 7. K7
	if segment['k7']:
		group_elements.append(f'<div class="k7-badge-condensed">{segment["k7"]}</div>')
		
	# 6. Statut coloré
	if segment['etat']:
		status_class = get_status_class_condensed(segment['etat'])
		group_elements.append(f'<div class="{status_class}">{segment["etat"]}</div>')
	
	# Assembler le groupe d'éléments
	if group_elements:
		group_html = '<div class="elements-group">' + ''.join(group_elements) + '</div>'
		elements.append(group_html)
	
	# Assembler tous les éléments
	content_html = ''.join(elements)
	
	# Afficher avec unsafe_allow_html=True
	st.markdown(
		f'<div class="segment-condensed fade-in">{content_html}</div>',
		unsafe_allow_html=True
	)

@st.cache_data
def calculate_all_boites_counts(stban_df, boite_names_list):
    """Calcule les prises pour toutes les boîtes en une fois"""
    if stban_df is None or not boite_names_list:
        return {}
    
    prise_col, pto_col = identify_columns(list(stban_df.columns))
    if not prise_col or not pto_col:
        return {}
    
    optimized_df = prepare_stban_for_search(stban_df, prise_col, pto_col)
    
    results = {}
    for boite in boite_names_list:
        results[boite] = calculate_prises_count_optimized(optimized_df, boite)
    
    return results
	
# Interface principale
def main():
	# Header amélioré avec logo
	try:
		# Essayer de charger le logo depuis la racine
		logo_base64 = get_base64_of_bin_file('./logo-ICT-group.png')
		logo_html = f'<img src="data:image/png;base64,{logo_base64}" alt="ICT Group Logo">'
	except:
		# Fallback si le logo n'est pas trouvé
		logo_html = '<div style="width: 80px; height: 80px; background: rgba(255,255,255,0.2); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 24px;">🔌</div>'
	
	st.markdown(f"""
	<div class="app-header fade-in">
		<div class="logo-container">
			{logo_html}
		</div>
		<div class="header-content">
			<h1>Route Optique ICT</h1>
			<p>Analyse avancée des infrastructures optiques</p>
		</div>
	</div>
	""", unsafe_allow_html=True)
	
	# Upload des fichiers
	st.markdown('<div class="upload-container fade-in">', unsafe_allow_html=True)
	st.markdown("### 📊 Charger vos fichiers")
	
	col1, col2 = st.columns(2)
	
	with col1:
		uploaded_file = st.file_uploader(
			"📑 Fichier Excel Route Optique (.xlsx, .xls)",
			type=['xlsx', 'xls'],
			key="route_optique"
		)
	
	with col2:
		stban_file = st.file_uploader(
			"📋 Fichier Excel STBAN (optionnel)",
			type=['xlsx', 'xls'],
			key="stban",
			help="STBAN pour calculer le nombre de prises"
		)
		
	st.markdown('</div>', unsafe_allow_html=True)
	
	# Charger le fichier STBAN si fourni
	stban_df = None
	if stban_file is not None:
		try:
			with st.spinner('⏳ Chargement du fichier STBAN (20 Mo)...'):
				# Lire le contenu du fichier une fois
				file_content = stban_file.read()
				stban_file.seek(0)  # Remettre le pointeur au début
				
				# Utiliser la fonction cachée
				stban_df = load_stban_file(file_content)
			
			if stban_df is not None and len(stban_df) > 0:
				st.success(f"✅ Fichier STBAN chargé et mis en cache ({len(stban_df)} lignes)")
				
				# Pré-identifier les colonnes
				prise_col, pto_col = identify_columns(list(stban_df.columns))
				
				if prise_col and pto_col:
					st.success(f"✅ Colonnes identifiées : {prise_col} | {pto_col}")
					
					# Pré-calculer le DataFrame optimisé
					with st.spinner('⚙️ Optimisation des données pour recherche rapide...'):
						_ = prepare_stban_for_search(stban_df, prise_col, pto_col)
						st.success("✅ Données optimisées et mises en cache")
				else:
					st.warning("⚠️ Colonnes PRISE/PTO non trouvées")
		
		except Exception as e:
			st.error(f"⚠️ Erreur: {str(e)}")
			stban_df = None
					
	if uploaded_file is not None:
		try:
			# Charger le fichier Excel
			try:
				df = pd.read_excel(uploaded_file, engine='openpyxl')
			except:
				try:
					df = pd.read_excel(uploaded_file, engine='xlrd')
				except:
					df = pd.read_excel(uploaded_file)
			
			# Extraire les valeurs uniques pour l'autocomplétion
			all_values = get_all_unique_values(df)
			
			# Extraire spécifiquement les noms de boîtes
			boite_names = extract_boite_names_from_df(df)
			
			# Interface de recherche avec autocomplétion
			st.markdown('<div class="search-container fade-in">', unsafe_allow_html=True)
			st.markdown("### 🔍 Recherche avec autocomplétion")
			
			# Choix du mode de recherche
			search_mode = st.radio(
				"Mode de recherche",
				["🎯 Recherche par boîte", "🔍 Recherche générale"],
				horizontal=True
			)
			
			if search_mode == "🎯 Recherche par boîte":
				# Recherche spécifique aux boîtes
				if boite_names:
					st.markdown('<div class="info-box">💡 Sélectionnez une boîte dans la liste pour une recherche précise</div>', unsafe_allow_html=True)
					
					col1, col2 = st.columns([3, 1])
					with col1:
						selected_value = st.selectbox(
							"Sélectionnez ou tapez une boîte",
							options=[''] + boite_names,
							key="boite_search"
						)
					
					with col2:
						search_button = st.button("🔍 Rechercher", type="primary", key="btn_boite")
				else:
					st.warning("⚠️ Aucune colonne 'boîte' trouvée dans le fichier")
					selected_value = None
					search_button = False
			else:
				# Recherche générale avec toutes les valeurs
				st.markdown('<div class="info-box">💡 Commencez à taper pour voir les suggestions</div>', unsafe_allow_html=True)
				
				col1, col2 = st.columns([3, 1])
				with col1:
					selected_value = st.selectbox(
						"Rechercher une valeur",
						options=[''] + all_values,
						key="general_search"
					)
				
				with col2:
					search_button = st.button("🔍 Rechercher", type="primary", key="btn_general")
			
			st.markdown('</div>', unsafe_allow_html=True)
			
			# Recherche
			if (selected_value and selected_value != '') or search_button:
				if selected_value and selected_value != '':
					# Recherche dans toutes les colonnes
					found_column_name = None
					found_column_name = df.columns[np.any(df == selected_value, axis=0)][0]
					#for col in df.columns:
						#if df[col].astype(str).str.contains(str(selected_value)).any():
							#found_column_name = col
							#break
					st.write(found_column_name)
					if found_column_name is None:
						return None

					col_index = df.columns.get_loc(found_column_name)
					target_col_index = col_index + 2
				
					if target_col_index >= len(df.columns):
						return None
				
					target_column_name = df.columns[target_col_index]

					results = df[(df[found_column_name] == selected_value) & (df[target_column_name] == 'STOCKEE')]	
					
					if len(results) > 0:
						# Construire le titre avec le nombre de résultats et éventuellement le nombre de prises
						results_title = f"### 📋 {len(results)} résultat(s) trouvé(s) pour '{selected_value}'"
	
						# Calculer le nombre de prises si STBAN est chargé et mode boîte
						prises_count_display = ""
						debug_mode = False
						if stban_df is not None and search_mode == "🎯 Recherche par boîte":
							prises_count = calculate_prises_count(stban_df, selected_value)
							if prises_count is not None and prises_count > 0:
								prises_count_display = f'<span class="prises-badge">🔌 Nombre de prises: {prises_count}</span>'
						
						# Afficher le titre avec le nombre de prises
						st.markdown(f'{results_title} {prises_count_display}', unsafe_allow_html=True)
						
						# Si plus de 10 résultats, permettre de limiter l'affichage
						if len(results) > 10:
							show_all = st.checkbox("Afficher tous les résultats", value=False)
							display_results = results if show_all else results.head(10)
						else:
							display_results = results
						
						# Afficher les résultats
						for idx, (_, row) in enumerate(display_results.iterrows()):
							
							# Formater l'identifiant
							tiroir, pos = get_tiroir_pos(row, df)
							pbo_tube, pbo_fibre = get_pbo_tube_fiber(row, df)
							
							# Construire l'identifiant
							base_id = f"{tiroir}P{pos}" if tiroir and pos else "N/A"
							if pbo_tube and pbo_fibre:
								try:
									tube_int = int(float(pbo_tube))
									fibre_int = int(float(pbo_fibre))
									full_id = f"{base_id} - T{tube_int}F{fibre_int}"
								except:
									full_id = f"{base_id} - T{pbo_tube}F{pbo_fibre}"
							else:
								full_id = base_id
							
							with st.expander(f"🔍 {full_id}", expanded=False):
								
								# Informations générales
								col1, col2 = st.columns(2)
								with col1:
									if len(row) > 0:
										st.markdown(f"""
										<div class="metric-container">
											<div class="metric-label">🏠 Tiroir</div>
											<div class="metric-value">{tiroir}</div>
										</div>
										""", unsafe_allow_html=True)
								with col2:
									if len(row) > 1:
										st.markdown(f"""
										<div class="metric-container">
											<div class="metric-label">📍 Position</div>
											<div class="metric-value">{pos}</div>
										</div>
										""", unsafe_allow_html=True)
								
								# Extraire et afficher les segments en format condensé avec couleurs
								segments = extract_route_segments(row, df)
								
								if segments:
									st.markdown("#### 🗺️ Route Détaillée")
	
									# Calculer les cumuls de longueurs
									cumulative_lengths = calculate_cumulative_lengths(segments)
									#st.write(cumulative_lengths)
									
									# Afficher chaque segment avec son cumul
									for i, segment in enumerate(segments):
										cumul = cumulative_lengths[i] if i < len(cumulative_lengths) else None
										display_segment_condensed_with_colors(segment, i, cumul)
								else:
									st.info("ℹ️ Aucun segment de route détaillée trouvé pour cette ligne")
									# Afficher les données brutes
									st.markdown("**📄 Données de la ligne :**")
									display_data = {}
									for i, value in enumerate(row):
										if pd.notna(value) and str(value).strip():
											col_name = df.columns[i] if i < len(df.columns) else f"Col {i+1}"
											display_data[col_name] = value
									
									if display_data:
										for key, value in display_data.items():
											st.text(f"{key}: {value}")
									
						if len(results) > 10 and not show_all:
							st.info(f"ℹ️ Affichage des 10 premiers résultats sur {len(results)} trouvés. Cochez 'Afficher tous les résultats' pour voir plus.")
							
					else:
						st.warning(f"❌ Aucun résultat trouvé pour '{selected_value}'")
						st.info("💡 Essayez avec un terme de recherche différent ou plus court")
				else:
					st.info("ℹ️ Veuillez sélectionner une valeur dans la liste déroulante")
				
		except Exception as e:
			st.error(f"⚠️ Erreur lors du traitement: {str(e)}")
			st.info("💡 Vérifiez que votre fichier Excel est valide")
	else:
		# Message d'accueil si aucun fichier n'est chargé
		st.info("👆 Veuillez charger un fichier Excel Route Optique pour commencer l'analyse")
		
if __name__ == "__main__":
    main()





