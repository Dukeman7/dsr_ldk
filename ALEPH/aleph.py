import streamlit as st
from streamlit_gsheets import GSheetsConnection
import plotly.graph_objects as go

# Configuración de página para que luzca en la Yoga
st.set_page_config(page_title="DSR_LDK - ALEPH", layout="wide")

# 1. Conexión y Carga de Datos
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    url_sheet = st.secrets["connections"]["gsheets"]["spreadsheet"]
    
    # Leemos la data principal (Logo y Porcentaje)
    df_head = conn.read(spreadsheet=url_sheet, worksheet="ALEPH", usecols=[0, 1, 2, 3], nrows=5)
    
    # --- VARIABLES CRÍTICAS ---
    url_logo = df_head.iloc[0, 1]  # Celda A2 (ajustado según tu GSheet)
    # Porcentaje en D3 (Fila 2, Col 3). Convertimos a float.
    porcentaje = float(df_head.iloc[1, 3]) * 100 if float(df_head.iloc[1, 3]) <= 1 else float(df_head.iloc[1, 3])

    # --- INTERFAZ ---
    st.image(url_logo, width=150)
    
    # 2. El Relojito (Plotly Gauge)
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = porcentaje,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 43], 'color': "red"},
                {'range': [43, 73], 'color': "yellow"},
                {'range': [73, 100], 'color': "green"}
            ],
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

    # 3. Títulos Dinámicos y Prioridades
    # Leemos títulos de C87 y C93
    titulo_p = conn.read(spreadsheet=url_sheet, worksheet="ALEPH", usecols=[2], skiprows=86, nrows=1).iloc[0,0]
    titulo_o = conn.read(spreadsheet=url_sheet, worksheet="ALEPH", usecols=[2], skiprows=92, nrows=1).iloc[0,0]
    
    # Leemos la lista de prioridades (ajusta el skiprows si es necesario)
    df_prioridades = conn.read(spreadsheet=url_sheet, worksheet="ALEPH", skiprows=87, nrows=4)

    st.markdown(f"### 🎯 **{titulo_p}**")
    for i in range(len(df_prioridades)):
        tarea = df_prioridades.iloc[i, 0] # Asumiendo que el nombre está en la primera col leída
        if st.checkbox(f"Prioridad {i+1}: {tarea}"):
            st.info(f"Pendiente de validación por Ing. Juancho (LDK)")

    st.divider()

    st.markdown(f"### 📋 **{titulo_o}**")
    reportes = ["Remisión de precios", "Reporte de reclamos", "Despliegue", "Reunión LDK"]
    for rep in reportes:
        if st.checkbox(rep):
            st.markdown(f"~~{rep}~~ ✅")

except Exception as e:
    st.error(f"Falta configurar algo: {e}")
