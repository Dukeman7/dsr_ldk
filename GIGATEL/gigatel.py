import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import time

# 1. APP
st.set_page_config(page_title="DSR_LDK - GIGATEL", layout="wide")

# 2. RUTA DEL LOGO
ruta_logo = os.path.join(os.path.dirname(__file__), "LOGO_GIGATEL.png") 

# --- EL MOTOR BLINDADO ---
@st.cache_data(ttl=600)
def cargar_datos(url):
    # Forzamos la descarga del CSV limpio
    url_fresca = f"{url}&t={time.time()}"
    # engine='python' y on_bad_lines='skip' eliminan el error de las comillas
    return pd.read_csv(url_fresca, engine='python', on_bad_lines='skip')

# URL LIMPIA: Solo el ID y el GID
URL_SHEET = "https://docs.google.com/spreadsheets/d/1GYEizLwSybQ9-ezFD1gPnSytQyaNF2DWiJrwKcR68V4/export?format=csv&gid=1010668241"

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

    # --- LECTURA DE PRIORIDADES ---
    total_filas = len(df)
    if total_filas > 85:
        titulo_p = df.iloc[85, 2]
        st.markdown(f"## 🎯 **{titulo_p}**")
        for i in range(7):
            if (86 + i) < total_filas:
                tarea = df.iloc[86 + i, 2]
                marca = df.iloc[86 + i, 0]
                if pd.notna(tarea) and str(tarea).strip() != "":
                    if pd.notna(marca) and '*' in str(marca):
                        st.success(f"✅ ~~{i+1}. {tarea}~~ *(Validado por LDK)*")
                    else:
                        if st.checkbox(f"{i+1}. {tarea}", key=f"prio_{i}"):
                            st.info(f"✅ Recibido. Al validar esta evidencia, su cumplimiento subirá.")

    # --- LECTURA DE OBLIGACIONES ---
    if total_filas > 100:
        st.divider()
        titulo_o = df.iloc[100, 2]
        st.markdown(f"## 📋 **{titulo_o}**")
        for j in range(4):
            if (101 + j) < total_filas:
                reporte = df.iloc[101 + j, 2]
                marca_rep = df.iloc[101 + j, 0]
                if pd.notna(reporte) and str(reporte).strip() != "":
                    if pd.notna(marca_rep) and '*' in str(marca_rep):
                        st.success(f"✅ ~~{reporte}~~ *(Validado por LDK)*")
                    else:
                        if st.checkbox(reporte, key=f"rep_{j}"):
                            st.info(f"✅ Recibido para revisión LDK.")

except Exception as e:
    st.error(f"Error de sincronización: {e}")

st.divider()
if st.button("🔄 Sincronizar Sistema LDK"):
    st.cache_data.clear()
