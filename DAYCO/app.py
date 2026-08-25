import io
import os
import datetime
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

# ... (configuración y variables de fecha iguales)

# --- EL MOTOR BLINDADO ---


@st.cache_data(ttl=600)
def cargar_datos(url):
  import requests

  response = requests.get(url)
  # Leemos el contenido binario usando BytesIO y especificamos openpyxl explícitamente
  return pd.read_excel(io.BytesIO(response.content), sheet_name="DAYCO", engine='openpyxl')


URL_SHEET = "https://docs.google.com/spreadsheets/d/1GYEizLwSybQ9-ezFD1gPnSytQyaNF2DWiJrwKcR68V4/export?format=xlsx&gid=1597813868"

# El resto de tu código sigue exactamente igual...
