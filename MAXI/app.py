import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="DSR_LDK - MAXI CABLE, C.A.", layout="wide")

ruta_logo = os.path.join(os.path.dirname(__file__), "LOGO.png") 

# --- ¡PONGA EL GID DE MAXI CABLE AQUÍ! ---
URL_SHEET = "https://docs.google.com/spreadsheets/d/1GYEizLwSybQ9-ezFD1gPnSytQyaNF2DWiJrwKcR68V4/export?format=csv&gid=1984654544"

try:
    df = pd.read_csv(URL_SHEET)

    # El Relojito (Esto siempre funciona)
    porcentaje_raw = df.iloc[1, 3]
    valor_limpio = str(porcentaje_raw).replace(',', '.').replace('%', '').strip()
    porcentaje = float(valor_limpio)
    if porcentaje <= 1: porcentaje = porcentaje * 100

    if os.path.exists(ruta_logo):
        st.image(ruta_logo, width=90)
        st.markdown(f"### **MAXI CABLE, C.A.**")
    else:
        st.markdown(f"# **MAXI CABLE, C.A.**")
    
    st.caption("📍 Auditoría de Cumplimiento Regulatorio - LDK")
    st.divider() 

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

    # --- PARCHE ANTICRASH (Lee solo si las filas existen) ---
    total_filas = len(df)
    
    if total_filas > 85:
        titulo_p = df.iloc[85, 2]
        st.markdown(f"## 🎯 **{titulo_p}**")
        for i in range(7):
            if (86 + i) < total_filas:
                tarea = df.iloc[86 + i, 2]
                if pd.notna(tarea) and str(tarea).strip() != "":
                    if st.checkbox(f"{i+1}. {tarea}", key=f"prio_{i}"):
                        st.info(f"✅ Recibido. Al validar esta evidencia, su cumplimiento subirá.")

    if total_filas > 91:
        st.divider()
        titulo_o = df.iloc[91, 2]
        st.markdown(f"## 📋 **{titulo_o}**")
        for j in range(4):
            if (95 + j) < total_filas:
                reporte = df.iloc[95 + j, 2]
                if pd.notna(reporte) and str(reporte).strip() != "":
                    if st.checkbox(reporte, key=f"rep_{j}"):
                        st.markdown(f"~~{reporte}~~ ✅")

except Exception as e:
    st.error(f"Error de sincronización: {e}")

if st.button("🔄 Sincronizar con Auditoría LDK"):
    st.rerun()
