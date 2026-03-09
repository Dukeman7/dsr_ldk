import streamlit as st
from streamlit_gsheets import GSheetsConnection

# 1. Conexión al Libro (Asegúrate de configurar secrets.toml con tu URL)
conn = st.connection("gsheets", type=GSheetsConnection)

# 1. Intenta forzar la lectura del secreto así:
url = st.secrets["connections"]["gsheets"]["spreadsheet"]
df_info = conn.read(spreadsheet=url, worksheet="ALEPH", usecols=[0, 1, 2, 3], nrows=5)

# 3. Leemos las Prioridades (Ajusta los índices según tu Excel)
# Asumiendo que las prioridades están en una sección fija abajo
df_prioridades = conn.read(worksheet="ALEPH", skiprows=20, nrows=10) 

# --- INTERFAZ EN LA YOGA ---
st.image(url_logo, width=150)

# Aquí va tu Dial/Relojito usando la variable 'porcentaje'
# ... (Código del Gauge de Plotly) ...
# 1. Extraemos el texto de las celdas específicas
# Celda C87 -> Fila 86, Columna 2 (C es la columna 2: A=0, B=1, C=2)
titulo_prioridades = conn.read(worksheet="ALEPH", usecols=[2], skiprows=86, nrows=1).iloc[0,0]

# Celda C93 -> Fila 92, Columna 2
titulo_obligaciones = conn.read(worksheet="ALEPH", usecols=[2], skiprows=92, nrows=1).iloc[0,0]

# 2. Los usamos en Streamlit
st.markdown(f"###🎯 **{titulo_prioridades}**")
# ... aquí tus checks de prioridades ...

st.markdown(f"###📋 **{titulo_obligaciones}**")
# ... aquí tus checks de obligaciones ...

for i in range(4):
    tarea = df_prioridades.iloc[i, 1] # Nombre de la prioridad
    if st.checkbox(f"{i+1}. {tarea}"):
        st.info(f"Pendiente de validación por Ing. Juancho (LDK)")

# st.subheader("📋 OBLIGACIONES PERIÓDICAS")
# Los 4 reportes que mencionaste
reportes = ["Remisión de precios", "Reporte de reclamos", "Despliegue", "Reunión LDK"]
for rep in reportes:
    if st.checkbox(rep):
        st.markdown(f"~~{rep}~~ ✅")
