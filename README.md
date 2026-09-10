# Proyecto_Final_PyFA_DSCI

## 👤 Autor

- **Nombre completo:** David Sebastian Carlos Ipanaque
- **Especialización:** Python for Analytics
- **Año:** 2026

---


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

- **Home:** presentación del proyecto (Introducción).
- **Caso de Estudio N°3:** carga del dataset y desarrollo del EDA, distribuido
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
| 9️⃣ Dinámico | Aplicación de Multiselect, cruce dinámico con `renewal` y filtro con slider/checkbox |
| 🔟 Hallazgos | Resumen e insights principales del EDA |
| 1️⃣1️⃣ Conclusiones | 5 conclusiones finales, redactadas y orientadas a decisiones |

Toda la lógica del EDA está desarrollada a partir de la clase `DataAnalyzer`
, ubicada en el código(`app.py`), aplicando Programación Orientada a Objetos (POO): estadística
descriptiva, detección de outliers, clasificación de variables, tablas de
nulos, conteos categóricos y tasas de renovación. Un conjunto separado de
**funciones auxiliares** se encarga del funcionamiento de la interfaz: carga/validación del CSV,
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

## ▶️ Instrucciones de ejecución

#### 🏠 Módulo "Home"

Es la pantalla de presentación del proyecto. **No requiere cargar ningún
archivo y no ejecuta ningún análisis.** Al ingresar aquí se observa:

- El título del trabajo y el logo de Python.
- La descripción del objetivo del análisis (qué se busca responder con el EDA).
- Los datos del autor (nombre completo, especialización y año).
- Una explicación general del dataset `InsuranceCompany.csv` y de la variable
  objetivo `renewal`.
- El listado de tecnologías utilizadas en el proyecto.

Este módulo es la **presentación/introducción del proyecto**.

#### 👤 Módulo "Caso de Estudio N°3"

Es el espacio donde se desarrolla el análisis. Al ingresar, el sidebar muestra
además el botón **"Seleccione su archivo"** (`st.file_uploader`), que exige
cargar el archivo `InsuranceCompany.csv`.

- **Mientras no se cargue un archivo**, la pantalla solo muestra un aviso
  pidiendo cargarlo: no se ejecuta ningún cálculo ni se muestra ningún dato.
- **Una vez cargado y validado el archivo** (se verifica que sea `.csv` y que
  contenga la columna `renewal`), la aplicación muestra, en orden:
  1. Un resumen con 4 métricas clave (registros, variables, renovaciones y
     tasa de renovación), una vista previa del dataset y sus dimensiones.
  2. **8 pestañas** con los 10 ítems del EDA y las conclusiones finales
     (detalladas en la tabla). Cada pestaña incluye
     texto explicativo, al menos una tabla o gráfico, y widgets interactivos
     (selectbox, multiselect, slider o checkbox) donde aplica, para que el
     propio usuario elija qué variable analizar.

Este módulo sirve para que cualquier usuario con el archivo
`InsuranceCompany.csv` (o una versión similar, siempre que conserve la
columna `renewal`) pueda explorar por su cuenta los datos y llegar a sus
propias lecturas, sin necesidad de escribir código.


---

## 🖼️ Capturas de la app

# Home
<!--
  ![Home](capturas/Home.png)
  ![Carga del dataset](capturas/Carga_Dataset.png)
  ![Ítem numérico](ruta/a/tu/imagen_item_numerico.png)
  ![Ítem categórico](ruta/a/tu/imagen_item_categorico.png)
  ![Hallazgos y conclusiones](ruta/a/tu/imagen_hallazgos.png)
-->

*(Espacio reservado — pega aquí tus capturas de pantalla)*

---

## 🔗 Enlaces relevantes

- **Repositorio GitHub:** `https://github.com/sebastiancarlos8/Proyecto_Final_PyFA_DSCI`
- **Aplicación (Streamlit Cloud):** `https://proyectofinalpyfadsci-c6xuwnardurhodxxe9zcpx.streamlit.app/`

---

