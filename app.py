import base64
from io import BytesIO
import pandas as pd
from PIL import Image
import streamlit as st

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="AutoMarket Colombia - Compra y Venta",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. ESTILOS CSS PERSONALIZADOS (Diseño Profesional)
st.markdown(
    """
    <style>
    /* Estilo general y tipografía */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Encabezado */
    .hero-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
    }

    /* Tarjeta de Vehículo */
    .card-container {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 1.5rem;
    }
    .card-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #0f172a;
        margin-top: 0.5rem;
        margin-bottom: 0.25rem;
    }
    .price-tag {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2563eb;
    }
    .badge-city {
        background-color: #f1f5f9;
        color: #475569;
        padding: 0.25rem 0.6rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    .cuota-info {
        font-size: 0.85rem;
        color: #16a34a;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .spec-text {
        font-size: 0.9rem;
        color: #64748b;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# 3. FUNCIONES AUXILIARES
def img_to_base64(image):
    """Convierte un objeto de imagen PIL a string Base64 para almacenar de forma segura."""
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return f"data:image/jpeg;base64,{base64.b64encode(buffered.getvalue()).decode()}"


# 4. DATOS DE INICIALIZACIÓN (Inventario Base)
if "inventario" not in st.session_state:
    st.session_state.inventario = [
        {
            "id": 1,
            "titulo": "Mazda CX-30 2.0 Grand Touring",
            "marca": "Mazda",
            "año": 2022,
            "precio": 108000000,
            "km": 24000,
            "ciudad": "Bogotá",
            "combustible": "Gasolina",
            "caja": "Automática",
            "placa": "9",
            "foto": "https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=600",
            "descripcion": "Único dueño, mantenimientos al día en concesionario. Cojinería en cuero, techo corredizo y excelente estado estético.",
        },
        {
            "id": 2,
            "titulo": "Toyota Hilux 2.8 4x4 Diesel",
            "marca": "Toyota",
            "año": 2021,
            "precio": 195000000,
            "km": 42000,
            "ciudad": "Medellín",
            "combustible": "Diésel",
            "caja": "Mecánica",
            "placa": "3",
            "foto": "https://images.unsplash.com/photo-1559416523-140ddc3d238c?w=600",
            "descripcion": "Camioneta en impecables condiciones. Llantas nuevas, duraliner, carpa plana y nunca chocado.",
        },
        {
            "id": 3,
            "titulo": "BMW Serie 3 320i Executive",
            "marca": "BMW",
            "año": 2020,
            "precio": 125000000,
            "km": 38000,
            "ciudad": "Cali",
            "combustible": "Gasolina",
            "caja": "Automática",
            "placa": "5",
            "foto": "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=600",
            "descripcion": "Sedán de lujo, motor 2.0 Turbo, pantalla multimedia táctil, sensores 360° y modos de manejo configurables.",
        },
    ]

# 5. ENCABEZADO PRINCIPAL (Hero Section)
st.markdown(
    """
    <div class="hero-header">
        <div class="hero-title">🚗 AutoMarket Colombia</div>
        <div class="hero-subtitle">Plataforma integral de compra y venta de vehículos verificados.</div>
    </div>
""",
    unsafe_allow_html=True,
)

# 6. ESTRUCTURA DE NAVEGACIÓN
tab_catalogo, tab_publicar = st.tabs(
    ["🔎 Catálogo de Vehículos", "➕ Publicar Mi Vehículo"]
)

# -----------------------------------------------------------------------------
# PESTAÑA 1: CATÁLOGOS Y BÚSQUEDA
# -----------------------------------------------------------------------------
with tab_catalogo:
    df_inv = pd.DataFrame(st.session_state.inventario)

    # BARRA LATERAL - FILTROS
    st.sidebar.header("🎯 Filtros de Búsqueda")

    # Filtro por Marca
    marcas_opt = ["Todas"] + sorted(list(df_inv["marca"].unique()))
    marca_sel = st.sidebar.selectbox("Marca", marcas_opt)

    # Filtro por Ciudad
    ciudades_opt = ["Todas"] + sorted(list(df_inv["ciudad"].unique()))
    ciudad_sel = st.sidebar.selectbox("Ciudad", ciudades_opt)

    # Filtro por Presupuesto
    precio_max_val = int(df_inv["precio"].max())
    precio_sel = st.sidebar.slider(
        "Presupuesto Máximo ($ COP)",
        min_value=10000000,
        max_value=precio_max_val,
        value=precio_max_val,
        step=5000000,
    )

    # Filtro por Transmisión
    caja_opt = st.sidebar.multiselect(
        "Transmisión",
        options=df_inv["caja"].unique(),
        default=df_inv["caja"].unique(),
    )

    # APLICAR FILTROS
    df_filtered = df_inv.copy()
    if marca_sel != "Todas":
        df_filtered = df_filtered[df_filtered["marca"] == marca_sel]
    if ciudad_sel != "Todas":
        df_filtered = df_filtered[df_filtered["ciudad"] == ciudad_sel]

    df_filtered = df_filtered[
        (df_filtered["precio"] <= precio_sel)
        & (df_filtered["caja"].isin(caja_opt))
    ]

    # DESPLIEGUE DEL INVENTARIO
    st.write(
        f"Se encontraron **{len(df_filtered)}** vehículos disponibles según tus criterios:"
    )

    if not df_filtered.empty:
        # Rejilla en 3 columnas
        cols = st.columns(3)

        for idx, row in df_filtered.reset_index(drop=True).iterrows():
            with cols[idx % 3]:
                st.markdown('<div class="card-container">', unsafe_allow_html=True)

                # Mostrar Imagen (Soporta URL o carga local Base64)
                st.image(row["foto"], use_column_width=True)

                # Datos Básicos
                st.markdown(
                    f'<div class="card-title">{row["titulo"]}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<span class="badge-city">📍 {row["ciudad"]}</span>',
                    unsafe_allow_html=True,
                )

                # Formato Monetario y Cuota Estimada
                precio_fmt = f"$ {row['precio']:,} COP".replace(",", ".")
                cuota_est = (
                    f"$ {int(row['precio'] * 0.017):,} COP".replace(",", ".")
                )

                st.markdown(
                    f'<div class="price-tag">{precio_fmt}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="cuota-info">🏦 Cuota aprox.: {cuota_est} /mes</div>',
                    unsafe_allow_html=True,
                )

                # Ficha Resumida
                st.markdown(
                    f"""
                    <div class="spec-text">
                        📅 <b>Año:</b> {row['año']}<br>
                        🛣️ <b>Kilometraje:</b> {row['km']:,} km<br>
                        ⚙️ <b>Caja:</b> {row['caja']} | ⛽ <b>Combustible:</b> {row['combustible']}<br>
                        🔢 <b>Placa termina en:</b> {row['placa']}
                    </div>
                """.replace(
                        ",", "."
                    ),
                    unsafe_allow_html=True,
                )

                st.write("")

                # Integración WhatsApp Comercial
                telefono_asesor = "573001234567"  # Cambiar por tu línea oficial
                mensaje_wa = f"Hola, me interesa el vehículo {row['titulo']} con precio de {precio_fmt}. ¿Sigue disponible?"
                url_whatsapp = f"https://wa.me/{telefono_asesor}?text={mensaje_wa.replace(' ', '%20')}"

                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    st.link_button(
                        "📲 WhatsApp", url_whatsapp, use_container_width=True
                    )
                with col_b2:
                    # Pop-up de detalles ampliados
                    with st.popover("📋 Detalles"):
                        st.markdown(f"### {row['titulo']}")
                        st.write(f"**Descripción:** {row['descripcion']}")
                        st.write(f"**Ciudad de venta:** {row['ciudad']}")
                        st.write(
                            f"**Último dígito de placa:** {row['placa']}"
                        )

                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info(
            "No se encontraron vehículos con los filtros aplicados. Intenta ampliar el rango de presupuesto o cambiar las opciones."
        )

# -----------------------------------------------------------------------------
# PESTAÑA 2: FORMULARIO DE CARGA
# -----------------------------------------------------------------------------
with tab_publicar:
    st.header("📋 Publica tu Vehículo")
    st.write(
        "Ingresa la información técnica de tu carro y sube una fotografía desde tu dispositivo."
    )

    with st.form("form_nuevo_vehiculo", clear_on_submit=True):
        f_col1, f_col2 = st.columns(2)

        with f_col1:
            titulo = st.text_input(
                "Título de la publicación*",
                placeholder="Ej. Chevrolet Onix 1.0 Turbo 2022",
            )
            marca = st.text_input("Marca*", placeholder="Ej. Chevrolet")
            precio = st.number_input(
                "Precio ($ COP)*", min_value=5000000, value=35000000, step=1000000
            )
            km = st.number_input(
                "Kilometraje actual*", min_value=0, value=45000, step=1000
            )
            ciudad = st.text_input("Ciudad de ubicación*", placeholder="Ej. Bucaramanga")

        with f_col2:
            año = st.number_input(
                "Año modelo*", min_value=1980, max_value=2027, value=2021
            )
            caja = st.selectbox("Transmisión*", ["Automática", "Mecánica", "Tiptronic"])
            combustible = st.selectbox(
                "Combustible*", ["Gasolina", "Diésel", "Híbrido", "Eléctrico"]
            )
            placa = st.text_input(
                "Último dígito de la placa*", max_chars=1, placeholder="Ej. 4"
            )

        descripcion = st.text_area(
            "Descripción detallada del estado técnico y equipamiento:",
            placeholder="Mencionante SOAT, tecno, estado de llantas, único dueño, etc.",
        )

        # Módulo Cargar Imagen
        imagen_archivo = st.file_uploader(
            "Fotografía del vehículo (JPG, PNG)*:", type=["jpg", "jpeg", "png"]
        )

        btn_guardar = st.form_submit_button("🚀 Guardar y Publicar en la App")

        if btn_guardar:
            if titulo and marca and ciudad and placa and imagen_archivo is not None:
                # Procesar imagen cargada
                img_pil = Image.open(imagen_archivo)
                img_base64 = img_to_base64(img_pil)

                nuevo_auto = {
                    "id": len(st.session_state.inventario) + 1,
                    "titulo": titulo,
                    "marca": marca,
                    "año": int(año),
                    "precio": int(precio),
                    "km": int(km),
                    "ciudad": ciudad,
                    "combustible": combustible,
                    "caja": caja,
                    "placa": placa,
                    "foto": img_base64,
                    "descripcion": descripcion
                    if descripcion
                    else "Sin descripción adicional.",
                }

                st.session_state.inventario.append(nuevo_auto)
                st.success(
                    f"¡El vehículo **'{titulo}'** ha sido cargado con éxito en el catálogo público!"
                )
            else:
                st.error(
                    "Por favor completa todos los campos requeridos (*) y sube una imagen del vehículo."
                )
