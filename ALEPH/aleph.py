import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# 1. ESTO SIEMPRE VA DE PRIMERO
st.set_page_config(page_title="DSR_LDK - ALEPH", layout="wide")

# 2. RUTA DEL LOGO
ruta_logo = os.path.join(os.path.dirname(__file__), "logo.png") 

# URL de Exportación CSV
URL_SHEET = "https://docs.google.com/spreadsheets/d/1GYEizLwSybQ9-ezFD1gPnSytQyaNF2DWiJrwKcR68V4/export?format=csv&gid=958551789"

try:
    # Leemos todo el bloque de datos
    df = pd.read_csv(URL_SHEET)

    # --- 1. LIMPIEZA DEL PORCENTAJE ---
    porcentaje_raw = df.iloc[1, 3]
    valor_limpio = str(porcentaje_raw).replace(',', '.').replace('%', '').strip()
    porcentaje = float(valor_limpio)
    if porcentaje <= 1: porcentaje = porcentaje * 100

    # --- 2. TÍTULOS DINÁMICOS ---
    titulo_p = df.iloc[85, 2]
    titulo_o = df.iloc[91, 2]

    # --- INTERFAZ ---
    if os.path.exists(ruta_logo):
        st.image(ruta_logo, width=220)
    else:
        st.markdown(f"# **ALEPH NETWORKS, C.A.**") 
        st.caption("📍 Auditoría de Cumplimiento Regulatorio - LDK")

    # EL RELOJITO
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

    # --- 3. PRIORIDADES DEL MES ---
    st.markdown(f"## 🎯 **{titulo_p}**")
    for i in range(4):
        tarea = df.iloc[86 + i, 2]
        if st.checkbox(f"{i+1}. {tarea}", key=f"prio_{i}"):
            st.info(f"✅ Recibido. Al validar esta evidencia, su cumplimiento subirá.")

    st.divider()

    # --- 4. OBLIGACIONES PERIÓDICAS ---
    st.markdown(f"## 📋 **{titulo_o}**")
    for j in range(4):
        reporte = df.iloc[92 + j, 2]
        if st.checkbox(reporte, key=f"rep_{j}"):
            st.markdown(f"~~{reporte}~~ ✅")

except Exception as e:
    st.error(f"Error de sincronización: {e}")

# Botón de actualización
if st.button("🔄 Sincronizar con Auditoría LDK"):
    st.rerun()
