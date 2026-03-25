import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="DSR_LDK - TU RED 18, C.A.", layout="wide")

# Buscador de logo a prueba de balas
ruta_logo = None
directorio_actual = os.path.dirname(__file__)
for archivo in os.listdir(directorio_actual):
    if archivo.lower() in ['logor.png', 'logor.jpg', 'logor.jpeg']:
        ruta_logo = os.path.join(directorio_actual, archivo)
        break

# --- PEGAR AQUÍ EL GID DE TR-18 ---
URL_SHEET = "https://docs.google.com/spreadsheets/d/1GYEizLwSybQ9-ezFD1gPnSytQyaNF2DWiJrwKcR68V4/export?format=csv&gid=985636361"

try:
    df = pd.read_csv(URL_SHEET)

    # El Relojito de la Verdad
    porcentaje_raw = df.iloc[1, 3]
    valor_limpio = str(porcentaje_raw).replace(',', '.').replace('%', '').strip()
    porcentaje = float(valor_limpio)
    if porcentaje <= 1: porcentaje = porcentaje * 100

    if ruta_logo:
        st.image(ruta_logo, width=90)
        st.markdown(f"### **TU RED 18, C.A.**")
    else:
        st.markdown(f"# **TU RED 18, C.A.**")
    
    st.caption("📍 Auditoría de Cumplimiento Regulatorio (CONATEL) - LDK")
    st.divider() 

    # Gráfico en modo Alerta Severa
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = porcentaje,
        title = {'text': "Nivel de Cumplimiento Regulatorio (ALERTA CRÍTICA)", 'font': {'color': "red"}},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkred"},
            'steps': [
                {'range': [0, 43], 'color': "#ffb3b3"}, # Fondo rojo claro de emergencia
                {'range': [43, 73], 'color': "yellow"},
                {'range': [73, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': porcentaje
            }
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.error("🚨 **ESTADO DE EMERGENCIA REGULATORIA** 🚨\nEl nivel de cumplimiento actual (29.1%) expone a la operadora a sanciones severas o revocatoria por parte de CONATEL. La gestión se encuentra paralizada por falta de entrega de recaudos.")

# ... (arriba de esto queda su relojito intacto) ...

    st.markdown("---")
    st.error("🚨 **ESTADO DE EMERGENCIA REGULATORIA** 🚨\nEl nivel de cumplimiento actual expone a la operadora a sanciones severas. La gestión se encuentra paralizada por falta de entrega de recaudos.")

    # --- 1. LAS 20 PRIORIDADES ---
    # Asumiendo que el título está en la Fila 87, Columna C (índice 85, 2) como en Aleph
    f_codigo_p = 85 
    col = 2 

    try:
        if f_codigo_p < len(df):
            titulo_p = df.iloc[f_codigo_p, col]
            st.markdown(f"## 🎯 **{titulo_p}** (Gestión Detenida)")
            
            # Aquí está la magia: escanea hasta 25 celdas hacia abajo buscando sus 20 tareas
            for i in range(25): 
                if (f_codigo_p + 1 + i) < len(df):
                    tarea = df.iloc[f_codigo_p + 1 + i, col] 
                    if pd.notna(tarea) and str(tarea).strip() != "":
                        st.error(f"❌ PENDIENTE POR EL CLIENTE: {tarea}") 
    except Exception:
        pass

    st.divider()

    # --- 2. LAS 4 OBLIGACIONES PERIÓDICAS ---
    # ¡ATENCIÓN COMANDANTE! Ponga aquí el número de fila real donde quedó este título en su Excel
    FILA_PERIODICAS = 110 # <--- ¡CAMBIE ESTE 110 POR LA FILA CORRECTA!
    f_codigo_o = FILA_PERIODICAS - 2

    try:
        if f_codigo_o < len(df):
            titulo_o = df.iloc[f_codigo_o, col]
            st.markdown(f"## 📋 **{titulo_o}**")
            for j in range(4):
                if (f_codigo_o + 1 + j) < len(df):
                    reporte = df.iloc[f_codigo_o + 1 + j, col]
                    if pd.notna(reporte) and str(reporte).strip() != "":
                        st.error(f"❌ REPORTE MENSUAL FALTANTE: {reporte}")
    except Exception:
        pass

except Exception as e:
    st.error(f"Error de sincronización con la base de datos de auditoría: {e}")
