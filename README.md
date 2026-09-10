# Proyecto_Final_PyFA_DSCI

# 🛡️ CASO N° 3: Insurance Company

Aplicación desarrollada con **Python** y **Streamlit** para realizar un
**Análisis Exploratorio de Datos (EDA)** sobre el dataset `InsuranceCompany.csv`,
desarrollada como **Caso de Estudio N°3** 

---

## 📌 Descripción del proyecto

El proyecto busca identificar, de forma **descriptiva**, qué factores se
relacionan con la **renovación de pólizas de seguro** (variable objetivo
`renewal`) a partir de información histórica de clientes: datos demográficos,
económicos, historial de pagos, comportamiento de morosidad, canal de
captación, tipo de residencia, valor de la prima y puntaje de evaluación del
cliente.

> El proyecto tiene un enfoque exploratorio, **no** construye modelos predictivos.
> Está orientado a apoyar la toma de decisiones (por ejemplo, priorizar
> campañas de retención), aplicando de forma integrada estadística
> descriptiva, Programación Orientada a Objetos (POO) y visualización de datos.

La aplicación está organizada en dos módulos navegables desde el sidebar
(`st.sidebar.selectbox`):

- **Home:** presentación del proyecto (sin análisis).
- **Caso de Estudio N°3:** carga del dataset y el núcleo del EDA, distribuido
  en 8 pestañas (`st.tabs`): las primeras 7 cubren los **10 ítems de análisis**
  exigidos por el caso de estudio (algunas pestañas agrupan 2 ítems
  relacionados) y la octava reúne las **Conclusiones finales** del proyecto.

| Pestaña | Contenido |
|---|---|
| 1️⃣-2️⃣ Información y Variables | `.info()`, tipos de dato, nulos, y clasificación numéricas/categóricas |
| 3️⃣-4️⃣ Estadística y Nulos | `.describe()`, media/mediana/desviación, outliers (regla IQR) y análisis de faltantes |
| 5️⃣ Numéricas | Histogramas + interpretación de la distribución |
| 6️⃣ Categóricas | Conteos, proporciones y gráfico de barras |
| 7️⃣-8️⃣ Bivariado | Numérica vs `renewal` (boxplot) y categórica vs `renewal` (barras apiladas) |
| 9️⃣ Dinámico | Multiselect, cruce dinámico con `renewal` y filtro con slider/checkbox |
| 🔟 Hallazgos | Resumen ejecutivo e insights principales del EDA |
| 1️⃣1️⃣ Conclusiones | 5 conclusiones finales, redactadas y orientadas a decisiones |

Toda la lógica de análisis está encapsulada en la clase `DataAnalyzer`
(`app.py`), aplicando Programación Orientada a Objetos: estadística
descriptiva, detección de outliers, clasificación de variables, tablas de
nulos, conteos categóricos y tasas de renovación. Un conjunto separado de
**funciones auxiliares** se encarga de la interfaz: carga/validación del CSV,
gráficos (Matplotlib/Seaborn) e interpretaciones automáticas en lenguaje
natural (f-strings).

---

## 🛠️ Tecnologías utilizadas

- 🔗 GitHub
- 🎨 Streamlit (sidebar, tabs, columns, selectbox, multiselect, slider, checkbox)
- 🐍 Google Colab / Python
- 🔢 NumPy
- 🐼 Pandas
- 📊 Matplotlib
- 📈 Seaborn
- 🧩 Programación Orientada a Objetos (POO)

---

## 📂 Estructura del repositorio

```
insurance-eda-streamlit/
├── app.py                     # Aplicación Streamlit (código fuente)
├── requirements.txt           # Dependencias del proyecto
├── InsuranceCompany.csv       # Dataset utilizado en el análisis
├── DMC.png                    # Logo institucional (sidebar)
├── Python_logo.png            # Logo de Python (módulo Home)
└── README.md                  # Este archivo
```

---

## ▶️ Instrucciones de ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/[TU-USUARIO]/[TU-REPOSITORIO].git
cd [TU-REPOSITORIO]
```

### 2. Crear un entorno virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en `http://localhost:8501`. Desde el
**sidebar** (panel lateral) se ve, en todo momento, el logo institucional
(`DMC.png`) y el menú desplegable **"Seleccione un módulo"**, que permite
alternar entre los dos espacios de la aplicación:

#### 🏠 Módulo "Home"

Es la pantalla de presentación del proyecto. **No requiere cargar ningún
archivo y no ejecuta ningún análisis.** Al ingresar aquí se observa:

- El título del trabajo y el logo de Python.
- La descripción del objetivo del análisis (qué se busca responder con el EDA).
- Los datos del autor (nombre completo, especialización y año).
- Una explicación general del dataset `InsuranceCompany.csv` y de la variable
  objetivo `renewal`.
- El listado de tecnologías utilizadas en el proyecto.

Este módulo sirve como **carta de presentación**: es lo primero que ve
cualquier persona (por ejemplo, el docente o un reclutador) para entender de
qué trata el proyecto antes de entrar al análisis.

#### 👤 Módulo "Caso de Estudio N°3"

Es el espacio donde ocurre el análisis. Al ingresar, el sidebar muestra
además el botón **"Seleccione su archivo"** (`st.file_uploader`), que exige
cargar el archivo `InsuranceCompany.csv`.

- **Mientras no se cargue un archivo**, la pantalla solo muestra un aviso
  pidiendo cargarlo: no se ejecuta ningún cálculo ni se muestra ningún dato.
- **Una vez cargado y validado el archivo** (se verifica que sea `.csv` y que
  contenga la columna `renewal`), la aplicación muestra, en orden:
  1. Un resumen con 4 métricas clave (registros, variables, renovaciones y
     tasa de renovación), una vista previa del dataset y sus dimensiones.
  2. **8 pestañas** con los 10 ítems del EDA y las conclusiones finales
     (detalladas en la tabla de la sección anterior). Cada pestaña incluye
     texto explicativo, al menos una tabla o gráfico, y widgets interactivos
     (selectbox, multiselect, slider o checkbox) donde aplica, para que el
     propio usuario elija qué variable analizar.

Este módulo sirve para que cualquier usuario con el archivo
`InsuranceCompany.csv` (o una versión similar, siempre que conserve la
columna `renewal`) pueda explorar por su cuenta los datos y llegar a sus
propias lecturas, sin necesidad de escribir código.

### 5. Despliegue en Streamlit Community Cloud

1. Sube este repositorio a tu cuenta de GitHub (público o accesible desde tu
   cuenta de Streamlit Cloud).
2. Ingresa a [share.streamlit.io](https://share.streamlit.io) e inicia sesión
   con tu cuenta de GitHub.
3. Haz clic en **"New app"**, selecciona el repositorio, la rama (`main`) y el
   archivo principal (`app.py`).
4. Haz clic en **"Deploy"**. Streamlit Cloud instalará automáticamente las
   dependencias listadas en `requirements.txt`.
5. Copia la URL generada (ej. `https://tu-usuario-insurance-eda.streamlit.app`)
   y agrégala en la sección de enlaces de este README y en el PDF final.

---

## 🖼️ Capturas de la app

<!--
  Pega aquí tus capturas de pantalla una vez que ejecutes o despliegues la
  app. Sugerencia: incluir al menos una del módulo Home, una de la carga del
  dataset, una de un ítem numérico, una de un ítem categórico y una de
  Hallazgos/Conclusiones. Ejemplo de sintaxis (descomentar y ajustar rutas):

  ![Home](ruta/a/tu/imagen_home.png)
  ![Carga del dataset](ruta/a/tu/imagen_carga.png)
  ![Ítem numérico](ruta/a/tu/imagen_item_numerico.png)
  ![Ítem categórico](ruta/a/tu/imagen_item_categorico.png)
  ![Hallazgos y conclusiones](ruta/a/tu/imagen_hallazgos.png)
-->

*(Espacio reservado — pega aquí tus capturas de pantalla)*

---

## 🔗 Enlaces relevantes

- **Repositorio GitHub:** `[PEGAR AQUÍ EL LINK DE TU REPOSITORIO]`
- **Aplicación desplegada (Streamlit Cloud):** `[PEGAR AQUÍ EL LINK DE TU APP]`

---

## 👤 Autor

- **Nombre completo:** David Sebastian Carlos Ipanaque
- **Especialización:** Python for Analytics
- **Año:** 2026

---

## 📊 Sobre el dataset

`InsuranceCompany.csv` contiene información histórica de clientes de una
compañía de seguros. La variable objetivo es `renewal` (1 = renovó la
póliza, 0 = no renovó).

| Variable | Descripción |
|---|---|
| `id` | Identificador único del cliente/póliza |
| `perc_premium_paid_by_cash_credit` | % de la prima pagada en efectivo/crédito |
| `age_in_days` | Edad del cliente en días |
| `age_years` *(derivada)* | Edad del cliente en años, calculada en la app |
| `Income` | Ingreso mensual del cliente |
| `Count_3-6_months_late` | Pagos demorados entre 3 y 6 meses |
| `Count_6-12_months_late` | Pagos demorados entre 6 y 12 meses |
| `Count_more_than_12_months_late` | Pagos demorados por más de 12 meses |
| `application_underwriting_score` | Puntaje de evaluación de riesgo del cliente |
| `no_of_premiums_paid` | Número total de primas pagadas |
| `sourcing_channel` | Canal de captación del cliente |
| `residence_area_type` | Tipo de área de residencia (Urbana/Rural) |
| `premium` | Valor monetario de la prima |
| `renewal` | Variable objetivo: 1 = renovó, 0 = no renovó |

---

## ⚠️ Alcance y limitaciones

Este proyecto tiene un enfoque **descriptivo**, no predictivo. Los hallazgos e
insights presentados corresponden a relaciones observadas en los datos
históricos y no deben interpretarse como relaciones causales.
