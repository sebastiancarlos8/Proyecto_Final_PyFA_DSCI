import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
from io import StringIO

# __________________________
# Configuración de la página

# Se va a personalizar el título, ícono y modificar el uso de todo el ancho de la pantalla

# Debido a la distribución de gráficos, tablas e información presentada y analizada para el Dataset,
# se requiere de una amplia distribución en la pantalla, es por ello, que se optó por modificar el
# uso de la pantalla.


st.set_page_config(
    page_title="Insurance Company - EDA",
    page_icon="🛡️",
    layout="wide"
)


# _________________________________________________________________________________
# Aplicación de Programación Orientada a Objetos, mediante la clase 'Data Analyzer'

# La clase va a centralizar toda la lógica respecto al análisis exploratorio de datos aplicado en el DataFrame: estadística
# descriptiva, clasificación de variables, tablas de nulos, cruces con la variable objetivo, entre otros.


class DataAnalyzer:

    # Se guardará la tabla una vez para que pueda ser utilizada para las funciones

    def __init__(self, dataframe):
        self.df = dataframe

    # Convierte la salida del método df.info() en texto para que pueda ser mostrado como texto
    def informacion_general(self):
        buffer = StringIO()
        self.df.info(buf=buffer)
        return buffer.getvalue()

    # Muestra la tabla de tipo de dato de cada columna
    def tipos_datos(self):
        return self.df.dtypes.astype(str).to_frame("Tipo de dato")

    # Cuenta los valores nulos por columna y calcula el % que representan del total de filas
    def valores_nulos(self):
        nulos = self.df.isnull().sum()
        porcentaje = (nulos / len(self.df) * 100).round(2)

        resultado = pd.DataFrame({
            "Valores nulos": nulos,
            "Porcentaje (%)": porcentaje
        })

        return resultado.sort_values("Valores nulos", ascending=False)

    # Separa e identifica qué columnas son numéricas y cuáles son categóricas.
    def clasificar_variables(self):
        numericas = self.df.select_dtypes(include=np.number).columns.tolist()
        categoricas = self.df.select_dtypes(exclude=np.number).columns.tolist()
        return numericas, categoricas

    # Muestra los principales datos estadísticos de cada variable de forma ordenada.
    def estadisticas_descriptivas(self):
        return self.df.describe().T

    # Calcula las principales medidas estadísticas de una columna numérica, ignorando los valores faltantes.
    def estadistica_columna(self, columna):
        serie = self.df[columna].dropna()

        return {
            "Media": np.mean(serie),
            "Mediana": np.median(serie),
            "Moda": serie.mode().iloc[0] if not serie.mode().empty else np.nan,
            "Desviación estándar": np.std(serie),
            "Mínimo": np.min(serie),
            "Máximo": np.max(serie)
        }

    # Detecta valores atípicos en una columna usando el rango intercuartílico (IQR): 'todo valor por debajo de Q1 - 1.5*IQR o por encima de Q3 + 1.5*IQR'.
    def detectar_outliers_iqr(self, columna):

        serie = self.df[columna].dropna()

        q1 = np.percentile(serie, 25)
        q3 = np.percentile(serie, 75)
        iqr = q3 - q1

        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr

        outliers = serie[(serie < limite_inferior) | (serie > limite_superior)]

        return {
            "Q1": q1,
            "Q3": q3,
            "IQR": iqr,
            "Límite inferior": limite_inferior,
            "Límite superior": limite_superior,
            "Cantidad de outliers": len(outliers),
            "Porcentaje (%)": round(len(outliers) / len(serie) * 100, 2)
        }

    # Muestra la cantidad y el porcentaje de cada categoría, incluyendo los valores nulos.
    def conteo_categorico(self, columna):
        conteo = self.df[columna].value_counts(dropna=False)
        porcentaje = (conteo / len(self.df) * 100).round(2)

        return pd.DataFrame({
            "Conteo": conteo,
            "Proporción (%)": porcentaje
        })

    # Compara las categorías mostrando qué porcentaje de cada una renueva.
    def tasa_renovacion(self, columna):
        tabla = pd.crosstab(
            self.df[columna],
            self.df["renewal"],
            normalize="index"
        ) * 100

        tabla = tabla.rename(columns={0: "No", 1: "Sí"})
        return tabla.round(2)

# ____________________
# Funciones Auxiliares

# Carga el archivo seleccionado y verifica que sea de formato CSV.
def cargar_dataset(archivo):

    if archivo is None:
        return None

    nombre = archivo.name.lower()

    try:
        if nombre.endswith(".csv"):
            datos = pd.read_csv(archivo)
        else:
            st.error(
                "El archivo seleccionado debe estar en formato .csv."
            )
            return None
        return datos
    except Exception as error:
        st.error(f"No fue posible leer el archivo: {error}")
        return None

# Convierte la variable renewal a valores numéricos: 0 para No y 1 para Sí.
def normalizar_renewal(df):

    if df["renewal"].dtype == object:
        mapeo = {
            "yes": 1, "sí": 1, "si": 1, "1": 1,
            "no": 0, "0": 0
        }
        df["renewal"] = (
            df["renewal"].astype(str).str.strip().str.lower().map(mapeo)
        )
    return df

# Crea una nueva columna con la edad en años a partir de la edad en días.
def agregar_edad_anios(df):

    if "age_in_days" in df.columns and "age_years" not in df.columns:
        df["age_years"] = (df["age_in_days"] / 365).round(1)
    return df

# Muestra un resumen del dataset mediante 4 métricas principales: 'Total de clientes', 'Total variables', 'Renovaciones' y 'Tasa de renovación'.
def mostrar_metrica_resumen(df):

    total_clientes = len(df)
    total_variables = len(df.columns)
    renovaciones = df["renewal"].sum()
    tasa_renovacion = renovaciones / total_clientes * 100

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👥 Registros", f"{total_clientes:,}")

    with col2:
        st.metric("📊 Variables", f"{total_variables}")

    with col3:
        st.metric("🔄 Renovaciones", f"{int(renovaciones):,}")

    with col4:
        st.metric("📈 Tasa de renovación", f"{tasa_renovacion:.2f}%")

#_____________________
# Creación de gráficas

# Muestra la distribución de una variable numérica mediante un histograma y una curva de densidad.
def grafico_histograma(df, columna):

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.histplot(
        data=df,
        x=columna,
        kde=True,
        ax=ax
    )
    ax.set_title(f"Distribución de {columna}")
    ax.set_xlabel(columna)
    ax.set_ylabel("Frecuencia")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)  # libera memoria; evita acumular figuras entre reruns

# Registros de cada categoría mediante un gráfico de barras.
def grafico_categorico(df, columna):

    conteo = df[columna].value_counts().reset_index()
    conteo.columns = [columna, "Conteo"]

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(
        data=conteo,
        x=columna,
        y="Conteo",
        ax=ax
    )
    ax.set_title(f"Distribución de {columna}")
    ax.set_xlabel(columna)
    ax.set_ylabel("Cantidad")
    plt.xticks(rotation=30)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# Explica la distribución de los datos comparando la media y la mediana.
def interpretar_distribucion(df, columna):

    serie = df[columna].dropna()

    media = np.mean(serie)
    mediana = np.median(serie)
    desviacion = np.std(serie)

    if media > mediana * 1.10:
        forma = "presenta una posible asimetría positiva, debido a que la media supera a la mediana."
    elif media < mediana * 0.90:
        forma = "presenta una posible asimetría negativa, debido a que la media es inferior a la mediana."
    else:
        forma = "presenta una distribución relativamente cercana entre media y mediana."

    st.info(
        f"**Interpretación:** La variable **{columna}** tiene una media de "
        f"{media:,.2f}, una mediana de {mediana:,.2f} y una desviación estándar "
        f"de {desviacion:,.2f}. En términos descriptivos, {forma}"
    )

# Compara una variable numérica entre quienes renovaron y quienes no, mostrando también los valores atípicos mediante una gráfica de cajas.
def grafico_numerica_renovacion(df, columna):

    datos = df[[columna, "renewal"]].dropna().copy()
    datos["renewal_label"] = datos["renewal"].map({0: "No", 1: "Sí"})

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.boxplot(
        data=datos,
        x="renewal_label",
        y=columna,
        ax=ax
    )
    ax.set_title(f"{columna} según renovación")
    ax.set_xlabel("Renovación")
    ax.set_ylabel(columna)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    resumen = datos.groupby("renewal_label")[columna].agg(
        ["mean", "median"]
    ).round(2)

    resumen.columns = ["Media", "Mediana"]
    st.dataframe(resumen, use_container_width=True)

    if len(resumen) == 2:
        diferencia = resumen.loc["Sí", "Media"] - resumen.loc["No", "Media"]

        if diferencia > 0:
            st.info(
                f"Los clientes que renovaron presentan una media de **{columna}** "
                f"superior en {diferencia:,.2f} unidades respecto a quienes no renovaron."
            )
        else:
            st.info(
                f"Los clientes que renovaron presentan una media de **{columna}** "
                f"inferior en {abs(diferencia):,.2f} unidades respecto a quienes no renovaron."
            )

# Muestra cómo se distribuyen los valores de una variable numérica, a través gráfica de barras apiladas(100%).

def grafico_categorica_renovacion(df, columna):

    tabla = pd.crosstab(
        df[columna],
        df["renewal"],
        normalize="index"
    ) * 100

    tabla = tabla.rename(columns={0: "No", 1: "Sí"})

    fig, ax = plt.subplots(figsize=(10, 5))
    tabla.plot(
        kind="bar",
        stacked=True,
        ax=ax
    )

    ax.set_title(f"Renovación según {columna}")
    ax.set_xlabel(columna)
    ax.set_ylabel("Proporción (%)")
    ax.legend(title="Renovación")
    plt.xticks(rotation=30)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.dataframe(tabla.round(2), use_container_width=True)


# ___________________________
# MENÚ PRINCIPAL DEL PROYECTO

# Las imágenes DMC.png y Python_logo.png se cargan de forma directa porque
# permanecerán siempre disponibles en el repositorio, junto a este app.py.
st.sidebar.image("DMC.png", width=100)
st.sidebar.title("📚 Contenido")
modulos = st.sidebar.selectbox("Seleccione un módulo",["Home", "Caso de Estudio N°3"])



#_______________________________
# MÓDULO 1 y 2: HOME y CASO N° 3

if modulos == "Home":

    st.title("Trabajo Final - Módulo Python Fundamentals")

    # Logo de Python como imagen de portada del módulo Home.
    st.image("Python_logo.png", width=500)

    st.subheader("Descripción del objetivo del análisis")

    st.markdown(
        """
        El presente proyecto desarrolla una aplicación interactiva para realizar
        un **Análisis Exploratorio de Datos (EDA)** sobre información histórica
        de clientes de una compañía de seguros.

        El objetivo del análisis busca identificar patrones descriptivos relacionados con la
        **renovación de pólizas**, utilizando estadística descriptiva,
        clasificación de variables y visualizaciones interactivas.

        El proyecto tiene un enfoque de análisis y toma de decisiones, sin
        desarrollar modelos predictivos.
        """
    )

    st.subheader("Elaborado por")

    st.write("**Nombre completo:** David Sebastian Carlos Ipanaque")
    st.write("**Módulo:** 🐍 Especialización en Python for Analytics")
    st.write("**Año:** 2026")

    st.subheader("Información general del Dataset")

    st.markdown(
        """
        El dataset **InsuranceCompany.csv** contiene información histórica
        relacionada con clientes de una compañía de seguros. Incluye variables
        demográficas, económicas, historial de pagos, comportamiento de
        morosidad, canal de captación, tipo de residencia, valor de la prima
        y puntaje de evaluación del cliente.

        La variable **renewal** representa si el cliente renovó o no su póliza.
        """
    )

    st.subheader("🛠️ Tecnologías utilizadas")

    st.markdown(
        """
        Para el presente proyecto se utilizaron las siguientes tecnologías:

        - 🔗 GitHub
        - 🎨 Streamlit
        - 🐍 Google Colab / Python
        - 🔢 NumPy
        - 🐼 Pandas
        - 📊 Matplotlib
        - 📈 Seaborn
        - 🧩 Programación Orientada a Objetos (POO)
        """
    )

else:

    st.title("👤 Caso de Estudio N°3")
    st.markdown(
        """
        ### Análisis Exploratorio de Datos - Insurance Company

        Utilice el panel lateral para cargar el archivo **InsuranceCompany.csv**.
        El análisis se ejecutará únicamente después de validar la carga del
        dataset.
        """
    )

    archivo = st.sidebar.file_uploader(
        "📂 Seleccione su archivo",
        type=["csv"]
    )

    # Ningún análisis se ejecuta si 'datos' es None (archivo no cargado o inválido).
    datos = cargar_dataset(archivo)

    if datos is not None:

        # Validación adicional: la variable objetivo 'renewal' es obligatoria para todo el módulo de EDA (tasas de renovación, análisis bivariado, hallazgos, entre otros.).
        if "renewal" not in datos.columns:
            st.error(
                "El archivo cargado no contiene la columna `renewal`, "
                "necesaria para este análisis. Verifique que el archivo "
                "corresponda a InsuranceCompany.csv."
            )
            st.stop()

        # Prepara los datos para el análisis, homogenizando 'renewal' a 0/1 y agregando la columna derivada 'age_years' (edad en años).
        datos = normalizar_renewal(datos)
        datos = agregar_edad_anios(datos)

        st.success(
            f"Archivo **{archivo.name}** cargado correctamente."
        )

        analyzer = DataAnalyzer(datos)

        # ______________________________________________
        # VISTA PREVIA Y DIMENSIONES (Carga del dataset)

        st.subheader("📂 Carga y validación del dataset")

        mostrar_metrica_resumen(datos)

        col1, col2 = st.columns(2)

        with col1:
            st.write("### Vista previa")
            st.dataframe(
                datos.head(),
                use_container_width=True
            )

        with col2:
            st.write("### Dimensiones")
            st.write(
                f"El dataset contiene **{datos.shape[0]:,} filas** "
                f"y **{datos.shape[1]} columnas**."
            )

            st.write("### Variables")
            st.write(", ".join(datos.columns.tolist()))

        st.divider()

        # ____________
        # TABS DEL EDA

        # Se usan 8 pestañas: las primeras 7 organizan los 10 ítems de
        # análisis solicitados por el caso de estudio (algunas pestañas
        # agrupan 2 ítems relacionados), y la última pestaña adicional
        # ("Conclusiones") reúne las 5 conclusiones finales del proyecto.

        tabs = st.tabs([
            "1️⃣-2️⃣ Información y Variables",
            "3️⃣-4️⃣ Estadística y Nulos",
            "5️⃣ Numéricas",
            "6️⃣ Categóricas",
            "7️⃣-8️⃣ Bivariado",
            "9️⃣ Dinámico",
            "🔟 Hallazgos",
            "1️⃣1️⃣ Conclusiones"
        ])

        # _______________________________________
        # ÍTEM 1: Información general del dataset

        with tabs[0]:

            st.header("📌 Ítem 1: Información general del dataset")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Información mediante .info()")
                st.text(analyzer.informacion_general())

            with col2:
                st.subheader("Tipos de datos")
                st.dataframe(
                    analyzer.tipos_datos(),
                    use_container_width=True
                )

            st.subheader("Valores nulos")
            nulos = analyzer.valores_nulos()

            st.dataframe(
                nulos,
                use_container_width=True
            )

        # __________________________________
        # ÍTEM 2: Clasificación de variables

        with tabs[0]:

            st.header("📌 Ítem 2: Clasificación de variables")

            numericas, categoricas = analyzer.clasificar_variables()

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🔢 Variables numéricas")
                st.metric(
                    "Cantidad",
                    len(numericas)
                )

                for variable in numericas:
                    st.write(f"• {variable}")

            with col2:
                st.subheader("🔤 Variables categóricas")
                st.metric(
                    "Cantidad",
                    len(categoricas)
                )

                for variable in categoricas:
                    st.write(f"• {variable}")

            st.info(
                f"Se identificaron **{len(numericas)} variables numéricas** y "
                f"**{len(categoricas)} variables categóricas** mediante una "
                f"función personalizada integrada en la clase `DataAnalyzer`."
            )


        # _________________________________
        # ÍTEM 3: Estadísticas descriptivas

        with tabs[1]:

            st.header("📌 Ítem 3: Estadísticas descriptivas")

            st.write(
                "La tabla resume las principales medidas descriptivas "
                "de las variables numéricas."
            )

            estadisticas = analyzer.estadisticas_descriptivas()
            st.dataframe(
                estadisticas.round(2),
                use_container_width=True
            )

            numericas, _ = analyzer.clasificar_variables()

            variable_estadistica = st.selectbox(
                "Seleccione una variable para profundizar:",
                numericas,
                key="estadistica_variable"
            )

            resultado = analyzer.estadistica_columna(
                variable_estadistica
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Media",
                    f"{resultado['Media']:,.2f}"
                )

            with col2:
                st.metric(
                    "Mediana",
                    f"{resultado['Mediana']:,.2f}"
                )

            with col3:
                st.metric(
                    "Desviación estándar",
                    f"{resultado['Desviación estándar']:,.2f}"
                )

            st.write(
                f"Para **{variable_estadistica}**, la media y la mediana "
                f"permiten observar la tendencia central, mientras que la "
                f"desviación estándar permite evaluar la dispersión de los datos."
            )

            # Detección de outliers con la regla del IQR.
            # Ayuda a explicar por qué, en variables como 'Income', la media puede quedar muy por encima de la mediana.

            outliers = analyzer.detectar_outliers_iqr(variable_estadistica)

            st.write("#### Detección de valores atípicos (regla IQR)")
            st.write(
                f"Se identificaron **{outliers['Cantidad de outliers']:,} "
                f"valores atípicos** ({outliers['Porcentaje (%)']}% del total) "
                f"fuera del rango [{outliers['Límite inferior']:,.2f}, "
                f"{outliers['Límite superior']:,.2f}]."
            )


        # _____________________________________
        # ÍTEM 4: Análisis de valores faltantes

        with tabs[1]:

            st.header("📌 Ítem 4: Análisis de valores faltantes")

            nulos = analyzer.valores_nulos()

            solo_nulos = nulos[nulos["Valores nulos"] > 0]

            if solo_nulos.empty:
                st.success("No se identificaron valores faltantes.")
            else:
                st.dataframe(
                    solo_nulos,
                    use_container_width=True
                )

                fig, ax = plt.subplots(figsize=(9, 5))

                sns.barplot(
                    x=solo_nulos.index,
                    y=solo_nulos["Valores nulos"],
                    ax=ax
                )

                ax.set_title("Cantidad de valores faltantes")
                ax.set_xlabel("Variable")
                ax.set_ylabel("Valores nulos")
                plt.xticks(rotation=45, ha="right")
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)

                mayor_nulo = solo_nulos["Valores nulos"].idxmax()
                cantidad_nulo = solo_nulos.loc[
                    mayor_nulo,
                    "Valores nulos"
                ]

                st.warning(
                    f"La variable con mayor cantidad de valores faltantes es "
                    f"**{mayor_nulo}**, con **{cantidad_nulo:,} registros**. "
                    f"Este aspecto debe considerarse antes de realizar análisis "
                    f"que involucren directamente dicha variable."
                )


        # ___________________________________________
        # ÍTEM 5: Distribución de variables numéricas

        with tabs[2]:

            st.header("📌 Ítem 5: Distribución de variables numéricas")

            numericas, _ = analyzer.clasificar_variables()

            variable_hist = st.selectbox(
                "Seleccione una variable numérica:",
                numericas,
                key="hist_variable"
            )

            grafico_histograma(
                datos,
                variable_hist
            )

            interpretar_distribucion(
                datos,
                variable_hist
            )


        # _________________________________________
        # ÍTEM 6: Análisis de variables categóricas

        with tabs[3]:

            st.header("📌 Ítem 6: Análisis de variables categóricas")

            _, categoricas = analyzer.clasificar_variables()

            variable_cat = st.selectbox(
                "Seleccione una variable categórica:",
                categoricas,
                key="cat_variable"
            )

            resultado_cat = analyzer.conteo_categorico(
                variable_cat
            )

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Conteos y proporciones")
                st.dataframe(
                    resultado_cat,
                    use_container_width=True
                )

            with col2:
                grafico_categorico(
                    datos,
                    variable_cat
                )

            categoria_mayor = resultado_cat["Conteo"].idxmax()
            cantidad_mayor = resultado_cat.loc[
                categoria_mayor,
                "Conteo"
            ]

            porcentaje_mayor = resultado_cat.loc[
                categoria_mayor,
                "Proporción (%)"
            ]

            st.info(
                f"La categoría con mayor frecuencia en **{variable_cat}** es "
                f"**{categoria_mayor}**, con **{cantidad_mayor:,} registros** "
                f"({porcentaje_mayor:.2f}% del total)."
            )


        # ___________________________________________________
        # ÍTEM 7: Análisis bivariado - Numérica vs categórica

        with tabs[4]:

            st.header(
                "📌 Ítem 7: Análisis bivariado - Numérica vs categórica"
            )

            st.write(
                "Se compara una variable numérica frente a la variable "
                "categórica objetivo 'renewal'."
            )

            numericas, _ = analyzer.clasificar_variables()

            # No utilizar ID como variable analítica principal
            opciones_num = [
                x for x in numericas
                if x != "renewal" and x != "id"
            ]

            variable_bivariada = st.selectbox(
                "Seleccione una variable numérica:",
                opciones_num,
                key="bivariado_num"
            )

            grafico_numerica_renovacion(
                datos,
                variable_bivariada
            )

            st.write(
                f"El gráfico permite comparar la distribución de "
                f"**{variable_bivariada}** entre clientes que renovaron "
                f"y clientes que no renovaron."
            )


        # _____________________________________________________
        # ÍTEM 8: Análisis bivariado - Categórica vs categórica

        with tabs[4]:

            st.header(
                "📌 Ítem 8: Análisis bivariado - Categórica vs categórica"
            )

            _, categoricas = analyzer.clasificar_variables()

            opciones_cat = [
                x for x in categoricas
                if x != "renewal"
            ]

            variable_cat_bivariada = st.selectbox(
                "Seleccione una variable categórica:",
                opciones_cat,
                key="bivariado_cat"
            )

            grafico_categorica_renovacion(
                datos,
                variable_cat_bivariada
            )

            st.write(
                f"Las proporciones permiten comparar el comportamiento de "
                f"renovación entre las categorías de **{variable_cat_bivariada}**."
            )

        # ___________________________________________________
        # ÍTEM 9: Análisis basado en parámetros seleccionados

        with tabs[5]:

            st.header(
                "📌 Ítem 9: Análisis basado en parámetros seleccionados"
            )

            numericas, categoricas = analyzer.clasificar_variables()

            st.subheader("Selección múltiple de variables")

            variables_seleccionadas = st.multiselect(
                "Seleccione una o más variables numéricas:",
                [
                    x for x in numericas
                    if x != "id" and x != "renewal"
                ],
                default=[
                    "Income",
                    "premium"
                ] if "Income" in numericas and "premium" in numericas else [],
                key="multi_variables"
            )

            if variables_seleccionadas:

                st.write(
                    f"Se seleccionaron **{len(variables_seleccionadas)} "
                    f"variables** para el análisis."
                )

                resumen_seleccionado = datos[
                    variables_seleccionadas
                ].describe().T

                st.dataframe(
                    resumen_seleccionado.round(2),
                    use_container_width=True
                )

            st.divider()

            st.subheader("Cruce dinámico con la variable objetivo")

            # Widget: el usuario elige una variable CATEGÓRICA
            # Permite seleccionar una variable categórica y calcula su tasa de renovación según la opción elegida.

            variable_cruce = st.selectbox(
                "Seleccione una variable categórica para calcular su tasa de renovación:",
                [x for x in categoricas if x != "renewal"],
                key="cruce_categorica"
            )

            st.dataframe(
                analyzer.tasa_renovacion(variable_cruce),
                use_container_width=True
            )

            st.divider()

            st.subheader("Filtro dinámico")

            variable_slider = st.selectbox(
                "Seleccione una variable para filtrar:",
                [
                    x for x in numericas
                    if x != "id" and x != "renewal"
                ],
                key="slider_variable"
            )

            minimo = float(datos[variable_slider].min())
            maximo = float(datos[variable_slider].max())

            rango = st.slider(
                f"Seleccione el rango de {variable_slider}:",
                min_value=minimo,
                max_value=maximo,
                value=(minimo, maximo),
                key="rango_slider"
            )

            datos_filtrados = datos[
                datos[variable_slider].between(
                    rango[0],
                    rango[1]
                )
            ]

            st.write(
                f"Registros dentro del rango seleccionado: "
                f"**{len(datos_filtrados):,}**"
            )

            st.dataframe(
                datos_filtrados.head(20),
                use_container_width=True
            )

            mostrar_interpretacion = st.checkbox(
                "Mostrar interpretación del filtro",
                value=True,
                key="mostrar_interpretacion"
            )

            if mostrar_interpretacion:

                porcentaje = (
                    len(datos_filtrados) /
                    len(datos) * 100
                )

                st.info(
                    f"El rango seleccionado concentra "
                    f"**{len(datos_filtrados):,} registros**, equivalentes "
                    f"al **{porcentaje:.2f}%** del dataset."
                )


        # ________________________
        # ÍTEM 10: Hallazgos clave

        with tabs[6]:

            st.header("📌 Ítem 10: Hallazgos clave")

            tasa_general = datos["renewal"].mean() * 100

            income_media_no = datos.loc[
                datos["renewal"] == 0,
                "Income"
            ].mean()

            income_media_si = datos.loc[
                datos["renewal"] == 1,
                "Income"
            ].mean()

            premium_media_no = datos.loc[
                datos["renewal"] == 0,
                "premium"
            ].mean()

            premium_media_si = datos.loc[
                datos["renewal"] == 1,
                "premium"
            ].mean()

            cash_no = datos.loc[
                datos["renewal"] == 0,
                "perc_premium_paid_by_cash_credit"
            ].mean()

            cash_si = datos.loc[
                datos["renewal"] == 1,
                "perc_premium_paid_by_cash_credit"
            ].mean()

            canal_renovacion = (
                datos.groupby("sourcing_channel")["renewal"]
                .mean()
                .mul(100)
                .sort_values(ascending=False)
            )

            mejor_canal = canal_renovacion.index[0]
            mejor_tasa_canal = canal_renovacion.iloc[0]

            st.subheader("📌 Resumen general")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Tasa general de renovación",
                    f"{tasa_general:.2f}%"
                )

            with col2:
                st.metric(
                    "Canal con mayor tasa de renovación",
                    f"{mejor_canal} ({mejor_tasa_canal:.2f}%)"
                )

            st.subheader("🔎 Principales insights")

            st.markdown(
                f"""
                **1. Renovación:** La tasa global de renovación del dataset
                es de **{tasa_general:.2f}%**, lo que muestra una mayor
                concentración de clientes en la categoría de renovación
                (dataset desbalanceado hacia "Sí renueva").

                **2. Ingreso:** El ingreso mensual promedio es de
                **{income_media_si:,.2f}** entre quienes renovaron y de
                **{income_media_no:,.2f}** entre quienes no renovaron.

                **3. Prima:** El valor promedio de la prima es de
                **{premium_media_si:,.2f}** para clientes que renovaron frente
                a **{premium_media_no:,.2f}** para quienes no renovaron.

                **4. Forma de pago:** El porcentaje promedio de la prima
                pagado mediante efectivo/crédito es de **{cash_si:.2f}%**
                en quienes renovaron frente a **{cash_no:.2f}%** en quienes
                no renovaron.

                **5. Canal de captación:** El canal **{mejor_canal}** presenta
                la mayor tasa descriptiva de renovación, con
                **{mejor_tasa_canal:.2f}%**.
                """
            )

            st.warning(
                "Estos hallazgos corresponden a relaciones descriptivas "
                "observadas en el dataset. No deben interpretarse como "
                "relaciones causales ni como predicciones."
            )


        # ____________________________________________
        # ÍTEM 11 (adicional): Conclusiones finales
        # Se ubica en su propia pestaña, separada de "Hallazgos", porque
        # conceptualmente cierra el proyecto completo (las 5 conclusiones
        # exigidas por el caso de estudio) y no es un ítem más del EDA.

        with tabs[7]:

            st.header("📝 Conclusiones finales")

            st.markdown(
                """
                **1.** La tasa de renovación del portafolio es alta (por encima del
                90%), lo que sugiere que la compañía mantiene, en general, una
                base de clientes fidelizada; sin embargo, el segmento que no
                renueva —aunque minoritario— representa una oportunidad concreta
                de mejora en retención.

                **2.** Los clientes morosos (con pagos atrasados de 3 a 6, de 6 a
                12 o de más de 12 meses) muestran, de forma descriptiva, una menor
                tendencia a renovar su póliza. Esto posiciona el historial de
                morosidad como una señal temprana útil para priorizar acciones
                comerciales de retención.

                **3.** El canal de captación (`sourcing_channel`) influye en el
                comportamiento de renovación observado: algunos canales concentran
                tasas de renovación más altas que otros, lo que puede orientar
                decisiones sobre en qué canales invertir esfuerzos comerciales.

                **4.** Variables económicas como el ingreso (`Income`) y el valor
                de la prima (`premium`) presentan distribuciones con asimetría y
                valores atípicos relevantes, por lo que cualquier análisis o
                reporte que use sus promedios debe complementarse con la mediana
                y la dispersión para no llegar a conclusiones distorsionadas.

                **5.** El puntaje de evaluación del cliente
                (`application_underwriting_score`) presenta una cantidad
                considerable de valores faltantes, por lo que antes de utilizarlo
                en futuros análisis (incluyendo eventuales modelos predictivos)
                se recomienda definir una estrategia explícita de tratamiento de
                datos faltantes.
                """
            )

            st.caption(
                "Estas conclusiones se basan en relaciones descriptivas "
                "identificadas mediante el EDA y buscan apoyar decisiones de "
                "negocio (por ejemplo, foco de campañas de retención), sin "
                "constituir un modelo predictivo."
            )

    else:

        st.info(
            "📂 Cargue el archivo **InsuranceCompany.csv** desde el panel "
            "lateral para iniciar el análisis."
        )
