import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import datetime

st.set_page_config(page_title="DSR_LDK - TU RED 18, C.A.", layout="wide")

# Buscador de logo a prueba de balas
ruta_logo = None
directorio_actual = os.path.dirname(__file__)
for archivo in os.listdir(directorio_actual):
    if archivo.lower() in ['logor.png', 'logor.jpg', 'logor.jpeg']:
        ruta_logo = os.path.join(directorio_actual, archivo)
        break

# --- URL TÁCTICA EN TIEMPO REAL (BYPASS CACHÉ GOOGLE) ---
URL_SHEET = "https://docs.google.com/spreadsheets/d/1GYEizLwSybQ9-ezFD1gPnSytQyaNF2DWiJrwKcR68V4/gviz/tq?tqx=out:csv&gid=985636361"

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

    # --- MENSAJE DE ALERTA CORREGIDO (Una sola vez) ---
    st.markdown("---")
    st.error("🚨 **ESTADO DE EMERGENCIA REGULATORIA** 🚨\nEl nivel de cumplimiento actual expone a la operadora a sanciones severas o revocatoria por parte de CONATEL. La gestión se encuentra paralizada por falta de entrega de recaudos.")

    # --- RELOJ INTERNO PARA EL MES DINÁMICO EN ESPAÑOL ---
    meses_esp = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    mes_actual = meses_esp[datetime.date.today().month - 1]

    # Definición de Columnas en Python (A=0, B=1, C=2)
    COL_MARCADOR = 0 
    COL_NUMERO = 1   
    COL_TEXTO = 2    

    # --- 1. LAS 20 PRIORIDADES ---
    f_codigo_p = 85 # Fila 87 de Excel

    try:
        if f_codigo_p < len(df):
            st.markdown(f"## 🎯 **Prioridades del Mes ({mes_actual})**")
            
            for i in range(20): 
                fila = f_codigo_p + 1 + i
                if fila < len(df):
                    marcador = df.iloc[fila, COL_MARCADOR]
                    numero = df.iloc[fila, COL_NUMERO]
                    tarea = df.iloc[fila, COL_TEXTO] 
                    
                    if pd.notna(tarea) and str(tarea).strip() != "":
                        # Limpiar el número (por si Pandas le pone un .0)
                        num_str = f"{str(numero).replace('.0', '')}. " if pd.notna(numero) and str(numero).strip() != "" else ""
                        
                        # Lógica del Asterisco arreglada
                        if pd.notna(marcador) and '*' in str(marcador):
                            st.success(f"✅ COMPLETADO: ~~{num_str}{tarea}~~ *(Validado por LDK)*")
                        else:
                            st.error(f"❌ PENDIENTE POR EL CLIENTE: {num_str}{tarea}") 
    except Exception:
        pass

    st.divider()

    # --- 2. LAS 4 OBLIGACIONES PERIÓDICAS ---
    FILA_PERIODICAS = 110 # <--- ¡RECUERDE CAMBIAR ESTO POR LA FILA REAL EN SU EXCEL!
    f_codigo_o = FILA_PERIODICAS - 2

    try:
        if f_codigo_o < len(df):
            st.markdown(f"## 📋 **Obligaciones Periódicas Asesor ({mes_actual})**")
            
            for j in range(4):
                fila_o = f_codigo_o + 1 + j
                if fila_o < len(df):
                    marcador_o = df.iloc[fila_o, COL_MARCADOR]
                    reporte = df.iloc[fila_o, COL_TEXTO]
                    
                    if pd.notna(reporte) and str(reporte).strip() != "":
                        # ¡AQUÍ ESTABA EL ERROR! Ahora lee 'marcador_o'
                        if pd.notna(marcador_o) and '*' in str(marcador_o):
                            st.success(f"✅ ~~{reporte}~~ *(Validado por LDK)*")
                        else:
                            # ¡AQUÍ ESTABA LA INDENTACIÓN ROTA!
                            if st.checkbox(reporte, key=f"rep_{j}"):
                                st.info(f"✅ Recibido para revisión LDK.")

    except Exception:
        pass

except Exception as e:
    st.error(f"Error de sincronización con la base de datos de auditoría: {e}")

# --- BOTÓN DE ACTUALIZACIÓN RESTAURADO ---
st.divider()
if st.button("🔄 Sincronizar Sistema LDK"):
    st.rerun()
