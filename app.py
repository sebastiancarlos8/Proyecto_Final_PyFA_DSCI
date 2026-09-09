import streamlit as st
import numpy as np
import pandas as pd

st.sidebar.image("DMC.png", width = 100)
st.sidebar.title("Contenido")
modulos = st.sidebar.selectbox("Seleccione un módulo",["Home","Caso de Estudio N° X"])

if modulos == "Home":
  st.title("Trabajo Final - Módulo Python Fundamentals")
  st.image("Python_logo.png", width = 500)
  st.subheader("Descripción del objetivo del análisis")
  st.markdown("""xxxx""")
  st.subheader("Elaborado por")
  st.write("**Nombre completo:** David Sebastian Carlos Ipanaque")
  st.write("**Módulo:** 🐍 Especialización en Python for Analytics")
  st.write("**Año:** 2026")
  st.subheader("Información general del Dataset")
  st.markdown("""Egresado de la carrera de Ingeniería Industrial, con experiencia en analítica de datos en el sector retail, consumo masivo y seguros, dentro del área comercial y de recursos humanos. \nApasionado por la lógica, recursos humanos, uso de datos masivos y programación.""")
  st.subheader("🛠️ Tecnologías utilizadas")
  st.markdown("""Para el presente proyecto, se utilizaron las siguientes tecnologías.\n- 🔗 GitHub\n- 🎨 Streamlit\n- 🐍 Google Colab - Python\n- 🔢 NumPy\n- 🐼 Pandas\n- 📚 Librerías externas\n- 🧩 Programación Orientada a Objetos(POO)""")

else:
 st.title("👤 Caso de Estudio N° X")

 st.markdown("""xxxx.
    """)

 archivo = st.sidebar.file_uploader("Seleccione su archivo")

 if archivo is not None:
   st.write("Su archivo ha sido cargado")
  
   if archivo.name.endswith(".csv"):
    datos = pd.read_csv(archivo)
    st.write(datos)
      
   elif archivo.name.endswith(".xlsx"):
     datos = pd.read_excel(archivo)
     st.write(datos)
  
 else:
    st.write("Cargue su archivo")
