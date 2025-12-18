import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configurare pagină
st.set_page_config(page_title="Proiect EDA - Beers & Breweries", layout="wide")

# --- INIȚIALIZARE SESSION STATE ---
if 'df_beers' not in st.session_state:
    st.session_state['df_beers'] = None
if 'df_breweries' not in st.session_state:
    st.session_state['df_breweries'] = None
if 'df_final' not in st.session_state:
    st.session_state['df_final'] = None

# --- MENIU LATERAL ---
st.sidebar.title("🎓 Proiect EDA - Bere Artizanală în USA")
st.sidebar.markdown("**Student:** Cristian Țabîră")
st.sidebar.markdown("**Grupa:** 1128 BDSA")
st.sidebar.divider()

pagini = [
    "📖 Prezentare Proiect", 
    "1️⃣ Cerința 1: Încărcare & Filtrare", 
    "2️⃣ Cerința 2: Statistici & Lipsă", 
    "3️⃣ Cerința 3: Distribuții", 
    "4️⃣ Cerința 4: Categorice", 
    "5️⃣ Cerința 5: Corelații & Outlieri"
]
pagina_selectata = st.sidebar.radio("Navigare secțiuni:", pagini)

if pagina_selectata == "📖 Prezentare Proiect":
    st.title("🍺 Analiza Exploratorie a Pieței de Bere Artizanală")
    
    st.markdown("""
    ### 🎯 Obiectivul Proiectului
    Acest proiect realizează o **Analiză Exploratorie a Datelor** utilizând un set de date corelat format din:
    * **Beers**: Informații despre sortimente (nume, stil, conținut alcool, amărăciune).
    * **Breweries**: Detalii despre locația berăriilor (oraș, stat).
    
    Scopul este de a identifica pattern-uri în producția de bere, corelația între caracteristicile chimice (ABV vs IBU) și distribuția geografică a berăriilor.

    
    ### 📂 Structura Analizei
    Datele au fost preluate de pe Kaggle, eu sunt un mare băutor de bere🍺 așa că am căutat ceva de interes. 
    """)
    
    st.info("💡Fluxul începe prin încărcarea fișierelor CSV în secțiunea **Cerința 1**.")


# --- CERINȚA 1: ÎNCĂRCARE ȘI FILTRARE ---
elif pagina_selectata == "1️⃣ Cerința 1: Încărcare & Filtrare":
    st.header("Cerința 1: Încărcare, Validare și Filtrare")
    
    tab_incarcare, tab_filtrare = st.tabs(["📥 Încărcare & Validare", "🔍 Filtrare Date"])

    with tab_incarcare:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📦 Tabel Beri")
            f_beers = st.file_uploader("Încarcă beers.csv", type=["csv", "xlsx"], key="u_beers")
            if f_beers:
                st.session_state['df_beers'] = pd.read_csv(f_beers) if f_beers.name.endswith('.csv') else pd.read_excel(f_beers)
                st.success(f"✅ Beers încărcat: {len(st.session_state['df_beers'])} rânduri")
        
        with col2:
            st.subheader("🏭 Tabel Berării")
            f_breweries = st.file_uploader("Încarcă breweries.csv", type=["csv", "xlsx"], key="u_breweries")
            if f_breweries:
                st.session_state['df_breweries'] = pd.read_csv(f_breweries) if f_breweries.name.endswith('.csv') else pd.read_excel(f_breweries)
                st.success(f"✅ Breweries încărcat: {len(st.session_state['df_breweries'])} rânduri")

        # Buton pentru JOIN 
        if st.session_state['df_beers'] is not None and st.session_state['df_breweries'] is not None:
            st.divider()
            if st.button("🔗 Încarcă fișierele"):
                df_b = st.session_state['df_beers'].copy()
                df_br = st.session_state['df_breweries'].copy()
                df_br = df_br.rename(columns={"Unnamed: 0": "brewery_id", "name": "brewery_name"})
                st.session_state['df_final'] = pd.merge(df_b, df_br, on="brewery_id")
                st.success("🎉 Join realizat cu succes! Datele sunt disponibile pentru analize complexe.")

    with tab_filtrare:
        # Selector pentru ce tabel dorim să filtrăm
        optiuni_tabel = []
        if st.session_state['df_beers'] is not None: optiuni_tabel.append("Beri (Beers)")
        if st.session_state['df_breweries'] is not None: optiuni_tabel.append("Berării (Breweries)")
        if st.session_state['df_final'] is not None: optiuni_tabel.append("Dataset Unit (Join)")

        if not optiuni_tabel:
            st.warning("⚠️ Încarcă datele în tab-ul de Încărcare.")
        else:
            tabel_ales = st.selectbox("Alege tabelul pentru filtrare și vizualizare:", optiuni_tabel)
            
            if tabel_ales == "Beri (Beers)": df_selectat = st.session_state['df_beers']
            elif tabel_ales == "Berării (Breweries)": df_selectat = st.session_state['df_breweries']
            else: df_selectat = st.session_state['df_final']

            st.write(f"### Preview {tabel_ales} (Primele 10 rânduri)")
            st.dataframe(df_selectat.head(10))

            st.divider()
            
            # Filtrare Dinamică (Cerința 1)
            df_filtrat = df_selectat.copy()
            c1, c2 = st.columns(2)
        
            # Identificăm coloanele automat
            num_cols = df_selectat.select_dtypes(include=[np.number]).columns.tolist()
            cat_cols = df_selectat.select_dtypes(include=['object']).columns.tolist()

            with c1:
                st.write("#### 🔢 Filtre Numerice")
                for col in num_cols:
                    if col != 'brewery_id' and col != 'id': # Evităm ID-urile pentru slidere
                        min_v, max_v = float(df_selectat[col].min()), float(df_selectat[col].max())
                        val = st.slider(f"{col}", min_v, max_v, (min_v, max_v), key=f"s_{col}")
                        df_filtrat = df_filtrat[(df_filtrat[col] >= val[0]) & (df_filtrat[col] <= val[1])]

            with c2:
                st.write("#### 🔠 Filtre Categorice")
                
                # Definim coloanele prioritare pentru filtrare în funcție de tabel
                if tabel_ales == "Beri (Beers)":
                    cat_filtre = ["style"] 
                elif tabel_ales == "Berării (Breweries)":
                    cat_filtre = ["state", "city"]
                else: # Dataset Unit
                    cat_filtre = ["style", "state", "city"]

                for col in cat_filtre:
                    if col in df_selectat.columns:
                        opt = sorted(df_selectat[col].dropna().unique().tolist())
                        help_text = "Selectează unul sau mai multe stiluri de bere" if col == "style" else ""
                        sel = st.multiselect(f"Filtrează după {col}", opt, key=f"m_{col}", help=help_text)
                        if sel: 
                            df_filtrat = df_filtrat[df_filtrat[col].isin(sel)]

            st.info(f"Rânduri înainte: {len(df_selectat)} | Rânduri după: {len(df_filtrat)}")
            st.dataframe(df_filtrat)

# --- CERINȚA 2: STATISTICI ---
elif pagina_selectata == "2️⃣ Cerința 2: Statistici & Lipsă":
    st.header("Cerința 2: Explorarea Datelor și Valorile Lipsă")
    
    if st.session_state['df_final'] is not None:
        df = st.session_state['df_final']
        
        st.subheader("📏 Structură Dataset")
        st.write(f"Dataset-ul conține **{df.shape[0]}** rânduri și **{df.shape[1]}** coloane.")
        st.write("**Tipuri de date:**", df.dtypes.astype(str))
        
        st.divider()
        st.subheader("❓ Analiza Valorilor Lipsă")
        null_df = pd.DataFrame({
            'Valori Lipsă': df.isnull().sum(),
            'Procent (%)': (df.isnull().sum() / len(df) * 100).round(2)
        }).sort_values('Valori Lipsă', ascending=False)
        
        st.table(null_df[null_df['Valori Lipsă'] > 0])
        
        # Grafic valori lipsă
        fig_missing = px.bar(null_df[null_df['Valori Lipsă'] > 0], y='Procent (%)', 
                             title="Distribuția valorilor lipsă", color_discrete_sequence=['#E74C3C'])
        st.plotly_chart(fig_missing, use_container_width=True)
        
        st.divider()
        st.subheader("📊 Statistici Descriptive, Quartile și Outlieri")
        st.dataframe(df.describe())

        # Vizualizare quartile și outlieri prin Box Plot (pentru toate numericele)
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        # Excludem ID-urile din vizualizare
        clean_num_cols = [c for c in num_cols if c not in ['brewery_id', 'id']]
        
        st.write("### Vizualizare Quartile și Outlieri (Box Plots)")
        fig_outliers = px.box(df[clean_num_cols], title="Identificarea Outlierilor și a Quartilelor pe coloanele numerice")
        st.plotly_chart(fig_outliers, use_container_width=True)
        st.divider()
        st.subheader("🧹 Curățarea Datelor (Opțional)")
        st.write("Dacă doriți să eliminați sau să completați valorile lipsă pentru analize mai precise:")
        
        metoda_curatare = st.selectbox("Alege o metodă de tratare a valorilor lipsă:", 
                                        ["Nicio acțiune", "Elimină rândurile cu valori lipsă", "Înlocuiește cu Media coloanei", "Înlocuiește cu Mediana coloanei"])
        
        if metoda_curatare != "Nicio acțiune":
            df_curat = df.copy()
            if metoda_curatare == "Elimină rândurile cu valori lipsă":
                df_curat = df_curat.dropna()
                st.warning(f"Au fost eliminate rândurile cu NaN. Rânduri rămase: {len(df_curat)}")
            elif metoda_curatare == "Înlocuiește cu Media coloanei":
                df_curat = df_curat.fillna(df_curat.mean(numeric_only=True))
                st.success("Valorile lipsă au fost înlocuite cu media.")
            elif metoda_curatare == "Înlocuiește cu Mediana coloanei":
                df_curat = df_curat.fillna(df_curat.median(numeric_only=True))
                st.success("Valorile lipsă au fost înlocuite cu mediana.")
            
            # Putem salva acest df_curat în session state dacă vrem ca restul cerințelor să îl folosească
            if st.button("Aplică modificările pentru tot proiectul"):
                st.session_state['df_final'] = df_curat
                st.rerun()

    else:
        st.error("❌ Te rugăm să încarci datele la Cerința 1!")   

elif pagina_selectata == "3️⃣ Cerința 3: Distribuții":
    st.header("Cerința 3: Analiza Distribuției unei variabile numerice")
    
    if st.session_state['df_final'] is not None:
        df = st.session_state['df_final']
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        clean_num_cols = [c for c in num_cols if c not in ['brewery_id', 'id']]

        # Selectare coloană numerică
        col_aleasa = st.selectbox("Selectează variabila pentru analiză:", clean_num_cols)
        
        # Slider pentru Bins
        num_bins = st.slider("Selectează numărul de intervale (bins) pentru histogramă:", 10, 100, 30)

        c1, c2 = st.columns(2)
        
        with c1:
            # Histogramă interactivă
            fig_hist = px.histogram(df, x=col_aleasa, nbins=num_bins, title=f"Histogramă: {col_aleasa}",
                                   color_discrete_sequence=['#3498DB'], marginal="rug")
            st.plotly_chart(fig_hist, use_container_width=True)

        with c2:
            # Box plot pentru aceeași coloană
            fig_box = px.box(df, y=col_aleasa, title=f"Box Plot: {col_aleasa}", color_discrete_sequence=['#F1C40F'])
            st.plotly_chart(fig_box, use_container_width=True)

        # Calcul și afișare Medie, Mediană, Std
        st.subheader(f"📈 Indicatori statistici pentru {col_aleasa}")
        m1, m2, m3 = st.columns(3)
        m1.metric("Medie (Mean)", round(df[col_aleasa].mean(), 3))
        m2.metric("Mediană (Median)", round(df[col_aleasa].median(), 3))
        m3.metric("Deviație Standard (Std)", round(df[col_aleasa].std(), 3))
        
    else:
        st.error("❌ Te rugăm să încarci ambele fișiere la Cerința 1!")

elif pagina_selectata == "4️⃣ Cerința 4: Categorice":
    st.header("Cerința 4: Analiza Variabilelor Categorice")
    
    if st.session_state['df_final'] is not None:
        df = st.session_state['df_final']
        
        # Identificare automată coloane categorice
        cat_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        # Selectare coloană categorică
        col_cat = st.selectbox("Selectează coloana categorică de vizualizat:", cat_cols)
        
        # Creare tabel frecvențe (Absolute și Procente)
        frecv_abs = df[col_cat].value_counts().reset_index()
        frecv_abs.columns = [col_cat, 'Frecvență Absolută']
        frecv_abs['Procent (%)'] = ((frecv_abs['Frecvență Absolută'] / len(df)) * 100).round(2)

        # Vizualizare Count Plot (Bar Chart)
        # Luăm top 20 categorii dacă sunt prea multe (ex: orașe) pentru a fi lizibil
        top_n = st.slider("Afișează primele N categorii (după frecvență):", 5, 50, 15)
        
        fig_count = px.bar(frecv_abs.head(top_n), x=col_cat, y='Frecvență Absolută', 
                           title=f"Top {top_n} {col_cat} ca frecvență",
                           text_auto=True, color='Frecvență Absolută', color_continuous_scale='Viridis')
        st.plotly_chart(fig_count, use_container_width=True)

        # Tabel frecvențe
        st.subheader(f"📋 Tabel de frecvențe pentru {col_cat}")
        st.dataframe(frecv_abs)
        
    else:
        st.error("❌ Te rugăm să încarci datele la Cerința 1!")

elif pagina_selectata == "5️⃣ Cerința 5: Corelații & Outlieri":
    st.header("Cerința 5: Analiza Corelațiilor și Detectarea Outlierilor (Metoda IQR)")
    
    if st.session_state['df_final'] is not None:
        df = st.session_state['df_final']
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        # Excludem coloanele de tip ID care nu au sens în corelații sau outlieri
        clean_num_cols = [c for c in num_cols if c not in ['brewery_id', 'id']]
        
        # --- SUB-SECȚIUNEA 1: CORELAȚII ---
        st.subheader("🔗 1. Matricea de Corelație")
        
        # Calcul corelație
        corr_matrix = df[clean_num_cols].corr()
        
        # Heatmap interactiv
        fig_corr = px.imshow(corr_matrix, text_auto='.2f', aspect="auto",
                             color_continuous_scale='RdBu_r', 
                             title="Heatmap: Corelații între variabilele numerice")
        st.plotly_chart(fig_corr, use_container_width=True)
        
        st.divider()
        st.subheader("📈 2. Corelația Pearson între două variabile")
        
        c1, c2 = st.columns(2)
        with c1:
            var_x = st.selectbox("Alege variabila X:", clean_num_cols, index=0)
        with c2:
            var_y = st.selectbox("Alege variabila Y:", clean_num_cols, index=1 if len(clean_num_cols)>1 else 0)
        
        # Calcul Pearson
        pearson_val = df[var_x].corr(df[var_y], method='pearson')
        
        st.metric(f"Coeficient de corelație Pearson ({var_x} vs {var_y})", f"{pearson_val:.4f}")
        
        # Scatter Plot
        fig_scatter = px.scatter(df, x=var_x, y=var_y, trendline="ols",
                                 title=f"Scatter Plot: {var_x} vs {var_y}",
                                 color_discrete_sequence=['#2ECC71'])
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        st.divider()
        
        # --- SUB-SECȚIUNEA 2: OUTLIERI (IQR) ---
        st.subheader("🚫 3. Detecția Outlierilor (Metoda IQR)")
        st.write("Metoda **Interquartile Range (IQR)** identifică valorile care depășesc pragurile: $[Q1 - 1.5 \cdot IQR]$ și $[Q3 + 1.5 \cdot IQR]$.")
        
        outlier_data = []
        
        for col in clean_num_cols:
            # Calculăm quartilele ignorând valorile lipsă
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Identificăm rândurile
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            count = len(outliers)
            percent = (count / len(df)) * 100
            
            outlier_data.append({
                'Coloană': col,
                'Q1': round(Q1, 4),
                'Q3': round(Q3, 4),
                'IQR': round(IQR, 4),
                'Outlieri': count,
                'Procent (%)': round(percent, 2)
            })
            
        outlier_df = pd.DataFrame(outlier_data)
        st.table(outlier_df)
        
        # Vizualizare outlieri pentru coloana selectată la Cerința 3 sau una nouă
        st.write("### Vizualizare Outlieri (Box Plot)")
        col_out = st.selectbox("Selectează coloana pentru vizualizarea outlierilor pe grafic:", clean_num_cols)
        fig_box_out = px.box(df, y=col_out, points="all", # afișăm toate punctele pentru a vedea densitatea
                             title=f"Box Plot Detaliat: {col_out}", color_discrete_sequence=['#E67E22'])
        st.plotly_chart(fig_box_out, use_container_width=True)
        
    else:
        st.error("❌ Te rugăm să încarci datele la Cerința 1!")
else:
    st.info("Secțiune în lucru...")