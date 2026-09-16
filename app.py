import streamlit as st
import pandas as pd
from PIL import Image

# Configuración del sitio web
st.set_page_config(page_title="VendeTuNave - Catálogo", page_icon="🚗", layout="wide")

# Estilos CSS
st.markdown("""
    <style>
    .precio-tag {
        color: #1a73e8;
        font-size: 22px;
        font-weight: bold;
    }
    .cuota-estimada {
        color: #28a745;
        font-size: 14px;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar inventario en el estado de sesión para agregar vehículos dinámicamente
if "inventario" not in st.session_state:
    st.session_state.inventario = [
        {
            "id": 1,
            "titulo": "Mercedes Benz CLA 180 2020",
            "marca": "Mercedes Benz",
            "año": 2020,
            "precio": 110000000,
            "km": 53000,
            "ciudad": "Ibagué",
            "combustible": "Gasolina",
            "caja": "Automática",
            "foto": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=600"
        },
        {
            "id": 2,
            "titulo": "BMW X4 M40i 2021",
            "marca": "BMW",
            "año": 2021,
            "precio": 195000000,
            "km": 55600,
            "ciudad": "Cali",
            "combustible": "Gasolina",
            "caja": "Automática",
            "foto": "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=600"
        }
    ]

# ENCABEZADO
st.title("🚗 VendeTuNave - Publica y Encuentra tu Vehículo")
st.write("Gestiona e inspecciona publicaciones de vehículos en tiempo real.")
st.divider()

# Pestañas de la aplicación: Ver Catálogo vs Cargar Vehículo
tab_catalogo, tab_subir = st.tabs(["📌 Ver Catálogo", "➕ Publicar Nuevo Vehículo"])

# PESTAÑA 1: CATÁLOGO DE VEHÍCULOS
with tab_catalogo:
    df_inventario = pd.DataFrame(st.session_state.inventario)
    
    st.sidebar.header("🔍 Buscar Vehículo")
    marcas = ["Todas"] + sorted(list(df_inventario["marca"].unique()))
    marca_sel = st.sidebar.selectbox("Marca:", marcas)
    
    df_filtrado = df_inventario.copy()
    if marca_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado["marca"] == marca_sel]
        
    if not df_filtrado.empty:
        cols = st.columns(3)
        for idx, row in df_filtrado.reset_index(drop=True).iterrows():
            col_idx = idx % 3
            with cols[col_idx]:
                st.image(row["foto"], use_column_width=True)
                st.subheader(row["titulo"])
                
                precio_fmt = f"$ {row['precio']:,} COP"
                cuota_aprox = f"$ {int(row['precio'] * 0.0168):,} COP / mes aprox."
                
                st.markdown(f"<div class='precio-tag'>{precio_fmt}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='cuota-estimada'>🏦 Cuota est.: {cuota_aprox}</div><br>", unsafe_allow_html=True)
                
                st.write(f"📅 **Año:** {row['año']} — 🛣️ **Km:** {row['km']:,}")
                st.write(f"📍 **{row['ciudad']}** | {row['combustible']} | {row['caja']}")
                
                num_whatsapp = "573001234567"
                msj = f"Hola, vi en la web el vehículo {row['titulo']} de $ {row['precio']:,} COP y quiero más información."
                url_wa = f"https://wa.me/{num_whatsapp}?text={msj.replace(' ', '%20')}"
                st.link_button("📲 Contactar por WhatsApp", url_wa, use_container_width=True)
                st.write("---")

# PESTAÑA 2: FORMULARIO PARA CARGAR IMÁGENES Y DATOS
with tab_subir:
    st.header("Cargar Nuevo Vehículo al Inventario")
    
    with st.form("form_publicar", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            titulo = st.text_input("Título de la publicación:", placeholder="Ej: Renault Duster 2.0 2018")
            marca = st.text_input("Marca:", placeholder="Ej: Renault")
            precio = st.number_input("Precio ($ COP):", min_value=1000000, step=500000)
            km = st.number_input("Kilometraje:", min_value=0, step=1000)
            
        with col2:
            año = st.number_input("Año:", min_value=1990, max_value=2027, value=2021)
            ciudad = st.text_input("Ciudad:", placeholder="Ej: Medellín")
            caja = st.selectbox("Transmisión:", ["Automática", "Mecánica"])
            combustible = st.selectbox("Combustible:", ["Gasolina", "Diésel", "Híbrido", "Eléctrico"])
        
        # Módulo para subir la imagen directamente desde la Galería o Archivos
        imagen_subida = st.file_uploader("Selecciona la foto del vehículo (JPG, PNG, JPEG):", type=["jpg", "png", "jpeg"])
        
        guardar = st.form_submit_button("🚀 Guardar y Publicar Vehículo")
        
        if guardar:
            if titulo and marca and imagen_subida is not None:
                # Procesar la imagen subida directamente
                img = Image.open(imagen_subida)
                
                nuevo_vehiculo = {
                    "id": len(st.session_state.inventario) + 1,
                    "titulo": titulo,
                    "marca": marca,
                    "año": año,
                    "precio": precio,
                    "km": km,
                    "ciudad": ciudad,
                    "combustible": combustible,
                    "caja": caja,
                    "foto": img
                }
                
                st.session_state.inventario.append(nuevo_vehiculo)
                st.success(f"¡El vehículo '{titulo}' fue cargado exitosamente al catálogo!")
            else:
                st.error("Por favor completa los campos principales y adjunta una foto antes de publicar.")
