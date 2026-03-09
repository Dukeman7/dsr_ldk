import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuración de página
st.set_page_config(page_title="DSR_LDK - ALEPH", layout="wide")

# URL DIRECTA (Sustituimos el uso de Secrets)
URL_SHEET = "https://docs.google.com/spreadsheets/d/1GYEizLwSybQ9-ezFD1gPnSytQyaNF2DWiJrwKcR68V4/export?format=csv&gid=958551789"

try:
    # Leemos la data usando Pandas directo (más rápido y evita el error del conector)
    df = pd.read_csv(URL_SHEET)
    
    # --- VARIABLES SEGÚN TU EXCEL ---
    # Logo en A2 (Fila 0 de datos si hay header, columna A)
    url_logo = "TU_URL_RAW_DE_GITHUB_AQUI" # Ponla fija aquí por ahora para asegurar
    
    # Porcentaje en D3. En Pandas, si D3 es la celda: 
    # Fila 1 (porque la 0 es el header), Columna 'D' (o índice 3)
    # Ajusta los índices según veas tu tabla
    porcentaje_raw = df.iloc[1, 3] 
    porcentaje = float(porcentaje_raw) * 100 if float(porcentaje_raw) <= 1 else float(porcentaje_raw)

    # --- INTERFAZ ---
    st.image(url_logo, width=150)
    
    # El Relojito
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = porcentaje,
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

    # Títulos Dinámicos (Leídos por posición)
    # Nota: Tendrás que ajustar estos índices según cómo Pandas lea tu hoja
    st.markdown(f"### 🎯 PRIORIDADES DE MARZO")
    # ... resto del código ...

except Exception as e:
    st.error(f"Error al conectar: {e}")
