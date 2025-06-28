
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Control de Ganancias", layout="centered")
st.title("📊 Control de Ganancias Diarias de Arbitraje")

# Entradas del usuario
capital = st.number_input("Capital por operación (COP)", value=30000000, step=1000000)
tasa_compra = st.number_input("Tasa de cambio COP/USD", value=3900)
spread = st.number_input("Ganancia por dólar (spread)", value=50)
operaciones_dia = st.number_input("Operaciones por día", value=2)

# Parámetros fijos
fx_tax_rate = 0.004
gov_tax_rate = 0.15

# Cálculos
usd_comprados = capital / tasa_compra
cop_venta = usd_comprados * (tasa_compra + spread)
ganancia_bruta = cop_venta - capital
ganancia_bruta_dia = ganancia_bruta * operaciones_dia
impuesto_fx = (capital * operaciones_dia) * fx_tax_rate
impuesto_gob = ganancia_bruta_dia * gov_tax_rate
ganancia_neta_dia = ganancia_bruta_dia - impuesto_fx - impuesto_gob
ganancia_mensual = ganancia_neta_dia * 30

# Mostrar resultados
st.subheader("📅 Resultados diarios")
st.write(f"USD comprados por operación: {usd_comprados:,.2f}")
st.write(f"COP recibidos por venta total: {cop_venta * operaciones_dia:,.0f}")
st.write(f"Ganancia bruta diaria: {ganancia_bruta_dia:,.0f} COP")
st.write(f"Impuesto 4x1000: {impuesto_fx:,.0f} COP")
st.write(f"Impuesto gobierno (15%): {impuesto_gob:,.0f} COP")
st.success(f"Ganancia neta diaria: {ganancia_neta_dia:,.0f} COP")

st.subheader("📆 Resultado mensual estimado")
st.success(f"Ganancia neta mensual: {ganancia_mensual:,.0f} COP")

# Historial
if "registro" not in st.session_state:
    st.session_state.registro = []

if st.button("Guardar registro de hoy"):
    hoy = datetime.today().strftime("%Y-%m-%d")
    st.session_state.registro.append({
        "Fecha": hoy,
        "USD comprados": round(usd_comprados, 2),
        "COP recibido": round(cop_venta * operaciones_dia),
        "Ganancia bruta": round(ganancia_bruta_dia),
        "Impuesto 4x1000": round(impuesto_fx),
        "Impuesto Gobierno": round(impuesto_gob),
        "Ganancia neta": round(ganancia_neta_dia)
    })

if st.session_state.registro:
    df = pd.DataFrame(st.session_state.registro)
    st.subheader("📈 Historial de registros")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar historial en CSV", data=csv, file_name="registro_arbitraje.csv", mime="text/csv")
