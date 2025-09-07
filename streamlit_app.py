# --- Fonctions Utilitaires ---

def get_base64_of_bin_file(bin_file):
    """Convertit un fichier binaire en base64 pour l'affichage d'images locales."""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

# Charger le CSS personnalisé depuis un fichier externe
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Appliquer le CSS
load_css('style.css')

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
def extract_boite_names_from_df(df):
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
    prise_col, pto_col = identify_columns(stban_df.columns)
    if not prise_col or not pto_col:
        st.warning("Colonnes 'REF_PBO_PRISE' ou 'REF_PBO_PTO' introuvables dans le fichier STBAN.")
        return None
    optimized_df = prepare_stban_for_search(stban_df, prise_col, pto_col)
    return calculate_prises_count_optimized(optimized_df, boite_name)

# --- Fonctions d'Affichage ---

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

def display_detailed_route(row):
    """Affiche la route détaillée pour une ligne de résultat."""
    # Extraire Tiroir et Position
    tiroir, position = None, None
    for item in row.dropna():
        item_str = str(item)
        if 'Tiroir' in item_str:
            tiroir = item_str
        elif 'Position' in item_str:
            position = item_str

    col1, col2 = st.columns(2)
    with col1:
        if tiroir:
            st.markdown(f'<div class="metric-container"><div class="metric-label">Tiroir</div><div class="metric-value">{tiroir.split(":")[-1].strip()}</div></div>', unsafe_allow_html=True)
    with col2:
        if position:
            st.markdown(f'<div class="metric-container"><div class="metric-label">Position</div><div class="metric-value">{position.split(":")[-1].strip()}</div></div>', unsafe_allow_html=True)
    
    st.markdown("<h4>Route Détaillée</h4>", unsafe_allow_html=True)

    # Afficher les segments de la route
    for item in row.dropna():
        item_str = str(item)
        if 'Tiroir' in item_str or 'Position' in item_str:
            continue

        # Utiliser des expressions régulières pour extraire les informations
        cable_match = re.search(r'([A-Z0-9\-]+_\d+F\d*)\s*/\s*(\d+ml)\s*\((\d+ml)\)', item_str)
        
        elements_html = ''
        status_html = ''
        
        if cable_match:
            cable_name, length, total_length = cable_match.groups()
            elements_html += f'<div class="cable-name-condensed">{cable_name} ({length})</div>'
            remaining_text = item_str[cable_match.end():].strip()
            parts = [p.strip() for p in remaining_text.split(',')]
        else:
            parts = [p.strip() for p in item_str.split(',')]

        elements_group = ''
        for part in parts:
            status_class = get_status_class(part)
            if status_class:
                status_html = f'<div class="{status_class}">{part}</div>'
            else:
                color = get_color_from_text(part)
                badge_class = 'boite-badge-condensed' if 'BPE' in part or 'CAS' in part else 'tube-badge-condensed'
                elements_group += f'<span class="{badge_class}" style="background-color: {color}20; color: {color}; border-color: {color};">{part}</span>'
        
        if elements_group:
            elements_html += f'<div class="elements-group">{elements_group}</div>'

        st.markdown(f'<div class="segment-condensed fade-in">{elements_html}{status_html}</div>', unsafe_allow_html=True)

# --- Interface Utilisateur (UI) ---

# En-tête de l'application
logo_base64 = get_base64_of_bin_file("logo-ICT-group.png")
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
        st.session_state.boite_names = get_all_unique_values(df)
        if st.session_state.stban_df is not None:
            # Si le fichier STBAN est chargé, ajouter ses noms de boîtes et supprimer les doublons
            st.session_state.boite_names.extend(extract_boite_names_from_df(st.session_state.stban_df))
            st.session_state.boite_names = sorted(list(set(st.session_state.boite_names)))
            st.session_state.stban_processed = True # Marquer que le STBAN a été traité pour les noms de boîtes
        

    with st.container(border=True):
        st.markdown('## 🔍 Recherche avec autocomplétion')
        search_mode = st.radio("Mode de recherche", ("Recherche par boîte", "Recherche générale"), horizontal=True, key="search_mode")

        search_term = ''
        if search_mode == "Recherche par boîte":
            if st.session_state.route_optique_df is not None:
                search_term = st.selectbox("Sélectionnez une boîte", st.session_state.boite_names, key="boite_selectbox", label_visibility="collapsed")
                if st.session_state.stban_df is None:
                    st.info("Le fichier STBAN n'est pas chargé. Le calcul du nombre de prises ne sera pas disponible pour la recherche par boîte.")
            else:
                st.info("Veuillez charger un fichier Excel Route Optique pour activer la recherche par boîte.")
                search_term = st.selectbox("Sélectionnez une boîte", ["Veuillez charger un fichier ROP"], key="boite_selectbox", label_visibility="collapsed", disabled=True)

        else:
            # La recherche générale utilise toujours les valeurs uniques du fichier ROP
            search_term = st.selectbox("Recherche générale", st.session_state.all_unique_values, key="general_search_selectbox", label_visibility="collapsed")

        if st.button("Rechercher", type="primary", use_container_width=True) and search_term:
            st.markdown(f'### Résultats pour : <span class="search-term-highlight">{search_term}</span>', unsafe_allow_html=True)

            # Affichage du nombre de prises
            if st.session_state.stban_df is not None and search_mode == "Recherche par boîte":
                with st.spinner("Calcul du nombre de prises..."):
                    prises_count = calculate_prises_count(st.session_state.stban_df, search_term)
                if prises_count is not None:
                    st.markdown(f'<div class="prises-badge">🔌 Nombre de prises : <strong>{prises_count}</strong></div>', unsafe_allow_html=True)
            
            # Recherche des ROPs
            matching_rows = df[df.apply(lambda row: row.astype(str).str.contains(re.escape(search_term), case=False, na=False).any(), axis=1)]

            if not matching_rows.empty:
                st.success(f"{len(matching_rows)} ROP trouvée(s).")
                for index, row in matching_rows.iterrows():
                    expander_title = f"ROP {index + 1} - {row.dropna().iloc[0] if not row.dropna().empty else 'Détails'}"
                    with st.expander(expander_title):
                        display_detailed_route(row)
            else:
                st.warning("Aucun résultat trouvé pour votre recherche.")
