import streamlit as st
import pandas as pd

# Configuración del Búnker
st.set_page_config(page_title="Búnker Tracker Multi-Cliente", page_icon="🏢", layout="wide")
st.title("🏢 Tablero de Cumplimiento Regulatorio y Fiscal")
st.markdown("---")

# 1. Selector de Cliente
clientes = ["ALEPH", "MAXI CABLE", "TU RED 18", "DAYCO", "TCA SERVICES", "URBALINK"]
cliente_seleccionado = st.selectbox("🔍 Seleccione el Cliente Operativo:", clientes)

# 2. Alertas Específicas por Cliente
if cliente_seleccionado == "MAXI CABLE":
    st.error("🚨 ALERTA FINANCIERA: Carga Impositiva Nacional proyectada al **50.4%** de los ingresos brutos. Requiere revisión contable de escudos fiscales.")
elif cliente_seleccionado == "TU RED 18":
    st.warning("⚠️ ATENCIÓN: Conflicto actual con Alcaldía de Sucre (3% Actividades Económicas). Se recuerda que esto es competencia exclusiva del Departamento Contable, no de la gestión regulatoria.")

# 3. Base de Datos de Obligaciones (Basado en su listado maestro)
datos = {
    "Categoría": [
        "CONATEL", "CONATEL", "CONATEL", "CONATEL", "CONATEL",
        "ALCALDÍA", "SENIAT", "SENIAT", "SENIAT", "PARAFISCAL", "PARAFISCAL"
    ],
    "Impuesto / Contribución": [
        "Art. 146 LOTEL", "Art. 147 LOTEL", "Art. 150 LOTEL (Fondo Universal)", "Art. 151 LOTEL", "Art. 148 LOTEL",
        "Actividades Económicas (Ingreso Bruto)", "IVA Ventas", "Anticipo ISLR", "IGTF Ventas", "SSO (Seguro Social)", "FAOV"
    ],
    "Porcentaje": [
        "2,30%", "0,50%", "1,00%", "0,50%", "0,20% a 0,50%",
        "1% al 3%", "16%", "1%", "3%", "9% al 11%", "3%"
    ],
    "Periodicidad": [
        "Trimestral", "Trimestral", "Trimestral", "Trimestral", "Anual",
        "Mensual", "Quincenal", "Quincenal", "Quincenal", "Mensual", "Mensual"
    ],
    "Responsable de Gestión": [
        "BÚNKER (Regulatorio)", "BÚNKER (Regulatorio)", "BÚNKER (Regulatorio)", "BÚNKER (Regulatorio)", "BÚNKER (Regulatorio)",
        "Contabilidad Interna", "Contabilidad Interna", "Contabilidad Interna", "Contabilidad Interna", "RRHH / Administración", "RRHH / Administración"
    ],
    "Estatus Actual": [
        "Al Día", "Al Día", "Al Día", "Al Día", "Pendiente Declaración",
        "En Revisión", "Al Día", "Al Día", "Al Día", "Al Día", "Al Día"
    ]
}

df = pd.DataFrame(datos)

# 4. Filtros de visualización
st.subheader(f"📋 Matriz de Obligaciones para: {cliente_seleccionado}")
filtro = st.radio("Filtrar por Departamento Responsable:", ["Ver Todo", "Solo BÚNKER (CONATEL)", "Solo Contabilidad Interna"])

if filtro == "Solo BÚNKER (CONATEL)":
    df_mostrar = df[df["Responsable de Gestión"] == "BÚNKER (Regulatorio)"]
elif filtro == "Solo Contabilidad Interna":
    df_mostrar = df[df["Responsable de Gestión"].str.contains("Contabilidad|RRHH")]
else:
    df_mostrar = df

# Función para colorear
def colorear_responsable(val):
    if "BÚNKER" in str(val):
        return 'background-color: #e6f2ff; color: #004c99; font-weight: bold'
    elif "Contabilidad" in str(val) or "RRHH" in str(val):
        return 'background-color: #fff0f5; color: #800040'
    return ''

# Mostrar la tabla estilizada
st.dataframe(df_mostrar.style.map(colorear_responsable, subset=['Responsable de Gestión']), use_container_width=True)

# 5. Firma de límite de alcance
st.markdown("---")
st.info("💡 **Nota de Alcance del Servicio:** La Oficina Regulatoria garantiza el estricto cumplimiento y pago de los tributos de CONATEL (Aprox. 4.8%). La gestión, cálculo y liquidación de tributos nacionales (SENIAT), municipales (Alcaldías) y parafiscales son responsabilidad exclusiva del contador colegiado de la empresa operadora.")
