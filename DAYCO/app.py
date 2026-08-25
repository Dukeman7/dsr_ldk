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


ruta_logo = os.path.join(os.path.dirname(__file__), "Logo_Dayco.png")

# --- URL DE EXPORTACIÓN CSV CON EL GID EXACTO DE DAYCO ---
URL_SHEET = "https://docs.google.com/spreadsheets/d/1GYEizLwSybQ9-ezFD1gPnSytQyaNF2DWiJrwKcR68V4/export?format=csv&gid=1597813868"

try:
  df = cargar_datos(URL_SHEET)

  # --- EL RELOJITO (Leyendo celda D2 -> fila 1, columna 3) ---
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

  # --- BÚSQUEDA INTELIGENTE DINÁMICA (Sin importar el número de fila) ---
  df_str = df.astype(str)

  # Buscar fila que contenga PRIORIDADES
  idx_prio = df_str[
      df_str.apply(
          lambda row: row.astype(str)
          .str.contains("PRIORIDADES", case=False)
          .any(),
          axis=1,
      )
  ].index

  # Buscar fila que contenga OBLIGACIONES
  idx_obli = df_str[
      df_str.apply(
          lambda row: row.astype(str)
          .str.contains("OBLIGACIONES", case=False)
          .any(),
          axis=1,
      )
  ].index

  total_filas = len(df)

  # 🎯 PRIORIDADES DEL MES
  if len(idx_prio) > 0:
    fila_p = idx_prio[0]
    titulo_p = df.iloc[fila_p, 2] if df.shape[1] > 2 else "PRIORIDADES"
    st.markdown(f"## 🎯 **{titulo_p}**")

    for i in range(1, 20):  # Rango seguro de elementos
      sig_fila = fila_p + i
      if sig_fila < total_filas:
        tarea = df.iloc[sig_fila, 2] if df.shape[1] > 2 else None
        marca = df.iloc[sig_fila, 0] if df.shape[1] > 0 else None  # Columna A

        if (
            pd.notna(tarea)
            and str(tarea).strip() != ""
            and "OBLIGACIONES" not in str(tarea).upper()
        ):
          if pd.notna(marca) and "*" in str(marca):
            st.success(f"✅ ~~{i}. {tarea}~~ *(Validado por LDK)*")
          else:
            if st.checkbox(f"{i}. {tarea}", key=f"dayco_prio_dyn_{sig_fila}"):
              st.info(
                  f"✅ Recibido. Al validar esta evidencia, su cumplimiento"
                  " subirá."
              )

  # 📋 OBLIGACIONES PERIÓDICAS
  if len(idx_obli) > 0:
    st.divider()
    fila_o = idx_obli[0]
    titulo_o = df.iloc[fila_o, 2] if df.shape[1] > 2 else "OBLIGACIONES"
    st.markdown(f"## 📋 **{titulo_o}**")

    for j in range(1, 25):  # Rango seguro de elementos
      sig_fila_o = fila_o + j
      if sig_fila_o < total_filas:
        reporte = df.iloc[sig_fila_o, 2] if df.shape[1] > 2 else None
        marca_rep = df.iloc[sig_fila_o, 0] if df.shape[1] > 0 else None  # Columna A

        if pd.notna(reporte) and str(reporte).strip() != "":
          if pd.notna(marca_rep) and "*" in str(marca_rep):
            st.success(f"✅ ~~{reporte}~~ *(Validado por LDK)*")
          else:
            if st.checkbox(
                reporte, key=f"dayco_obli_dyn_{sig_fila_o}"
            ):  # Key única
              st.info(f"✅ Recibido para revisión LDK.")

except Exception as e:
  st.error(f"Error de sincronización: {e}")

st.divider()

if st.button("🔄 Sincronizar con Auditoría LDK", key="btn_sync_dayco_dyn"):
  st.cache_data.clear()
  st.rerun()
