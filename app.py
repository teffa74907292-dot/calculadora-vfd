import streamlit as st
st.set_page_config(page_title="Calculadora de Ahorro VFD", page_icon="⚡")

st.title("⚡ Calculadora de Ahorro Energético con VFD")
st.write("Estima cuánto puedes ahorrar al pasar de un control por válvula a un Variador de Frecuencia.")

with st.sidebar:
    st.header("Parámetros del Sistema")
    potencia_hp = st.number_input("Potencia de la bomba (HP)", value=10.0)
    horas_anuales = st.number_input("Horas de operación al año", value=4000)
    costo_kwh = st.number_input("Costo de energía (USD/kWh)", value=0.12)
    eficiencia_motor = st.slider("Eficiencia del motor (%)", 70, 98, 90) / 100

st.subheader("Perfil de Carga")
st.info("¿A qué porcentaje de su capacidad total opera la bomba habitualmente?")
flujo_promedio = st.slider("Porcentaje de flujo promedio (%)", 10, 100, 70) / 100

# --- CÁLCULOS ---
# 1 HP = 0.746 kW
kw_nominales = (potencia_hp * 0.746) / eficiencia_motor

# Consumo sin VFD (asumiendo válvula de estrangulamiento, que ahorra poco)
# Estimación simplificada: el consumo baja linealmente con el flujo en válvulas
consumo_valvula = kw_nominales * (0.85 + 0.15 * flujo_promedio) * horas_anuales

# Consumo con VFD (Ley de Afinidad al cubo)
consumo_vfd = kw_nominales * (flujo_promedio**3) * horas_anuales

ahorro_kwh = consumo_valvula - consumo_vfd
ahorro_dinero = ahorro_kwh * costo_kwh

# --- RESULTADOS ---
col1, col2 = st.columns(2)
with col1:
    st.metric("Ahorro Anual (kWh)", f"{ahorro_kwh:,.2f}")
with col2:
    st.metric("Ahorro Anual (USD)", f"${ahorro_dinero:,.2f}")

st.success(f"¡Instalar un VFD reduciría tu consumo en un { (ahorro_kwh/consumo_valvula)*100:.1f} %!")
