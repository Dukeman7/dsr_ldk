import datetime
import os
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="DSR_LDK - DAYCO", layout="wide")


# 2. BLINDAJE DE CACHÉ Y LECTURA CSV
@st.cache_data(ttl=600)
def cargar_datos(url):
  return pd.read_csv(url)


# Ruta del logo de Dayco
ruta_logo = os.path.join(os.path.dirname(__file__), "Logo_Dayco.png")

# --- URL DE EXPORTACIÓN CSV CON EL GID EXACTO DE DAYCO ---
URL_SHEET = "https://docs.google.com/spreadsheets/d/1GYEizLwSybQ9-ezFD1gPnSytQyaNF2DWiJrwKcR68V4/export?format=csv&gid=1597813868"

try:
  df = cargar_datos(URL_SHEET)

  # --- EL RELOJITO (Leyendo celda D2 -> fila 1, columna 3 en índice 0) ---
  porcentaje_raw = df.iloc[1, 3]
  valor_limpio = str(porcentaje_raw).replace(",", ".").replace("%", "").strip()
  porcentaje = float(valor_limpio)
  if porcentaje <= 1:
    porcentaje = porcentaje * 100

  # --- CABECERA ---
  if os.path.exists(ruta_logo):
    st.image(ruta_logo, width=150)
    st.markdown(f"### **DAYCO TELECOM, C.A.**")
  else:
    st.markdown(f"# **DAYCO TELECOM, C.A.**")

  st.caption("📍 Auditoría de Cumplimiento Regulatorio - LDK")
  st.divider()

  # --- GRÁFICO (GAUGE) ---
  fig = go.Figure(
      go.Indicator(
          mode="gauge+number",
          value=porcentaje,
          title={"text": "Estado de Cumplimiento Regulatorio"},
          gauge={
              "axis": {"range": [0, 100]},
              "bar": {"color": "black"},
              "steps": [
                  {"range": [0, 43], "color": "red"},
                  {"range": [43, 73], "color": "yellow"},
                  {"range": [73, 100], "color": "green"},
              ],
          },
      )
  )
  st.plotly_chart(fig, use_container_width=True)

  # --- PARCHE ANTICRASH Y LECTURA DE ASTERISCOS ---
  total_filas = len(df)

  # 🎯 PRIORIDADES DEL MES (Ajusta el índice base de la fila según corresponda en tu CSV de Dayco)
  # Si en el CSV de Dayco el título de prioridades está en otra fila, dime el número exacto
  fila_titulo_prio = (
      85  # Ajusta este número según la fila donde esté el título en Dayco
  )
  if total_filas > fila_titulo_prio:
    titulo_p = df.iloc[fila_titulo_prio, 2]
    st.markdown(f"## 🎯 **{titulo_p}**")
    for i in range(17):
      fila_item = (fila_titulo_prio + 1) + i
      if fila_item < total_filas:
        tarea = df.iloc[fila_item, 2]
        marca = df.iloc[fila_item, 0]  # LECTURA DE LA COLUMNA A

        if pd.notna(tarea) and str(tarea).strip() != "":
          if pd.notna(marca) and "*" in str(marca):
            st.success(f"✅ ~~{i+1}. {tarea}~~ *(Validado por LDK)*")
          else:
            if st.checkbox(
                f"{i+1}. {tarea}", key=f"dayco_prio_{i}"
            ):  # Key única para evitar choques
              st.info(
                  f"✅ Recibido. Al validar esta evidencia, su cumplimiento"
                  " subirá."
              )

  # 📋 OBLIGACIONES PERIÓDICAS
  fila_titulo_obli = (
      108  # Ajusta este número según la fila donde esté el título en Dayco
  )
  if total_filas > fila_titulo_obli:
    st.divider()
    titulo_o = df.iloc[fila_titulo_obli, 2]
    st.markdown(f"## 📋 **{titulo_o}**")
    for j in range(10):  # Rango de obligaciones periódicas
      fila_item_o = (fila_titulo_obli + 1) + j
      if fila_item_o < total_filas:
        reporte = df.iloc[fila_item_o, 2]
        marca_rep = df.iloc[fila_item_o, 0]  # LECTURA DE LA COLUMNA A

        if pd.notna(reporte) and str(reporte).strip() != "":
          if pd.notna(marca_rep) and "*" in str(marca_rep):
            st.success(f"✅ ~~{reporte}~~ *(Validado por LDK)*")
          else:
            if st.checkbox(
                reporte, key=f"dayco_rep_{j}"
            ):  # Key única para evitar choques
              st.info(f"✅ Recibido para revisión LDK.")

except Exception as e:
  st.error(f"Error de sincronización: {e}")

st.divider()

# Botón que limpia la memoria y fuerza la lectura de la hoja
if st.button("🔄 Sincronizar con Auditoría LDK", key="btn_sync_dayco_master"):
  st.cache_data.clear()
  st.rerun()
