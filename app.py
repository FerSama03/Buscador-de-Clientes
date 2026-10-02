import streamlit as st
import sqlite3
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Buscador de RUC y Clientes", page_icon="🔍", layout="wide")

#interruptor de contraseña
USAR_CONTRASEÑA = False  # Cambiar a False para desactivar la contraseña

# Define aquí la contraseña para ingresar
CONTRASEÑA_CORRECTA = "030607" 

# --- FUNCIÓN DE CONTROL DE ACCESO ---
def pedir_contrasena():
    if not USAR_CONTRASEÑA:
        return True  # No se requiere contraseña, permitir acceso
    
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.title("🔒 Acceso Restringido")
        st.subheader("Distribuidora Los Hermanos")
        
        clave_ingresada = st.text_input("Ingrese la contraseña de acceso:", type="password")
        
        if st.button("Ingresar"):
            if clave_ingresada == CONTRASEÑA_CORRECTA:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("❌ Contraseña incorrecta")
        return False
    return True

# --- CONTENIDO DE LA APLICACIÓN ---
if pedir_contrasena():
    st.title("DISTRIBUIDORA LOS HERMANOS")
    st.write("Bienvenido al buscador de Clientes. Aquí puedes encontrar rápidamente la información que necesitas.")
    st.write("Ingresa nombre del cliente para realizar la búsqueda instantánea.")

    # Botón para cerrar sesión si se desea
    with st.sidebar:
        if st.button("Cerrar sesión"):
            st.session_state.autenticado = False
            st.rerun()

    busqueda = st.text_input("Ingrese el Nombre del Cliente:", placeholder="Ej: Papilú o 4010750-7")

    if busqueda:
        conn = sqlite3.connect('clientes.db')
        
        query = """
            SELECT DISTINCT ruc AS 'RUC / CI', razon_social AS 'Cliente', zona AS 'Zona', direccion AS 'Dirección'
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
            st.warning("No se encontraron clientes que coincidan con la búsqueda.")
    else:
        st.info("Creador: Futuro Ing. L.F")
