import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from scipy.stats import kurtosis, skew
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler, Normalizer, RobustScaler, \
    QuantileTransformer
import warnings
import pymongo
from datetime import datetime

warnings.filterwarnings('ignore')

# Configurare pagină
st.set_page_config(
    page_title="Seminar AVM - Analiza Volumelor Mari de Date",
    page_icon="     ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizat
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    .method-box {
        background-color: #f0f8ff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #3498db;
        margin: 1rem 0;
    }
    .why-box {
        background-color: #fff9e6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #f39c12;
        margin: 1rem 0;
    }
    .theory-box {
        background-color: #f0f0f0;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .code-explanation {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# Funcție pentru încărcarea datelor din MongoDB
@st.cache_data(ttl=3600)
def load_data_from_mongodb(connection_string, database_name, collection_name, projection=None, sort_field=None):
    """Încarcă datele din MongoDB cu caching"""
    try:
        client = pymongo.MongoClient(connection_string)
        db = client[database_name]
        collection = db[collection_name]

        projection_dict = {"_id": 0}
        if projection:
            projection_dict.update(projection)

        sort_list = [(sort_field, 1)] if sort_field else None

        cursor = collection.find({}, projection=projection_dict, sort=sort_list)
        df = pd.DataFrame.from_dict(list(cursor))
        cursor.close()
        client.close()
        df = pd.read_csv("clienti_daune.csv")
        return df, None
    except Exception as e:
        return None, str(e)

@st.cache_data(ttl=3600)
def load_data_from_csv(uploaded_file):
    """Încarcă datele dintr-un fișier CSV încărcat în Streamlit."""
    df = pd.read_csv(uploaded_file)
    return df
# Sidebar Navigation
def sidebar_navigation():
    st.sidebar.markdown("#  Seminar AVM")
    st.sidebar.markdown("### Navighează:")

    sections = [
        " Acasă",
        " Introducere în Streamlit",
        " Conexiune MongoDB & Încărcare Date",
        " Curățarea Datelor",
        " Detectarea Valorilor Anormale",
        " Prelucrarea Șirurilor de Caractere",
        " Standardizare și Normalizare",
        " Statistici Descriptive",
        " Reprezentări Grafice",
        " Rezumat & Concluzii"
    ]

    selected = st.sidebar.radio("Selectează Modulul:", sections)

    st.sidebar.markdown("---")
    st.sidebar.markdown("###  Despre Seminar")
    st.sidebar.info(
        "Seminar 1 - Analiza Volumelor Mari de Date în Python\n\n"
        "Metode de prelucrare, analiză și vizualizare a datelor utilizând "
        "pandas, numpy, sklearn și MongoDB."
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("###   Etapele Analizei")
    st.sidebar.markdown("""
    1. **Organizare date** - MongoDB, SQL
    2. **Prelucrare date** - Curățare, standardizare
    3. **Analiză date** - Descriptivă, diagnostic, predictivă
    """)

    return selected


# Pagina de Acasă
def show_home():
    st.markdown('<h1 class="main-header"> Seminar 1 - Analiza Volumelor Mari de Date în Python</h1>',
                unsafe_allow_html=True)

    st.markdown("""
    ## 
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="method-box">
        <h3>Organizare Date</h3>
        <ul>
            <li>BD Relaționale (Oracle, MySQL)</li>
            <li>BD NoSQL (MongoDB)</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="method-box">
        <h3>Prelucrare Date</h3>
        <ul>
            <li>Curățarea datelor</li>
            <li>Îmbunătățirea acurateței</li>
            <li>Standardizare și normalizare</li>
            <li>Statistici descriptive</li>
            <li>Reducerea volumului</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="method-box">
        <h3>Analiză Date</h3>
        <ul>
            <li>Analiză descriptivă</li>
            <li>Analiză diagnostic</li>
            <li>Analiză predictivă</li>
            <li>Analiză prescriptivă</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    ## Structura Seminarului

    Acest seminar acoperă **metode de prelucrare a datelor în Python**, cu focus pe:

    1. **Curățarea datelor**: Eliminarea duplicatelor și tratarea valorilor lipsă
    2. **Detectarea anomaliilor**: Identificarea și tratarea outlier-ilor
    3. **Prelucrarea textului**: Transformarea și standardizarea șirurilor
    4. **Scalarea datelor**: Standardizare și normalizare
    5. **Analiza statistică**: Skewness, kurtosis, corelații
    6. **Vizualizări**: Histograme, boxplot, heatmap, pie chart

    ### Setul de Date

    Vom lucra cu baza de date **DAUNE_LEASING** care conține informații despre:
    - **CLIENTI_LEASING**: Date clienți (vârstă, profesie, venit, etc.)
    - **CLIENTI_DAUNE**: Date daune (marcă auto, componente, valoare daună)

    """)



# Introducere Streamlit
def show_streamlit_intro():
    st.markdown('<h1 class="main-header"> Introducere în Streamlit</h1>', unsafe_allow_html=True)

    st.markdown("""
    ## Ce este Streamlit?

    **Streamlit** este un framework Python open-source pentru crearea rapidă de aplicații web interactive 
    pentru data science și machine learning, fără a fi nevoie de cunoștințe HTML, CSS sau JavaScript.
    """)

    st.markdown('<div class="sub-header">Principiul de Bază</div>', unsafe_allow_html=True)

    st.markdown("""
    Streamlit transformă codul Python în elemente web interactive printr-un proces simplu:

    1. **Scrii cod Python** normal
    2. **Adaugi comenzi Streamlit** (st.write, st.button, etc.)
    3. **Rulezi cu** `streamlit run app.py`
    4. **Aplicația se deschide** automat în browser
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("###  Exemplu Cod")
        st.code("""
import streamlit as st
import pandas as pd

# Titlu
st.title("Prima Mea Aplicație")

# Text
st.write("Bună lume!")

# Input
name = st.text_input("Numele tău:")
st.write(f"Salut, {name}!")

# DataFrame
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})
st.dataframe(df)
        """, language="python")

    with col2:
        st.markdown("###  Rezultat Vizual")
        st.info("Codul din stânga produce:")
        st.markdown("**Titlu**: Prima Mea Aplicație")
        st.markdown("**Text**: Bună lume!")
        demo_name = st.text_input("Numele tău:", key="demo_name")
        if demo_name:
            st.write(f"Salut, {demo_name}!")
        demo_df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        st.dataframe(demo_df)

    st.markdown('<div class="sub-header">Componente Esențiale Streamlit</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([" Display", " Widgets", " Layout", " Data"])

    with tab1:
        st.markdown("### Metode de Afișare")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Cod:**")
            st.code("""
# Text și titluri
st.title("Titlu Mare")
st.header("Header")
st.subheader("Subheader")
st.text("Text simplu")
st.write("Text cu markdown **bold**")

# Markdown
st.markdown("Text *italic* și **bold**")

# LaTeX
st.latex(r'\\bar{x} = \\frac{1}{n}\\sum x_i')

# Mesaje
st.success("Succes!")
st.info("Info")
st.warning("Atenție")
st.error("Eroare")
            """, language="python")

        with col2:
            st.markdown("**Output:**")
            st.title("Titlu Mare")
            st.header("Header")
            st.subheader("Subheader")
            st.text("Text simplu")
            st.write("Text cu markdown **bold**")
            st.markdown("Text *italic* și **bold**")
            st.latex(r'\bar{x} = \frac{1}{n}\sum x_i')
            st.success("Succes!")
            st.info("Info")
            st.warning("Atenție")
            st.error("Eroare")

    with tab2:
        st.markdown("### Widget-uri Interactive")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Cod:**")
            st.code("""
# Input text
text = st.text_input("Introdu text:")

# Number input
number = st.number_input("Număr:", 0, 100, 50)

# Slider
slider = st.slider("Slider:", 0, 100, 50)

# Select box
option = st.selectbox("Alege:", ["A", "B", "C"])

# Multiselect
multi = st.multiselect("Alege multiple:", ["1", "2", "3"])

# Checkbox
check = st.checkbox("Bifează")

# Button
if st.button("Apasă"):
    st.write("Buton apăsat!")

# Radio
radio = st.radio("Alege unul:", ["X", "Y", "Z"])
            """, language="python")

        with col2:
            st.markdown("**Încearcă:**")
            demo_text = st.text_input("Introdu text:", key="widget_text")
            demo_number = st.number_input("Număr:", 0, 100, 50, key="widget_number")
            demo_slider = st.slider("Slider:", 0, 100, 50, key="widget_slider")
            demo_select = st.selectbox("Alege:", ["A", "B", "C"], key="widget_select")
            demo_multi = st.multiselect("Alege multiple:", ["1", "2", "3"], key="widget_multi")
            demo_check = st.checkbox("Bifează", key="widget_check")
            if st.button("Apasă", key="widget_button"):
                st.success("Buton apăsat!")
            demo_radio = st.radio("Alege unul:", ["X", "Y", "Z"], key="widget_radio")

    with tab3:
        st.markdown("### Organizarea Layout-ului")

        st.markdown("**1. Coloane**")
        st.code("""
col1, col2, col3 = st.columns(3)

with col1:
    st.write("Coloana 1")

with col2:
    st.write("Coloana 2")

with col3:
    st.write("Coloana 3")
        """, language="python")

        demo_col1, demo_col2, demo_col3 = st.columns(3)
        with demo_col1:
            st.info("Coloana 1")
        with demo_col2:
            st.success("Coloana 2")
        with demo_col3:
            st.warning("Coloana 3")

        st.markdown("**2. Tabs**")
        st.code("""
tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])

with tab1:
    st.write("Conținut Tab 1")

with tab2:
    st.write("Conținut Tab 2")
        """, language="python")

        st.markdown("**3. Expander**")
        st.code("""
with st.expander("Click pentru a extinde"):
    st.write("Conținut ascuns")
        """, language="python")

        with st.expander("Încearcă aici"):
            st.write("Conținut ascuns revelat!")

    with tab4:
        st.markdown("### Lucrul cu Date")

        st.code("""
import pandas as pd

# Creează DataFrame
df = pd.DataFrame({
    'col1': [1, 2, 3],
    'col2': [4, 5, 6]
})

# Afișează ca tabel interactiv
st.dataframe(df)

# Afișează ca tabel static
st.table(df)

# Metrici
st.metric(
    label="Vânzări",
    value="1,234",
    delta="12%"
)

# Grafice
st.line_chart(df)
st.bar_chart(df)
        """, language="python")

        demo_df = pd.DataFrame({
            'col1': [1, 2, 3, 4, 5],
            'col2': [10, 20, 15, 25, 30]
        })

        st.markdown("**DataFrame Interactiv:**")
        st.dataframe(demo_df)

        st.markdown("**Metrică:**")
        st.metric("Vânzări", "1,234", "12%")

        st.markdown("**Grafic:**")
        st.line_chart(demo_df)

    st.markdown('<div class="sub-header">Concepte Importante</div>', unsafe_allow_html=True)

    with st.expander(" Rerun - Cum Funcționează Streamlit"):
        st.markdown("""
        ### Modelul de Execuție

        Streamlit **rerulează întregul script** de fiecare dată când:
        - Utilizatorul interacționează cu un widget
        - Un fișier este modificat (în development)

        ```python
        import streamlit as st

        # Acest cod rulează de FIECARE DATĂ
        st.title("Aplicația Mea")

        # Când user-ul schimbă slider-ul, tot script-ul se rerulează
        value = st.slider("Valoare", 0, 100)
        st.write(f"Valoarea este: {value}")
        ```

        ### De Aceea Caching ! 
        """)

    with st.expander("Caching - Optimizarea Performanței"):
        st.markdown("""
        ### @st.cache_data

        Folosește caching pentru operații costisitoare:

        ```python
        import streamlit as st
        import pandas as pd

        # FĂRĂ caching - LENT (rulează de fiecare dată)
        def load_data():
            return pd.read_csv('large_file.csv')  # 10 secunde

        # CU caching - RAPID (rulează o singură dată)
        @st.cache_data
        def load_data_cached():
            return pd.read_csv('large_file.csv')  # 10 secunde prima dată, apoi instant

        # Folosește funcția cached
        df = load_data_cached()  # Instant după prima rulare!
        ```

        **Când să folosești caching:**
        - Încărcarea datelor din fișiere/baze de date
        - Calcule complexe
        - API calls
        - Procesarea datelor mari
        """)

    with st.expander(" Session State - Păstrarea Datelor"):
        st.markdown("""
        ### st.session_state

        Session state păstrează date între reruns:

        ```python
        import streamlit as st

        # Inițializare
        if 'counter' not in st.session_state:
            st.session_state.counter = 0

        # Increment la click
        if st.button('Incrementează'):
            st.session_state.counter += 1

        # Afișează valoarea (persistă între rerun-uri)
        st.write(f"Counter: {st.session_state.counter}")
        ```

        **Exemplu live:**
        """)

        # Demo session state
        if 'demo_counter' not in st.session_state:
            st.session_state.demo_counter = 0

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button(' Incrementează', key="inc_demo"):
                st.session_state.demo_counter += 1

        with col2:
            st.metric("Counter", st.session_state.demo_counter)

        with col3:
            if st.button(' Reset', key="reset_demo"):
                st.session_state.demo_counter = 0

    st.markdown('<div class="success-box">', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# Conexiune MongoDB
def show_mongodb_connection():
    st.markdown('<h1 class="main-header"> Conexiune MongoDB & Încărcare Date</h1>', unsafe_allow_html=True)

    st.markdown("""
    ## Conectarea la Baza de Date

    În acest modul vom învăța cum să:
    1. Ne conectăm la MongoDB
    2. Încărcăm date în DataFrame pandas
    3. Explorăm structura datelor
    """)

    st.markdown('<div class="sub-header">Pasul 1: Parametrii de Conexiune</div>', unsafe_allow_html=True)

    # Default connection parameters
    default_conn = "mongodb://master:stud1234@193.226.34.57:27017/?authSource=daune_leasing&authMechanism=SCRAM-SHA-256"
    default_db = "daune_leasing"

    with st.expander(" Despre Conexiunea MongoDB", expanded=False):
        st.markdown("""
        ### Structura Connection String-ului MongoDB

        ```
        mongodb://[username:password@]host[:port]/[?options]
        ```

        **Componentele:**
        - `mongodb://` - Protocol
        - `username:password` - Credențiale
        - `host:port` - Server și port (default: 27017)
        - `authSource` - Baza de date pentru autentificare
        - `authMechanism` - Mecanism de autentificare

        ### Cod Python pentru Conexiune

        ```python
        import pymongo
        import pandas as pd

        # Conectare
        conn = pymongo.MongoClient(connection_string)
        db = conn[database_name]
        collection = db[collection_name]

        # Interogare
        projection = {"_id": 0}  # Exclude _id
        sort = [("ID_CLIENT", 1)]  # Sortare
        cursor = collection.find({}, projection=projection, sort=sort)

        # Conversie la DataFrame
        df = pd.DataFrame.from_dict(list(cursor))
        cursor.close()
        ```
        """)

    # Connection inputs
    col1, col2 = st.columns([3, 1])

    with col1:
        connection_string = st.text_input(
            "Connection String MongoDB:",
            value=default_conn,
            help="Format: mongodb://user:pass@host:port/?authSource=db"
        )

    with col2:
        database_name = st.text_input(
            "Database:",
            value=default_db
        )

    st.markdown('<div class="sub-header">Pasul 2: Selectează Colecția</div>', unsafe_allow_html=True)

    collection_choice = st.radio(
        "Alege colecția de încărcat:",
        ["clienti_leasing", "clienti_daune", "Custom"],
        horizontal=True
    )

    if collection_choice == "Custom":
        collection_name = st.text_input("Numele colecției:", value="clienti_leasing")
    else:
        collection_name = collection_choice

    # Advanced options
    with st.expander(" Opțiuni "):
        col1, col2 = st.columns(2)

        with col1:
            use_projection = st.checkbox("Folosește proiecție (selectează coloane specifice)", value=False)
            if use_projection:
                projection_cols = st.text_area(
                    "Coloane (separate prin virgulă):",
                    value="ID_CLIENT, NUME_CLIENT, VARSTA, SEX",
                    help="Lasă gol pentru toate coloanele"
                )

        with col2:
            use_sort = st.checkbox("Sortează rezultatele", value=True)
            if use_sort:
                sort_field = st.text_input("Câmp pentru sortare:", value="ID_CLIENT")
            else:
                sort_field = None

    st.markdown('<div class="sub-header">Alternativă: Încarcă datele dintr-un fișier CSV</div>', unsafe_allow_html=True)

    with st.expander(" Încarcă fișier CSV (fără MongoDB)"):
        uploaded_csv = st.file_uploader("Alege fișierul CSV:", type=["csv"])

        if uploaded_csv is not None:
            try:
                df_csv = load_data_from_csv(uploaded_csv)
                st.session_state['df'] = df_csv
                st.session_state['collection_name'] = "csv_upload"

                st.success(f"Date încărcate cu succes din CSV! ({len(df_csv):,} rânduri, {len(df_csv.columns)} coloane)")

                st.dataframe(df_csv.head(10), use_container_width=True)

            except Exception as e:
                st.error(f"Eroare la citirea CSV-ului: {e}")

    # Load button
    if st.button(" Încarcă Date", type="primary"):
        with st.spinner("Se conectează la MongoDB..."):
            # Prepare projection
            projection = None
            if use_projection and projection_cols:
                cols = [col.strip() for col in projection_cols.split(',')]
                projection = {col: 1 for col in cols}

            # Load data
            df, error = load_data_from_mongodb(
                connection_string,
                database_name,
                collection_name,
                projection=projection,
                sort_field=sort_field
            )

            if error:
                st.error(f" Eroare la conectare: {error}")
            else:
                # Store in session state
                st.session_state['df'] = df
                st.session_state['collection_name'] = collection_name
                st.success(f" Date încărcate cu succes din colecția '{collection_name}'!")

    # Display data if loaded
    if 'df' in st.session_state:
        df = st.session_state['df']
        collection = st.session_state.get('collection_name', 'unknown')

        st.markdown('<div class="sub-header">Pasul 3: Explorarea Datelor Încărcate</div>', unsafe_allow_html=True)

        # Data overview
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Rânduri", f"{len(df):,}")

        with col2:
            st.metric("Total Coloane", len(df.columns))

        with col3:
            memory_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
            st.metric(" Memorie", f"{memory_mb:.2f} MB")

        with col4:
            missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)
            st.metric(" Valori Lipsă", f"{missing_pct:.1f}%")

        # Tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs([" Preview", " Info", " Statistici", " Vizualizare"])

        with tab1:
            st.markdown("### Primele Rânduri")
            n_rows = st.slider("Număr rânduri de afișat:", 5, 50, 10, key="preview_rows")
            st.dataframe(df.head(n_rows), use_container_width=True)

            with st.expander("Ultimele Rânduri"):
                st.dataframe(df.tail(n_rows), use_container_width=True)

        with tab2:
            st.markdown("### Informații Dataset")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Tipuri de Date:**")
                dtype_df = pd.DataFrame({
                    'Coloană': df.columns,
                    'Tip': df.dtypes.astype(str),
                    'Non-Null': df.count().values,
                    'Null': df.isnull().sum().values
                })
                st.dataframe(dtype_df, use_container_width=True)

            with col2:
                st.markdown("**Distribuția Tipurilor:**")
                type_counts = df.dtypes.astype(str).value_counts()
                fig = px.pie(
                    values=type_counts.values,
                    names=type_counts.index,
                    title="Tipuri de Date"
                )
                st.plotly_chart(fig, use_container_width=True)

        with tab3:
            st.markdown("### Statistici Descriptive")

            # Numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                st.markdown("**Coloane Numerice:**")
                st.dataframe(df[numeric_cols].describe(), use_container_width=True)

            # Categorical columns
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            if categorical_cols:
                st.markdown("**Coloane Categorice:**")
                cat_summary = pd.DataFrame({
                    col: [
                        df[col].nunique(),
                        df[col].mode()[0] if len(df[col].mode()) > 0 else None,
                        df[col].value_counts().iloc[0] if len(df[col]) > 0 else 0,
                        f"{(df[col].value_counts().iloc[0] / len(df) * 100):.1f}%" if len(df[col]) > 0 else "0%"
                    ] for col in categorical_cols
                }, index=['Valori Unice', 'Cel Mai Comun', 'Frecvență', 'Procent']).T
                st.dataframe(cat_summary, use_container_width=True)

        with tab4:
            st.markdown("### Vizualizare Valori Lipsă")

            missing = df.isnull().sum()
            missing_pct = (missing / len(df)) * 100
            missing_df = pd.DataFrame({
                'Coloană': missing.index,
                'Număr Lipsă': missing.values,
                'Procent': missing_pct.values
            }).sort_values('Număr Lipsă', ascending=False)

            cols_with_missing = missing_df[missing_df['Număr Lipsă'] > 0]

            if len(cols_with_missing) > 0:
                fig = px.bar(
                    cols_with_missing,
                    x='Coloană',
                    y='Procent',
                    title='Procentul Valorilor Lipsă pe Coloană',
                    text='Număr Lipsă'
                )
                fig.update_traces(textposition='outside')
                st.plotly_chart(fig, use_container_width=True)

                st.dataframe(cols_with_missing, use_container_width=True)
            else:
                st.success(" Nu există valori lipsă în dataset!")

            # Heatmap for missing values
            if len(cols_with_missing) > 0:
                st.markdown("### Heatmap Valori Lipsă (primele 50 rânduri)")
                colours = ['#ffff00', '#000099']  # yellow = missing, blue = present
                fig, ax = plt.subplots(figsize=(12, 8))
                sns.heatmap(df.head(50).isnull(), cmap=sns.color_palette(colours),
                            cbar=False, yticklabels=False, ax=ax)
                ax.set_title("Galben = Lipsă, Albastru = Prezent")
                st.pyplot(fig)

        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown(f"""
        ###  Date Încărcate cu Succes!

        Ai încărcat **{len(df):,} rânduri** și **{len(df.columns)} coloane** din colecția `{collection}`.

        Poți continua acum cu metodele de prelucrare a datelor în secțiunile următoare! 
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info(" Configurează conexiunea și apasă butonul 'Încarcă Date' pentru a începe!")


# Curățarea Datelor
def show_data_cleaning():
    st.markdown('<h1 class="main-header"> Curățarea Datelor</h1>', unsafe_allow_html=True)

    if 'df' not in st.session_state:
        st.warning("Te rog să încarci mai întâi datele din secțiunea 'Conexiune MongoDB'!")
        return

    df = st.session_state['df'].copy()

    st.markdown("""
    ## Metode de Curățare a Datelor

    Curățarea datelor include:
    1. **Eliminarea duplicatelor**
    2. **Tratarea valorilor lipsă**
    3. **Corectarea erorilor de date**
    """)

    # Eliminarea duplicatelor
    st.markdown('<div class="sub-header">Metoda 1: Eliminarea Duplicatelor</div>', unsafe_allow_html=True)

    with st.expander(" Teorie: drop_duplicates()", expanded=True):
        st.markdown("""
        ### DataFrame.drop_duplicates()

        Elimină rândurile duplicate din DataFrame.

        **Sintaxă:**
        ```python
        DataFrame.drop_duplicates(
            subset=None,      # Coloane de verificat
            keep='first',     # 'first', 'last', False
            inplace=False,    # Modifică DataFrame-ul original
            ignore_index=False # Resetează indexul
        )
        ```

        **Parametrii:**
        - `subset`: Coloane specifice de verificat (None = toate)
        - `keep='first'`: Păstrează prima apariție
        - `keep='last'`: Păstrează ultima apariție
        - `keep=False`: Elimină toate duplicatele
        - `inplace=True`: Modifică DataFrame-ul original

        **Exemplu:**
        ```python
        # Elimină duplicate pe toate coloanele
        df_clean = df.drop_duplicates()

        # Elimină duplicate doar pe coloana 'ID'
        df_clean = df.drop_duplicates(subset=['ID_CLIENT'])

        # Păstrează ultima apariție
        df_clean = df.drop_duplicates(subset=['ID_CLIENT'], keep='last')
        ```
        """)

    st.markdown("### Găsește și Elimină Duplicate")

    # Select columns for duplicate check
    all_cols = df.columns.tolist()
    default_cols = ['ID_CLIENT'] if 'ID_CLIENT' in all_cols else [all_cols[0]]

    duplicate_cols = st.multiselect(
        "Selectează coloanele pentru verificarea duplicatelor:",
        all_cols,
        default=default_cols
    )

    if duplicate_cols:
        # Find duplicates
        duplicates = df[df.duplicated(subset=duplicate_cols, keep=False)]
        n_duplicates = len(df[df.duplicated(subset=duplicate_cols)])

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(" Total Rânduri", len(df))

        with col2:
            st.metric(" Duplicate Găsite", n_duplicates)

        with col3:
            pct_dup = (n_duplicates / len(df) * 100) if len(df) > 0 else 0
            st.metric(" Procent Duplicate", f"{pct_dup:.2f}%")

        if n_duplicates > 0:
            st.warning(f"⚠ Găsite {n_duplicates} rânduri duplicate!")

            with st.expander(" Vezi Duplicate"):
                st.dataframe(duplicates.sort_values(by=duplicate_cols).head(20), use_container_width=True)

            # Options for handling duplicates
            keep_option = st.radio(
                "Ce apariție vrei să păstrezi?",
                ['first', 'last', False],
                format_func=lambda x: {
                    'first': 'Prima apariție',
                    'last': 'Ultima apariție',
                    False: 'Elimină toate (nu păstra nimic)'
                }[x],
                horizontal=True
            )

            if st.button(" Elimină Duplicate", type="primary"):
                df_clean = df.drop_duplicates(subset=duplicate_cols, keep=keep_option)
                n_removed = len(df) - len(df_clean)

                st.success(f" Eliminate {n_removed} rânduri duplicate!")
                st.metric(" Rânduri Rămase", len(df_clean))

                # Store cleaned data
                st.session_state['df_clean'] = df_clean

                # Show before/after
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Înainte:**")
                    st.dataframe(df.head(10), use_container_width=True)

                with col2:
                    st.markdown("**După:**")
                    st.dataframe(df_clean.head(10), use_container_width=True)

                # Code used
                with st.expander(" Cod Utilizat"):
                    st.code(f"""
import pandas as pd

# Găsește duplicate
duplicates = df[df.duplicated(subset={duplicate_cols}, keep=False)]
print(f"Găsite {{len(duplicates)}} duplicate")

# Elimină duplicate
df_clean = df.drop_duplicates(subset={duplicate_cols}, keep='{keep_option}')
print(f"Rămase {{len(df_clean)}} rânduri")
                    """, language="python")
        else:
            st.success(" Nu există duplicate în dataset!")

    # Tratarea valorilor lipsă
    st.markdown('<div class="sub-header">Metoda 2: Tratarea Valorilor Lipsă</div>', unsafe_allow_html=True)

    with st.expander(" Teorie: Metode de Tratare a Valorilor Lipsă", expanded=True):
        st.markdown("""
        ### Metode Disponibile

        #### 1. fillna() - Înlocuire cu Valoare
        ```python
        # Cu o valoare constantă
        df['col'].fillna(0)
        df['col'].fillna('MISSING')

        # Cu medie/mediană/mod
        df['col'].fillna(df['col'].mean())
        df['col'].fillna(df['col'].median())
        df['col'].fillna(df['col'].mode()[0])

        # Pentru tot DataFrame-ul
        df.fillna(df.mean())  # Media pentru numerice
        ```

        #### 2. interpolate() - Interpolare
        ```python
        df.interpolate(
            method='linear',        # Metodă interpolare
            axis=0,                 # 0=coloane, 1=rânduri
            limit=None,             # Nr max NaN-uri consecutive
            limit_direction='forward' # Direcție: forward, backward, both
        )
        ```

        **Metode de interpolare:**
        - `linear`: Interpolare liniară (default)
        - `polynomial`: Interpolare polinomială
        - `spline`: Spline
        - `time`: Pentru date temporale
        - `pad`: Forward fill
        - `backfill`: Backward fill

        #### 3. dropna() - Eliminare
        ```python
        # Elimină rânduri cu orice NaN
        df.dropna()

        # Elimină doar dacă TOATE valorile sunt NaN
        df.dropna(how='all')

        # Elimină dacă minimum X valori non-NaN
        df.dropna(thresh=5)

        # Elimină coloane cu NaN
        df.dropna(axis=1)
        ```

        ### Strategii Recomandate

        | Situație | Metodă Recomandată |
        |----------|-------------------|
        | < 5% lipsă | Eliminare (dropna) |
        | 5-30% lipsă, numeric | Medie/Mediană |
        | 5-30% lipsă, categoric | Mod (cel mai frecvent) |
        | > 30% lipsă | Valoare specială ('MISSING') sau eliminare coloană |
        | Date temporale | Interpolare |
        """)

    st.markdown("### Analizează și Tratează Valorile Lipsă")
    df.dropna()
    # Analyze missing values
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    missing_df = pd.DataFrame({
        'Coloană': missing.index,
        'Număr Lipsă': missing.values,
        'Procent': missing_pct.values,
        'Tip': df.dtypes.values
    }).sort_values('Număr Lipsă', ascending=False)

    cols_with_missing = missing_df[missing_df['Număr Lipsă'] > 0]

    if len(cols_with_missing) > 0:
        st.markdown("### Coloane cu Valori Lipsă")
        st.dataframe(cols_with_missing, use_container_width=True)

        # Visualize
        fig = px.bar(
            cols_with_missing,
            x='Coloană',
            y='Procent',
            color='Tip',
            title='Valori Lipsă pe Coloană',
            text='Număr Lipsă'
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

        # Treatment options
        st.markdown("### Selectează Metoda de Tratare")

        col_to_treat = st.selectbox(
            "Selectează coloana de tratat:",
            cols_with_missing['Coloană'].tolist()
        )

        col_type = df[col_to_treat].dtype
        is_numeric = np.issubdtype(col_type, np.number)

        # Different strategies based on type
        if is_numeric:
            strategy = st.radio(
                "Alege strategia:",
                ['mean', 'median', 'constant', 'interpolate', 'drop'],
                format_func=lambda x: {
                    'mean': ' Medie',
                    'median': ' Mediană',
                    'constant': ' Valoare Constantă',
                    'interpolate': ' Interpolare',
                    'drop': ' Elimină Rânduri'
                }[x],
                horizontal=True
            )

            if strategy == 'constant':
                fill_value = st.number_input("Valoarea de înlocuire:", value=0.0)
            elif strategy == 'interpolate':
                interp_method = st.selectbox(
                    "Metodă interpolare:",
                    ['linear', 'polynomial', 'spline'],
                    help="Linear = cel mai comun"
                )
        else:
            strategy = st.radio(
                "Alege strategia:",
                ['mode', 'constant', 'drop'],
                format_func=lambda x: {
                    'mode': 'Mod (Cel mai frecvent)',
                    'constant': ' Valoare Constantă',
                    'drop': ' Elimină Rânduri'
                }[x],
                horizontal=True
            )

            if strategy == 'constant':
                fill_value = st.text_input("Valoarea de înlocuire:", value="_MISSING_")

        if st.button(" Aplică ", type="primary"):
            df_treated = df.copy()

            try:
                if strategy == 'mean':
                    fill_val = df_treated[col_to_treat].mean()
                    df_treated[col_to_treat].fillna(fill_val, inplace=True)
                    st.success(f" Înlocuite cu media: {fill_val:.2f}")

                elif strategy == 'median':
                    fill_val = df_treated[col_to_treat].median()
                    df_treated[col_to_treat].fillna(fill_val, inplace=True)
                    st.success(f" Înlocuite cu mediana: {fill_val:.2f}")

                elif strategy == 'mode':
                    fill_val = df_treated[col_to_treat].mode()[0]
                    df_treated[col_to_treat].fillna(fill_val, inplace=True)
                    st.success(f" Înlocuite cu modul: {fill_val}")

                elif strategy == 'constant':
                    df_treated[col_to_treat].fillna(fill_value, inplace=True)
                    st.success(f"Înlocuite cu: {fill_value}")

                elif strategy == 'interpolate':
                    df_treated[col_to_treat].interpolate(
                        method=interp_method,
                        limit_direction='both',
                        inplace=True
                    )
                    st.success(f" Aplicată interpolare {interp_method}")

                elif strategy == 'drop':
                    df_treated.dropna(subset=[col_to_treat], inplace=True)
                    n_dropped = len(df) - len(df_treated)
                    st.success(f" Eliminate {n_dropped} rânduri")

                # Store treated data
                st.session_state['df_treated'] = df_treated

                # Show results
                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Înainte - Valori Lipsă", df[col_to_treat].isnull().sum())

                with col2:
                    st.metric("După - Valori Lipsă", df_treated[col_to_treat].isnull().sum())

                # Show sample
                with st.expander(" Vezi Modificările"):
                    comparison_df = pd.DataFrame({
                        'Înainte': df[col_to_treat].head(20),
                        'După': df_treated[col_to_treat].head(20)
                    })
                    st.dataframe(comparison_df, use_container_width=True)

                # Show code
                with st.expander(" Cod Utilizat"):
                    if strategy == 'mean':
                        code = f"""
import pandas as pd
import numpy as np

# Înlocuire cu media
fill_value = df['{col_to_treat}'].mean()
df['{col_to_treat}'].fillna(fill_value, inplace=True)
                        """
                    elif strategy == 'median':
                        code = f"""
import pandas as pd
import numpy as np

# Înlocuire cu mediana
fill_value = df['{col_to_treat}'].median()
df['{col_to_treat}'].fillna(fill_value, inplace=True)
                        """
                    elif strategy == 'mode':
                        code = f"""
import pandas as pd

# Înlocuire cu modul (cel mai frecvent)
fill_value = df['{col_to_treat}'].mode()[0]
df['{col_to_treat}'].fillna(fill_value, inplace=True)
                        """
                    elif strategy == 'constant':
                        code = f"""
import pandas as pd

# Înlocuire cu valoare constantă
df['{col_to_treat}'].fillna({repr(fill_value)}, inplace=True)
                        """
                    elif strategy == 'interpolate':
                        code = f"""
import pandas as pd

# Interpolare
df['{col_to_treat}'].interpolate(
    method='{interp_method}',
    limit_direction='both',
    inplace=True
)
                        """
                    else:  # drop
                        code = f"""
import pandas as pd

# Elimină rânduri cu NaN
df.dropna(subset=['{col_to_treat}'], inplace=True)
                        """

                    st.code(code, language="python")

            except Exception as e:
                st.error(f" Eroare: {str(e)}")

    else:
        st.success(" Nu există valori lipsă în dataset!")

    # Tratare completă (toate coloanele)
    st.markdown("### Tratare Automată pentru Toate Coloanele")

    with st.expander("Aplică Strategie Globală"):
        st.markdown("""
        Aplică o strategie de tratare pentru toate coloanele cu valori lipsă simultan.
        """)

        global_strategy = st.radio(
            "Strategie globală:",
            ['smart', 'drop_rows', 'drop_cols'],
            format_func=lambda x: {
                'smart': ' Smart (Medie pt numeric, Mod pt categoric)',
                'drop_rows': ' Elimină Rânduri cu NaN',
                'drop_cols': 'Elimină Coloane cu > 30% NaN'
            }[x]
        )

        if st.button(" Aplică Tratare Globală", type="primary"):
            df_global = df.copy()

            if global_strategy == 'smart':
                # Numeric columns - mean
                numeric_cols = df_global.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    if df_global[col].isnull().sum() > 0:
                        df_global[col].fillna(df_global[col].mean(), inplace=True)

                # Categorical columns - mode
                cat_cols = df_global.select_dtypes(include=['object']).columns
                for col in cat_cols:
                    if df_global[col].isnull().sum() > 0:
                        mode_val = df_global[col].mode()[0] if len(df_global[col].mode()) > 0 else 'MISSING'
                        df_global[col].fillna(mode_val, inplace=True)

                st.success("Aplicată")

            elif global_strategy == 'drop_rows':
                df_global.dropna(inplace=True)
                n_dropped = len(df) - len(df_global)
                st.success(f" Eliminate {n_dropped} rânduri!")

            else:  # drop_cols
                threshold = 0.3
                for col in df_global.columns:
                    if (df_global[col].isnull().sum() / len(df_global)) > threshold:
                        df_global.drop(columns=[col], inplace=True)
                n_dropped_cols = len(df.columns) - len(df_global.columns)
                st.success(f" Eliminate {n_dropped_cols} coloane!")

            # Store and show results
            st.session_state['df_global_clean'] = df_global

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Înainte - Total NaN", df.isnull().sum().sum())
                st.metric("Înainte - Dimensiune", f"{df.shape[0]} × {df.shape[1]}")

            with col2:
                st.metric("După - Total NaN", df_global.isnull().sum().sum())
                st.metric("După - Dimensiune", f"{df_global.shape[0]} × {df_global.shape[1]}")

            with st.expander(" Cod Utilizat"):
                if global_strategy == 'smart':
                    code = """
import pandas as pd
import numpy as np

# Tratare smart
# Numeric: înlocuire cu media
numeric_cols = df.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    if df[col].isnull().sum() > 0:
        df[col].fillna(df[col].mean(), inplace=True)

# Categoric: înlocuire cu modul
cat_cols = df.select_dtypes(include=['object']).columns
for col in cat_cols:
    if df[col].isnull().sum() > 0:
        df[col].fillna(df[col].mode()[0], inplace=True)
                    """
                elif global_strategy == 'drop_rows':
                    code = """
import pandas as pd

# Elimină toate rândurile cu NaN
df.dropna(inplace=True)
                    """
                else:
                    code = """
import pandas as pd

# Elimină coloanele cu > 30% NaN
threshold = 0.3
for col in df.columns:
    if (df[col].isnull().sum() / len(df)) > threshold:
        df.drop(columns=[col], inplace=True)
                    """

                st.code(code, language="python")



def show_outlier_detection():
    st.markdown('<h1 class="main-header"> Detectarea Valorilor Anormale (Outlieri)</h1>', unsafe_allow_html=True)

    if 'df' not in st.session_state:
        st.warning("Te rog să încarci mai întâi datele din secțiunea 'Conexiune MongoDB'!")
        return

    df = st.session_state['df'].copy()
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if not numeric_cols:
        st.error("Nu există coloane numerice în dataset!")
        return

    st.markdown("""
    ## Detectarea și Tratarea Outlierilor

    **Outlierii** sunt valori care diferă semnificativ de restul datelor.
    Pot fi:
    - Erori de măsurare sau introducere
    - Valori extreme valide
    - Indicatori ai unor fenomene rare
    """)

    st.markdown('<div class="sub-header">Metoda 1: Analiză cu Histogramă</div>', unsafe_allow_html=True)

    with st.expander(" Teorie: Histograme pentru Outlieri", expanded=False):
        st.markdown("""
        ### Histograme

        Histogramele arată distribuția valorilor și ajută la identificarea vizuală a outlierilor.

        ```python
        # Histogramă simplă
        df['column'].hist(bins=100)
        plt.show()

        # Cu pandas
        df['column'].plot(kind='hist', bins=50, edgecolor='black')
        ```

        **Ce să cauți:**
        - Valori izolate departe de distribuția principală
        - Distribuții bimodale (două vârfuri)
        - Cozi lungi (long tail)
        """)

    col_for_hist = st.selectbox("Selectează coloana pentru histogramă:", numeric_cols, key="hist_col")

    col1, col2 = st.columns([2, 1])

    with col1:
        fig = px.histogram(
            df,
            x=col_for_hist,
            nbins=50,
            title=f'Histogramă: {col_for_hist}',
            marginal='box'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Statistici")
        stats_df = pd.DataFrame({
            'Metrică': ['Minim', 'Q1 (25%)', 'Mediană', 'Q3 (75%)', 'Maxim', 'Media', 'Std Dev'],
            'Valoare': [
                df[col_for_hist].min(),
                df[col_for_hist].quantile(0.25),
                df[col_for_hist].median(),
                df[col_for_hist].quantile(0.75),
                df[col_for_hist].max(),
                df[col_for_hist].mean(),
                df[col_for_hist].std()
            ]
        })
        st.dataframe(stats_df, use_container_width=True)

    st.markdown('<div class="sub-header">Metoda 2: Box Plot</div>', unsafe_allow_html=True)

    with st.expander(" Teorie: Box Plot și IQR", expanded=False):
        st.markdown("""
        ### Box Plot (Diagramă Cutie)

        Box plot-ul arată distribuția datelor folosind cuartile și identifică outlierii.

        **Componente:**
        - **Cutia**: Conține 50% din date (Q1 la Q3)
        - **Linia din cutie**: Mediana (Q2)
        - **Mustățile**: Se extind până la 1.5 × IQR
        - **Puncte izolate**: Outlieri (peste mustăți)

        **IQR (Interquartile Range)**:
        ```
        IQR = Q3 - Q1
        Lower fence = Q1 - 1.5 × IQR
        Upper fence = Q3 + 1.5 × IQR
        ```

        **Cod Python:**
        ```python
        # Box plot simplu
        df.boxplot(column='col_name')

        # Identifică outlieri
        Q1 = df['col'].quantile(0.25)
        Q3 = df['col'].quantile(0.75)
        IQR = Q3 - Q1

        lower_fence = Q1 - 1.5 * IQR
        upper_fence = Q3 + 1.5 * IQR

        outliers = df[(df['col'] < lower_fence) | (df['col'] > upper_fence)]
        ```
        """)

    col_for_box = st.selectbox("Selectează coloana pentru box plot:", numeric_cols, key="box_col")

    # Calculate IQR and outliers
    Q1 = df[col_for_box].quantile(0.25)
    Q3 = df[col_for_box].quantile(0.75)
    IQR = Q3 - Q1
    lower_fence = Q1 - 1.5 * IQR
    upper_fence = Q3 + 1.5 * IQR

    outliers = df[(df[col_for_box] < lower_fence) | (df[col_for_box] > upper_fence)]
    n_outliers = len(outliers)
    pct_outliers = (n_outliers / len(df) * 100) if len(df) > 0 else 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(" Total Valori", len(df))

    with col2:
        st.metric("Outlieri Găsiți", n_outliers)

    with col3:
        st.metric(" Procent Outlieri", f"{pct_outliers:.2f}%")

    # Box plot
    fig = px.box(
        df,
        y=col_for_box,
        points='outliers',
        title=f'Box Plot: {col_for_box}'
    )
    fig.add_hline(y=lower_fence, line_dash="dash", line_color="red", annotation_text="Lower Fence")
    fig.add_hline(y=upper_fence, line_dash="dash", line_color="red", annotation_text="Upper Fence")
    st.plotly_chart(fig, use_container_width=True)

    if n_outliers > 0:
        with st.expander(" Vezi Outlierii"):
            st.dataframe(outliers[[col_for_box]].describe(), use_container_width=True)
            st.dataframe(outliers.head(20), use_container_width=True)

    st.markdown('<div class="sub-header">Metoda 3: Detectare cu Quantile</div>', unsafe_allow_html=True)

    with st.expander("Teorie: Metoda Quantilelor", expanded=False):
        st.markdown("""
        ### Detectare cu Quantile

        Elimină valorile extreme bazate pe percentile.

        **Cod:**
        ```python
        # Definește praguri (de ex. 1% și 99%)
        q_low = df['col'].quantile(0.01)
        q_high = df['col'].quantile(0.99)

        # Filtrează
        df_filtered = df[(df['col'] >= q_low) & (df['col'] <= q_high)]
        ```

        **Avantaje:**
        - Simplu de implementat
        - Control exact asupra procentului eliminat
        - Nu presupune distribuție normală

        **Dezavantaje:**
        - Elimină automat un procent fix
        - Poate elimina valori valide
        """)

    col1, col2 = st.columns(2)

    with col1:
        q_low_pct = st.slider("Quantila inferioară (%):", 0.0, 10.0, 1.0, 0.5)

    with col2:
        q_high_pct = st.slider("Quantila superioară (%):", 90.0, 100.0, 99.0, 0.5)

    col_for_quantile = st.selectbox("Selectează coloana:", numeric_cols, key="quantile_col")

    q_low = df[col_for_quantile].quantile(q_low_pct / 100)
    q_high = df[col_for_quantile].quantile(q_high_pct / 100)

    df_filtered = df[(df[col_for_quantile] >= q_low) & (df[col_for_quantile] <= q_high)]
    n_removed = len(df) - len(df_filtered)

    st.info(f"""
    **Praguri:**
    - Quantila {q_low_pct}%: {q_low:.2f}
    - Quantila {q_high_pct}%: {q_high:.2f}

    **Rezultat:** {n_removed} valori vor fi eliminate ({(n_removed / len(df) * 100):.2f}%)
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Înainte Filtrare")
        fig1 = px.box(df, y=col_for_quantile, title="Original")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("### După Filtrare")
        fig2 = px.box(df_filtered, y=col_for_quantile, title="Filtrat")
        st.plotly_chart(fig2, use_container_width=True)

    if st.button(" Aplică Filtrare Quantile", type="primary"):
        st.session_state['df_filtered'] = df_filtered
        st.success(f" Eliminate {n_removed} valori outlier!")

        with st.expander("    Cod Utilizat"):
            st.code(f"""
import pandas as pd

# Definește quantilele
q_low = df['{col_for_quantile}'].quantile({q_low_pct / 100})
q_high = df['{col_for_quantile}'].quantile({q_high_pct / 100})

# Filtrează datele
df_filtered = df[(df['{col_for_quantile}'] >= q_low) & 
                 (df['{col_for_quantile}'] <= q_high)]

print(f"Înainte: {{len(df)}} rânduri")
print(f"După: {{len(df_filtered)}} rânduri")
print(f"Eliminate: {{len(df) - len(df_filtered)}} rânduri")
            """, language="python")

    st.markdown('<div class="sub-header">Metoda 4: Variabile Categorice</div>', unsafe_allow_html=True)

    cat_cols = df.select_dtypes(include=['object']).columns.tolist()

    if cat_cols:
        with st.expander(" Teorie: Outlieri în Date Categorice"):
            st.markdown("""
            ### Detectare Outlieri în Date Categorice

            Pentru variabile categorice, "outlierii" sunt categorii cu frecvență foarte mică.

            **Cod:**
            ```python
            # Numără frecvențele
            value_counts = df['categorie'].value_counts()

            # Vizualizează
            value_counts.plot(kind='bar')

            # Găsește categorii rare (< 1%)
            threshold = len(df) * 0.01
            rare_categories = value_counts[value_counts < threshold]
            ```
            """)

        cat_col = st.selectbox("Selectează coloana categorică:", cat_cols, key="cat_col")

        value_counts = df[cat_col].value_counts()
        value_counts_pct = (value_counts / len(df) * 100).round(2)

        fig = px.bar(
            x=value_counts.index,
            y=value_counts.values,
            labels={'x': cat_col, 'y': 'Frecvență'},
            title=f'Distribuția Categoriilor: {cat_col}',
            text=value_counts.values
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

        # Show frequency table
        freq_df = pd.DataFrame({
            'Categorie': value_counts.index,
            'Frecvență': value_counts.values,
            'Procent': value_counts_pct.values
        })
        st.dataframe(freq_df, use_container_width=True)

        # Identify rare categories
        threshold_pct = st.slider("Prag pentru categorii rare (%):", 0.1, 10.0, 1.0, 0.1)
        threshold_count = len(df) * (threshold_pct / 100)

        rare_cats = value_counts[value_counts < threshold_count]

        if len(rare_cats) > 0:
            st.warning(f" Găsite {len(rare_cats)} categorii rare (< {threshold_pct}%)")
            st.dataframe(pd.DataFrame({
                'Categorie Rară': rare_cats.index,
                'Frecvență': rare_cats.values
            }), use_container_width=True)



def show_string_processing():
    st.markdown('<h1 class="main-header">Prelucrarea Șirurilor de Caractere</h1>', unsafe_allow_html=True)

    if 'df' not in st.session_state:
        st.warning(" Te rog să încarci mai întâi datele din secțiunea 'Conexiune MongoDB'!")
        return

    df = st.session_state['df'].copy()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()

    if not cat_cols:
        st.error("Nu există coloane text în dataset!")
        return

    st.markdown("""
    ## Metode de Prelucrare a Textului

    Prelucrarea șirurilor include:
    1. **Curățare și standardizare** - lowercase, strip, replace
    2. **Filtrare** - păstrarea doar anumitor valori
    3. **Transformare** - encoding în valori numerice
    """)

    st.markdown('<div class="sub-header">Metoda 1: Filtrarea Valorilor</div>', unsafe_allow_html=True)

    with st.expander(" Teorie: Filtrare cu isin()", expanded=False):
        st.markdown("""
        ### Filtrarea Valorilor din Liste

        Metoda `isin()` verifică dacă valorile dintr-o coloană se regăsesc într-o listă.

        **Sintaxă:**
        ```python
        # Verifică apartenența
        df['col'].isin(lista_valori)  # Returnează boolean Series

        # Filtrează DataFrame-ul
        df_filtered = df[df['col'].isin(lista_valori)]

        # Filtrare cu lowercase
        df_filtered = df[df['col'].str.lower().isin(lista_valori)]
        ```

        **Exemplu:**
        ```python
        # Listă profesii acceptate
        profesii_valide = ['medic', 'inginer', 'profesor']

        # Filtrează doar aceste profesii
        df_filtrat = df[df['PROFESIA'].str.lower().isin(profesii_valide)]

        # SAU: Marchează restul ca "ALTA PROFESIE"
        df['CATEGORIE'] = df['PROFESIA'].where(
            df['PROFESIA'].str.lower().isin(profesii_valide),
            'ALTA PROFESIE'
        )
        ```
        """)

    st.markdown("### Exemplu: Filtrarea Profesiilor")

    # Exemplu cu PROFESIA dacă există
    if 'PROFESIA' in cat_cols:
        col_to_filter = 'PROFESIA'
    else:
        col_to_filter = st.selectbox("Selectează coloana text:", cat_cols, key="filter_col")

    # Show current distribution
    st.markdown(f"### Distribuția Curentă: {col_to_filter}")

    value_counts = df[col_to_filter].value_counts()

    fig = px.bar(
        x=value_counts.index,
        y=value_counts.values,
        title=f'Frecvența Valorilor din {col_to_filter}',
        labels={'x': col_to_filter, 'y': 'Frecvență'},
        text=value_counts.values
    )
    fig.update_traces(textposition='outside')
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

    # Define valid values
    st.markdown("### Definește Valori Valide")

    unique_vals = df[col_to_filter].dropna().unique().tolist()

    # Preset lists for common columns
    if col_to_filter == 'PROFESIA':
        default_list = ['muncitor necalificat', 'profesor', 'agricultor',
                        'asistent medical', 'barman', 'economist', 'inginer',
                        'medic', 'pensionar']
    else:
        default_list = unique_vals[:5] if len(unique_vals) >= 5 else unique_vals

    valid_values = st.multiselect(
        "Selectează valorile valide:",
        options=unique_vals,
        default=[v for v in default_list if v in unique_vals]
    )

    if valid_values:
        col1, col2 = st.columns(2)

        with col1:
            filter_method = st.radio(
                "Metodă de filtrare:",
                ['keep_only', 'mark_other'],
                format_func=lambda x: {
                    'keep_only': ' Păstrează Doar Valorile Valide',
                    'mark_other': ' Marchează Restul ca "ALTA CATEGORIE"'
                }[x]
            )

        with col2:
            case_sensitive = st.checkbox("Case sensitive", value=False)

        if st.button("  Aplică Filtrarea", type="primary"):
            df_filtered = df.copy()

            # Prepare comparison
            if case_sensitive:
                mask = df_filtered[col_to_filter].isin(valid_values)
            else:
                valid_lower = [v.lower() for v in valid_values]
                mask = df_filtered[col_to_filter].str.lower().isin(valid_lower)

            if filter_method == 'keep_only':
                df_filtered = df_filtered[mask]
                n_removed = len(df) - len(df_filtered)
                st.success(f"   Păstrate {len(df_filtered)} rânduri, eliminate {n_removed}")
            else:
                # Create new column with category
                new_col = f'{col_to_filter}_CATEGORIE'
                df_filtered[new_col] = df_filtered[col_to_filter].where(mask, 'ALTA CATEGORIE')
                st.success(f"   Creată coloana nouă: {new_col}")

            # Store result
            st.session_state['df_filtered_text'] = df_filtered

            # Show results
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Înainte")
                st.dataframe(df[col_to_filter].value_counts().head(10), use_container_width=True)

                fig1 = px.bar(
                    x=df[col_to_filter].value_counts().head(10).index,
                    y=df[col_to_filter].value_counts().head(10).values,
                    title="Distribuție Originală"
                )
                st.plotly_chart(fig1, use_container_width=True)

            with col2:
                st.markdown("### După")
                if filter_method == 'keep_only':
                    st.dataframe(df_filtered[col_to_filter].value_counts(), use_container_width=True)

                    fig2 = px.bar(
                        x=df_filtered[col_to_filter].value_counts().index,
                        y=df_filtered[col_to_filter].value_counts().values,
                        title="Distribuție Filtrată"
                    )
                else:
                    new_col = f'{col_to_filter}_CATEGORIE'
                    st.dataframe(df_filtered[new_col].value_counts(), use_container_width=True)

                    fig2 = px.bar(
                        x=df_filtered[new_col].value_counts().index,
                        y=df_filtered[new_col].value_counts().values,
                        title="Distribuție cu Categorii"
                    )

                st.plotly_chart(fig2, use_container_width=True)

            # Show code
            with st.expander("    Cod Utilizat"):
                if filter_method == 'keep_only':
                    if case_sensitive:
                        code = f"""
import pandas as pd

# Definește lista de valori valide
valid_values = {valid_values}

# Filtrează
df_filtered = df[df['{col_to_filter}'].isin(valid_values)]

print(f"Înainte: {{len(df)}} rânduri")
print(f"După: {{len(df_filtered)}} rânduri")
                        """
                    else:
                        code = f"""
import pandas as pd

# Definește lista de valori valide (lowercase)
valid_values = {[v.lower() for v in valid_values]}

# Filtrează cu lowercase
df_filtered = df[df['{col_to_filter}'].str.lower().isin(valid_values)]

print(f"Înainte: {{len(df)}} rânduri")
print(f"După: {{len(df_filtered)}} rânduri")
                        """
                else:
                    new_col = f'{col_to_filter}_CATEGORIE'
                    if case_sensitive:
                        code = f"""
import pandas as pd

# Definește lista de valori valide
valid_values = {valid_values}

# Creează coloană nouă
df['{new_col}'] = df.loc[
    df['{col_to_filter}'].isin(valid_values),
    '{col_to_filter}'
]

# Înlocuiește restul cu 'ALTA CATEGORIE'
df['{new_col}'] = df['{new_col}'].fillna('ALTA CATEGORIE')
                        """
                    else:
                        code = f"""
import pandas as pd

# Definește lista de valori valide (lowercase)
valid_values = {[v.lower() for v in valid_values]}

# Creează coloană nouă
df['{new_col}'] = df.loc[
    df['{col_to_filter}'].str.lower().isin(valid_values),
    '{col_to_filter}'
]

# Înlocuiește restul cu 'ALTA CATEGORIE'
df['{new_col}'] = df['{new_col}'].fillna('ALTA CATEGORIE')
                        """

                st.code(code, language="python")

    st.markdown('<div class="sub-header">Metoda 2: Label Encoding</div>', unsafe_allow_html=True)

    with st.expander("Teorie: LabelEncoder", expanded=False):
        st.markdown("""
        ### Transformarea Categoriilor în Numere

        **LabelEncoder** din sklearn transformă categorii text în valori numerice (0, 1, 2, ...).

        **Când să folosești:**
        - Pentru algoritmi ML care necesită input numeric
        - Pentru variabile ordinale (cu ordine naturală)

        **Cod:**
        ```python
        from sklearn.preprocessing import LabelEncoder

        # Creează encoder
        le = LabelEncoder()

        # Transformă
        df['col_encoded'] = le.fit_transform(df['col'].astype(str))

        # Vezi maparea
        mapping = dict(zip(le.classes_, le.transform(le.classes_)))
        print(mapping)
        # {'categorie1': 0, 'categorie2': 1, 'categorie3': 2}
        ```

        **Exemplu:**
        ```python
        # Date originale
        df['STARE_CIVILA'] = ['casatorit', 'necasatorit', 'casatorit', 'divortat']

        # După encoding
        df['STARE_CIVILA_ENCODED'] = [0, 2, 0, 1]
        # casatorit=0, divortat=1, necasatorit=2 (alfabetic)
        ```

        **IMPORTANT:** LabelEncoder sortează alfabetic categoriile!
        """)

    st.markdown("### Transformă Categorii în Numere")

    cols_to_encode = st.multiselect(
        "Selectează coloanele de transformat:",
        cat_cols,
        default=cat_cols[:2] if len(cat_cols) >= 2 else cat_cols
    )

    if cols_to_encode and st.button(" Aplică Label Encoding", type="primary"):
        df_encoded = df.copy()

        mappings = {}

        for col in cols_to_encode:
            le = LabelEncoder()
            df_encoded[f'{col}_ENCODED'] = le.fit_transform(df_encoded[col].astype(str))

            # Store mapping
            mappings[col] = dict(zip(le.classes_, le.transform(le.classes_)))

        st.session_state['df_encoded'] = df_encoded
        st.success(f"   Transformate {len(cols_to_encode)} coloane!")

        # Show results
        for col in cols_to_encode:
            with st.expander(f"      Mapare: {col}"):
                st.markdown(f"### {col} → {col}_ENCODED")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Original:**")
                    st.dataframe(df[col].value_counts(), use_container_width=True)

                with col2:
                    st.markdown("**Encoded:**")
                    mapping_df = pd.DataFrame({
                        'Categorie': list(mappings[col].keys()),
                        'Cod': list(mappings[col].values())
                    }).sort_values('Cod')
                    st.dataframe(mapping_df, use_container_width=True)

                # Sample comparison
                st.markdown("**Exemplu Transformare:**")
                sample_df = pd.DataFrame({
                    'Original': df[col].head(10),
                    'Encoded': df_encoded[f'{col}_ENCODED'].head(10)
                })
                st.dataframe(sample_df, use_container_width=True)

        # Show code
        with st.expander("    Cod Utilizat"):
            code = f"""
from sklearn.preprocessing import LabelEncoder
import pandas as pd

# Creează encoder pentru fiecare coloană
"""
            for col in cols_to_encode:
                code += f"""
# Transformă {col}
le_{col.lower()} = LabelEncoder()
df['{col}_ENCODED'] = le_{col.lower()}.fit_transform(df['{col}'].astype(str))

# Vezi maparea
mapping = dict(zip(le_{col.lower()}.classes_, 
                  le_{col.lower()}.transform(le_{col.lower()}.classes_)))
print(f"{col} mapping: {{mapping}}")
"""

            st.code(code, language="python")

    st.markdown('<div class="sub-header">Metoda 3: Discretizare (Binning)</div>', unsafe_allow_html=True)

    with st.expander("Teorie: pd.cut() și pd.qcut()", expanded=False):
        st.markdown("""
        ### Transformarea Variabilelor Continue în Discrete

        #### pd.cut() - Bins de Lățime Egală

        Împarte datele în intervale de lățime egală.

        ```python
        # Împarte în 5 bins egale
        df['col_binned'] = pd.cut(df['col'], bins=5)

        # Bins custom
        df['col_binned'] = pd.cut(
            df['col'],
            bins=[0, 25, 50, 75, 100],
            labels=['Scăzut', 'Mediu', 'Ridicat', 'Foarte Ridicat']
        )

        # Cu labels numeric
        df['col_binned'] = pd.cut(df['col'], bins=10, labels=False)
        ```

        #### pd.qcut() - Bins de Frecvență Egală (Quantile-based)

        Împarte datele astfel încât fiecare bin să conțină aproximativ același număr de observații.

        ```python
        # Împarte în 4 quartile
        df['col_quartile'] = pd.qcut(df['col'], q=4)

        # Cu labels custom
        df['col_quartile'] = pd.qcut(
            df['col'],
            q=4,
            labels=['Q1', 'Q2', 'Q3', 'Q4']
        )

        # Cu labels numeric
        df['col_quartile'] = pd.qcut(df['col'], q=10, labels=False)
        ```

        ### Diferența dintre cut() și qcut():

        - **cut()**: Intervale de aceeași lățime → Bins pot avea frecvențe diferite
        - **qcut()**: Fiecare bin are ~același număr de elemente → Intervale de lățimi diferite

        **Exemplu:**
        ```python
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100]

        # cut() - lățime egală
        # Bins: [1-33], [33-66], [66-100]
        # Majoritatea în primul bin!

        # qcut() - frecvență egală
        # Bins: [1-3.67], [3.67-6.33], [6.33-100]
        # ~3-4 elemente per bin
        ```
        """)

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if numeric_cols:
        st.markdown("### Discretizează Variabilă Continuă")

        col_to_bin = st.selectbox("Selectează coloana numerică:", numeric_cols, key="bin_col")

        col1, col2 = st.columns(2)

        with col1:
            bin_method = st.radio(
                "Metodă:",
                ['cut', 'qcut'],
                format_func=lambda x: {
                    'cut': ' cut() - Lățime Egală',
                    'qcut': ' qcut() - Frecvență Egală'
                }[x]
            )

        with col2:
            n_bins = st.slider("Număr bins:", 2, 20, 5)

        use_labels = st.checkbox("Folosește labels custom", value=False)

        if use_labels:
            labels_input = st.text_input(
                "Labels (separate prin virgulă):",
                value=f"{','.join([f'Bin_{i + 1}' for i in range(n_bins)])}"
            )
            labels = [l.strip() for l in labels_input.split(',')]

            if len(labels) != n_bins:
                st.error(f" Trebuie {n_bins} labels, ai furnizat {len(labels)}")
                labels = False
        else:
            labels = False

        if st.button(" Aplică Discretizarea", type="primary"):
            df_binned = df.copy()

            try:
                if bin_method == 'cut':
                    df_binned[f'{col_to_bin}_BINNED'] = pd.cut(
                        df_binned[col_to_bin],
                        bins=n_bins,
                        labels=labels
                    )
                else:
                    df_binned[f'{col_to_bin}_BINNED'] = pd.qcut(
                        df_binned[col_to_bin],
                        q=n_bins,
                        labels=labels,
                        duplicates='drop'
                    )

                st.session_state['df_binned'] = df_binned
                st.success("   Discretizare aplicată!")

                # Show results
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### Histogramă Originală")
                    fig1 = px.histogram(df, x=col_to_bin, nbins=50)
                    st.plotly_chart(fig1, use_container_width=True)

                    st.metric("Valori Unice", df[col_to_bin].nunique())

                with col2:
                    st.markdown("### Distribuție Bins")
                    bin_counts = df_binned[f'{col_to_bin}_BINNED'].value_counts().sort_index()

                    fig2 = px.bar(
                        x=bin_counts.index.astype(str),
                        y=bin_counts.values,
                        labels={'x': 'Bin', 'y': 'Frecvență'},
                        text=bin_counts.values
                    )
                    fig2.update_traces(textposition='outside')
                    st.plotly_chart(fig2, use_container_width=True)

                    st.metric("Bins Create", df_binned[f'{col_to_bin}_BINNED'].nunique())

                # Show mapping
                with st.expander("      Mapping Bins"):
                    mapping_df = df_binned[[col_to_bin, f'{col_to_bin}_BINNED']].drop_duplicates().sort_values(
                        col_to_bin)
                    st.dataframe(mapping_df.head(20), use_container_width=True)

                # Show code
                with st.expander("    Cod Utilizat"):
                    if bin_method == 'cut':
                        if labels:
                            code = f"""
import pandas as pd

# Discretizare cu cut() și labels custom
labels = {labels}
df['{col_to_bin}_BINNED'] = pd.cut(
    df['{col_to_bin}'],
    bins={n_bins},
    labels=labels
)
                            """
                        else:
                            code = f"""
import pandas as pd

# Discretizare cu cut() și labels numerice
df['{col_to_bin}_BINNED'] = pd.cut(
    df['{col_to_bin}'],
    bins={n_bins},
    labels=False
)
                            """
                    else:  # qcut
                        if labels:
                            code = f"""
import pandas as pd

# Discretizare cu qcut() și labels custom
labels = {labels}
df['{col_to_bin}_BINNED'] = pd.qcut(
    df['{col_to_bin}'],
    q={n_bins},
    labels=labels,
    duplicates='drop'
)
                            """
                        else:
                            code = f"""
import pandas as pd

# Discretizare cu qcut() și labels numerice
df['{col_to_bin}_BINNED'] = pd.qcut(
    df['{col_to_bin}'],
    q={n_bins},
    labels=False,
    duplicates='drop'
)
                            """

                    st.code(code, language="python")

            except Exception as e:
                st.error(f" Eroare: {str(e)}")
                st.info(" Încearcă să reduci numărul de bins sau folosește qcut cu duplicates='drop'")


def show_standardization():
    st.markdown('<h1 class="main-header">      Standardizare și Normalizare</h1>', unsafe_allow_html=True)

    if 'df' not in st.session_state:
        st.warning("     Te rog să încarci mai întâi datele din secțiunea 'Conexiune MongoDB'!")
        return

    df = st.session_state['df'].copy()
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if not numeric_cols:
        st.error("Nu există coloane numerice în dataset!")
        return

    st.markdown("""
    ## Metode de Scalare a Datelor

    Scalarea aduce toate variabilele la o scară comună pentru:
    - **Machine Learning**: Multe algoritmi sunt sensibili la scară
    - **Comparații**: Poți compara variabile cu unități diferite
    - **Vizualizare**: Grafice mai clare
    """)

    st.markdown('<div class="sub-header">Metode Disponibile</div>', unsafe_allow_html=True)

    with st.expander(" Teorie: Metode de Scalare", expanded=True):
        st.markdown("""
        ### 1. StandardScaler (Z-Score Normalization)

        Transformă datele să aibă **media = 0** și **deviație standard = 1**.

        **Formula:**
        ```
        z = (x - μ) / σ
        ```
        unde μ = media, σ = deviația standard

        **Cod:**
        ```python
        from sklearn.preprocessing import StandardScaler

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df[numeric_cols])
        ```

        **Când să folosești:**
        - Algoritmi sensibili la scară (SVM, KNN, Neural Networks)
        - Când datele sunt aproximativ normale
        - Când vrei să păstrezi outlieri (nu sunt comprimate excesiv)

        ---

        ### 2. MinMaxScaler (Normalizare 0-1)

        Transformă datele în intervalul **[0, 1]**.

        **Formula:**
        ```
        x_scaled = (x - min) / (max - min)
        ```

        **Cod:**
        ```python
        from sklearn.preprocessing import MinMaxScaler

        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(df[numeric_cols])
        ```

        **Când să folosești:**
        - Neural Networks (funcții activare sigmoid/tanh)
        - Când ai nevoie de interval specific [0,1]
        - Când nu ai outlieri extremi

        ---

        ### 3. RobustScaler (Robust la Outlieri)

        Folosește **mediana** și **IQR** în loc de medie și std.

        **Formula:**
        ```
        x_scaled = (x - median) / IQR
        ```
        unde IQR = Q3 - Q1

        **Cod:**
        ```python
        from sklearn.preprocessing import RobustScaler

        scaler = RobustScaler()
        X_scaled = scaler.fit_transform(df[numeric_cols])
        ```

        **Când să folosești:**
        - Când ai outlieri în date
        - Când StandardScaler distorsionează prea mult datele
        - Pentru date cu distribuții înclinate

        ---

        ### 4. Normalizer (L1/L2 Norm)

        Scalează **fiecare rând** să aibă normă unitară.

        **Cod:**
        ```python
        from sklearn.preprocessing import Normalizer

        scaler = Normalizer(norm='l2')  # sau 'l1', 'max'
        X_scaled = scaler.fit_transform(df[numeric_cols])
        ```

        **Când să folosești:**
        - Text mining (TF-IDF)
        - Când direcția e mai importantă decât magnitudinea
        - Clustering

        ---

        ### 5. QuantileTransformer (Transformare la Distribuție Uniformă/Normală)

        Transformă distribuția la una uniformă sau normală.

        **Cod:**
        ```python
        from sklearn.preprocessing import QuantileTransformer

        scaler = QuantileTransformer(
            n_quantiles=1000,
            output_distribution='uniform'  # sau 'normal'
        )
        X_scaled = scaler.fit_transform(df[numeric_cols])
        ```

        **Când să folosești:**
        - Date cu distribuții foarte înclinate
        - Când vrei să "forțezi" o distribuție normală
        - Robust la outlieri

        ---

        ### Comparație Rapidă

        | Metodă | Sensibil Outlieri | Interval | Când |
        |--------|------------------|----------|------|
        | StandardScaler | DA | (-∞, +∞) | Date normale, no outlieri |
        | MinMaxScaler | DA | [0, 1] | Neural nets, no outlieri |
        | RobustScaler | NU | (-∞, +∞) | Cu outlieri |
        | Normalizer | NU | Normă = 1 | Text, clustere |
        | QuantileTransformer | NU | [0, 1] sau normal | Distribuții înclinate |
        """)

    st.markdown("### Selectează Date și Metodă")

    # Select columns
    cols_to_scale = st.multiselect(
        "Selectează coloanele numerice de scalat:",
        numeric_cols,
        default=numeric_cols[:3] if len(numeric_cols) >= 3 else numeric_cols
    )

    if not cols_to_scale:
        st.warning("Selectează cel puțin o coloană!")
        return

    # Select method
    scaling_method = st.selectbox(
        "Selectează metoda de scalare:",
        ['StandardScaler', 'MinMaxScaler', 'RobustScaler', 'Normalizer', 'QuantileTransformer'],
        help="Vezi teoria pentru detalii despre fiecare metodă"
    )

    # Method-specific options
    if scaling_method == 'Normalizer':
        norm_type = st.radio(
            "Tip normă:",
            ['l1', 'l2', 'max'],
            format_func=lambda x: {
                'l1': 'L1 (Manhattan)',
                'l2': 'L2 (Euclidean)',
                'max': 'Max'
            }[x],
            horizontal=True
        )
    elif scaling_method == 'QuantileTransformer':
        n_quantiles = st.slider("Număr quantile:", 10, 1000, 100, 10)
        output_dist = st.radio(
            "Distribuție output:",
            ['uniform', 'normal'],
            horizontal=True
        )
    elif scaling_method == 'RobustScaler':
        quantile_range = st.slider(
            "Quantile range (Q1, Q3):",
            (0, 100),
            (25, 75),
            1
        )

    if st.button(" Aplică Scalarea", type="primary"):
        # Prepare data
        X = df[cols_to_scale].copy()
        X_clean = X.fillna(X.mean())  # Fill NaN pentru scalare

        # Apply scaling
        try:
            if scaling_method == 'StandardScaler':
                scaler = StandardScaler()
            elif scaling_method == 'MinMaxScaler':
                scaler = MinMaxScaler()
            elif scaling_method == 'RobustScaler':
                scaler = RobustScaler(quantile_range=quantile_range)
            elif scaling_method == 'Normalizer':
                scaler = Normalizer(norm=norm_type)
            else:  # QuantileTransformer
                scaler = QuantileTransformer(
                    n_quantiles=n_quantiles,
                    output_distribution=output_dist
                )

            X_scaled = scaler.fit_transform(X_clean)

            # Create scaled DataFrame
            df_scaled = pd.DataFrame(
                X_scaled,
                columns=[f'{col}_SCALED' for col in cols_to_scale],
                index=X.index
            )

            # Combine with original
            df_result = pd.concat([X, df_scaled], axis=1)

            st.session_state['df_scaled'] = df_result
            st.success(f"   Scalare aplicată cu {scaling_method}!")

            # Show statistics comparison
            st.markdown("### Comparație Statistici: Înainte vs După")

            stats_before = X_clean.describe()
            stats_after = df_scaled.describe()

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Înainte Scalare:**")
                st.dataframe(stats_before, use_container_width=True)

            with col2:
                st.markdown("**După Scalare:**")
                st.dataframe(stats_after, use_container_width=True)

            # Visualize distributions
            st.markdown("### Comparație Distribuții")

            for col in cols_to_scale:
                with st.expander(f"      {col}"):
                    fig = go.Figure()

                    # Original
                    fig.add_trace(go.Histogram(
                        x=X_clean[col],
                        name='Original',
                        opacity=0.7,
                        nbinsx=30
                    ))

                    # Scaled
                    fig.add_trace(go.Histogram(
                        x=df_scaled[f'{col}_SCALED'],
                        name='Scaled',
                        opacity=0.7,
                        nbinsx=30
                    ))

                    fig.update_layout(
                        title=f'Distribuție: {col}',
                        barmode='overlay',
                        xaxis_title='Valoare',
                        yaxis_title='Frecvență'
                    )

                    st.plotly_chart(fig, use_container_width=True)

                    # Box plots
                    fig_box = go.Figure()

                    fig_box.add_trace(go.Box(
                        y=X_clean[col],
                        name='Original',
                        boxmean=True
                    ))

                    fig_box.add_trace(go.Box(
                        y=df_scaled[f'{col}_SCALED'],
                        name='Scaled',
                        boxmean=True
                    ))

                    fig_box.update_layout(title=f'Box Plot: {col}')
                    st.plotly_chart(fig_box, use_container_width=True)

            # Show code
            with st.expander("    Cod Utilizat"):
                if scaling_method == 'StandardScaler':
                    code = f"""
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

# Selectează coloane
cols_to_scale = {cols_to_scale}
X = df[cols_to_scale]

# Tratează NaN
X_clean = X.fillna(X.mean())

# Aplică scalare
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_clean)

# Creează DataFrame
df_scaled = pd.DataFrame(
    X_scaled,
    columns=[f'{{col}}_SCALED' for col in cols_to_scale],
    index=X.index
)

print("Media după scalare:", X_scaled.mean(axis=0))
print("Std după scalare:", X_scaled.std(axis=0))
                    """

                elif scaling_method == 'MinMaxScaler':
                    code = f"""
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

# Selectează coloane
cols_to_scale = {cols_to_scale}
X = df[cols_to_scale].fillna(df[cols_to_scale].mean())

# Aplică scalare
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Creează DataFrame
df_scaled = pd.DataFrame(
    X_scaled,
    columns=[f'{{col}}_SCALED' for col in cols_to_scale]
)

print("Min după scalare:", X_scaled.min(axis=0))
print("Max după scalare:", X_scaled.max(axis=0))
                    """

                elif scaling_method == 'RobustScaler':
                    code = f"""
from sklearn.preprocessing import RobustScaler
import pandas as pd

# Selectează coloane
cols_to_scale = {cols_to_scale}
X = df[cols_to_scale].fillna(df[cols_to_scale].mean())

# Aplică scalare (robust la outlieri)
scaler = RobustScaler(quantile_range={quantile_range})
X_scaled = scaler.fit_transform(X)

# Creează DataFrame
df_scaled = pd.DataFrame(
    X_scaled,
    columns=[f'{{col}}_SCALED' for col in cols_to_scale]
)
                    """

                elif scaling_method == 'Normalizer':
                    code = f"""
from sklearn.preprocessing import Normalizer
import pandas as pd

# Selectează coloane
cols_to_scale = {cols_to_scale}
X = df[cols_to_scale].fillna(df[cols_to_scale].mean())

# Aplică normalizare (per rând)
scaler = Normalizer(norm='{norm_type}')
X_scaled = scaler.fit_transform(X)

# Creează DataFrame
df_scaled = pd.DataFrame(
    X_scaled,
    columns=[f'{{col}}_SCALED' for col in cols_to_scale]
)
                    """

                else:  # QuantileTransformer
                    code = f"""
from sklearn.preprocessing import QuantileTransformer
import pandas as pd

# Selectează coloane
cols_to_scale = {cols_to_scale}
X = df[cols_to_scale].fillna(df[cols_to_scale].mean())

# Aplică transformare quantile
scaler = QuantileTransformer(
    n_quantiles={n_quantiles},
    output_distribution='{output_dist}'
)
X_scaled = scaler.fit_transform(X)

# Creează DataFrame
df_scaled = pd.DataFrame(
    X_scaled,
    columns=[f'{{col}}_SCALED' for col in cols_to_scale]
)
                    """

                st.code(code, language="python")

        except Exception as e:
            st.error(f" Eroare la scalare: {str(e)}")
            st.info(" Verifică dacă există valori NaN sau infinite în date")

    # Comparison tool
    st.markdown('<div class="sub-header">Comparație între Metode</div>', unsafe_allow_html=True)

    with st.expander(" Compară Toate Metodele"):
        if st.button("      Generează Comparație", key="compare_methods"):
            if len(cols_to_scale) > 0:
                # Select one column for comparison
                comp_col = cols_to_scale[0]
                X_comp = df[[comp_col]].fillna(df[[comp_col]].mean())

                # Apply all methods
                methods = {
                    'Original': X_comp.values,
                    'StandardScaler': StandardScaler().fit_transform(X_comp),
                    'MinMaxScaler': MinMaxScaler().fit_transform(X_comp),
                    'RobustScaler': RobustScaler().fit_transform(X_comp),
                }

                # Create comparison plot
                fig = go.Figure()

                for method_name, data in methods.items():
                    fig.add_trace(go.Box(
                        y=data.flatten(),
                        name=method_name,
                        boxmean=True
                    ))

                fig.update_layout(
                    title=f'Comparație Metode Scalare: {comp_col}',
                    yaxis_title='Valoare',
                    showlegend=True
                )

                st.plotly_chart(fig, use_container_width=True)

                # Statistics table
                stats_comparison = pd.DataFrame({
                    method: [
                        data.min(),
                        np.percentile(data, 25),
                        np.median(data),
                        np.percentile(data, 75),
                        data.max(),
                        data.mean(),
                        data.std()
                    ]
                    for method, data in methods.items()
                }, index=['Min', 'Q1', 'Median', 'Q3', 'Max', 'Mean', 'Std'])

                st.markdown("### Statistici Comparative")
                st.dataframe(stats_comparison, use_container_width=True)



def show_descriptive_statistics():
    st.markdown('<h1 class="main-header">      Statistici Descriptive</h1>', unsafe_allow_html=True)

    if 'df' not in st.session_state:
        st.warning("     Te rog să încarci mai întâi datele din secțiunea 'Conexiune MongoDB'!")
        return

    df = st.session_state['df'].copy()
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if not numeric_cols:
        st.error("Nu există coloane numerice în dataset!")
        return

    st.markdown("""
    ## Analiza Statistică a Datelor

    Statisticile descriptive ne ajută să înțelegem:
    - **Tendința centrală**: Medie, mediană, mod
    - **Dispersia**: Deviație standard, varianță, interval
    - **Forma distribuției**: Skewness, kurtosis
    - **Relațiile**: Corelație, covarianță
    """)

    st.markdown('<div class="sub-header">Metoda 1: Agregări (Summary Statistics)</div>', unsafe_allow_html=True)

    with st.expander(" Teorie: describe() și Statistici de Bază", expanded=True):
        st.markdown("""
        ### DataFrame.describe()

        Generează statistici descriptive comprehensive pentru coloane numerice.

        **Cod:**
        ```python
        # Statistici de bază
        df.describe()

        # Include toate coloanele (chiar și categorice)
        df.describe(include='all')

        # Percentile custom
        df.describe(percentiles=[.1, .25, .5, .75, .9])
        ```

        **Output conține:**
        - `count`: Număr valori non-null
        - `mean`: Media aritmetică
        - `std`: Deviația standard
        - `min`: Valoarea minimă
        - `25%`: Prima cuartilă (Q1)
        - `50%`: Mediana (Q2)
        - `75%`: A treia cuartilă (Q3)
        - `max`: Valoarea maximă

        ### Statistici Individuale

        ```python
        # Media
        df['col'].mean()

        # Mediana
        df['col'].median()

        # Modul (cel mai frecvent)
        df['col'].mode()[0]

        # Deviația standard
        df['col'].std()

        # Varianța
        df['col'].var()

        # Min și Max
        df['col'].min()
        df['col'].max()

        # Quantile
        df['col'].quantile(0.25)  # Q1
        df['col'].quantile(0.75)  # Q3
        ```
        """)

    st.markdown("### Statistici Comprehensive")

    # Full describe
    st.markdown("#### Toate Coloanele Numerice")
    desc_df = df[numeric_cols].describe()
    st.dataframe(desc_df, use_container_width=True)

    # Custom percentiles
    with st.expander("Percentile Custom"):
        percentiles_input = st.text_input(
            "Percentile (0-100, separate prin virgulă):",
            value="1, 10, 25, 50, 75, 90, 99"
        )

        try:
            percentiles = [float(p.strip()) / 100 for p in percentiles_input.split(',')]
            custom_desc = df[numeric_cols].describe(percentiles=percentiles)
            st.dataframe(custom_desc, use_container_width=True)
        except:
            st.error("Format invalid! Folosește numere separate prin virgulă.")

    st.markdown('<div class="sub-header">Metoda 2: Skewness (Asimetria)</div>', unsafe_allow_html=True)

    with st.expander("Teorie: Skewness", expanded=False):
        st.markdown("""
        ### Indicele de Asimetrie (Skewness)

        Măsoară gradul de asimetrie a distribuției față de media.

        **Formula:**
        ```
        Skewness = E[(X - μ)³] / σ³
        ```

        **Interpretare:**
        - **Skewness ≈ 0**: Distribuție simetrică (normală)
        - **Skewness > 0**: Înclinată la dreapta (right-skewed)
          - Coadă lungă spre dreapta
          - Medie > Mediană
          - Ex: Venituri (puțini oameni cu venituri foarte mari)
        - **Skewness < 0**: Înclinată la stânga (left-skewed)
          - Coadă lungă spre stânga
          - Medie < Mediană
          - Ex: Vârsta la deces (majoritatea mor la vârste înaintate)

        **Clasificare:**
        - `|skewness| < 0.5`: Aproximativ simetrică
        - `0.5 < |skewness| < 1`: Moderat înclinată
        - `|skewness| > 1`: Foarte înclinată

        **Cod:**
        ```python
        # Cu pandas
        df['col'].skew()

        # Cu scipy
        from scipy.stats import skew
        skew(df['col'])

        # Pentru tot DataFrame-ul
        df.skew()
        ```
        """)

    st.markdown("### Calculează Skewness")

    # Calculate skewness
    skewness = df[numeric_cols].skew()
    skewness_df = pd.DataFrame({
        'Coloană': skewness.index,
        'Skewness': skewness.values,
        'Interpretare': skewness.apply(lambda x:
                                       'Simetrică' if abs(x) < 0.5 else
                                       'Moderat înclinată dreapta' if 0.5 <= x < 1 else
                                       'Foarte înclinată dreapta' if x >= 1 else
                                       'Moderat înclinată stânga' if -1 < x <= -0.5 else
                                       'Foarte înclinată stânga'
                                       ).values
    }).sort_values('Skewness', key=abs, ascending=False)

    col1, col2 = st.columns([2, 1])

    with col1:
        # Plot skewness
        fig = px.bar(
            skewness_df,
            x='Coloană',
            y='Skewness',
            color='Interpretare',
            title='Skewness pe Coloane',
            text='Skewness'
        )
        fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
        fig.add_hline(y=0, line_dash="dash", line_color="black")
        fig.add_hline(y=0.5, line_dash="dot", line_color="green", annotation_text="Moderate threshold")
        fig.add_hline(y=-0.5, line_dash="dot", line_color="green")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Tabel Skewness")
        st.dataframe(skewness_df, use_container_width=True)

    # Visualize most skewed
    most_skewed = skewness_df.iloc[0]['Coloană']

    with st.expander(f"      Vizualizare: {most_skewed} (Cea Mai Înclinată)"):
        fig = go.Figure()

        fig.add_trace(go.Histogram(
            x=df[most_skewed].dropna(),
            nbinsx=50,
            name='Histogramă'
        ))

        # Add mean and median lines
        mean_val = df[most_skewed].mean()
        median_val = df[most_skewed].median()

        fig.add_vline(x=mean_val, line_dash="dash", line_color="red", annotation_text=f"Medie: {mean_val:.2f}")
        fig.add_vline(x=median_val, line_dash="dash", line_color="blue",
                      annotation_text=f"Mediană: {median_val:.2f}")

        fig.update_layout(title=f'Distribuție {most_skewed} (Skewness: {skewness_df.iloc[0]["Skewness"]:.3f})')
        st.plotly_chart(fig, use_container_width=True)

        st.info(f"""
        **Interpretare:**
        - Medie: {mean_val:.2f}
        - Mediană: {median_val:.2f}
        - Diferență: {abs(mean_val - median_val):.2f}
        - {skewness_df.iloc[0]['Interpretare']}
        """)

    st.markdown('<div class="sub-header">Metoda 3: Kurtosis (Aplatizarea)</div>', unsafe_allow_html=True)

    with st.expander("Teorie: Kurtosis", expanded=False):
        st.markdown("""
        ### Indicele de Aplatizare (Kurtosis)

        Măsoară "greutatea" cozilor distribuției (outlieri potențiali).

        **Formula:**
        ```
        Kurtosis = E[(X - μ)⁴] / σ⁴
        ```

        **Tipuri:**

        1. **Mesokurtic** (Kurtosis ≈ 3 sau 0 în "excess kurtosis")
           - Distribuție normală
           - Cozi "normale"

        2. **Leptokurtic** (Kurtosis > 3 sau excess > 0)
           - Vârf ascuțit
           - Cozi grele (multe outlieri)
           - Mai multe valori extreme decât normalul

        3. **Platykurtic** (Kurtosis < 3 sau excess < 0)
           - Vârf plat
           - Cozi ușoare (puțini outlieri)
           - Mai puține valori extreme decât normalul

        **Interpretare Practică:**
        - `excess kurtosis > 0`: ATENȚIE la outlieri!
        - `excess kurtosis < 0`: Date mai uniforme

        **Cod:**
        ```python
        # Cu pandas (excess kurtosis, Fisher=True)
        df['col'].kurt()

        # Cu scipy
        from scipy.stats import kurtosis

        # Pearson (kurtosis absolut, cu 3)
        kurtosis(df['col'], fisher=False)

        # Fisher (excess kurtosis, fără 3)
        kurtosis(df['col'], fisher=True)

        # Pentru tot DataFrame-ul
        df.kurtosis()
        ```
        """)

    st.markdown("### Calculează Kurtosis")

    # Calculate kurtosis
    kurt = df[numeric_cols].kurtosis()  # Excess kurtosis (Fisher)
    kurt_df = pd.DataFrame({
        'Coloană': kurt.index,
        'Excess Kurtosis': kurt.values,
        'Interpretare': kurt.apply(lambda x:
                                   'Mesokurtic (Normal)' if -0.5 <= x <= 0.5 else
                                   'Leptokurtic (Cozi grele)' if x > 0.5 else
                                   'Platykurtic (Cozi ușoare)'
                                   ).values
    }).sort_values('Excess Kurtosis', key=abs, ascending=False)

    col1, col2 = st.columns([2, 1])

    with col1:
        fig = px.bar(
            kurt_df,
            x='Coloană',
            y='Excess Kurtosis',
            color='Interpretare',
            title='Kurtosis pe Coloane',
            text='Excess Kurtosis'
        )
        fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
        fig.add_hline(y=0, line_dash="dash", line_color="black")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Tabel Kurtosis")
        st.dataframe(kurt_df, use_container_width=True)

    st.markdown('<div class="sub-header">Metoda 4: Matricea de Corelație</div>', unsafe_allow_html=True)

    with st.expander(" Teorie: Corelație", expanded=False):
        st.markdown("""
        ### Coeficientul de Corelație

        Măsoară puterea și direcția relației liniare între două variabile.

        **Tipuri:**

        1. **Pearson** (cel mai comun)
           - Măsoară relații liniare
           - Interval: [-1, +1]
           - Sensibil la outlieri

        2. **Spearman** (rang-based)
           - Măsoară relații monotonice
           - Robust la outlieri
           - Pentru date ordinale

        3. **Kendall**
           - Alternativă la Spearman
           - Mai robust pentru seturi mici

        **Interpretare:**
        - `r = +1`: Corelație pozitivă perfectă
        - `r = 0`: Fără relație liniară
        - `r = -1`: Corelație negativă perfectă

        **Forță:**
        - `|r| < 0.3`: Slabă
        - `0.3 ≤ |r| < 0.7`: Moderată
        - `|r| ≥ 0.7`: Puternică

        **IMPORTANT: Corelație ≠ Cauzalitate!**

        **Cod:**
        ```python
        # Matrice corelație
        corr = df.corr()  # Pearson (default)
        corr = df.corr(method='spearman')
        corr = df.corr(method='kendall')

        # Corelație între două coloane
        df['col1'].corr(df['col2'])

        # Covarianță
        df.cov()
        ```
        """)

    st.markdown("### Matrice de Corelație")

    # Select correlation method
    corr_method = st.radio(
        "Metoda de corelație:",
        ['pearson', 'spearman', 'kendall'],
        format_func=lambda x: {
            'pearson': 'Pearson (Linear)',
            'spearman': 'Spearman (Rank)',
            'kendall': 'Kendall (Rank)'
        }[x],
        horizontal=True
    )

    # Calculate correlation
    corr_matrix = df[numeric_cols].corr(method=corr_method)

    # Heatmap
    fig = px.imshow(
        corr_matrix,
        text_auto='.2f',
        aspect='auto',
        color_continuous_scale='RdBu_r',
        color_continuous_midpoint=0,
        title=f'Heatmap Corelație ({corr_method.capitalize()})'
    )
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

    # Strong correlations
    st.markdown("### Corelații Puternice (|r| > 0.7)")

    # Get upper triangle
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
    corr_upper = corr_matrix.where(mask)

    # Flatten and filter
    strong_corr = []
    for col in corr_upper.columns:
        for idx in corr_upper.index:
            val = corr_upper.loc[idx, col]
            if not pd.isna(val) and abs(val) > 0.7:
                strong_corr.append({
                    'Variabila 1': idx,
                    'Variabila 2': col,
                    'Corelație': val,
                    'Forță': 'Foarte Puternică' if abs(val) > 0.9 else 'Puternică'
                })

    if strong_corr:
        strong_corr_df = pd.DataFrame(strong_corr).sort_values('Corelație', key=abs, ascending=False)
        st.dataframe(strong_corr_df, use_container_width=True)

        st.warning("""
             **Multicoliniaritate Potențială!**

        Variabile foarte corelate pot cauza probleme în modelare:
        - Redundanță (informație duplicată)
        - Instabilitate în modele de regresie
        - Dificultăți în interpretare

        **Soluții:**
        - Elimină una dintre variabilele corelate
        - Folosește PCA pentru reducerea dimensionalității
        - Folosește regularizare (Ridge, Lasso)
        """)
    else:
        st.success("   Nu există corelații foarte puternice (|r| > 0.7)")

    # Show code
    with st.expander("    Cod Utilizat"):
        st.code(f"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Calculează corelația
corr_matrix = df[numeric_cols].corr(method='{corr_method}')

# Afișează
print(corr_matrix)

# Heatmap cu seaborn
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap='RdBu_r', center=0, 
            fmt='.2f', square=True, linewidths=1)
plt.title('Matrice de Corelație')
plt.tight_layout()
plt.show()

# Găsește corelații puternice
threshold = 0.7
strong_corr = corr_matrix[abs(corr_matrix) > threshold]
print("Corelații puternice:")
print(strong_corr)
        """, language="python")


def show_graphical_representations():
    st.markdown('<h1 class="main-header">Reprezentări Grafice</h1>', unsafe_allow_html=True)

    if 'df' not in st.session_state:
        st.warning("Te rog să încarci mai întâi datele din secțiunea 'Conexiune MongoDB'!")
        return

    df = st.session_state['df'].copy()

    st.markdown("""
    ## Vizualizarea Datelor

    Graficele ne ajută să:
    - Înțelegem rapid distribuțiile
    - Identificăm pattern-uri și tendințe
    - Comparăm grupuri
    - Comunicăm insights
    """)

    # Găsește coloane necesare
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()

    st.markdown('<div class="sub-header">Box Plot - Comparații pe Grupuri</div>', unsafe_allow_html=True)

    with st.expander("Despre Box Plot"):
        st.markdown("""
        **Box Plot** arată distribuția datelor și identifică outlieri.

        Util pentru:
        - Compararea distribuțiilor între grupuri
        - Identificarea outlierilor
        - Vizualizarea quartilelor
```python
        # Simplu
        df.boxplot(column='valoare', by='categorie')

        # Cu plotly
        fig = px.box(df, x='categorie', y='valoare', color='grup')
```
        """)

    if not numeric_cols:
        st.error("Nu există coloane numerice în dataset!")
        return

    if not cat_cols:
        st.error("Nu există coloane categorice în dataset!")
        return

    col1, col2 = st.columns(2)

    with col1:
        box_y = st.selectbox("Variabila numerică (Y):", numeric_cols, key="box_y")

    with col2:
        box_x = st.selectbox("Grupare (X):", cat_cols, key="box_x")

    box_color = st.selectbox(
        "Culoare pe categorie (opțional):",
        [None] + cat_cols,
        key="box_color"
    )

    try:
        fig = px.box(
            df,
            x=box_x,
            y=box_y,
            color=box_color if box_color else box_x,
            title=f'Box Plot: {box_y} pe {box_x}',
            points='outliers'
        )
        st.plotly_chart(fig, use_container_width=True)

        # Statistics by group
        with st.expander("Statistici pe Grupuri"):
            stats = df.groupby(box_x)[box_y].describe()
            st.dataframe(stats, use_container_width=True)

    except Exception as e:
        st.error(f"Eroare la generarea graficului: {str(e)}")
        st.info("Verifică dacă există valori valide în coloanele selectate.")

def show_summary():
    st.markdown('<h1 class="main-header">🎓 Rezumat & Concluzii</h1>', unsafe_allow_html=True)

    st.markdown("""
    ## Rezumatul Seminarului

    Ai parcurs un tutorial comprehensiv despre **Analiza Volumelor Mari de Date în Python**!
    """)

    st.markdown('<div class="sub-header">Ce Ai Învățat</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ###   Prelucrarea Datelor

        1. **Curățarea Datelor**
           - Eliminarea duplicatelor (`drop_duplicates`)
           - Tratarea valorilor lipsă (`fillna`, `interpolate`)
           - Metode: medie, mediană, mod, interpolare

        2. **Detectarea Outlierilor**
           - Histograme și box plots
           - Metoda IQR (Interquartile Range)
           - Metoda quantilelor
           - Tratarea outlierilor

        3. **Prelucrarea Textului**
           - Filtrarea cu `isin()`
           - Label Encoding (text → numere)
           - Discretizare (`cut`, `qcut`)
        """)

    with col2:
        st.markdown("""
        ###       Analiza Datelor

        4. **Scalarea Datelor**
           - StandardScaler (Z-score)
           - MinMaxScaler (0-1)
           - RobustScaler (robust la outlieri)
           - Normalizer, QuantileTransformer

        5. **Statistici Descriptive**
           - Agregări: medie, mediană, std
           - Skewness (asimetria)
           - Kurtosis (aplatizarea)
           - Matrice de corelație

        6. **Vizualizări**
           - Box plots, Pie charts
           - Line charts, Heatmaps
           - Bar charts, Histograme
        """)

    st.markdown('<div class="sub-header">Metode Cheie de Reținut</div>', unsafe_allow_html=True)

    # Create summary table
    methods_summary = pd.DataFrame({
        'Metodă': [
            'drop_duplicates()',
            'fillna()',
            'interpolate()',
            'isin()',
            'LabelEncoder',
            'cut() / qcut()',
            'StandardScaler',
            'describe()',
            'skew() / kurt()',
            'corr()',
            'px.box() / px.pie()'
        ],
        'Scop': [
            'Elimină rânduri duplicate',
            'Înlocuiește valori lipsă',
            'Interpolare pentru NaN',
            'Filtrează valori din listă',
            'Transformă text în numere',
            'Discretizare continue → discrete',
            'Scalează date (μ=0, σ=1)',
            'Statistici comprehensive',
            'Asimetrie și aplatizare',
            'Matrice corelații',
            'Vizualizări interactive'
        ],
        'Bibliotecă': [
            'pandas',
            'pandas',
            'pandas',
            'pandas',
            'sklearn',
            'pandas',
            'sklearn',
            'pandas',
            'pandas',
            'pandas',
            'plotly'
        ]
    })

    st.dataframe(methods_summary, use_container_width=True)

    st.markdown('<div class="sub-header">Workflow Complet de Analiză</div>', unsafe_allow_html=True)

    st.markdown("""
    ### Pipeline Tipic de Prelucrare Date

    ```python
    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import StandardScaler, LabelEncoder

    # 1. ÎNCĂRCARE
    df = pd.read_csv('date.csv')
    # sau din MongoDB
    df = pd.DataFrame(list(collection.find({})))

    # 2. EXPLORARE INIȚIALĂ
    print(df.info())
    print(df.describe())
    print(df.isnull().sum())

    # 3. CURĂȚARE
    # Duplicate
    df = df.drop_duplicates(subset=['ID'])

    # Valori lipsă
    for col in numeric_cols:
        df[col].fillna(df[col].mean(), inplace=True)

    for col in cat_cols:
        df[col].fillna(df[col].mode()[0], inplace=True)

    # 4. OUTLIERI
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower) & (df[col] <= upper)]

    # 5. TRANSFORMĂRI
    # Encoding
    le = LabelEncoder()
    for col in cat_cols:
        df[f'{col}_encoded'] = le.fit_transform(df[col])

    # Discretizare
    df['age_group'] = pd.cut(df['age'], bins=5)

    # 6. SCALARE
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    # 7. ANALIZĂ
    print(df.skew())
    print(df.kurtosis())
    print(df.corr())

    # 8. VIZUALIZARE
    df.boxplot(column='value', by='category')
    df['category'].value_counts().plot(kind='pie')

    # 9. SALVARE
    df.to_csv('date_curate.csv', index=False)
    ```
    """)

    st.markdown('<div class="sub-header">Best Practices</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ###    DO (Fă)

        - **Explorează** datele înainte de orice prelucrare
        - **Documentează** pașii de curățare
        - **Salvează** versiuni intermediate
        - **Vizualizează** după fiecare transformare
        - **Verifică** asumpțiile statistice
        - **Testează** pe un subset înainte
        - **Păstrează** datele originale
        """)

    with col2:
        st.markdown("""
        ###  DON'T (Nu Face)

        - Nu elimina outlieri fără să investigezi
        - Nu aplica transformări fără să înțelegi impactul
        - Nu ignora valorile lipsă
        - Nu presupune normalitate fără să verifici
        - Nu confunda corelație cu cauzalitate
        - Nu scalezi fără să păstrezi valorile originale
        - Nu elimina date valabile
        """)

    st.markdown('<div class="sub-header">Resurse Suplimentare</div>', unsafe_allow_html=True)

    resources = {
        'Documentație': [
            '[Pandas Documentation](https://pandas.pydata.org/docs/)',
            '[Scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)',
            '[Plotly Python](https://plotly.com/python/)',
            '[Seaborn Tutorial](https://seaborn.pydata.org/tutorial.html)'
        ],
        'Tutoriale': [
            '[Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/)',
            '[Real Python - Pandas](https://realpython.com/pandas-python-explore-dataset/)',
            '[Kaggle Learn](https://www.kaggle.com/learn)',
            '[DataCamp - Pandas](https://www.datacamp.com/courses/pandas-foundations)'
        ],
        ' Cursuri': [
            '[Coursera - Applied Data Science with Python](https://www.coursera.org/specializations/data-science-python)',
            '[edX - Data Analysis with Python](https://www.edx.org/learn/data-analysis)',
            '[Udacity - Data Analyst Nanodegree](https://www.udacity.com/course/data-analyst-nanodegree--nd002)'
        ]
    }

    for category, links in resources.items():
        with st.expander(category):
            for link in links:
                st.markdown(link)

    st.markdown('<div class="success-box">', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Download summary as PDF
    if st.button(" Descarcă Rezumat (Text)", type="primary"):
        summary_text = """
SEMINAR 1 - ANALIZA VOLUMELOR MARI DE DATE ÎN PYTHON
REZUMAT COMPLET

=== METODE DE PRELUCRARE ===

1. CURĂȚAREA DATELOR
   - drop_duplicates(): Elimină duplicate
   - fillna(): Înlocuiește NaN
   - interpolate(): Interpolare valori

2. DETECTAREA OUTLIERILOR
   - Histograme și box plots
   - Metoda IQR
   - Metoda quantilelor

3. PRELUCRAREA TEXTULUI
   - isin(): Filtrare valori
   - LabelEncoder: Text → Numere
   - cut()/qcut(): Discretizare

4. SCALAREA DATELOR
   - StandardScaler: Z-score
   - MinMaxScaler: Normalizare 0-1
   - RobustScaler: Robust outlieri

5. STATISTICI DESCRIPTIVE
   - describe(): Rezumat
   - skew(): Asimetrie
   - kurtosis(): Aplatizare
   - corr(): Corelații

6. VIZUALIZĂRI
   - Box plots, Pie charts
   - Line charts, Heatmaps
   - Bar charts, Histograme

=== WORKFLOW COMPLET ===

1. Încărcare date
2. Explorare (info, describe, isnull)
3. Curățare (duplicate, NaN)
4. Outlieri (IQR, quantile)
5. Transformări (encoding, discretizare)
6. Scalare (StandardScaler, etc.)
7. Analiză (statistici, corelații)
8. Vizualizare (grafice)
9. Salvare date curate

=== BEST PRACTICES ===

DO:
✓ Explorează datele
✓ Documentează pașii
✓ Salvează versiuni
✓ Vizualizează
✓ Verifică asumpții

DON'T:
✗ Nu elimina fără investigație
✗ Nu ignora NaN
✗ Nu presupune normalitate
✗ Nu confunda corelație cu cauzalitate


        """

        st.download_button(
            label=" Descarcă",
            data=summary_text,
            file_name="seminar_avm_rezumat.txt",
            mime="text/plain"
        )


    # Adaugă în if __name__ == "__main__" din fișierul principal:
if __name__ == "__main__":
    selected_module = sidebar_navigation()

    if selected_module == " Acasă":
        show_home()
    elif selected_module == " Introducere în Streamlit":
        show_streamlit_intro()
    elif selected_module == " Conexiune MongoDB & Încărcare Date":
        show_mongodb_connection()
    elif selected_module == " Curățarea Datelor":
        show_data_cleaning()
    elif selected_module == " Detectarea Valorilor Anormale":
        show_outlier_detection()

    elif selected_module == " Prelucrarea Șirurilor de Caractere":
        show_string_processing()
    elif selected_module == " Standardizare și Normalizare":
        show_standardization()
    elif selected_module == " Statistici Descriptive":
        show_descriptive_statistics()
    elif selected_module == " Reprezentări Grafice":
        show_graphical_representations()
    elif selected_module == " Rezumat & Concluzii":
        show_summary()