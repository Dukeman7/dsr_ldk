import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# --- LÓGICA DE LOGO LOCAL ---
# Buscamos el archivo en la misma carpeta que el script
ruta_logo = os.path.join(os.path.dirname(__file__), "logo.png") 

if os.path.exists(ruta_logo):
    st.image(ruta_logo, width=150)
else:
    # Si el nombre es distinto (ejemplo: logo.jpg), ajusta la línea de arriba
    st.error(f"⚠️ No encontré el archivo '{ruta_logo}' en el repositorio.")
    st.info("Asegúrate de que el nombre del archivo coincida exactamente (mayúsculas/minúsculas).")
# Configuración para la pantalla táctil de la Yoga
st.set_page_config(page_title="DSR_LDK - ALEPH", layout="wide")

# URL de Exportación CSV (Asegúrate que el GID sea el de la pestaña ALEPH)
URL_SHEET = "https://docs.google.com/spreadsheets/d/1GYEizLwSybQ9-ezFD1gPnSytQyaNF2DWiJrwKcR68V4/export?format=csv&gid=958551789"

try:
    # Leemos todo el bloque de datos
    df = pd.read_csv(URL_SHEET)

    # --- 1. LIMPIEZA DEL PORCENTAJE (Celda D3 -> Fila 1, Col 3) ---
    porcentaje_raw = df.iloc[1, 3]
    valor_limpio = str(porcentaje_raw).replace(',', '.').replace('%', '').strip()
    porcentaje = float(valor_limpio)
    if porcentaje <= 1: porcentaje = porcentaje * 100

    # --- 2. TÍTULOS DINÁMICOS (C87 y C93) ---
    # Nota: skiprows en read_csv muerde filas, así que usamos el df ya cargado
    # C87 es Fila 85, Col 2 | C93 es Fila 91, Col 2 (ajustando por el header)
    titulo_p = df.iloc[85, 2]
    titulo_o = df.iloc[91, 2]

    # --- INTERFAZ ---
if os.path.exists(ruta_logo):
    st.image(ruta_logo, width=220)
else:
    # Si el logo falla, ponemos el nombre con fuerza
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

    # --- 3. PRIORIDADES DEL MES (Dinámicas desde la fila 87) ---
    st.markdown(f"## 🎯 **{titulo_p}**")
    
    # Leemos 4 tareas debajo de la fila 87 (Columna C)
    for i in range(4):
        tarea = df.iloc[86 + i, 2] # Empieza en C87
        if st.checkbox(f"{i+1}. {tarea}", key=f"prio_{i}"):
            st.info(f"✅ Recibido. Al validar esta evidencia, su cumplimiento subirá. (Pendiente revisión LDK)")

    st.divider()

    # --- 4. OBLIGACIONES PERIÓDICAS (Dinámicas desde la fila 93) ---
    st.markdown(f"## 📋 **{titulo_o}**")
    
    for j in range(4):
        reporte = df.iloc[92 + j, 2] # Empieza en C93
        if st.checkbox(reporte, key=f"rep_{j}"):
            st.markdown(f"~~{reporte}~~ ✅")
            st.caption("Aviso enviado al Ing. Juancho para revisión de soporte.")

except Exception as e:
    st.error(f"Error de sincronización: {e}")
    st.info("Revisa que el Google Sheet esté publicado como CSV y que las celdas C87/C93 tengan texto.")

# Botón de actualización manual para el cliente
if st.button("🔄 Sincronizar con Auditoría LDK"):
    st.rerun()
