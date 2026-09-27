import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Buscador de RUC", page_icon="🔍", layout="wide")

st.title("DISTRIBUIDORA LOS HERMANOS")
st.write("Bienvenido al buscador de clientes. Aquí puedes encontrar rápidamente la información que necesitas.")

busqueda = st.text_input("Ingrese el Nombre del Cliente:", placeholder="Ej: Ferreteria, Autoservi, Masato, etc.")

if busqueda:
    conn = sqlite3.connect('clientes.db')
    
    # Se agrega DISTINCT para ignorar filas exactamente iguales
    query = """
        SELECT DISTINCT ruc AS 'RUC / CI', razon_social AS 'Cliente / Razón Social', zona AS 'Zona'
        FROM clientes 
        WHERE ruc LIKE ? OR razon_social LIKE ?
    """
    
    param = f"%{busqueda}%"
    df_resultados = pd.read_sql_query(query, conn, params=(param, param))
    conn.close()
    
    st.subheader(f"Resultados encontrados ({len(df_resultados)})")
    
    if not df_resultados.empty:
        st.dataframe(df_resultados, use_container_width=True)
    else:
        st.warning("No se encontraron clientes que coincidieron con la búsqueda.")
else:
    st.info("Este programa fue hecho y creado por L.F.")