import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# 1. CONFIGURACIÓN INICIAL
st.set_page_config(page_title="DSR_LDK - GIGATEL", layout="wide")

# 2. BLINDAJE DE CACHÉ (Para no saturar Google Sheets)
@st.cache_data(ttl=600)
def cargar_datos(url):
    return pd.read_csv(url)

# Asegúrate de tener el logo de Gigatel en la misma carpeta con este nombre
ruta_logo = os.path.join(os.path.dirname(__file__), "LOGO_GIGATEL.png") 

# --- ¡PONGA EL GID DE GIGATEL AQUÍ! ---
# Reemplaza toda esta URL cuando tengas la nueva
URL_SHEET = "https://docs.google.com/spreadsheets/d/TU_ID_DE_DOCUMENTO_AQUI/export?format=csv&gid=1010668241"

try:
    df = cargar_datos(URL_SHEET)

    # --- EL RELOJITO ---
    porcentaje_raw = df.iloc[1, 3]
    valor_limpio = str(porcentaje_raw).replace(',', '.').replace('%', '').strip()
    porcentaje = float(valor_limpio)
    if porcentaje <= 1: porcentaje = porcentaje * 100

    # --- CABECERA ---
    if os.path.exists(ruta_logo):
        st.image(ruta_logo, width=90)
        st.markdown(f"### **GIGATEL (Telecomunicaciones RHJ, C.A.)**")
    else:
        st.markdown(f"# **GIGATEL (Telecomunicaciones RHJ, C.A.)**")
    
    st.caption("📍 Auditoría de Cumplimiento Regulatorio - LDK")
    st.divider() 

    # --- GRÁFICO ---
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = porcentaje,
        title = {'text': "Estado de Cumplimiento Regulatorio"},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 43], 'color': "red"},
                {'range': [43, 73], 'color': "yellow"},
                {'range': [73, 100], 'color': "green"}
            ],
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

    # --- PARCHE ANTICRASH Y LECTURA DE ASTERISCOS ---
    total_filas = len(df)
    
    # 🎯 PRIORIDADES DEL MES
    if total_filas > 85:
        titulo_p = df.iloc[85, 2]
        st.markdown(f"## 🎯 **{titulo_p}**")
        for i in range(7):
            if (86 + i) < total_filas:
                tarea = df.iloc[86 + i, 2]
                marca = df.iloc[86 + i, 0] # LECTURA DE LA COLUMNA A
                
                if pd.notna(tarea) and str(tarea).strip() != "":
                    # Si detecta el asterisco en la Columna A
                    if pd.notna(marca) and '*' in str(marca):
                        st.success(f"✅ ~~{i+1}. {tarea}~~ *(Validado por LDK)*")
                    else:
                        # Si no hay asterisco, muestra el checkbox normal
                        if st.checkbox(f"{i+1}. {tarea}", key=f"prio_{i}"):
                            st.info(f"✅ Recibido. Al validar esta evidencia, su cumplimiento subirá.")

    # 📋 OBLIGACIONES PERIÓDICAS
    if total_filas > 91:
        st.divider()
        titulo_o = df.iloc[95, 2]
        st.markdown(f"## 📋 **{titulo_o}**")
        for j in range(4):
            if (96 + j) < total_filas:
                reporte = df.iloc[96 + j, 2]
                marca_rep = df.iloc[96 + j, 0] # LECTURA DE LA COLUMNA A
                
                if pd.notna(reporte) and str(reporte).strip() != "":
                    # Si detecta el asterisco en la Columna A
                    if pd.notna(marca_rep) and '*' in str(marca_rep):
                        st.success(f"✅ ~~{reporte}~~ *(Validado por LDK)*")
                    else:
                        # Si no hay asterisco, muestra el checkbox normal
                        if st.checkbox(reporte, key=f"rep_{j}"):
                            st.info(f"✅ Recibido para revisión LDK.")

except Exception as e:
    st.error(f"Error de sincronización: {e}")

st.divider()

# Botón que limpia la memoria y fuerza la lectura de la hoja
if st.button("🔄 Sincronizar con Auditoría LDK"):
    st.cache_data.clear()
    st.rerun()
