import datetime
import io
import os
import plotly.graph_objects as go
import pandas as pd
import requests
import streamlit as st

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="DSR_LDK - DAYCO", layout="wide")

# 2. RUTA DEL LOGO
ruta_logo = os.path.join(os.path.dirname(__file__), "Logo_Dayco.png")

# --- OBTENER EL MES EN CURSO DINÁMICAMENTE EN ESPAÑOL ---
meses_es = {
    1: "ENERO",
    2: "FEBRERO",
    3: "MARZO",
    4: "ABRIL",
    5: "MAYO",
    6: "JUNIO",
    7: "JULIO",
    8: "AGOSTO",
    9: "SEPTIEMBRE",
    10: "OCTUBRE",
    11: "NOVIEMBRE",
    12: "DICIEMBRE",
}
mes_actual = meses_es[datetime.datetime.now().month]

# --- EL MOTOR BLINDADO CON BYTESIO Y OPENPYXL ---


@st.cache_data(ttl=600)
def cargar_datos(url):
  response = requests.get(url)
  # Forzamos explícitamente el nombre de la pestaña en mayúsculas o tal como la tengas en el Excel
  return pd.read_excel(
      io.BytesIO(response.content), sheet_name="DAYCO", engine="openpyxl"
  )


URL_SHEET = "https://docs.google.com/spreadsheets/d/1GYEizLwSybQ9-ezFD1gPnSytQyaNF2DWiJrwKcR68V4/export?format=xlsx"

try:
  df = cargar_datos(URL_SHEET)

 # --- EL RELOJITO (Leyendo exactamente la celda D2) ---
  try:
    # D2 corresponde a la fila 0, columna 3 en Pandas (A=0, B=1, C=2, D=3)
    porcentaje_raw = df.iloc[0, 3] if pd.notna(df.iloc[0, 3]) else 29.7
    valor_limpio = (
        str(porcentaje_raw).replace(",", ".").replace("%", "").strip()
    )
    porcentaje = float(valor_limpio)
    if porcentaje <= 1:
      porcentaje = porcentaje * 100
  except:
    porcentaje = 33.7  # Valor seguro de respaldo

  # --- CABECERA ---
  if os.path.exists(ruta_logo):
    st.image(ruta_logo, width=150)
    st.markdown("### **DAYCO TELECOM, C.A.**")
  else:
    st.markdown("# **DAYCO TELECOM, C.A.**")

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

  # --- BÚSQUEDA INTELIGENTE DE SECCIONES ---
  df_str = df.astype(str)

  patron_prio = f"PRIORIDADES DEL MES DE {mes_actual}"
  idx_prio = df_str[
      df_str.apply(
          lambda row: row.astype(str).str.contains(patron_prio, case=False).any(),
          axis=1,
      )
  ].index

  if len(idx_prio) == 0:
    idx_prio = df_str[
        df_str.apply(
            lambda row: row.astype(str)
            .str.contains("PRIORIDADES", case=False)
            .any(),
            axis=1,
        )
    ].index

  idx_obli = df_str[
      df_str.apply(
          lambda row: row.astype(str)
          .str.contains("OBLIGACIONES PERIÓDICAS", case=False)
          .any(),
          axis=1,
      )
  ].index

  # --- LECTURA DE PRIORIDADES ---
  if len(idx_prio) > 0:
    fila_p = idx_prio[0]
    titulo_p = f"PRIORIDADES DEL MES DE {mes_actual}"
    st.markdown(f"## 🎯 **{titulo_p}**")

    for i in range(1, 10):
      sig_fila = fila_p + i
      if sig_fila < len(df):
        tarea = df.iloc[sig_fila, 2] if df.shape[1] > 2 else None
        marca = df.iloc[sig_fila, 1] if df.shape[1] > 1 else None
        if (
            pd.notna(tarea)
            and str(tarea).strip() != ""
            and "OBLIGACIONES" not in str(tarea)
        ):
          checkbox_key = f"chk_prio_unique_row_{sig_fila}"
          if pd.notna(marca) and "*" in str(marca):
            st.success(f"✅ ~~{i}. {tarea}~~ *(Validado por LDK)*")
          else:
            if st.checkbox(f"{i}. {tarea}", key=checkbox_key):
              st.info(
                  f"✅ Recibido. Al validar esta evidencia, su cumplimiento"
                  " subirá."
              )

  # --- LECTURA DE OBLIGACIONES ---
  if len(idx_obli) > 0:
    st.divider()
    fila_o = idx_obli[0]
    titulo_o = df.iloc[fila_o, 2] if df.shape[1] > 2 else "OBLIGACIONES PERIÓDICAS"
    st.markdown(f"## 📋 **{titulo_o}**")

    for j in range(1, 6):
      sig_fila_o = fila_o + j
      if sig_fila_o < len(df):
        reporte = df.iloc[sig_fila_o, 2] if df.shape[1] > 2 else None
        marca_rep = df.iloc[sig_fila_o, 1] if df.shape[1] > 1 else None
        if pd.notna(reporte) and str(reporte).strip() != "":
          checkbox_key_obli = f"chk_obli_unique_row_{sig_fila_o}"
          if pd.notna(marca_rep) and "*" in str(marca_rep):
            st.success(f"✅ ~~{reporte}~~ *(Validado por LDK)*")
          else:
            if st.checkbox(reporte, key=checkbox_key_obli):
              st.info(f"✅ Recibido para revisión LDK.")

except Exception as e:
  st.error(f"Error de sincronización con el motor LDK: {e}")

# --- DEPURACIÓN RÁPIDA (Comenta esto luego cuando ya lo veas) ---
with st.expander("🔍 Ver contenido de la tabla (Diagnóstico LDK)"):
  st.write(df.head(25))  # Muestra las primeras 25 filas del Excel

st.divider()
# Botón único con key forzada para evitar el choque de IDs
if st.button(
    "🔄 Sincronizar Sistema LDK", key="btn_sincronizar_ldk_master_unique"
):
  st.cache_data.clear()
  st.rerun()
