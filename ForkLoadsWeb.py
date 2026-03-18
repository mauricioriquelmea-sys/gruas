import streamlit as st
from PIL import Image
import os

# Configuración de la página
st.set_page_config(page_title="Structural Lab | Cargas Portuarias", layout="wide")

def main():
    st.title("⚓ ESTIMACIÓN DE CARGAS DE MAQUINARIA PORTUARIA")
    st.markdown("---")

    # Contenedor Principal (Dos columnas)
    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.header("📋 Parámetros de Entrada")
        
        # Inputs del usuario
        wc = st.number_input("Carga Contenedor (Wc) [kg]:", value=30000.0, step=500.0)
        wt = st.number_input("Peso Cargador (Wt) [kg]:", value=50000.0, step=500.0)
        fd = st.number_input("Factor Dinámico (Fd):", value=1.20, step=0.05)
        m = st.number_input("Ruedas Eje Frontal (M):", value=4, step=1)
        
        st.subheader("Distancias Geométricas")
        x1 = st.number_input("Distancia X1 [m]:", value=1.50, step=0.1)
        x2 = st.number_input("Distancia X2 [m]:", value=-3.50, step=0.1)
        xt = st.number_input("Distancia XT [m]:", value=-1.00, step=0.1)

        if st.button("CALCULAR CARGAS", type="primary"):
            if x1 == x2:
                st.error("Error: X1 y X2 no pueden ser iguales (división por cero).")
            else:
                # Lógica de Cálculo (Ecuación 4.7)
                a1 = -x2 / (x1 - x2)
                a2 = -x1 / (x2 - x1)
                b1 = (wt * (xt - x2)) / (x1 - x2)
                b2 = (wt * (xt - x1)) / (x2 - x1)

                # Cargas Finales (Ecuación 4.6)
                w1 = fd * ((a1 * wc + b1) / m)
                w2 = fd * ((a2 * wc + b2) / 2)

                # Mostrar Resultados
                st.markdown("---")
                st.success("### Resultados Finales")
                st.metric(label="W1 (Carga Frontal por Rueda)", value=f"{w1:,.1f} kg")
                st.metric(label="W2 (Carga Trasera por Rueda)", value=f"{w2:,.1f} kg")

    with col2:
        st.info("💡 Esquema de Distribución de Cargas (Figura 4.2)")
        
        # Gestión de ruta de imagen para Streamlit Cloud
        img_path = "F1.jpg"
        if os.path.exists(img_path):
            image = Image.open(img_path)
            st.image(image, caption="Diagrama de referencia para distribución de cargas", use_container_width=True)
        else:
            st.warning(f"⚠️ No se encontró el archivo {img_path}. Asegúrate de subirlo a tu repositorio de GitHub.")

if __name__ == "__main__":
    main()