# =========================================================
# BLOQUE 1 / 5 — Conexión + Configuración inicial + Login
# =========================================================
# ⚽ ScoutingApp Profesional v2 — Conectada a Google Sheets
# =========================================================
# - Carga directa desde "Scouting_DB" (Jugadores / Informes / Lista corta)
# - Login por roles (admin / scout / viewer)
# - Diseño oscuro #0a1a14 + acento #5a9a7c
# =========================================================

# ----------------------
# 📦 IMPORTS GENERALES
# ----------------------
import os
import base64
import re
import unicodedata
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

from io import BytesIO
from datetime import date, datetime, timedelta
from textwrap import dedent
from fpdf import FPDF
from st_aggrid import AgGrid, GridOptionsBuilder
import matplotlib.patches as patches
import gspread
from google.oauth2.service_account import Credentials
import requests
from PIL import Image
from ui.style import load_custom_css
from ui.components import section_header, section_note


def render_html_block(content: str):
    st.markdown(dedent(content).strip(), unsafe_allow_html=True)


def section_header(title, eyebrow=None, caption=None, centered=False):
    target = st
    if centered:
        left, middle, right = st.columns([1, 2.4, 1])
        target = middle

    if eyebrow:
        target.caption(str(eyebrow).upper())

    target.subheader(title)

st.set_page_config(
    page_title="ScoutingApp Profesional",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 🎨 HELPER VISUAL — PLOTLY GLASS (ANTI FONDO NEGRO)
# =========================================================
def apply_glass_plotly(fig):
    """
    Aplica un layout transparente y coherente con el diseño
    glass/futurista de la app.
    Elimina el fondo negro/blanco por defecto de Plotly.
    """
    titulo_actual = ""
    if getattr(fig.layout, "title", None) and getattr(fig.layout.title, "text", None):
        titulo_actual = fig.layout.title.text

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="rgba(255,255,255,0.92)",
            size=12,
            family="Manrope, sans-serif"
        ),
        title=dict(
            text=titulo_actual,
            font=dict(size=18, color="#ffffff", family="Sora, sans-serif"),
            x=0,
            xanchor="left"
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            font=dict(color="rgba(226,236,231,0.86)", size=11),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hoverlabel=dict(
            bgcolor="rgba(10,26,20,0.96)",
            bordercolor="rgba(90,154,124,0.38)",
            font=dict(color="#ffffff", family="Manrope, sans-serif")
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)",
            zeroline=False,
            showline=True,
            linecolor="rgba(255,255,255,0.08)",
            tickfont=dict(color="rgba(226,236,231,0.74)")
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)",
            zeroline=False,
            showline=False,
            tickfont=dict(color="rgba(226,236,231,0.74)")
        ),
        margin=dict(l=20, r=20, t=56, b=20)
    )
    return fig


# =========================================================
# BLOQUE DE CONEXIÓN A GOOGLE SHEETS (FINAL - SEGURO Y MULTIUSUARIO)
# =========================================================

import os, json, time
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
from datetime import datetime, timedelta

# --- CONFIGURACIÓN GENERAL ---
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
SHEET_ID = "1UU96mYjfLLBZt7vCkhEAe5pNJ0P2e9bp9eIggosZB-g"
CREDS_PATH = os.path.join("credentials", "credentials.json")

# =========================================================
# CONEXIÓN
# =========================================================
@st.cache_resource(show_spinner=False)
def conectar_sheets():
    try:
        if "GOOGLE_SERVICE_ACCOUNT_JSON" in st.secrets:
            creds_dict = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT_JSON"])
            creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
        else:
            if not os.path.exists(CREDS_PATH):
                st.error("❌ Falta credentials.json o secreto en Streamlit Cloud.")
                st.stop()
            creds = Credentials.from_service_account_file(CREDS_PATH, scopes=SCOPE)

        client = gspread.authorize(creds)
        return client.open_by_key(SHEET_ID)
    except Exception as e:
        st.error(f"⚠️ No se pudo conectar con Google Sheets: {e}")
        st.stop()


def normalizar_nombre_hoja(nombre):
    if nombre is None:
        return ""
    texto = unicodedata.normalize("NFKD", str(nombre).strip())
    texto = "".join(char for char in texto if not unicodedata.combining(char))
    texto = re.sub(r"\s+", " ", texto)
    return texto.casefold()


@st.cache_data(ttl=300, show_spinner=False)
def listar_hojas_disponibles():
    return [ws.title for ws in conectar_sheets().worksheets()]


# =========================================================
# OBTENER O CREAR HOJA
# =========================================================
def obtener_hoja(nombre_hoja: str, columnas_base: list = None):
    try:
        book = conectar_sheets()
        hojas = listar_hojas_disponibles()
        nombre_normalizado = normalizar_nombre_hoja(nombre_hoja)
        hojas_normalizadas = {
            normalizar_nombre_hoja(titulo): titulo for titulo in hojas
        }

        titulo_real = hojas_normalizadas.get(nombre_normalizado)
        if titulo_real:
            return book.worksheet(titulo_real)

        if nombre_hoja not in hojas:
            ws = book.add_worksheet(title=nombre_hoja, rows=500, cols=20)
            if columnas_base:
                ws.append_row(columnas_base)
            listar_hojas_disponibles.clear()
            st.warning(f"⚠️ Hoja '{nombre_hoja}' creada automáticamente.")
            return ws
        return book.worksheet(nombre_hoja)
    except Exception as e:
        st.error(f"⚠️ Error al obtener hoja '{nombre_hoja}': {e}")
        st.stop()


def col_letter(n: int) -> str:
    """Convierte un índice 1-based a la letra(s) correspondiente de columna (A, B, ..., Z, AA, AB...)."""
    s = ""
    while n > 0:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


# =========================================================
# CARGAR DATOS (con caché para evitar relogin + lecturas repetidas)
# =========================================================
@st.cache_data(ttl=120, show_spinner=False)
def cargar_datos_sheets(
    nombre_hoja: str,
    columnas_base: list = None,
    conservar_texto: bool = False,
) -> pd.DataFrame:
    try:
        ws = obtener_hoja(nombre_hoja, columnas_base)
        if conservar_texto:
            valores = ws.get_all_values()
            if valores:
                encabezados = valores[0]
                filas = valores[1:]
                df = pd.DataFrame(filas, columns=encabezados)
            else:
                df = pd.DataFrame(columns=columnas_base or [])
        else:
            data = ws.get_all_records()
            df = pd.DataFrame(data)
        if df.empty and columnas_base:
            df = pd.DataFrame(columns=columnas_base)
        return df
    except Exception as e:
        st.error(f"⚠️ Error al cargar '{nombre_hoja}': {e}")
        return pd.DataFrame(columns=columnas_base or [])


# =========================================================
# ACTUALIZAR HOJA (BLINDADA - SIN BORRAR)
# =========================================================
def actualizar_hoja(nombre_hoja: str, df: pd.DataFrame):
    """
    Actualiza sin borrar datos previos.
    Si existe el ID, actualiza esa fila. Si no, la agrega.
    Nunca borra toda la hoja.
    """
    try:
        ws = obtener_hoja(nombre_hoja, list(df.columns))
        data_actual = ws.get_all_records()
        df_actual = pd.DataFrame(data_actual)

        # Si la hoja está vacía, crea desde cero
        if df_actual.empty:
            ws.update([df.columns.values.tolist()] + df.values.tolist())
            st.toast(f"✅ Hoja '{nombre_hoja}' creada y actualizada.", icon="💾")
            return

        # Detectar columna de ID
        id_col = None
        for posible in ["ID_Jugador", "ID_Informe"]:
            if posible in df.columns:
                id_col = posible
                break

        # Fusión segura sin borrar
        if id_col:
            df_actual[id_col] = df_actual[id_col].astype(str)
            df[id_col] = df[id_col].astype(str)
            df_fusion = pd.concat([df_actual, df]).drop_duplicates(subset=[id_col], keep="last")
        else:
            df_fusion = pd.concat([df_actual, df]).drop_duplicates(keep="last")

        # Convertir todos los valores numpy.int64 a int antes de subir
        df_fusion = df_fusion.applymap(lambda x: int(x) if isinstance(x, np.integer) else x)

        # Subir a Sheets
        ws.update([df_fusion.columns.values.tolist()] + df_fusion.values.tolist())
        st.toast(f"💾 '{nombre_hoja}' actualizada correctamente (sin borrar datos).", icon="✅")

    except Exception as e:
        st.error(f"⚠️ Error al actualizar '{nombre_hoja}': {e}")


# =========================================================
# ELIMINAR FILA SEGURA (CONTROLADO)
# =========================================================
def eliminar_por_id(nombre_hoja: str, id_col: str, id_valor):
    """
    Elimina una fila específica por ID, sin tocar el resto.
    """
    try:
        ws = obtener_hoja(nombre_hoja)
        data_actual = ws.get_all_records()
        df = pd.DataFrame(data_actual)
        if id_col not in df.columns:
            st.error(f"⚠️ La hoja '{nombre_hoja}' no tiene la columna '{id_col}'.")
            return
        df = df[df[id_col].astype(str) != str(id_valor)]
        ws.update([df.columns.values.tolist()] + df.values.tolist())
        st.success(f"🗑️ Registro con {id_col}={id_valor} eliminado correctamente.")
    except Exception as e:
        st.error(f"⚠️ Error al eliminar en '{nombre_hoja}': {e}")


# =========================================================
# AGREGAR FILA NUEVA (SEGURA)
# =========================================================
def agregar_fila(nombre_hoja: str, fila: list):
    """Agrega una nueva fila sin tocar el resto."""
    try:
        ws = obtener_hoja(nombre_hoja)
        # Convertir todos los valores numpy.int64 a int antes de agregar
        fila = [int(x) if isinstance(x, np.integer) else x for x in fila]
        ws.append_row(fila, value_input_option="USER_ENTERED")
        st.toast(f"🟢 Nueva fila agregada en '{nombre_hoja}'.", icon="🟢")
        st.cache_data.clear()
    except Exception as e:
        st.error(f"⚠️ Error al agregar fila en '{nombre_hoja}': {e}")


# =========================================================
# BOTÓN MANUAL DE REFRESCO
# =========================================================
def boton_refrescar_datos():
    st.markdown("---")
    if st.button("🔄 Actualizar datos (refrescar desde Google Sheets)"):
        st.cache_data.clear()
        st.rerun()

# =========================================================
# CONFIGURACIÓN INICIAL DE LA APP
# =========================================================


# =========================================================
# ARCHIVOS LOCALES (usuarios y cancha)
# =========================================================
FILE_USERS = "usuarios.csv"
CANCHA_IMG = "CANCHA.png"

if not os.path.exists(FILE_USERS):
    st.error("⚠️ Falta el archivo usuarios.csv con columnas: Usuario,Contraseña,Rol")
    st.stop()

df_users = pd.read_csv(FILE_USERS)
if not all(col in df_users.columns for col in ["Usuario", "Contraseña", "Rol"]):
    st.error("El archivo usuarios.csv debe tener columnas: Usuario,Contraseña,Rol")
    st.stop()

# =========================================================
# BLOQUE DE LOGIN CON ROLES
# =========================================================
def autenticar_usuario(usuario, clave):
    match = df_users[(df_users["Usuario"] == usuario) & (df_users["Contraseña"] == clave)]
    if match.empty:
        return None
    return match.iloc[0]


def login_ui():
    if "user" not in st.session_state:
        st.session_state["user"] = None
        st.session_state["role"] = None

    if st.session_state["user"]:
        return True

    render_html_block("<div class='alab-login-top-spacer'></div>")

    render_html_block(
        """
        <div class="alab-login-hero">
            <div class="alab-login-kicker">Plataforma de scouting</div>
            <h1 class="alab-login-title">ScoutingApp Profesional</h1>
            <p class="alab-login-copy">
                Ingresá al entorno de seguimiento, shortlist e informes con la misma identidad visual
                que ya vive dentro de la app.
            </p>
            <div class="alab-login-chip-row">
                <span class="alab-dashboard-chip"><strong>Base</strong> Jugadores + informes</span>
                <span class="alab-dashboard-chip"><strong>Acceso</strong> Roles por usuario</span>
                <span class="alab-dashboard-chip"><strong>Flujo</strong> Scouting operativo</span>
            </div>
        </div>
        """
    )

    render_html_block("<div class='alab-login-section-gap'></div>")

    info_col, form_col = st.columns([1.05, 0.95], gap="large")

    with info_col:
        render_html_block(
            """
            <div class="alab-login-sidecard">
                <div class="alab-login-sidecard-title">Acceso centralizado</div>
                <p class="alab-login-sidecard-copy">
                    Consultá jugadores, revisá informes, seguí prioridades y mové decisiones de shortlist
                    sin salir del mismo entorno.
                </p>
                <div class="alab-login-bullet-list">
                    <span class="alab-login-bullet">Seguimiento por roles</span>
                    <span class="alab-login-bullet">Paneles y métricas unificadas</span>
                    <span class="alab-login-bullet">Carga y consulta sobre Google Sheets</span>
                </div>
            </div>
            """
        )

    with form_col:
        render_html_block(
            """
            <div class="alab-login-form-head">
                <div class="alab-login-form-title">Acceso a la plataforma</div>
                <p class="alab-login-form-copy">
                    Ingresá con tu usuario y contraseña para entrar al entorno de trabajo.
                </p>
            </div>
            """
        )

        with st.form("login_form_main"):
            usuario = st.text_input("Usuario", key="login_usuario_main", placeholder="Tu usuario")
            clave = st.text_input("Contraseña", type="password", key="login_clave_main", placeholder="Tu contraseña")
            enviar = st.form_submit_button("Ingresar", use_container_width=True)

    if enviar:
        usuario_validado = autenticar_usuario(usuario, clave)
        if usuario_validado is not None:
            st.session_state["user"] = usuario_validado["Usuario"]
            st.session_state["role"] = usuario_validado["Rol"]
            st.rerun()
        st.error("Usuario o contraseña incorrectos")
    return False
# =========================================================
# INICIALIZACIÓN DE USUARIO Y ROL GLOBAL
# =========================================================

# Siempre mostrar el bloque de login/acceso de usuario en la barra lateral
load_custom_css()
login_success = login_ui()
if not login_success:
    st.stop()

CURRENT_USER = st.session_state["user"]
CURRENT_ROLE = st.session_state["role"]

st.sidebar.title("🔐 Acceso de usuario")
st.sidebar.markdown("---")
st.sidebar.markdown(f"<b>Usuario:</b> {CURRENT_USER}", unsafe_allow_html=True)
st.sidebar.markdown(f"<b>Rol:</b> {CURRENT_ROLE}", unsafe_allow_html=True)
if st.sidebar.button("Cerrar sesión"):
    st.session_state["user"] = None
    st.session_state["role"] = None
    for clave in ["df_players", "df_reports", "df_short"]:
        st.session_state.pop(clave, None)
    st.rerun()


def inicializar_datasets_sesion():
    if all(
        clave in st.session_state
        for clave in ["df_players", "df_reports", "df_short"]
    ):
        return

    df_players, df_reports, df_short = cargar_datos()
    if "nombre_wyscout" not in df_players.columns:
        df_players["nombre_wyscout"] = ""

    st.session_state["df_players"] = df_players.copy()
    st.session_state["df_reports"] = df_reports.copy()
    st.session_state["df_short"] = df_short.copy()

def calcular_edad(fecha_nac):
    try:
        fn = datetime.strptime(str(fecha_nac), "%d/%m/%Y")
        hoy = date.today()
        return hoy.year - fn.year - ((hoy.month, hoy.day) < (fn.month, fn.day))
    except Exception:
        return "?"


def generar_id_unico(df, columna="ID_Jugador"):
    if columna not in df.columns or df.empty:
        return 1
    ids = df[columna].dropna().astype(str)
    nums = [int(i) for i in ids if i.isdigit()]
    return max(nums) + 1 if nums else 1


POSICION_ESTADISTICAS_CLAVE = {
    "Arquero": [
        ("Goles recibidos / 90", ["Goles_recibidos/90", "Goles_recibidos_90"]),
        ("Remates en contra / 90", ["Remates_en_contra/90", "Remates_en_contra_90"]),
        ("Porcentaje de paradas", ["Paradas"]),
        (
            "Porterías imbatidas / 90",
            ["Porterías_imbatidas_en_los_90", "Porterias_imbatidas_en_los_90"],
        ),
    ],
    "Defensa central derecho": [
        ("Duelos defensivos ganados", ["Duelos_defensivos_ganados"]),
        ("Duelos aéreos ganados", ["Duelos_aéreos_ganados", "Duelos_aereos_ganados"]),
        ("Interceptaciones / 90", ["Interceptaciones/90", "Interceptaciones_90"]),
        ("Precisión de pases", ["Precisión_pases", "Precision_pases"]),
        (
            "Precisión de pases largos",
            ["Precisión_pases_largos", "Precision_pases_largos"],
        ),
    ],
    "Defensa central izquierdo": [
        ("Duelos defensivos ganados", ["Duelos_defensivos_ganados"]),
        ("Duelos aéreos ganados", ["Duelos_aéreos_ganados", "Duelos_aereos_ganados"]),
        ("Interceptaciones / 90", ["Interceptaciones/90", "Interceptaciones_90"]),
        ("Precisión de pases", ["Precisión_pases", "Precision_pases"]),
        (
            "Precisión de pases largos",
            ["Precisión_pases_largos", "Precision_pases_largos"],
        ),
    ],
    "Lateral derecho": [
        ("Duelos defensivos ganados", ["Duelos_defensivos_ganados"]),
        ("Duelos aéreos ganados", ["Duelos_aéreos_ganados", "Duelos_aereos_ganados"]),
        ("Interceptaciones / 90", ["Interceptaciones/90", "Interceptaciones_90"]),
        ("Precisión de pases", ["Precisión_pases", "Precision_pases"]),
        (
            "Precisión de pases largos",
            ["Precisión_pases_largos", "Precision_pases_largos"],
        ),
    ],
    "Lateral izquierdo": [
        ("Duelos defensivos ganados", ["Duelos_defensivos_ganados"]),
        ("Duelos aéreos ganados", ["Duelos_aéreos_ganados", "Duelos_aereos_ganados"]),
        ("Interceptaciones / 90", ["Interceptaciones/90", "Interceptaciones_90"]),
        ("Precisión de pases", ["Precisión_pases", "Precision_pases"]),
        (
            "Precisión de pases largos",
            ["Precisión_pases_largos", "Precision_pases_largos"],
        ),
    ],
    "Mediocampista defensivo": [
        ("Duelos defensivos ganados", ["Duelos_defensivos_ganados"]),
        ("Interceptaciones / 90", ["Interceptaciones/90", "Interceptaciones_90"]),
        ("Precisión de pases", ["Precisión_pases", "Precision_pases"]),
        (
            "Precisión de pases largos",
            ["Precisión_pases_largos", "Precision_pases_largos"],
        ),
        ("Duelos ofensivos ganados", ["Duelos_atacantes_ganados"]),
    ],
    "Mediocampista mixto": [
        ("Duelos defensivos ganados", ["Duelos_defensivos_ganados"]),
        ("Interceptaciones / 90", ["Interceptaciones/90", "Interceptaciones_90"]),
        ("Precisión de pases", ["Precisión_pases", "Precision_pases"]),
        (
            "Precisión de pases largos",
            ["Precisión_pases_largos", "Precision_pases_largos"],
        ),
        ("Duelos ofensivos ganados", ["Duelos_atacantes_ganados"]),
    ],
    "Mediocampista ofensivo": [
        ("Duelos defensivos ganados", ["Duelos_defensivos_ganados"]),
        ("Interceptaciones / 90", ["Interceptaciones/90", "Interceptaciones_90"]),
        ("Precisión de pases", ["Precisión_pases", "Precision_pases"]),
        (
            "Precisión de pases largos",
            ["Precisión_pases_largos", "Precision_pases_largos"],
        ),
        ("Duelos ofensivos ganados", ["Duelos_atacantes_ganados"]),
    ],
    "Extremo derecho": [
        ("Duelos ofensivos ganados", ["Duelos_atacantes_ganados"]),
        ("Regates exitosos", ["Regates_realizados"]),
        ("Precisión de pases", ["Precisión_pases", "Precision_pases"]),
        (
            "Precisión de pases largos",
            ["Precisión_pases_largos", "Precision_pases_largos"],
        ),
        ("Precisión de centros", ["Precisión_centros", "Precision_centros"]),
    ],
    "Extremo izquierdo": [
        ("Duelos ofensivos ganados", ["Duelos_atacantes_ganados"]),
        ("Regates exitosos", ["Regates_realizados"]),
        ("Precisión de pases", ["Precisión_pases", "Precision_pases"]),
        (
            "Precisión de pases largos",
            ["Precisión_pases_largos", "Precision_pases_largos"],
        ),
        ("Precisión de centros", ["Precisión_centros", "Precision_centros"]),
    ],
    "Delantero centro": [
        ("Duelos ofensivos ganados", ["Duelos_atacantes_ganados"]),
        ("Duelos aéreos ganados", ["Duelos_aéreos_ganados", "Duelos_aereos_ganados"]),
        ("Precisión de pases", ["Precisión_pases", "Precision_pases"]),
        ("Precisión de remates", ["Tiros_a_la_portería", "Tiros_a_la_porteria"]),
    ],
}


def normalizar_clave_estadistica(valor):
    if valor is None or pd.isna(valor):
        return ""
    texto = str(valor).strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(char for char in texto if not unicodedata.combining(char))
    texto = texto.replace("%", " porcentaje ")
    texto = texto.replace("/", " ")
    texto = re.sub(r"[^a-z0-9]+", "_", texto)
    return texto.strip("_")


def obtener_columna_por_aliases(df, aliases):
    if df.empty:
        return None
    columnas_normalizadas = {
        normalizar_clave_estadistica(columna): columna for columna in df.columns
    }
    for alias in aliases:
        columna = columnas_normalizadas.get(normalizar_clave_estadistica(alias))
        if columna:
            return columna
    return None


def convertir_valor_numerico(valor):
    if valor is None or pd.isna(valor):
        return None
    if isinstance(valor, (int, float, np.integer, np.floating)):
        return float(valor)

    texto = str(valor).strip()
    if not texto or texto.lower() in {"nan", "none", "-", "—"}:
        return None

    texto = texto.replace("%", "")
    texto = re.sub(r"\s+", "", texto)
    texto = texto.replace("−", "-").replace("–", "-").replace("—", "-")

    if texto.count(",") > 1 and "." not in texto:
        texto = texto.replace(",", "")
    elif texto.count(".") > 1 and "," not in texto:
        texto = texto.replace(".", "")
    elif "," in texto and "." in texto:
        if texto.rfind(",") > texto.rfind("."):
            texto = texto.replace(".", "")
            texto = texto.replace(",", ".")
        else:
            texto = texto.replace(",", "")
    elif "," in texto:
        texto = texto.replace(",", ".")

    try:
        return float(texto)
    except ValueError:
        return None


def formatear_valor_estadistica(valor):
    numero = convertir_valor_numerico(valor)
    if numero is None:
        return "-"
    return f"{numero:.2f}"


@st.cache_data(ttl=120)
def cargar_datos_estadisticas():
    df_promedios = cargar_datos_sheets("Promedios de Liga", conservar_texto=True)
    df_data_jugadores = cargar_datos_sheets("Data Jugadores", conservar_texto=True)
    return df_promedios, df_data_jugadores


def obtener_fila_estadisticas_jugador(df_data_jugadores, nombre_wyscout):
    nombre_wyscout = str(nombre_wyscout).strip()
    if df_data_jugadores.empty or not nombre_wyscout:
        return None

    columna_nombre = obtener_columna_por_aliases(
        df_data_jugadores,
        [
            "Nombre jugador",
            "Nombre_jugador",
            "Jugador",
            "Nombre",
            "Player",
            "nombre_wyscout",
            "Nombre Wyscout",
        ],
    )
    if not columna_nombre:
        return None

    objetivo = normalizar_clave_estadistica(nombre_wyscout)
    if not objetivo:
        return None

    coincidencias = df_data_jugadores[
        df_data_jugadores[columna_nombre].astype(str).map(normalizar_clave_estadistica) == objetivo
    ]
    coincidencias = coincidencias.dropna(how="all")

    if coincidencias.empty or len(coincidencias) != 1:
        return None
    return coincidencias.iloc[0]


def obtener_resumen_estadisticas_jugador(jugador, df_data_jugadores):
    fila_jugador = obtener_fila_estadisticas_jugador(
        df_data_jugadores,
        jugador.get("nombre_wyscout", ""),
    )
    if fila_jugador is None:
        return {"partidos_jugados": "-", "minutos_jugados": "-"}

    columna_partidos = obtener_columna_por_aliases(
        df_data_jugadores,
        ["Partidos jugados", "Partidos_jugados"],
    )
    columna_minutos = obtener_columna_por_aliases(
        df_data_jugadores,
        ["Minutos jugados", "Minutos_jugados"],
    )

    partidos = formatear_valor_estadistica(fila_jugador.get(columna_partidos) if columna_partidos else None)
    minutos = formatear_valor_estadistica(fila_jugador.get(columna_minutos) if columna_minutos else None)

    if partidos != "-":
        try:
            partidos = str(int(round(float(partidos))))
        except ValueError:
            pass

    if minutos != "-":
        try:
            minutos = str(int(round(float(minutos))))
        except ValueError:
            pass

    return {
        "partidos_jugados": partidos,
        "minutos_jugados": minutos,
    }


def construir_tabla_estadisticas(jugador, df_promedios, df_data_jugadores):
    posicion = str(jugador.get("Posición", "")).strip()
    liga = str(jugador.get("Liga", "")).strip()
    nombre_wyscout = str(jugador.get("nombre_wyscout", "")).strip()
    metricas = POSICION_ESTADISTICAS_CLAVE.get(posicion, [])

    if not metricas:
        return None, "posicion_no_configurada"

    if not nombre_wyscout:
        return None, "jugador_sin_estadisticas"

    fila_jugador = obtener_fila_estadisticas_jugador(df_data_jugadores, nombre_wyscout)
    if fila_jugador is None:
        return None, "jugador_sin_estadisticas"

    fila_comparativa = {"Jugador / Promedio de liga": jugador.get("Nombre", "Jugador")}
    estadisticas_encontradas = 0

    for etiqueta, aliases in metricas:
        columna = obtener_columna_por_aliases(df_data_jugadores, aliases)
        valor = fila_jugador.get(columna) if columna else None
        fila_comparativa[etiqueta] = formatear_valor_estadistica(valor)
        if fila_comparativa[etiqueta] != "-":
            estadisticas_encontradas += 1

    if estadisticas_encontradas == 0:
        return None, "jugador_sin_estadisticas"

    filas = [fila_comparativa]

    if df_promedios.empty:
        return pd.DataFrame(filas), "sin_promedios"

    col_posicion = obtener_columna_por_aliases(df_promedios, ["Posición", "Posicion"])
    col_liga = obtener_columna_por_aliases(df_promedios, ["Liga"])
    col_anio = obtener_columna_por_aliases(df_promedios, ["Año", "Ano", "Temporada", "Year"])

    if not all([col_posicion, col_liga, col_anio]):
        return pd.DataFrame(filas), "sin_promedios"

    posicion_objetivo = normalizar_clave_estadistica(posicion)
    liga_objetivo = normalizar_clave_estadistica(liga)

    df_filtrado = df_promedios[
        (df_promedios[col_posicion].astype(str).map(normalizar_clave_estadistica) == posicion_objetivo)
        & (df_promedios[col_liga].astype(str).map(normalizar_clave_estadistica) == liga_objetivo)
    ].copy()

    if df_filtrado.empty:
        return pd.DataFrame(filas), "sin_promedios"

    df_filtrado["_anio_orden"] = pd.to_numeric(df_filtrado[col_anio], errors="coerce")
    df_filtrado = df_filtrado.dropna(subset=["_anio_orden"])

    if df_filtrado.empty:
        return pd.DataFrame(filas), "sin_promedios"

    df_filtrado = (
        df_filtrado.sort_values("_anio_orden", ascending=False)
        .drop_duplicates(subset=[col_anio], keep="first")
    )

    for _, fila_promedio in df_filtrado.iterrows():
        fila_anual = {
            "Jugador / Promedio de liga": f"Promedio de liga {int(fila_promedio['_anio_orden'])}"
        }
        for etiqueta, aliases in metricas:
            columna = obtener_columna_por_aliases(df_promedios, aliases)
            valor = fila_promedio.get(columna) if columna else None
            fila_anual[etiqueta] = formatear_valor_estadistica(valor)
        filas.append(fila_anual)

    return pd.DataFrame(filas), "ok"


def preparar_datos_graficos_estadisticas(tabla_estadisticas: pd.DataFrame):
    if tabla_estadisticas is None or tabla_estadisticas.empty or len(tabla_estadisticas.columns) < 2:
        return None, None, None

    etiqueta_columna = tabla_estadisticas.columns[0]
    metricas = [columna for columna in tabla_estadisticas.columns if columna != etiqueta_columna]

    df_chart = tabla_estadisticas.copy()
    for metrica in metricas:
        df_chart[metrica] = df_chart[metrica].apply(convertir_valor_numerico)

    df_chart = df_chart.dropna(how="all", subset=metricas)
    if df_chart.empty:
        return None, None, None

    df_long = df_chart.melt(
        id_vars=[etiqueta_columna],
        value_vars=metricas,
        var_name="Métrica",
        value_name="Valor",
    ).dropna(subset=["Valor"])

    if df_long.empty:
        return None, None, None

    def extraer_anio(etiqueta):
        match = re.search(r"(20\d{2})", str(etiqueta))
        return int(match.group(1)) if match else -1

    referencia_jugador = str(df_chart.iloc[0][etiqueta_columna])
    filas_liga = df_chart[df_chart[etiqueta_columna] != referencia_jugador].copy()
    fila_referencia = None
    if not filas_liga.empty:
        filas_liga["_anio"] = filas_liga[etiqueta_columna].apply(extraer_anio)
        fila_referencia = filas_liga.sort_values("_anio", ascending=False).iloc[0]

    return df_long, fila_referencia, referencia_jugador


def abreviar_titulo_estadistica_pdf(texto):
    equivalencias = {
        "Jugador / Promedio de liga": "Jugador / Prom. liga",
        "Goles recibidos / 90": "Goles rec./90",
        "Remates en contra / 90": "Remates c./90",
        "Porcentaje de paradas": "% paradas",
        "Porterías imbatidas / 90": "Port. imb./90",
        "Duelos defensivos ganados": "Duelos def.",
        "Duelos aéreos ganados": "Duelos aéreos",
        "Interceptaciones / 90": "Intercep./90",
        "Precisión de pases": "Prec. pases",
        "Precisión de pases largos": "Prec. pases largos",
        "Duelos ofensivos ganados": "Duelos of.",
        "Regates exitosos": "Regates",
        "Precisión de centros": "Prec. centros",
        "Precisión de remates": "Prec. remates",
    }
    return equivalencias.get(texto, texto)


def asegurar_espacio_pdf(pdf, alto_necesario):
    if pdf.get_y() + alto_necesario > pdf.h - pdf.b_margin - 8:
        pdf.add_page()


def valor_campo_pdf(valor, fallback="-"):
    if valor is None:
        return fallback
    if isinstance(valor, float) and pd.isna(valor):
        return fallback

    texto = str(valor).strip()
    if not texto or texto.lower() in {"nan", "none", "nat", "<na>"}:
        return fallback
    return sanitizar_texto_pdf(texto)


def medir_altura_texto_pdf(pdf, texto, ancho, alto_linea):
    texto = valor_campo_pdf(texto, "")
    ancho_util = max(float(ancho) - (pdf.c_margin * 2), 1)
    if not texto:
        return alto_linea

    cantidad_lineas = 1
    for parrafo in texto.split("\n"):
        palabras = parrafo.split()
        if not palabras:
            cantidad_lineas += 1
            continue

        linea_actual = ""
        for palabra in palabras:
            candidata = palabra if not linea_actual else f"{linea_actual} {palabra}"
            if pdf.get_string_width(candidata) <= ancho_util:
                linea_actual = candidata
            else:
                cantidad_lineas += 1
                linea_actual = palabra

    return max(cantidad_lineas, 1) * alto_linea


def abreviar_leyenda_grafico_pdf(texto, limite=28):
    texto = valor_campo_pdf(texto, "-")
    return texto if len(texto) <= limite else f"{texto[:limite - 1].rstrip()}…"


def formatear_formacion_pdf(valor):
    if valor is None or (isinstance(valor, float) and pd.isna(valor)):
        return "-"

    if isinstance(valor, pd.Timestamp) and pd.notna(valor):
        return f"{valor.day}-{valor.month}-{valor.year % 100}"

    if isinstance(valor, (datetime, date)):
        return f"{valor.day}-{valor.month}-{valor.year % 100}"

    texto = str(valor).strip()
    if not texto:
        return "-"

    fecha = pd.to_datetime(texto, errors="coerce", dayfirst=True)
    if pd.notna(fecha):
        partes_numericas = re.findall(r"\d+", texto)
        if len(partes_numericas) >= 3 and int(fecha.year) >= 2000:
            return f"{int(fecha.day)}-{int(fecha.month)}-{int(fecha.year) % 100}"

    return sanitizar_texto_pdf(texto)


def dibujar_titulo_seccion_pdf(pdf, titulo, subtitulo="", espacio_posterior_minimo=26):
    asegurar_espacio_pdf(pdf, (11 if not subtitulo else 15) + espacio_posterior_minimo)

    bloque_x = pdf.l_margin
    bloque_y = pdf.get_y()
    bloque_w = pdf.w - pdf.l_margin - pdf.r_margin
    bloque_h = 11 if not subtitulo else 15

    pdf.set_fill_color(15, 22, 28)
    pdf.set_draw_color(110, 132, 128)
    pdf.set_line_width(0.5)
    pdf.rect(bloque_x, bloque_y, bloque_w, bloque_h, "DF")
    pdf.set_fill_color(102, 140, 128)
    pdf.rect(bloque_x, bloque_y, 3.2, bloque_h, "F")

    pdf.set_xy(bloque_x + 7, bloque_y + 2.2)
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(245, 247, 248)
    pdf.cell(bloque_w - 14, 5, titulo, ln=True)

    if subtitulo:
        pdf.set_x(bloque_x + 7)
        pdf.set_font("Arial", "", 8.5)
        pdf.set_text_color(198, 207, 209)
        pdf.multi_cell(bloque_w - 14, 4, subtitulo)

    pdf.set_y(bloque_y + bloque_h + 4)


def crear_buffer_figura_pdf(fig, dpi=160):
    import matplotlib.pyplot as plt

    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=dpi, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    buffer.seek(0)
    return buffer


def obtener_alto_imagen_pdf(buffer, ancho_pdf):
    posicion_actual = buffer.tell()
    buffer.seek(0)
    with Image.open(buffer) as imagen:
        ancho_px, alto_px = imagen.size
    buffer.seek(posicion_actual)
    if not ancho_px:
        return ancho_pdf
    return ancho_pdf * (alto_px / ancho_px)


def crear_radar_valoracion_pdf(promedios_grupos):
    import matplotlib.pyplot as plt

    etiquetas = list(promedios_grupos.keys())
    valores = [promedios_grupos[etiqueta] if promedios_grupos[etiqueta] is not None else 0 for etiqueta in etiquetas]
    valores += valores[:1]
    angulos = np.linspace(0, 2 * np.pi, len(etiquetas), endpoint=False).tolist()
    angulos += angulos[:1]

    fig, ax = plt.subplots(figsize=(3.5, 3.5), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("#081510")
    ax.set_facecolor("#0d2019")
    ax.set_ylim(0, 10)
    ax.plot(angulos, valores, color="#19e28f", linewidth=2.2)
    ax.fill(angulos, valores, color="#19e28f", alpha=0.2)
    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(etiquetas, color="#e7f1eb", fontsize=8)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(["2", "4", "6", "8", "10"], color="#9ab5a6", fontsize=7)
    ax.grid(color="#254637", alpha=0.7)
    ax.spines["polar"].set_color("#3f7d60")
    return crear_buffer_figura_pdf(fig)


def crear_barras_estadisticas_pdf(tabla_estadisticas, fila_liga_referencia, etiqueta_jugador):
    import matplotlib.pyplot as plt

    if tabla_estadisticas is None or tabla_estadisticas.empty or fila_liga_referencia is None:
        return None

    etiqueta_columna = tabla_estadisticas.columns[0]
    metricas = [columna for columna in tabla_estadisticas.columns if columna != etiqueta_columna]
    metricas_orden = list(reversed(metricas))
    nombre_referencia = valor_campo_pdf(fila_liga_referencia.get(etiqueta_columna), "Promedio de liga")

    valores_jugador = []
    valores_liga = []
    etiquetas_validas = []
    for metrica in metricas_orden:
        valor_jugador = convertir_valor_numerico(tabla_estadisticas.iloc[0][metrica])
        valor_liga = convertir_valor_numerico(fila_liga_referencia.get(metrica))
        if valor_jugador is None and valor_liga is None:
            continue
        etiquetas_validas.append(metrica)
        valores_jugador.append(valor_jugador or 0)
        valores_liga.append(valor_liga or 0)

    if not etiquetas_validas:
        return None

    posiciones = np.arange(len(etiquetas_validas))
    alto_barra = 0.34

    fig, ax = plt.subplots(figsize=(7.8, 3.15))
    fig.patch.set_facecolor("#081510")
    ax.set_facecolor("#0d2019")
    barras_jugador = ax.barh(
        posiciones + alto_barra / 2,
        valores_jugador,
        height=alto_barra,
        color="#19e28f",
        label=abreviar_leyenda_grafico_pdf(etiqueta_jugador, 24),
    )
    barras_liga = ax.barh(
        posiciones - alto_barra / 2,
        valores_liga,
        height=alto_barra,
        color="#8fd3b4",
        label=abreviar_leyenda_grafico_pdf(nombre_referencia, 24),
    )

    ax.set_yticks(posiciones)
    ax.set_yticklabels(etiquetas_validas, color="#edf5f0", fontsize=8.5)
    ax.tick_params(axis="x", colors="#b7cec2", labelsize=8)
    ax.invert_yaxis()
    ax.grid(axis="x", color="#254637", alpha=0.65)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#335e4c")
    ax.spines["bottom"].set_color("#335e4c")
    ax.set_xlabel("Valor", color="#d6e4dc", fontsize=9)
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.09),
        ncol=2,
        frameon=False,
        labelcolor="#edf5f0",
        fontsize=7.2,
        handlelength=1.6,
        columnspacing=1.0,
    )
    plt.subplots_adjust(top=0.82, bottom=0.19, left=0.25, right=0.96)

    for barra in list(barras_jugador) + list(barras_liga):
        ancho = barra.get_width()
        ax.text(
            ancho + 0.08,
            barra.get_y() + barra.get_height() / 2,
            f"{ancho:.2f}",
            va="center",
            ha="left",
            color="#edf5f0",
            fontsize=7.5,
        )

    return crear_buffer_figura_pdf(fig)


def crear_radar_estadisticas_pdf(tabla_estadisticas, fila_liga_referencia, etiqueta_jugador):
    import matplotlib.pyplot as plt

    if tabla_estadisticas is None or tabla_estadisticas.empty or fila_liga_referencia is None:
        return None

    etiqueta_columna = tabla_estadisticas.columns[0]
    metricas = [columna for columna in tabla_estadisticas.columns if columna != etiqueta_columna]
    if not metricas:
        return None

    valores_jugador = [convertir_valor_numerico(tabla_estadisticas.iloc[0][metrica]) or 0 for metrica in metricas]
    valores_liga = [convertir_valor_numerico(fila_liga_referencia.get(metrica)) or 0 for metrica in metricas]
    angulos = np.linspace(0, 2 * np.pi, len(metricas), endpoint=False).tolist()
    angulos += angulos[:1]

    fig, ax = plt.subplots(figsize=(5.3, 5.0), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("#081510")
    ax.set_facecolor("#0d2019")
    ax.plot(angulos, valores_jugador + valores_jugador[:1], color="#19e28f", linewidth=2.2, label=abreviar_leyenda_grafico_pdf(etiqueta_jugador, 22))
    ax.fill(angulos, valores_jugador + valores_jugador[:1], color="#19e28f", alpha=0.18)
    ax.plot(angulos, valores_liga + valores_liga[:1], color="#8fd3b4", linewidth=2, label=abreviar_leyenda_grafico_pdf(fila_liga_referencia.get(etiqueta_columna), 22))
    ax.fill(angulos, valores_liga + valores_liga[:1], color="#8fd3b4", alpha=0.12)
    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(metricas, color="#edf5f0", fontsize=8)
    ax.tick_params(axis="y", colors="#a8c0b3", labelsize=7)
    ax.grid(color="#254637", alpha=0.65)
    ax.spines["polar"].set_color("#3f7d60")
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.13),
        ncol=2,
        frameon=False,
        labelcolor="#edf5f0",
        fontsize=7.2,
        handlelength=1.8,
        columnspacing=1.0,
    )
    plt.subplots_adjust(top=0.76, bottom=0.08)
    return crear_buffer_figura_pdf(fig)


def agregar_estadisticas_pdf(
    pdf,
    jugador,
    color_verde_principal,
    color_gris_fondo,
    color_gris_oscuro,
    color_texto,
):
    df_promedios, df_data_jugadores = cargar_datos_estadisticas()
    resumen_estadistico = obtener_resumen_estadisticas_jugador(jugador, df_data_jugadores)
    tabla_estadisticas, estado_estadisticas = construir_tabla_estadisticas(
        jugador,
        df_promedios,
        df_data_jugadores,
    )

    df_long_stats, fila_liga_referencia, etiqueta_jugador = preparar_datos_graficos_estadisticas(
        tabla_estadisticas
    )

    dibujar_titulo_seccion_pdf(
        pdf,
        "Comparativa estadística",
        "Incluye referencia de liga más reciente, radar comparativo y la tabla consolidada del jugador.",
        espacio_posterior_minimo=30,
    )

    resumen_y = pdf.get_y()
    resumen_x = pdf.l_margin
    resumen_w = pdf.w - pdf.l_margin - pdf.r_margin
    resumen_h = 11
    pdf.set_fill_color(11, 18, 24)
    pdf.set_draw_color(118, 138, 132)
    pdf.rect(resumen_x, resumen_y, resumen_w, resumen_h, "DF")
    pdf.set_xy(resumen_x + 4, resumen_y + 2)
    pdf.set_font("Arial", "B", 9)
    pdf.set_text_color(210, 220, 222)
    pdf.cell(0, 4, "RESUMEN DE COMPETICIÓN", ln=True)
    pdf.set_x(resumen_x + 4)
    pdf.set_font("Arial", "", 9.4)
    pdf.set_text_color(239, 245, 241)
    pdf.cell(
        0,
        4,
        f"Partidos jugados: {valor_campo_pdf(resumen_estadistico['partidos_jugados'])}   |   Minutos jugados: {valor_campo_pdf(resumen_estadistico['minutos_jugados'])}",
        ln=True,
    )
    pdf.ln(2.5)

    if tabla_estadisticas is None or tabla_estadisticas.empty:
        mensajes_estado = {
            "jugador_sin_estadisticas": "Jugador sin estadísticas disponibles",
            "posicion_no_configurada": "Sin estadísticas configuradas para la posición",
            "sin_promedios": "No hay promedios de liga disponibles",
        }
        mensaje = mensajes_estado.get(estado_estadisticas, "Sin estadísticas disponibles")
        pdf.set_font("Arial", "I", 9.5)
        pdf.set_text_color(188, 201, 194)
        pdf.multi_cell(0, 5.2, mensaje)
        pdf.ln(2)
        return

    grafico_barras = None
    grafico_radar = None
    if df_long_stats is not None and fila_liga_referencia is not None:
        grafico_barras = crear_barras_estadisticas_pdf(tabla_estadisticas, fila_liga_referencia, etiqueta_jugador)
        grafico_radar = crear_radar_estadisticas_pdf(tabla_estadisticas, fila_liga_referencia, etiqueta_jugador)

    if grafico_barras is not None:
        ancho_barras = pdf.w - pdf.l_margin - pdf.r_margin - 6
        alto_barras = obtener_alto_imagen_pdf(grafico_barras, ancho_barras)
        asegurar_espacio_pdf(pdf, alto_barras + 6)
        pdf.set_font("Arial", "B", 10)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 5, "Jugador vs promedio de liga más reciente", ln=True)
        pdf.ln(0.2)
        y_barras = pdf.get_y()
        barras_x = pdf.l_margin + ((pdf.w - pdf.l_margin - pdf.r_margin) - ancho_barras) / 2
        pdf.image(grafico_barras, x=barras_x, y=y_barras, w=ancho_barras)
        pdf.set_y(y_barras + alto_barras + 0.8)

    if grafico_radar is not None:
        radar_w = 82
        radar_h = obtener_alto_imagen_pdf(grafico_radar, radar_w)
        asegurar_espacio_pdf(pdf, radar_h + 6)
        pdf.set_font("Arial", "B", 10)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 5, "Radar comparativo", ln=True)
        pdf.ln(0.2)
        radar_x = (pdf.w - radar_w) / 2
        y_radar = pdf.get_y()
        pdf.image(grafico_radar, x=radar_x, y=y_radar, w=radar_w)
        pdf.set_y(y_radar + radar_h + 0.8)

    asegurar_espacio_pdf(pdf, 18 + (len(tabla_estadisticas) * 5.8))
    pdf.set_font("Arial", "B", 10)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 5, "Tabla comparativa", ln=True)
    pdf.ln(0.4)

    columnas = list(tabla_estadisticas.columns)
    ancho_total = pdf.w - pdf.l_margin - pdf.r_margin
    ancho_primera = 50
    ancho_resto = (ancho_total - ancho_primera) / max(1, len(columnas) - 1)
    anchos = [ancho_primera] + [ancho_resto] * (len(columnas) - 1)

    pdf.set_fill_color(23, 32, 38)
    pdf.set_text_color(255, 255, 255)
    pdf.set_draw_color(118, 138, 132)
    pdf.set_font("Arial", "B", 5.8)

    for columna, ancho in zip(columnas, anchos):
        titulo = sanitizar_texto_pdf(abreviar_titulo_estadistica_pdf(columna))
        pdf.cell(ancho, 5.8, titulo, border=1, align="C", fill=True)
    pdf.ln()

    for indice, (_, fila) in enumerate(tabla_estadisticas.iterrows()):
        es_jugador = indice == 0
        if es_jugador:
            pdf.set_fill_color(19, 28, 34)
            pdf.set_text_color(246, 251, 248)
            pdf.set_font("Arial", "B", 7.1)
        else:
            fill_color = (11, 18, 24) if indice % 2 else (17, 25, 31)
            pdf.set_fill_color(*fill_color)
            pdf.set_text_color(225, 235, 229)
            pdf.set_font("Arial", "", 6.5)

        for posicion_columna, (columna, ancho) in enumerate(zip(columnas, anchos)):
            valor = sanitizar_texto_pdf(str(fila.get(columna, "-")))
            alineacion = "L" if posicion_columna == 0 else "C"
            pdf.cell(ancho, 5.3, valor, border=1, align=alineacion, fill=True)
        pdf.ln()

    if estado_estadisticas == "sin_promedios":
        pdf.ln(0.5)
        pdf.set_font("Arial", "I", 7.5)
        pdf.set_text_color(177, 191, 184)
        pdf.cell(0, 5, "No hay promedios de liga disponibles para la posición y liga seleccionadas.", ln=True, align="L")

    pdf.ln(2)


# ---------------------------------------------------------
# FUNCIONES DE PROMEDIOS (OBLIGATORIAS PARA BLOQUE 3)
# ---------------------------------------------------------

def calcular_promedios_jugador(df_reports, id_jugador):
    if df_reports.empty:
        return None

    df = df_reports.copy()
    df["ID_Jugador"] = df["ID_Jugador"].astype(str)
    informes = df[df["ID_Jugador"] == str(id_jugador)]

    if informes.empty:
        return None

    metricas = [
        "Controles","Perfiles","Pase_corto","Pase_largo","Pase_filtrado",
        "1v1_defensivo","Recuperacion","Intercepciones","Duelos_aereos",
        "Regate","Velocidad","Duelos_ofensivos",
        "Resiliencia","Liderazgo","Inteligencia_tactica",
        "Inteligencia_emocional","Posicionamiento",
        "Vision_de_juego","Movimientos_sin_pelota"
    ]

    promedios = {}
    for m in metricas:
        if m in informes.columns:
            try:
                valores = (
                    informes[m]
                    .astype(str)
                    .str.replace(",", ".", regex=False)
                    .replace(["", "nan", "None", "-", "—"], 0)
                    .astype(float)
                )
                promedios[m] = round(valores.mean(), 2)
            except Exception:
                promedios[m] = 0.0
        else:
            promedios[m] = 0.0

    return promedios


def calcular_promedios_posicion(df_reports, df_players, posicion):
    if not posicion or df_reports.empty or df_players.empty:
        return None

    df_r = df_reports.copy()
    df_p = df_players.copy()

    df_r["ID_Jugador"] = df_r["ID_Jugador"].astype(str)
    df_p["ID_Jugador"] = df_p["ID_Jugador"].astype(str)

    ids = df_p[df_p["Posición"] == posicion]["ID_Jugador"].tolist()
    informes = df_r[df_r["ID_Jugador"].isin(ids)]

    if informes.empty:
        return None

    metricas = [
        "Controles","Perfiles","Pase_corto","Pase_largo","Pase_filtrado",
        "1v1_defensivo","Recuperacion","Intercepciones","Duelos_aereos",
        "Regate","Velocidad","Duelos_ofensivos",
        "Resiliencia","Liderazgo","Inteligencia_tactica",
        "Inteligencia_emocional","Posicionamiento",
        "Vision_de_juego","Movimientos_sin_pelota"
    ]

    promedios = {}
    for m in metricas:
        if m in informes.columns:
            try:
                valores = (
                    informes[m]
                    .astype(str)
                    .str.replace(",", ".", regex=False)
                    .replace(["", "nan", "None", "-", "—"], 0)
                    .astype(float)
                )
                promedios[m] = round(valores.mean(), 2)
            except Exception:
                promedios[m] = 0.0
        else:
            promedios[m] = 0.0

    return promedios


# ---------------------------------------------------------
# RADAR
# ---------------------------------------------------------

def radar_chart(prom_jugador, prom_posicion):
    if not prom_jugador:
        return

    categorias = list(prom_jugador.keys())
    valores_j = [float(prom_jugador.get(c, 0)) for c in categorias]
    valores_p = [float(prom_posicion.get(c, 0)) for c in categorias] if prom_posicion else [0]*len(categorias)

    valores_j += valores_j[:1]
    valores_p += valores_p[:1]

    angles = np.linspace(0, 2*np.pi, len(categorias), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("#0a1a14")
    ax.set_facecolor("#0a1a14")

    ax.plot(angles, valores_j, color="cyan", linewidth=2)
    ax.fill(angles, valores_j, color="cyan", alpha=0.25)

    ax.plot(angles, valores_p, color="orange", linewidth=2)
    ax.fill(angles, valores_p, color="orange", alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categorias, color="white", fontsize=9)
    ax.tick_params(colors="white")

    st.pyplot(fig)


# ---------------------------------------------------------
# FUNCIÓN AUXILIAR: SANITIZAR CARACTERES PARA PDF (AGRESIVA)
# ---------------------------------------------------------
def sanitizar_texto_pdf(texto):
    """
    Sanitización SELECTIVA de caracteres especiales no soportados por FPDF.
    - MANTIENE caracteres acentuados (á, é, í, ó, ú, ñ, etc.)
    - ELIMINA solo símbolos especiales problemáticos
    - Compatible con fuentes Latin-1 de FPDF
    """
    if not isinstance(texto, str):
        texto = str(texto)
    
    # Primero: Reemplazos de símbolos especiales PELIGROSOS (no acentos)
    reemplazos_especificos = {
        "•": "-",           # bullet point
        "○": "o",           # círculo vacío
        "●": "o",           # círculo lleno
        "·": ".",           # punto medio
        "×": "x",           # multiplicación
        "÷": "/",           # división
        "°": "o",           # grado
        "º": "o",           # ordinal
        "ª": "a",           # ordinal femenino
        "–": "-",           # en dash
        "—": "-",           # em dash
        "−": "-",           # minus
        "'": "'",           # comilla inteligente izquierda
        "'": "'",           # comilla inteligente derecha
        """: '"',           # comilla doble izquierda
        """: '"',           # comilla doble derecha
        "„": '"',           # comilla baja doble
        "‟": '"',           # comilla alta doble
        "«": '"',           # comilla francesa izquierda
        "»": '"',           # comilla francesa derecha
        "‹": "<",           # comilla simple izquierda
        "›": ">",           # comilla simple derecha
        "…": "...",         # ellipsis
        "‚": "'",           # comilla baja simple
        "‛": "'",           # comilla alta simple
        "ℓ": "l",           # script l
        "™": "TM",          # trademark
        "®": "R",           # registered
        "©": "C",           # copyright
        "℠": "SM",          # service mark
        "€": "EUR",         # euro
        "¥": "JPY",         # yen
        "£": "GBP",         # libra
        "¢": "cents",       # centavos
        "₹": "-",           # rupia
        "₽": "-",           # ruble
        "¤": "$",           # moneda genérica
        "§": "S",           # sección
        "¶": "P",           # párrafo
        "†": "+",           # dagger
        "‡": "++",          # double dagger
        "‰": "0/00",        # per mille
        "‱": "0/000",       # per ten thousand
        "↑": "^",           # arrow up
        "↓": "v",           # arrow down
        "←": "<",           # arrow left
        "→": ">",           # arrow right
        "◄": "<",           # pointer left
        "►": ">",           # pointer right
        "◆": "*",           # diamond
        "★": "*",           # star
        "☆": "*",           # star vacio
        "✓": "OK",          # checkmark
        "✗": "X",           # cross
        "✔": "OK",          # heavy checkmark
        "✕": "X",           # heavy cross
        "⚠": "!",           # warning
    }
    
    for viejo, nuevo in reemplazos_especificos.items():
        texto = texto.replace(viejo, nuevo)
    
    # Segundo: Usar encoding latin-1 (que FPDF SOPORTA natively)
    # latin-1 soporta: á, é, í, ó, ú, ñ, ü y otros caracteres europeos
    try:
        # Intentar codificar como latin-1 (si falla, usamos replace)
        texto = texto.encode('latin-1', errors='replace').decode('latin-1')
    except:
        # Fallback: usar ascii con replace
        texto = texto.encode('ascii', errors='replace').decode('ascii')
    
    # Tercero: Limpiar caracteres de control no-imprimibles
    texto = ''.join(c for c in texto if c.isprintable() or c.isspace())
    
    # Cuarto: Limpiar espacios múltiples
    texto = ' '.join(texto.split())
    
    return texto


# ---------------------------------------------------------
# CLASE FPDF CON SANITIZACIÓN AUTOMÁTICA
# ---------------------------------------------------------
class FPDF_SEGURO(FPDF):
    """Extensión de FPDF que sanitiza automáticamente todos los strings."""

    _background_cache = {}

    def _normalizar_ancho_texto(self, width):
        if width == 0:
            disponible = self.w - self.r_margin - self.get_x()
            if disponible <= (self.c_margin * 2 + 0.5):
                self.set_x(self.l_margin)
                disponible = self.w - self.r_margin - self.get_x()
            return max(disponible, self.c_margin * 2 + 0.5)
        if width is None:
            return 0
        if width < 0:
            disponible = self.w - self.r_margin - self.get_x() + width
            if disponible <= (self.c_margin * 2 + 0.5):
                self.set_x(self.l_margin)
                disponible = self.w - self.r_margin - self.get_x()
            return max(disponible, self.c_margin * 2 + 0.5)
        return width

    def header(self):
        fondo_path = "fondo informe cancha.png"
        if os.path.exists(fondo_path):
            fondo_bytes = self._background_cache.get(fondo_path)
            if fondo_bytes is None:
                with Image.open(fondo_path) as imagen_origen:
                    fondo_tratado = imagen_origen.convert("RGB")
                overlay = Image.new("RGB", fondo_tratado.size, (11, 33, 24))
                fondo_tratado = Image.blend(fondo_tratado, overlay, 0.48)
                fondo_buffer = BytesIO()
                fondo_tratado.save(fondo_buffer, format="PNG", optimize=True)
                fondo_bytes = fondo_buffer.getvalue()
                self._background_cache[fondo_path] = fondo_bytes
            self.image(BytesIO(fondo_bytes), x=0, y=0, w=self.w, h=self.h)
        else:
            self.set_fill_color(17, 27, 32)
            self.rect(0, 0, self.w, self.h, "F")

        self.set_draw_color(118, 138, 132)
        self.set_line_width(0.3)
        self.line(self.l_margin, 10, self.w - self.r_margin, 10)

    def footer(self):
        self.set_y(-10)
        self.set_draw_color(118, 138, 132)
        self.set_line_width(0.25)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.set_y(-8)
        self.set_font("Arial", "", 7)
        self.set_text_color(218, 224, 225)
        self.cell(0, 4, f"ScoutingApp Profesional  |  Página {self.page_no()}", align="R")

    def cell(self, w=0, h=0, text="", border=0, ln=False, align="", fill=False, link=""):
        w = self._normalizar_ancho_texto(w)
        text = sanitizar_texto_pdf(str(text)) if text else ""
        return super().cell(w, h, text, border, ln, align, fill, link)

    def multi_cell(self, w=0, h=0, text="", border=0, align="", fill=False):
        w = self._normalizar_ancho_texto(w)
        text = sanitizar_texto_pdf(str(text)) if text else ""
        return super().multi_cell(w, h, text, border, align, fill)

# FUNCION: GENERAR PDF REPORTE COMPLETO (OPTIMIZADO)
# ---------------------------------------------------------
def generar_pdf_reporte_completo(jugador, df_reports):
    """
    Genera un PDF completo alineado con la identidad visual actual de la aplicación.
    Incluye ficha completa del jugador, descripción, valoración de aspectos,
    comparativa estadística con gráficos y la secuencia de informes cargados.
    """
    try:
        import requests

        color_fondo = (17, 27, 32)
        color_panel = (11, 18, 24)
        color_panel_alt = (17, 25, 31)
        color_acento = (102, 140, 128)
        color_acento_suave = (210, 220, 222)
        color_texto = (246, 247, 248)
        color_texto_muted = (213, 219, 221)
        color_borde = (118, 138, 132)

        pdf = FPDF_SEGURO()
        pdf.set_margins(left=10, top=12, right=10)
        pdf.set_auto_page_break(auto=True, margin=12)
        pdf.alias_nb_pages()
        pdf.add_page()

        jugador_id = str(jugador.get("ID_Jugador"))
        informes_jugador = df_reports.copy()
        if not informes_jugador.empty and "ID_Jugador" in informes_jugador.columns:
            informes_jugador = informes_jugador.copy()
            informes_jugador["ID_Jugador"] = informes_jugador["ID_Jugador"].astype(str)
            informes_jugador = informes_jugador[informes_jugador["ID_Jugador"] == jugador_id].copy()

        def texto(clave, fallback="-"):
            return valor_campo_pdf(jugador.get(clave, fallback), fallback)

        def fecha_legible(valor):
            if valor is None:
                return "-"
            if isinstance(valor, pd.Timestamp) and pd.notna(valor):
                return valor.strftime("%d/%m/%Y")
            texto_valor = str(valor).strip()
            if not texto_valor:
                return "-"
            fecha = pd.to_datetime(texto_valor, errors="coerce", dayfirst=True)
            if pd.notna(fecha):
                return fecha.strftime("%d/%m/%Y")
            return sanitizar_texto_pdf(texto_valor)

        def dibujar_chip_resumen(x_pos, y_pos, ancho, alto, etiqueta, valor):
            valor = valor_campo_pdf(valor)
            padding_x = 3.2
            ancho_texto = max(ancho - (padding_x * 2), 8)
            pdf.set_fill_color(18, 26, 32)
            pdf.set_draw_color(*color_borde)
            pdf.rect(x_pos, y_pos, ancho, alto, "DF")
            pdf.set_xy(x_pos + padding_x, y_pos + 1.6)
            pdf.set_font("Arial", "B", 7.2)
            pdf.set_text_color(*color_acento)
            pdf.cell(ancho_texto, 3.5, etiqueta.upper(), ln=True)

            pdf.set_font("Arial", "B", 9.6 if len(valor) <= 22 else 8.8)
            pdf.set_text_color(*color_texto)
            alto_valor = medir_altura_texto_pdf(pdf, valor, ancho_texto, 3.8)
            y_valor = y_pos + max(5.2, ((alto - alto_valor) / 2) + 2.6)
            pdf.set_xy(x_pos + padding_x, y_valor)
            pdf.multi_cell(ancho_texto, 4.2, valor)

        def dibujar_pildoras_enlaces(x_pos, y_pos, ancho_disponible, enlaces):
            if not enlaces:
                return y_pos

            cursor_x = x_pos
            cursor_y = y_pos
            alto = 7
            for etiqueta, url in enlaces:
                ancho_pildora = max(24, min(pdf.get_string_width(etiqueta) + 8, ancho_disponible))
                if cursor_x + ancho_pildora > x_pos + ancho_disponible:
                    cursor_x = x_pos
                    cursor_y += alto + 2

                pdf.set_fill_color(22, 31, 38)
                pdf.set_draw_color(*color_borde)
                pdf.rect(cursor_x, cursor_y, ancho_pildora, alto, "DF")
                pdf.set_xy(cursor_x, cursor_y + 1.9)
                pdf.set_font("Arial", "B", 7.8)
                pdf.set_text_color(*color_acento_suave)
                pdf.cell(ancho_pildora, 3.5, etiqueta, align="C", link=str(url))
                cursor_x += ancho_pildora + 3

            return cursor_y + alto

        def descargar_foto(url_foto):
            if not str(url_foto).startswith("http"):
                return None
            try:
                response = requests.get(url_foto, timeout=8)
                if response.status_code != 200:
                    return None
                imagen = Image.open(BytesIO(response.content)).convert("RGB")
                lado = min(imagen.size)
                offset_x = (imagen.width - lado) // 2
                offset_y = (imagen.height - lado) // 2
                imagen = imagen.crop((offset_x, offset_y, offset_x + lado, offset_y + lado))
                imagen = imagen.resize((420, 420), Image.LANCZOS)
                buffer_imagen = BytesIO()
                imagen.save(buffer_imagen, format="PNG", optimize=True)
                buffer_imagen.seek(0)
                return buffer_imagen
            except Exception:
                return None

        grupos_aspectos = {
            "Habilidades técnicas": ["Controles", "Perfiles", "Pase_corto", "Pase_largo", "Pase_filtrado"],
            "Aspectos defensivos": ["1v1_defensivo", "Recuperacion", "Intercepciones", "Duelos_aereos"],
            "Aspectos ofensivos": ["Regate", "Velocidad", "Duelos_ofensivos"],
            "Aspectos mentales": ["Resiliencia", "Liderazgo", "Inteligencia_emocional"],
            "Aspectos tácticos": ["Inteligencia_tactica", "Posicionamiento", "Vision_de_juego", "Movimientos_sin_pelota"],
        }

        promedios_grupos = {}
        for grupo, metricas in grupos_aspectos.items():
            metricas_existentes = [m for m in metricas if m in informes_jugador.columns]
            if not metricas_existentes:
                promedios_grupos[grupo] = None
                continue
            valores_metricas = informes_jugador[metricas_existentes].apply(pd.to_numeric, errors="coerce")
            valores = valores_metricas.values.flatten()
            valores = [valor for valor in valores if pd.notna(valor)]
            promedio_grupo = round(np.mean(valores), 2) if valores else None
            promedios_grupos[grupo] = promedio_grupo
        promedio_global = round(
            np.mean([valor for valor in promedios_grupos.values() if valor is not None]),
            2,
        ) if any(valor is not None for valor in promedios_grupos.values()) else None

        fecha_nacimiento = fecha_legible(jugador.get("Fecha_Nac"))
        edad = calcular_edad(jugador.get("Fecha_Nac"))
        edad_texto = f"{edad} años" if str(edad) != "?" else "-"
        nacionalidad = texto("Nacionalidad")
        segunda_nacionalidad = texto("Segunda_Nacionalidad")
        nacionalidades = nacionalidad if segunda_nacionalidad == "-" else f"{nacionalidad} / {segunda_nacionalidad}"
        ultimo_informe = "-"
        if not informes_jugador.empty:
            fecha_ultimo = pd.to_datetime(informes_jugador.get("Fecha_Informe"), errors="coerce", dayfirst=True)
            if fecha_ultimo.notna().any():
                ultimo_informe = fecha_ultimo.max().strftime("%d/%m/%Y")

        encabezado_contexto = " · ".join(
            valor for valor in [texto("Club"), texto("Posición"), texto("Liga")] if valor != "-"
        ) or "Perfil sin contexto cargado"

        hero_y = 16
        hero_h = 22
        hero_w = pdf.w - pdf.l_margin - pdf.r_margin
        pdf.set_fill_color(*color_panel)
        pdf.set_draw_color(*color_borde)
        pdf.rect(pdf.l_margin, hero_y, hero_w, hero_h, "DF")

        pdf.set_y(hero_y + 3)
        pdf.set_font("Arial", "B", 8)
        pdf.set_text_color(*color_acento)
        pdf.cell(0, 4, "SCOUTING DOSSIER", ln=True)
        pdf.ln(0.5)
        pdf.set_font("Arial", "B", 22)
        pdf.set_text_color(*color_texto)
        pdf.multi_cell(0, 9, texto("Nombre", "Jugador"))
        pdf.set_font("Arial", "", 11)
        pdf.set_text_color(*color_texto_muted)
        pdf.multi_cell(0, 5.5, encabezado_contexto)
        pdf.set_y(hero_y + hero_h + 5)

        chips = [
            ("Posición", texto("Posición")),
            ("Club", texto("Club")),
            ("Liga", texto("Liga")),
            ("Edad", edad_texto),
            ("Último informe", ultimo_informe),
            ("Contrato", fecha_legible(jugador.get("Fecha_Fin_Contrato"))),
        ]
        chip_gap = 3
        chip_w = (pdf.w - pdf.l_margin - pdf.r_margin - chip_gap * 2) / 3
        chip_h = 12
        chip_y = pdf.get_y()
        for indice, (etiqueta, valor) in enumerate(chips):
            fila = indice // 3
            columna = indice % 3
            chip_x = pdf.l_margin + columna * (chip_w + chip_gap)
            chip_actual_y = chip_y + fila * (chip_h + chip_gap)
            dibujar_chip_resumen(chip_x, chip_actual_y, chip_w, chip_h, etiqueta, valor)
        pdf.set_y(chip_y + 2 * chip_h + chip_gap + 4)

        panel_y = pdf.get_y()
        panel_h = 68
        total_w = pdf.w - pdf.l_margin - pdf.r_margin
        foto_w = 50
        gap_panel = 6
        info_w = total_w - foto_w - gap_panel
        foto_x = pdf.l_margin
        info_x = foto_x + foto_w + gap_panel

        pdf.set_fill_color(*color_panel)
        pdf.set_draw_color(*color_borde)
        pdf.rect(foto_x, panel_y, foto_w, panel_h, "DF")
        pdf.rect(info_x, panel_y, info_w, panel_h, "DF")

        foto_buffer = descargar_foto(jugador.get("URL_Foto", ""))
        if foto_buffer is not None:
            pdf.image(foto_buffer, x=foto_x + 4, y=panel_y + 4, w=foto_w - 8, h=foto_w - 8)
        else:
            pdf.set_xy(foto_x + 6, panel_y + 29.5)
            pdf.set_font("Arial", "B", 11)
            pdf.set_text_color(*color_texto_muted)
            pdf.multi_cell(foto_w - 12, 5.2, "Sin foto disponible", align="C")

        pdf.set_xy(info_x + 4, panel_y + 4)
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(*color_texto)
        pdf.cell(info_w - 8, 5, "Ficha completa del jugador", ln=True)

        datos_jugador = [
            ("Nacimiento", fecha_nacimiento),
            ("Edad", edad_texto),
            ("Nacionalidades", nacionalidades),
            ("Altura", f"{texto('Altura')} cm" if texto("Altura") != "-" else "-"),
            ("Pie hábil", texto("Pie_Hábil")),
            ("Representante", texto("representante")),
            ("Segunda nacionalidad", texto("Segunda_Nacionalidad")),
            ("Fin de contrato", fecha_legible(jugador.get("Fecha_Fin_Contrato"))),
        ]

        col_w = max((info_w - 14) / 2, 24)
        inicio_datos_y = panel_y + 14
        for indice, (etiqueta, valor) in enumerate(datos_jugador):
            fila = indice // 2
            columna = indice % 2
            campo_x = info_x + 4 + columna * (col_w + 4)
            campo_y = inicio_datos_y + fila * 9.2
            pdf.set_xy(campo_x, campo_y)
            pdf.set_font("Arial", "B", 7)
            pdf.set_text_color(*color_acento_suave)
            pdf.cell(col_w, 3.4, etiqueta.upper(), ln=True)
            pdf.set_x(campo_x)
            pdf.set_font("Arial", "", 8.8)
            pdf.set_text_color(*color_texto)
            pdf.multi_cell(col_w, 4.1, valor)

        enlaces = []
        if str(jugador.get("URL_Perfil", "")).startswith("http"):
            enlaces.append(("Perfil externo", jugador.get("URL_Perfil")))
        if str(jugador.get("video_url", "")).startswith("http"):
            enlaces.append(("Video", jugador.get("video_url")))
        if str(jugador.get("Instagram", "")).startswith("http"):
            enlaces.append(("Instagram", jugador.get("Instagram")))

        enlaces_titulo_y = panel_y + panel_h - 17
        pdf.set_xy(info_x + 4, enlaces_titulo_y)
        pdf.set_font("Arial", "B", 7)
        pdf.set_text_color(*color_acento_suave)
        pdf.cell(info_w - 8, 3.5, "ENLACES EXTERNOS", ln=True)
        dibujar_pildoras_enlaces(info_x + 4, enlaces_titulo_y + 5, info_w - 8, enlaces)

        pdf.set_y(panel_y + panel_h + 3)

        descripcion = texto("Descripcion", "Sin descripción cargada.")
        lineas_desc = max(3, min(7, len(descripcion) // 105 + 1))
        desc_h = 14 + lineas_desc * 4.6
        desc_y = pdf.get_y()
        pdf.set_fill_color(*color_panel)
        pdf.set_draw_color(*color_borde)
        pdf.rect(pdf.l_margin, desc_y, total_w, desc_h, "DF")
        pdf.set_xy(pdf.l_margin + 4, desc_y + 3)
        pdf.set_font("Arial", "B", 11)
        pdf.set_text_color(*color_texto)
        pdf.cell(total_w - 8, 5, "Descripción", ln=True)
        pdf.set_x(pdf.l_margin + 4)
        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(*color_texto_muted)
        pdf.multi_cell(total_w - 8, 5, descripcion, align="J")
        pdf.set_y(desc_y + desc_h + 4)

        dibujar_titulo_seccion_pdf(
            pdf,
            "Valoración de aspectos",
            "Radar y promedio de puntuación brindada por el equipo de scouting.",
            espacio_posterior_minimo=72,
        )

        asegurar_espacio_pdf(pdf, 68)
        radar_valoracion = crear_radar_valoracion_pdf(promedios_grupos)
        bloque_y = pdf.get_y()
        radar_panel_w = 76
        resumen_panel_x = pdf.l_margin + radar_panel_w + 6
        resumen_panel_w = pdf.w - pdf.r_margin - resumen_panel_x
        bloque_h = 62

        pdf.set_fill_color(*color_panel)
        pdf.set_draw_color(*color_borde)
        pdf.rect(pdf.l_margin, bloque_y, radar_panel_w, bloque_h, "DF")
        pdf.rect(resumen_panel_x, bloque_y, resumen_panel_w, bloque_h, "DF")
        pdf.image(radar_valoracion, x=pdf.l_margin + 4, y=bloque_y + 5, w=radar_panel_w - 8)

        pdf.set_xy(resumen_panel_x + 4, bloque_y + 5)
        pdf.set_font("Arial", "B", 10)
        pdf.set_text_color(*color_acento_suave)
        pdf.cell(resumen_panel_w - 8, 4.5, "PROMEDIO GENERAL", ln=True)
        pdf.set_x(resumen_panel_x + 4)
        pdf.set_font("Arial", "B", 22)
        pdf.set_text_color(*color_texto)
        pdf.cell(resumen_panel_w - 8, 10, f"{promedio_global:.2f}" if promedio_global is not None else "-", ln=True)
        pdf.set_x(resumen_panel_x + 4)
        pdf.set_font("Arial", "", 8.5)
        pdf.set_text_color(*color_texto_muted)
        pdf.cell(resumen_panel_w - 8, 4.5, "Escala consolidada del cuerpo de scouting", ln=True)
        pdf.ln(1.5)

        for grupo, valor in promedios_grupos.items():
            pdf.set_x(resumen_panel_x + 4)
            pdf.set_font("Arial", "", 8.8)
            pdf.set_text_color(*color_texto_muted)
            pdf.cell(resumen_panel_w * 0.7, 5.2, grupo)
            pdf.set_font("Arial", "B", 9.6)
            pdf.set_text_color(*color_texto)
            pdf.cell(resumen_panel_w * 0.2, 5.2, f"{valor:.2f}" if valor is not None else "-", ln=True, align="R")

        pdf.set_y(bloque_y + bloque_h + 5)

        pdf.add_page()
        agregar_estadisticas_pdf(
            pdf,
            jugador,
            color_acento,
            color_fondo,
            color_panel,
            color_texto,
        )

        pdf.add_page()
        dibujar_titulo_seccion_pdf(
            pdf,
            "Secuencia de informes",
            "Listado consecutivo en el orden actual de visualización, con contexto operativo y observaciones completas.",
            espacio_posterior_minimo=34,
        )

        informes_export = informes_jugador.copy()
        if not informes_export.empty:
            columna_orden = None
            if "Fecha_Partido" in informes_export.columns:
                columna_orden = "Fecha_Partido"
            elif "Fecha_Informe" in informes_export.columns:
                columna_orden = "Fecha_Informe"
            if columna_orden:
                informes_export["__orden"] = pd.to_datetime(
                    informes_export[columna_orden],
                    errors="coerce",
                    dayfirst=True,
                )
                informes_export = informes_export.sort_values("__orden", ascending=False, na_position="last")
            else:
                informes_export = informes_export.copy()

        if informes_export.empty:
            pdf.set_font("Arial", "", 10)
            pdf.set_text_color(*color_texto_muted)
            pdf.multi_cell(0, 5.5, "No hay informes registrados para este jugador.")
        else:
            for indice, (_, informe) in enumerate(informes_export.iterrows(), start=1):
                observaciones = valor_campo_pdf(informe.get("Observaciones"), "Sin observaciones cargadas.")
                observaciones = observaciones[:2200]
                lineas_obs = max(3, min(18, len(observaciones) // 104 + 1))
                card_h = 34 + lineas_obs * 5
                asegurar_espacio_pdf(pdf, card_h + 4)

                card_x = pdf.l_margin
                card_y = pdf.get_y()
                card_w = pdf.w - pdf.l_margin - pdf.r_margin

                pdf.set_fill_color(*color_panel)
                pdf.set_draw_color(*color_borde)
                pdf.rect(card_x, card_y, card_w, card_h, "DF")
                pdf.set_fill_color(*color_panel_alt)
                pdf.rect(card_x, card_y, card_w, 11, "F")

                pdf.set_xy(card_x + 4, card_y + 3)
                pdf.set_font("Arial", "B", 11)
                pdf.set_text_color(*color_texto)
                ancho_titulo = card_w * 0.32
                ancho_fecha = card_w - 8 - ancho_titulo
                pdf.cell(ancho_titulo, 4.5, f"Informe {indice:02d}", align="L")
                pdf.set_font("Arial", "", 8.5)
                pdf.set_text_color(*color_acento_suave)
                pdf.cell(
                    ancho_fecha,
                    4.5,
                    f"Fecha partido: {fecha_legible(informe.get('Fecha_Partido'))}   |   Fecha carga: {fecha_legible(informe.get('Fecha_Informe'))}",
                    ln=True,
                    align="R",
                )

                meta_1 = f"Partido: {valor_campo_pdf(informe.get('Equipos_Resultados'))}"
                meta_2 = f"Formación: {formatear_formacion_pdf(informe.get('Formación'))}"

                pdf.set_xy(card_x + 4, card_y + 15)
                pdf.set_font("Arial", "", 9)
                pdf.set_text_color(*color_texto_muted)
                pdf.multi_cell(card_w - 8, 4.8, meta_1)
                pdf.set_x(card_x + 4)
                pdf.multi_cell(card_w - 8, 4.8, meta_2)

                pdf.set_x(card_x + 4)
                pdf.set_font("Arial", "B", 8.2)
                pdf.set_text_color(*color_acento_suave)
                pdf.cell(card_w - 8, 4.5, "OBSERVACIONES", ln=True)
                pdf.set_x(card_x + 4)
                pdf.set_font("Arial", "", 9.5)
                pdf.set_text_color(*color_texto)
                pdf.multi_cell(card_w - 8, 5, observaciones, align="J")

                pdf.set_y(card_y + card_h + 4)

        buffer = BytesIO()
        pdf.output(buffer)
        buffer.seek(0)
        return buffer

    except Exception as e:
        st.error(f"⚠️ Error al generar PDF: {e}")
        return None


# ---------------------------------------------------------
# CARGA DE DATOS
# ---------------------------------------------------------

@st.cache_data(ttl=120)
def cargar_datos():

    columnas_jug = [
        "ID_Jugador","Nombre","Fecha_Nac","Nacionalidad","Segunda_Nacionalidad",
        "Altura","Pie_Hábil","Posición","Caracteristica","Club","Liga",
        "Descripcion",  # NUEVO CAMPO
        "Sexo","URL_Foto","URL_Perfil","Instagram","Fecha_Fin_Contrato",
        "video_url","telefono","representante"
    ]

    columnas_inf = ["ID_Informe","ID_Jugador","Scout","Fecha_Partido","Fecha_Informe",
                    "Equipos_Resultados","Formación","Observaciones","Línea",
                    "Controles","Perfiles","Pase_corto","Pase_largo","Pase_filtrado",
                    "1v1_defensivo","Recuperacion","Intercepciones","Duelos_aereos",
                    "Regate","Velocidad","Duelos_ofensivos",
                    "Resiliencia","Liderazgo","Inteligencia_tactica",
                    "Inteligencia_emocional","Posicionamiento",
                    "Vision_de_juego","Movimientos_sin_pelota"]

    columnas_short = ["ID_Jugador","Nombre","Edad","Altura","Club","Posición",
                      "URL_Foto","URL_Perfil","Agregado_Por","Fecha_Agregado"]

    df_players = cargar_datos_sheets("Jugadores", columnas_jug)
    df_reports = cargar_datos_sheets("Informes", columnas_inf)
    df_short   = cargar_datos_sheets("Lista corta", columnas_short)

    # Normalización de IDs
    for df in (df_players, df_reports, df_short):
        if not df.empty and "ID_Jugador" in df.columns:
            df["ID_Jugador"] = df["ID_Jugador"].astype(str)

    return df_players, df_reports, df_short

# ---------------------------------------------------------
# INICIALIZACIÓN
# ---------------------------------------------------------

inicializar_datasets_sesion()

# =========================================================
# 🔐 FILTRADO GLOBAL DE DATOS POR USUARIO (ÚNICO)
# =========================================================

# Fuente completa (ALL)
df_players_all = st.session_state["df_players"].copy()
df_reports_all = st.session_state["df_reports"].copy()
df_short_all   = st.session_state["df_short"].copy()

if CURRENT_ROLE != "admin":
    # Informes: solo los del scout
    df_reports_user = df_reports_all[
        df_reports_all["Scout"] == CURRENT_USER
    ].copy()

    # Lista corta: solo lo agregado por el scout
    df_short_user = df_short_all[
        df_short_all["Agregado_Por"] == CURRENT_USER
    ].copy()

    # Jugadores relacionados (informes + lista corta)
    ids = (
        set(df_reports_user["ID_Jugador"].astype(str)) |
        set(df_short_user["ID_Jugador"].astype(str))
    )

    df_players_user = df_players_all[
        df_players_all["ID_Jugador"].astype(str).isin(ids)
    ].copy()

else:
    # Admin ve todo
    df_reports_user = df_reports_all.copy()
    df_short_user   = df_short_all.copy()
    df_players_user = df_players_all.copy()

# -----------------------------
# Menú principal
# -----------------------------
menu_options = [
    "Panel General",
    "Agenda",
    "Jugadores",
    "Ver informes",
    "Lista corta",
    "Panel Scouts",
    "Estadísticas",
]

if st.session_state.get("menu") not in menu_options:
    st.session_state["menu"] = "Panel General"

st.sidebar.markdown("### Navegación")
clicked_menu_option = None
for option in menu_options:
    button_key = f"menu_btn_{option.lower().replace(' ', '_')}"
    if st.sidebar.button(
        option,
        key=button_key,
        use_container_width=True,
        type="primary" if st.session_state["menu"] == option else "secondary",
    ):
        clicked_menu_option = option

if clicked_menu_option and clicked_menu_option != st.session_state["menu"]:
    st.session_state["menu"] = clicked_menu_option
    st.rerun()

menu = st.session_state["menu"]


# =========================================================
# BLOQUE 3 / 5 — Sección Jugadores
# =========================================================

if st.session_state["menu"] == "Jugadores":
    # ---------------------------------------------------------
    # DATASETS
    # ---------------------------------------------------------
    df_players = df_players_all.copy()      # 🔓 todos los jugadores
    df_reports = df_reports_user.copy()     # 🔐 solo informes del scout

    # ---------------------------------------------------------
    # OPCIONES PREDEFINIDAS
    # ---------------------------------------------------------
    opciones_pies = ["Derecho", "Izquierdo", "Ambidiestro"]

    opciones_posiciones = [
        "Arquero", "Lateral derecho", "Defensa central derecho",
        "Defensa central izquierdo", "Lateral izquierdo",
        "Mediocampista defensivo", "Mediocampista mixto",
        "Mediocampista ofensivo", "Extremo derecho",
        "Extremo izquierdo", "Delantero centro"
    ]

    opciones_ligas = [
        "Argentina - LPF", "Argentina - Primera Nacional", "Argentina - B Metro", "Argentina - Federal A", "Argentina - Primera C",
        "Argentina - Proyección", "Argentina - Reserva ascenso", "Argentina - Regional Amateur", "Argentina - Promocional Amateur", "Brasil - Serie A (Brasileirão)", "Brasil - Serie B",
        "Chile - Primera División", "Chile - Segunda División", "Uruguay - Primera División",
        "Uruguay - Segunda División", "Paraguay - División Profesional",
        "Colombia - Primera A", "Ecuador - LigaPro Serie A", "Ecuador - Serie B",
        "Perú - Liga 1", "Venezuela - Liga FUTVE", "México - Liga MX",
        "España - LaLiga", "España - LaLiga 2", "España - 1 RFEF", "España - 2 RFEF", "Italia - Serie A", "Italia - Serie B", "Italia - Serie C",
        "Inglaterra - Premier League", "Inglaterra - Championship",
        "Francia - Ligue 1", "Alemania - Bundesliga", "Portugal - Primeira Liga",
        "Países Bajos - Eredivisie", "Suiza - Super League",
        "Polonia - Liga Polaca", "Bélgica - Pro League",
        "Grecia - Super League", "Turquía - Süper Lig",
        "Arabia Saudita - Saudi Pro League", "Estados Unidos - MLS",
        "Otro"
    ]

    opciones_paises = [
        "Argentina", "Brasil", "Chile", "Uruguay", "Paraguay", "Colombia", "México",
        "Ecuador", "Perú", "Venezuela", "España", "Italia", "Francia", "Inglaterra",
        "Alemania", "Portugal", "Estados Unidos", "Canadá", "Bolivia",
        "Honduras", "Costa Rica", "El Salvador", "Panamá","Cuba",
        "República Dominicana", "Guatemala", "Haití", "Jamaica", "Otro"
    ]

    opciones_caracteristicas = [
        "agresivo", "completo", "tiempista", "dinámico", "velocista", "goleador",
        "juego de espalda", "líder defensivo", "versátil", "posicional",
        "habilidoso", "táctico", "aguerrido", "resolutivo", "creativo",
        "preciso", "criterioso", "aplomado", "potente", "temperamental",
        "técnico", "conductor", "proyección"
    ]

    # ---------------------------------------------------------
    # BUSCADOR DE JUGADORES
    # ---------------------------------------------------------
    opciones = {
        f"{row['Nombre']} - {row['Club']}": row["ID_Jugador"]
        for _, row in df_players.iterrows()
    }

    ultimo_registro_jugador = "-"
    if "Fecha_Informe" in df_reports.columns and not df_reports.empty:
        fechas_base_jug = pd.to_datetime(df_reports["Fecha_Informe"], format="%d/%m/%Y", errors="coerce")
        if fechas_base_jug.notna().any():
            ultimo_registro_jugador = fechas_base_jug.max().strftime("%d/%m/%Y")

    alcance_jugadores = "Base completa" if CURRENT_ROLE == "admin" else "Jugadores vinculados"

    render_html_block(
        f"""
        <div class="alab-dashboard-hero">
            <div class="alab-dashboard-hero-kicker">Repositorio</div>
            <h1 class="alab-dashboard-hero-title">Jugadores</h1>
            <div class="alab-dashboard-chip-row">
                <span class="alab-dashboard-chip"><strong>Alcance</strong> {alcance_jugadores}</span>
                <span class="alab-dashboard-chip"><strong>Jugadores</strong> {df_players['ID_Jugador'].nunique()}</span>
                <span class="alab-dashboard-chip"><strong>Informes visibles</strong> {len(df_reports)}</span>
                <span class="alab-dashboard-chip"><strong>Último registro</strong> {ultimo_registro_jugador}</span>
            </div>
        </div>
        """
    )

    seleccion_jug = ""
    seleccion_jug = st.selectbox(
        "🔍 Buscar jugador",
        [""] + list(opciones.keys())
    )

    # ---------------------------------------------------------
    # CREAR NUEVO JUGADOR
    # ---------------------------------------------------------
    if not seleccion_jug:

        render_html_block(
            f"""
            <div class="alab-mini-grid">
                <div class="alab-mini-stat">
                    <span class="alab-mini-label">Jugadores cargados</span>
                    <span class="alab-mini-value">{df_players['ID_Jugador'].nunique()}</span>
                    <span class="alab-mini-copy">Base disponible para búsqueda, edición o alta manual.</span>
                </div>
                <div class="alab-mini-stat">
                    <span class="alab-mini-label">Ligas cubiertas</span>
                    <span class="alab-mini-value">{df_players['Liga'].nunique() if 'Liga' in df_players.columns else 0}</span>
                    <span class="alab-mini-copy">Volumen actual de competencias representadas en el repositorio.</span>
                </div>
                <div class="alab-mini-stat">
                    <span class="alab-mini-label">Nacionalidades</span>
                    <span class="alab-mini-value">{df_players['Nacionalidad'].nunique() if 'Nacionalidad' in df_players.columns else 0}</span>
                    <span class="alab-mini-copy">Cobertura geográfica del universo de jugadores cargados.</span>
                </div>
            </div>
            """
        )

        section_header(
            "Alta de nuevo jugador",
        )


        # Mostrar toast persistente si corresponde
        if st.session_state.get("toast_guardado_jugador"):
            st.toast("✅ Jugador guardado correctamente.", icon="✅")
            st.session_state["toast_guardado_jugador"] = False


        with st.expander("➕ Agregar nuevo jugador", expanded=False):
            with st.form("nuevo_jugador_form", clear_on_submit=True):
                col1, col2 = st.columns(2)

                with col1:
                    nuevo_nombre = st.text_input("Nombre completo", value="")
                    nueva_fecha = st.text_input("Fecha de nacimiento (dd/mm/aaaa)", value="")
                    nueva_altura = st.number_input("Altura (cm)", 140, 210, 175)
                    nuevo_pie = st.selectbox("Pie hábil", opciones_pies, index=0)
                    nueva_posicion = st.selectbox("Posición principal", opciones_posiciones, index=0)
                    nueva_fecha_fin_contrato = st.text_input("Fin de contrato (dd/mm/aaaa)", value="")
                    nombre_wyscout = st.text_input("Nombre wyscout", value="")

                with col2:
                    nuevo_club = st.text_input("Club actual", value="")
                    nueva_liga = st.selectbox("Liga", opciones_ligas, index=0)
                    nueva_nacionalidad = st.selectbox("Nacionalidad", opciones_paises, index=0)
                    nueva_seg_nac = st.selectbox("Segunda nacionalidad", [""] + opciones_paises, index=0)
                    nueva_descripcion = st.text_area("Descripción del jugador", value="", height=80)
                    nueva_caracteristica = st.multiselect("Características", opciones_caracteristicas, default=[])
                    nueva_url_foto = st.text_input("URL Foto", value="")
                    nueva_url_perfil = st.text_input("URL Perfil", value="")
                    nueva_instagram = st.text_input("Instagram", value="")
                    nueva_video = st.text_input("URL Video", value="")
                    nuevo_telefono = st.text_input("Teléfono", value="")
                    nuevo_representante = st.text_input("Representante", value="")

                guardar = st.form_submit_button("💾 Guardar jugador")

                if guardar and nuevo_nombre:
                    try:
                        ws = obtener_hoja("Jugadores")
                        data_sheet = ws.get_all_records()
                        df_sheet = pd.DataFrame(data_sheet)

                        if not df_sheet.empty and "ID_Jugador" in df_sheet.columns:
                            max_id = pd.to_numeric(
                                df_sheet["ID_Jugador"],
                                errors="coerce"
                            ).max()
                            nuevo_id = int(max_id) + 1 if pd.notna(max_id) else 1
                        else:
                            nuevo_id = 1

                        car_str = ", ".join(nueva_caracteristica) if nueva_caracteristica else ""

                        fila = [
                            nuevo_id,                                 # 0 ID_Jugador
                            nuevo_nombre or "",                       # 1 Nombre
                            nueva_fecha or "",                        # 2 Fecha_Nac
                            nueva_nacionalidad or "",                # 3 Nacionalidad
                            nueva_seg_nac or "",                      # 4 Segunda nacionalidad
                            nueva_altura if nueva_altura else 175,     # 5 Altura
                            nuevo_pie or opciones_pies[0],             # 6 Pie hábil
                            nueva_posicion or opciones_posiciones[0],  # 7 Posición
                            car_str,                                   # 8 Caracteristica
                            nuevo_club or "",                         # 9 Club
                            nueva_liga or opciones_ligas[0],           # 10 Liga
                            nueva_descripcion or "",                  # 11 Descripcion
                            "",                                       # 12 Sexo
                            nueva_url_foto or "",                     # 13 URL_Foto
                            nueva_url_perfil or "",                   # 14 URL_Perfil
                            nueva_instagram or "",                    # 15 Instagram
                            nueva_fecha_fin_contrato or "",           # 16 Fin de contrato
                            nueva_video or "",                        # 17 URL Video
                            nuevo_telefono or "",                     # 18 Teléfono
                            nuevo_representante or "",                # 19 Representante
                            nombre_wyscout or ""                      # 20 nombre_wyscout
                        ]
                        # Convertir todos los valores numpy.int64 a int antes de guardar
                        import numpy as np
                        fila = [int(x) if isinstance(x, np.integer) else x for x in fila]
                        ws.append_row(fila, value_input_option="USER_ENTERED")
                        st.cache_data.clear()
                        st.session_state["toast_guardado_jugador"] = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al guardar jugador: {e}")

    # ---------------------------------------------------------
    # MOSTRAR JUGADOR SELECCIONADO
    # ---------------------------------------------------------
    if seleccion_jug:

        id_jugador = opciones[seleccion_jug]
        jugador = df_players[df_players["ID_Jugador"] == id_jugador].iloc[0]
        informes_jugador = df_reports[
            df_reports["ID_Jugador"].astype(str) == str(id_jugador)
        ].copy()
        shortlists_jugador = df_short_all[
            df_short_all["ID_Jugador"].astype(str) == str(id_jugador)
        ].copy()

        ultimo_informe = "-"
        if not informes_jugador.empty and "Fecha_Informe" in informes_jugador.columns:
            fechas_jugador = pd.to_datetime(
                informes_jugador["Fecha_Informe"],
                format="%d/%m/%Y",
                errors="coerce",
            ).dropna()
            if not fechas_jugador.empty:
                ultimo_informe = fechas_jugador.max().strftime("%d/%m/%Y")

        linea_actual = "-"
        if not informes_jugador.empty and "Línea" in informes_jugador.columns:
            linea_actual = str(informes_jugador.iloc[-1].get("Línea", "-")) or "-"

        section_header(f"Ficha de {jugador['Nombre']}")
        resumen_cols = st.columns(4)
        with resumen_cols[0]:
            st.metric("Informes visibles", len(informes_jugador))
        with resumen_cols[1]:
            st.metric("Último informe", ultimo_informe)
        with resumen_cols[2]:
            st.metric(
                "Presencia en shortlist",
                shortlists_jugador["Agregado_Por"].nunique() if not shortlists_jugador.empty else 0,
            )
        with resumen_cols[3]:
            st.metric("Contrato", jugador.get("Fecha_Fin_Contrato", "-") or "-")

        edad = calcular_edad(jugador.get("Fecha_Nac"))
        nac1 = jugador.get("Nacionalidad", "-")
        nac2 = jugador.get("Segunda_Nacionalidad", "")
        nacionalidades = nac1 if not nac2 else f"{nac1}, {nac2}"
        fin_contrato = jugador.get("Fecha_Fin_Contrato", "-") or "-"
        descripcion_jugador = str(jugador.get("Descripcion", "") or "").strip()
        caracteristicas = [
            item.strip() for item in str(jugador.get("Caracteristica", "") or "").split(",") if item.strip()
        ]
        badges_caracteristicas = "".join(
            f"<span class='alab-badge alab-badge-muted'>{item}</span>" for item in caracteristicas
        )
        if not badges_caracteristicas:
            badges_caracteristicas = "<span class='alab-player-panel-copy'>Sin rasgos destacados cargados.</span>"

        nacionalidad_secundaria = jugador.get("Segunda_Nacionalidad", "") or "No informada"
        scouts_shortlist = sorted(shortlists_jugador["Agregado_Por"].dropna().astype(str).unique().tolist()) if not shortlists_jugador.empty else []
        scouts_texto = ", ".join(scouts_shortlist[:4]) if scouts_shortlist else "Todavía no aparece en lista corta"
        foto_url = str(jugador.get("URL_Foto", "") or "").strip()
        club_actual = jugador.get("Club", "-") or "-"
        posicion_actual = jugador.get("Posición", "-") or "-"
        perfil_subtitulo = " · ".join(
            valor for valor in [club_actual, posicion_actual] if str(valor).strip() and str(valor).strip() != "-"
        ) or "Perfil principal"
        perfil_contexto = str(jugador.get("Liga", "-") or "-")

        links_html = []
        if str(jugador.get("URL_Perfil", "")).startswith("http"):
            links_html.append(f"<a href='{jugador['URL_Perfil']}' target='_blank'>Perfil externo</a>")
        if str(jugador.get("video_url", "")).startswith("http"):
            links_html.append(f"<a href='{jugador['video_url']}' target='_blank'>Ver video</a>")
        if str(jugador.get("Instagram", "")).startswith("http"):
            links_html.append(f"<a href='{jugador['Instagram']}' target='_blank'>Instagram</a>")
        links_row = "".join(f"<span class='alab-player-link'>{link}</span>" for link in links_html)
        if not links_row:
            links_row = "<span class='alab-player-link alab-player-link-disabled'>Sin enlaces externos</span>"

        foto_html = (
            f"<img src='{foto_url}' alt='Foto de {jugador.get('Nombre', 'jugador')}' class='alab-player-photo'/>"
            if foto_url.startswith("http")
            else "<div class='alab-player-photo-placeholder'>Sin foto</div>"
        )

        top_left, top_right = st.columns(2)
        bottom_left, bottom_right = st.columns(2)

        with top_left:
            render_html_block(
                f"""
                <div class="alab-player-panel alab-player-panel-tall alab-player-media-panel">
                    <div class="alab-player-media-row">
                        <div class="alab-player-media-wrap">
                            {foto_html}
                        </div>
                        <div class="alab-player-summary alab-player-summary-focused">
                            <div class="alab-player-identity-block alab-player-identity-block-compact">
                                <div class="alab-player-subtitle">{perfil_subtitulo}</div>
                                <div class="alab-player-context">{perfil_contexto}</div>
                            </div>
                            <div class="alab-player-link-row alab-player-link-row-inline">{links_row}</div>
                        </div>
                    </div>
                </div>
                """
            )

        with top_right:
            render_html_block(
                f"""
                <div class="alab-player-panel alab-player-panel-tall">
                    <div class="alab-player-panel-title">Lectura rápida</div>
                    <div class="alab-player-panel-copy">{descripcion_jugador or 'Todavía no hay una descripción cargada para este jugador.'}</div>
                    <div class="alab-badge-row" style="margin-top:0.9rem;">{badges_caracteristicas}</div>
                </div>
                """
            )

        with bottom_left:
            render_html_block(
                f"""
                <div class="alab-player-panel alab-player-panel-tall">
                    <div class="alab-player-panel-title">Ficha rápida</div>
                    <div class="alab-detail-grid">
                        <div class="alab-detail-item">
                            <span class="alab-detail-label">Nacimiento</span>
                            <span class="alab-detail-value">{jugador.get('Fecha_Nac', '')} ({edad} años)</span>
                        </div>
                        <div class="alab-detail-item">
                            <span class="alab-detail-label">Nacionalidad</span>
                            <span class="alab-detail-value">{nacionalidades}</span>
                        </div>
                        <div class="alab-detail-item">
                            <span class="alab-detail-label">Altura</span>
                            <span class="alab-detail-value">{jugador.get('Altura', '-')} cm</span>
                        </div>
                        <div class="alab-detail-item">
                            <span class="alab-detail-label">Pie hábil</span>
                            <span class="alab-detail-value">{jugador.get('Pie_Hábil', '-')}</span>
                        </div>
                        <div class="alab-detail-item">
                            <span class="alab-detail-label">Fin de contrato</span>
                            <span class="alab-detail-value">{fin_contrato}</span>
                        </div>
                        <div class="alab-detail-item">
                            <span class="alab-detail-label">Contacto</span>
                            <span class="alab-detail-value">{jugador.get('telefono', '-')}</span>
                        </div>
                        <div class="alab-detail-item">
                            <span class="alab-detail-label">Representante</span>
                            <span class="alab-detail-value">{jugador.get('representante', '-')}</span>
                        </div>
                    </div>
                </div>
                """
            )

        with bottom_right:
            render_html_block(
                f"""
                <div class="alab-player-panel alab-player-panel-tall">
                    <div class="alab-player-panel-title">Contexto de seguimiento</div>
                    <div class="alab-detail-grid">
                        <div class="alab-detail-item">
                            <span class="alab-detail-label">Segunda nacionalidad</span>
                            <span class="alab-detail-value">{nacionalidad_secundaria}</span>
                        </div>
                        <div class="alab-detail-item">
                            <span class="alab-detail-label">Última línea</span>
                            <span class="alab-detail-value">{linea_actual}</span>
                        </div>
                        <div class="alab-detail-item">
                            <span class="alab-detail-label">Shortlist</span>
                            <span class="alab-detail-value">{scouts_texto}</span>
                        </div>
                        <div class="alab-detail-item">
                            <span class="alab-detail-label">Nombre Wyscout</span>
                            <span class="alab-detail-value">{jugador.get('nombre_wyscout', '-') or '-'}</span>
                        </div>
                    </div>
                </div>
                """
            )

        render_html_block("<div class='alab-player-cta-gap'></div>")

        if CURRENT_ROLE in ["admin", "scout"]:
            accion_left, accion_center, accion_right = st.columns([1.2, 1, 1.2])
            with accion_center:
                if st.button("⭐ Agregar a lista corta", use_container_width=True):
                    try:
                        ws_short = obtener_hoja("Lista corta")
                        data_short = ws_short.get_all_records()
                        df_short_local = pd.DataFrame(data_short)

                        from datetime import date
                        hoy = date.today()
                        ANIO_ACTUAL = hoy.year
                        SEMESTRE_ACTUAL = 1 if hoy.month <= 6 else 2

                        if not df_short_local.empty:
                            df_short_local["Fecha_Agregado_dt"] = pd.to_datetime(
                                df_short_local["Fecha_Agregado"],
                                format="%d/%m/%Y",
                                errors="coerce"
                            )

                            df_short_local["Año"] = df_short_local["Fecha_Agregado_dt"].dt.year
                            df_short_local["Semestre"] = df_short_local["Fecha_Agregado_dt"].dt.month.apply(
                                lambda m: 1 if m <= 6 else 2
                            )

                            existe = df_short_local[
                                (df_short_local["ID_Jugador"].astype(str) == str(jugador["ID_Jugador"])) &
                                (df_short_local["Agregado_Por"] == CURRENT_USER) &
                                (df_short_local["Año"] == ANIO_ACTUAL) &
                                (df_short_local["Semestre"] == SEMESTRE_ACTUAL)
                            ]
                        else:
                            existe = pd.DataFrame()

                        if not existe.empty:
                            st.info("⚠️ Ya agregaste este jugador a tu lista corta en este semestre")
                        else:
                            nueva_fila = [
                                jugador["ID_Jugador"],
                                jugador["Nombre"],
                                edad,
                                jugador.get("Altura", "-"),
                                jugador.get("Club", "-"),
                                jugador.get("Posición", "-"),
                                jugador.get("URL_Foto", ""),
                                jugador.get("URL_Perfil", ""),
                                CURRENT_USER,
                                hoy.strftime("%d/%m/%Y")
                            ]
                            nueva_fila = [
                                int(x) if isinstance(x, (np.integer,)) else
                                float(x) if isinstance(x, (np.floating,)) else
                                str(x) if x is not None else ""
                                for x in nueva_fila
                            ]
                            ws_short.append_row(nueva_fila, value_input_option="USER_ENTERED")
                            st.toast("⭐ Jugador agregado a Lista Corta", icon="⭐")
                            st.cache_data.clear()

                    except Exception as e:
                        st.error(f"Error al agregar a lista corta: {e}")

            
        # ---------------------------------------------------------
        # EDITAR DATOS DEL JUGADOR
        # ---------------------------------------------------------
        with st.expander("✏️ Editar información del jugador", expanded=False):

            with st.form(f"editar_jugador_form_{jugador['ID_Jugador']}"):



                col1, col2 = st.columns(2)

                with col1:
                    e_nombre = st.text_input("Nombre completo", value=str(jugador.get("Nombre", "") or ""))
                    e_fecha = st.text_input("Fecha de nacimiento (dd/mm/aaaa)", value=str(jugador.get("Fecha_Nac", "") or ""))
                    try:
                        altura_val = int(float(jugador.get("Altura", 175)))
                        if not (140 <= altura_val <= 210):
                            altura_val = 175
                    except Exception:
                        altura_val = 175
                    e_altura = st.number_input("Altura (cm)", 140, 210, altura_val)
                    pie_val = jugador.get("Pie_Hábil", "") or ""
                    e_pie = st.selectbox(
                        "Pie hábil", opciones_pies,
                        index=opciones_pies.index(pie_val) if pie_val in opciones_pies else 0
                    )
                    pos_val = jugador.get("Posición", "") or ""
                    e_pos = st.selectbox(
                        "Posición", opciones_posiciones,
                        index=opciones_posiciones.index(pos_val) if pos_val in opciones_posiciones else 0
                    )
                    e_fin_contrato = st.text_input(
                        "Fin de contrato (dd/mm/aaaa)",
                        value=str(jugador.get("Fecha_Fin_Contrato", "") or "")
                    )
                    e_nombre_wyscout = st.text_input("Nombre wyscout", value=str(jugador.get("nombre_wyscout", "") or ""))

                with col2:
                    e_club = st.text_input("Club actual", value=str(jugador.get("Club", "") or ""))
                    liga_val = jugador.get("Liga", "") or ""
                    e_liga = st.selectbox(
                        "Liga", opciones_ligas,
                        index=opciones_ligas.index(liga_val) if liga_val in opciones_ligas else 0
                    )
                    nac_val = jugador.get("Nacionalidad", "") or ""
                    e_nac = st.selectbox(
                        "Nacionalidad principal", opciones_paises,
                        index=opciones_paises.index(nac_val) if nac_val in opciones_paises else 0
                    )
                    e_seg_opciones = [""] + opciones_paises
                    seg_val = jugador.get("Segunda_Nacionalidad", "") or ""
                    e_seg = st.selectbox(
                        "Segunda nacionalidad (opcional)",
                        e_seg_opciones,
                        index=e_seg_opciones.index(seg_val) if seg_val in e_seg_opciones else 0
                    )
                    car_val = str(jugador.get("Caracteristica", "") or "")
                    e_car = st.multiselect(
                        "Características",
                        opciones_caracteristicas,
                        default=[
                            c.strip().lower()
                            for c in car_val.split(",")
                            if c.strip().lower() in [o.lower() for o in opciones_caracteristicas]
                        ]
                    )
                    e_foto = st.text_input("URL de foto", value=str(jugador.get("URL_Foto", "") or ""))
                    e_link = st.text_input("URL perfil externo", value=str(jugador.get("URL_Perfil", "") or ""))
                    e_instagram = st.text_input("URL Instagram", value=str(jugador.get("Instagram", "") or ""))
                    e_video = st.text_input("URL Video", value=str(jugador.get("video_url", "") or ""))
                    e_telefono = st.text_input("Teléfono", value=str(jugador.get("telefono", "") or ""))
                    e_representante = st.text_input("Representante", value=str(jugador.get("representante", "") or ""))
                    e_descripcion = st.text_area(
                        "Descripción del jugador (párrafo introductorio)",
                        value=str(jugador.get("Descripcion", "") or ""),
                        height=80
                    )

                guardar_ed = st.form_submit_button("💾 Guardar cambios")

                if guardar_ed:
                    try:
                        ws = obtener_hoja("Jugadores")
                        data = ws.get_all_records()
                        df_actual = pd.DataFrame(data)

                        index_row = df_actual.index[
                            df_actual["ID_Jugador"].astype(str) == str(id_jugador)
                        ]


                        if not index_row.empty:
                            row_number = index_row[0] + 2
                            e_car_str = ", ".join(e_car) if e_car else ""
                            valores = [
                                id_jugador,           # 0
                                e_nombre,             # 1
                                e_fecha,              # 2
                                e_nac,                # 3
                                e_seg,                # 4
                                e_altura,             # 5
                                e_pie,                # 6
                                e_pos,                # 7
                                e_car_str,            # 8
                                e_club,               # 9
                                e_liga,               # 10
                                e_descripcion,        # 11 (NUEVO)
                                "",                  # 12 (Sexo, si se usa)
                                e_foto,               # 13
                                e_link,               # 14
                                e_instagram,          # 15
                                e_fin_contrato,       # 16
                                e_video,              # 17
                                e_telefono,           # 18
                                e_representante,      # 19
                                e_nombre_wyscout      # 20
                            ]

                            last_col = col_letter(len(valores))
                            ws.update(f"A{row_number}:{last_col}{row_number}", [valores])

                            st.cache_data.clear()
                            st.session_state["toast_guardado_jugador"] = True
                            st.rerun()
                        else:
                            st.warning("⚠️ No se encontró el jugador en la hoja.")

                    except Exception as e:
                        st.error(f"⚠️ Error al guardar: {e}")


        # ---------------------------------------------------------

        # ---------------------------------------------------------
        if CURRENT_ROLE in ["admin", "scout"]:

            st.markdown("---")
            section_header("Cargar nuevo informe")

            with st.form(f"nuevo_informe_form_{jugador['ID_Jugador']}", clear_on_submit=True):

                scout = CURRENT_USER
                fecha_partido = st.date_input("Fecha del partido", format="DD/MM/YYYY")
                equipos_resultados = st.text_input("Equipos y resultado")
                formacion = st.selectbox(
                    "Formación",
                    ["4-2-3-1","4-1-4-1", "4-3-1-2", "4-1-3-2", "4-4-2", "4-3-3", "3-5-2", "3-4-3", "5-3-2"]
                )

                observaciones = st.text_area("Observaciones generales", height=100)

                linea = st.selectbox(
                    "Línea de seguimiento",
                    [
                        "Exponencial",
                        "Destacado",
                        "Acorde",
                        "Desarrollo",
                        "En observación"
                    ]
                )

                with st.expander("🎯 Habilidades técnicas"):
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        controles = st.slider("Controles", 1, 10, 5, 1)
                        perfiles = st.slider("Perfiles", 1, 10, 5, 1)

                    with col2:
                        pase_corto = st.slider("Pase corto", 1, 10, 5, 1)
                        pase_largo = st.slider("Pase largo", 1, 10, 5, 1)

                    with col3:
                        pase_filtrado = st.slider("Pase filtrado", 1, 10, 5, 1)

                with st.expander("Aspectos defensivos"):
                    col1, col2 = st.columns(2)

                    with col1:
                        v1_def = st.slider("1v1 defensivo", 1, 10, 5, 1)
                        recuperacion = st.slider("Recuperación", 1, 10, 5, 1)

                    with col2:
                        intercepciones = st.slider("Intercepciones", 1, 10, 5, 1)
                        duelos_aereos = st.slider("Duelos aéreos", 1, 10, 5, 1)

                with st.expander("Aspectos ofensivos"):
                    col1, col2 = st.columns(2)

                    with col1:
                        regate = st.slider("Regate", 1, 10, 5, 1)
                        velocidad = st.slider("Velocidad", 1, 10, 5, 1)

                    with col2:
                        duelos_of = st.slider("Duelos ofensivos", 1, 10, 5, 1)

                with st.expander("Aspectos mentales / psicológicos"):
                    col1, col2 = st.columns(2)

                    with col1:
                        resiliencia = st.slider("Resiliencia", 1, 10, 5, 1)
                        liderazgo = st.slider("Liderazgo", 1, 10, 5, 1)

                    with col2:
                        int_tactica = st.slider("Inteligencia táctica", 1, 10, 5, 1)
                        int_emocional = st.slider("Inteligencia emocional", 1, 10, 5, 1)

                with st.expander("Aspectos tácticos"):
                    col1, col2 = st.columns(2)

                    with col1:
                        posicionamiento = st.slider("Posicionamiento", 1, 10, 5, 1)
                        vision = st.slider("Visión de juego", 1, 10, 5, 1)

                    with col2:
                        movimientos = st.slider("Movimientos sin pelota", 1, 10, 5, 1)

                guardar_informe = st.form_submit_button("Guardar informe")

                if guardar_informe:
                    try:

                        def to_float_safe(v):
                            try:
                                if isinstance(v, str):
                                    v = v.replace(",", ".")
                                return round(float(v), 2)
                            except Exception:
                                return 0.0

                        nuevo = [
                            generar_id_unico(df_reports_all, "ID_Informe"),
                            jugador["ID_Jugador"],
                            CURRENT_USER,
                            fecha_partido.strftime("%d/%m/%Y"),
                            date.today().strftime("%d/%m/%Y"),
                            equipos_resultados,
                            formacion,
                            observaciones,
                            linea,
                            to_float_safe(controles),
                            to_float_safe(perfiles),
                            to_float_safe(pase_corto),
                            to_float_safe(pase_largo),
                            to_float_safe(pase_filtrado),
                            to_float_safe(v1_def),
                            to_float_safe(recuperacion),
                            to_float_safe(intercepciones),
                            to_float_safe(duelos_aereos),
                            to_float_safe(regate),
                            to_float_safe(velocidad),
                            to_float_safe(duelos_of),
                            to_float_safe(resiliencia),
                            to_float_safe(liderazgo),
                            to_float_safe(int_tactica),
                            to_float_safe(int_emocional),
                            to_float_safe(posicionamiento),
                            to_float_safe(vision),
                            to_float_safe(movimientos)
                        ]

                        ws_inf = obtener_hoja("Informes")
                        import numpy as np
                        nuevo = [int(x) if isinstance(x, np.integer) else x for x in nuevo]
                        ws_inf.append_row(nuevo, value_input_option="USER_ENTERED")

                        st.cache_data.clear()
                        st.session_state["toast_guardado_informe"] = jugador["Nombre"]
                        st.rerun()
                    except Exception as e:
                        st.error(f"⚠️ Error al guardar el informe: {e}")

        # Mostrar toast persistente si corresponde (edición jugador o informe)
        if st.session_state.get("toast_guardado_jugador"):
            st.toast("✅ Datos actualizados correctamente.", icon="✅")
            st.session_state["toast_guardado_jugador"] = False
        if st.session_state.get("toast_guardado_informe"):
            st.toast(f"✅ Informe guardado correctamente para {st.session_state['toast_guardado_informe']}", icon="✅")
            st.session_state["toast_guardado_informe"] = False




# =========================================================
# BLOQUE ESTADÍSTICAS — Comparativo jugador vs promedio de liga
# =========================================================

if st.session_state["menu"] == "Estadísticas":

    st.subheader("Estadísticas comparativas")
    section_header(
        "Comparativa jugador vs promedio de liga",
        eyebrow="Estadísticas",
        caption="Consultá la referencia competitiva del jugador seleccionado sin intervenir los widgets nativos de exploración.",
    )

    df_players = df_players_all.copy()

    opciones = {
        f"{row['Nombre']} - {row['Club']}": row["ID_Jugador"]
        for _, row in df_players.iterrows()
    }

    seleccion_jug = st.selectbox(
        "🔍 Buscar jugador",
        [""] + list(opciones.keys()),
        key="estadisticas_buscar_jugador"
    )

    if seleccion_jug:
        id_jugador = str(opciones[seleccion_jug])
        jugador = df_players[df_players["ID_Jugador"].astype(str) == id_jugador].iloc[0]

        df_promedios, df_data_jugadores = cargar_datos_estadisticas()
        resumen_estadistico = obtener_resumen_estadisticas_jugador(jugador, df_data_jugadores)

        st.markdown(
            f"**Jugador:** {jugador.get('Nombre', '-')}  |  "
            f"**Posición:** {jugador.get('Posición', '-')}  |  "
            f"**Liga:** {jugador.get('Liga', '-')}"
        )
        st.markdown(
            f"**Partidos jugados:** {resumen_estadistico['partidos_jugados']}  |  "
            f"**Minutos jugados:** {resumen_estadistico['minutos_jugados']}"
        )

        tabla_estadisticas, estado_estadisticas = construir_tabla_estadisticas(
            jugador,
            df_promedios,
            df_data_jugadores,
        )

        if estado_estadisticas == "jugador_sin_estadisticas":
            st.info("Jugador sin estadísticas disponibles")
        elif estado_estadisticas == "posicion_no_configurada":
            st.warning("No hay estadísticas clave configuradas para la posición seleccionada.")
        else:
            if estado_estadisticas == "sin_promedios":
                st.warning("No hay promedios de liga disponibles para la posición y liga seleccionadas.")

            st.dataframe(
                tabla_estadisticas,
                use_container_width=True,
                hide_index=True,
            )

            df_long_stats, fila_liga_referencia, etiqueta_jugador = preparar_datos_graficos_estadisticas(
                tabla_estadisticas
            )

            if df_long_stats is not None:
                st.markdown("---")
                section_header("Visualizaciones comparativas")

                if fila_liga_referencia is not None:
                    nombre_referencia = str(fila_liga_referencia[tabla_estadisticas.columns[0]])
                    metricas_radar = [
                        columna
                        for columna in tabla_estadisticas.columns
                        if columna != tabla_estadisticas.columns[0]
                    ]
                    metricas_orden = list(reversed(metricas_radar))

                    df_comparacion_directa = df_long_stats[
                        df_long_stats[tabla_estadisticas.columns[0]].isin([etiqueta_jugador, nombre_referencia])
                    ].copy()
                    df_comparacion_directa["Métrica"] = pd.Categorical(
                        df_comparacion_directa["Métrica"],
                        categories=metricas_orden,
                        ordered=True,
                    )
                    df_comparacion_directa = df_comparacion_directa.sort_values("Métrica")

                    fig_metricas = px.bar(
                        df_comparacion_directa,
                        x="Valor",
                        y="Métrica",
                        color=tabla_estadisticas.columns[0],
                        orientation="h",
                        barmode="group",
                        text="Valor",
                        title="Jugador vs promedio de liga más reciente",
                    )
                    fig_metricas.update_traces(
                        texttemplate="%{text:.2f}",
                        textposition="outside",
                        hovertemplate="<b>%{fullData.name}</b><br>%{y}: %{x:.2f}<extra></extra>",
                    )
                    fig_metricas.update_layout(
                        xaxis_title="Valor",
                        yaxis_title="",
                        legend_title_text="Referencia",
                        bargap=0.34,
                    )
                    fig_metricas.update_xaxes(showgrid=True, zeroline=False)
                    fig_metricas.update_yaxes(categoryorder="array", categoryarray=metricas_orden)
                    apply_glass_plotly(fig_metricas)
                    st.plotly_chart(fig_metricas, use_container_width=True)

                    section_header("Radar comparativo")
                    valores_jugador = [
                        convertir_valor_numerico(tabla_estadisticas.iloc[0][metrica]) or 0
                        for metrica in metricas_radar
                    ]
                    valores_liga = [
                        convertir_valor_numerico(fila_liga_referencia.get(metrica)) or 0
                        for metrica in metricas_radar
                    ]

                    fig_radar = go.Figure()
                    fig_radar.add_trace(
                        go.Scatterpolar(
                            r=valores_jugador + valores_jugador[:1],
                            theta=metricas_radar + metricas_radar[:1],
                            fill="toself",
                            name=etiqueta_jugador,
                            line=dict(color="#19e28f", width=3),
                            fillcolor="rgba(25, 226, 143, 0.22)",
                            hovertemplate="<b>" + etiqueta_jugador + "</b><br>%{theta}: %{r:.2f}<extra></extra>",
                        )
                    )
                    fig_radar.add_trace(
                        go.Scatterpolar(
                            r=valores_liga + valores_liga[:1],
                            theta=metricas_radar + metricas_radar[:1],
                            fill="toself",
                            name=nombre_referencia,
                            line=dict(color="#8fd3b4", width=2),
                            fillcolor="rgba(143, 211, 180, 0.12)",
                            hovertemplate="<b>" + nombre_referencia + "</b><br>%{theta}: %{r:.2f}<extra></extra>",
                        )
                    )
                    fig_radar.update_layout(
                        title="Radar vs promedio de liga más reciente",
                        hovermode="closest",
                        hoverlabel=dict(
                            bgcolor="rgba(10,26,20,0.96)",
                            bordercolor="rgba(25,226,143,0.34)",
                            font=dict(color="#ffffff", family="Manrope, sans-serif", size=12),
                        ),
                        polar=dict(
                            bgcolor="rgba(0,0,0,0)",
                            radialaxis=dict(
                                showline=False,
                                gridcolor="rgba(255,255,255,0.08)",
                                tickfont=dict(color="rgba(226,236,231,0.74)"),
                            ),
                            angularaxis=dict(
                                gridcolor="rgba(255,255,255,0.06)",
                                tickfont=dict(color="rgba(226,236,231,0.82)", size=11),
                            ),
                        ),
                        showlegend=True,
                        margin=dict(l=30, r=30, t=56, b=24),
                    )
                    apply_glass_plotly(fig_radar)
                    st.plotly_chart(fig_radar, use_container_width=True)
                else:
                    st.info("No hay suficientes promedios de liga para construir la comparación gráfica.")



# =========================================================
# BLOQUE 4 / 5 — Ver Informes (optimizado y con ficha completa)
# =========================================================

if st.session_state["menu"] == "Ver informes":
    # ---------------------------------------------------------
    # DATASETS SEGÚN ROL
    # ---------------------------------------------------------
    df_players = df_players_all.copy()     # 🔓 todos los jugadores

    if CURRENT_ROLE == "admin":
        df_reports = df_reports_all.copy()     # admin ve todo
    else:
        df_reports = df_reports_user.copy()    # scout ve solo sus informes

    # ---------------------------------------------------------
    # UNIFICACIÓN SEGURA
    # ---------------------------------------------------------
    try:
        df_reports["ID_Jugador"] = df_reports["ID_Jugador"].astype(str)
        df_players["ID_Jugador"] = df_players["ID_Jugador"].astype(str)
        df_merged = df_reports.merge(df_players, on="ID_Jugador", how="left")
    except Exception as e:
        st.error(f"❌ Error al unir datos: {e}")
        st.stop()

    ultimo_informe_base = "-"
    if "Fecha_Informe" in df_reports.columns and not df_reports.empty:
        fechas_tmp = pd.to_datetime(df_reports["Fecha_Informe"], format="%d/%m/%Y", errors="coerce")
        if fechas_tmp.notna().any():
            ultimo_informe_base = fechas_tmp.max().strftime("%d/%m/%Y")

    alcance_informes = "Base completa" if CURRENT_ROLE == "admin" else "Tus informes"

    render_html_block(
        f"""
        <div class="alab-dashboard-hero">
            <div class="alab-dashboard-hero-kicker">Repositorio</div>
            <h1 class="alab-dashboard-hero-title">Ver informes</h1>
            <div class="alab-dashboard-chip-row">
                <span class="alab-dashboard-chip"><strong>Alcance</strong> {alcance_informes}</span>
                <span class="alab-dashboard-chip"><strong>Informes</strong> {len(df_reports)}</span>
                <span class="alab-dashboard-chip"><strong>Último registro</strong> {ultimo_informe_base}</span>
            </div>
        </div>
        """
    )

    # =========================================================
    # FILTROS SUPERIORES
    # =========================================================
    section_header("Filtros")

    f1, f2, f3, f4, f5, f6 = st.columns(6)

    with f1:
        filtro_scout = st.multiselect(
            "Scout",
            sorted(df_merged["Scout"].dropna().unique())
        )

    with f2:
        opciones_jugadores = sorted(df_merged["Nombre"].dropna().unique())
        default_sel = st.session_state.get('filtro_jugador_default', None)
        filtro_jugador = st.multiselect(
            "Jugador",
            opciones_jugadores,
            default=default_sel
        )
        # Limpiar valor temporal si se usó
        if 'filtro_jugador_default' in st.session_state:
            try:
                del st.session_state['filtro_jugador_default']
            except Exception:
                pass

    with f3:
        filtro_club = st.multiselect(
            "Club",
            sorted(df_merged["Club"].dropna().unique())
        )

    with f4:
        filtro_pos = st.multiselect(
            "Posición",
            sorted(df_merged["Posición"].dropna().unique())
        )

    with f5:
        filtro_linea = st.multiselect(
            "Línea",
            sorted(df_merged["Línea"].dropna().unique())
        )

    with f6:
        filtro_nac = st.multiselect(
            "Nacionalidad",
            sorted(df_merged["Nacionalidad"].dropna().unique())
        )

    # ---------------------------------------------------------
    # APLICAR FILTROS
    # ---------------------------------------------------------
    df_filtrado = df_merged.copy()

    if filtro_scout:
        df_filtrado = df_filtrado[df_filtrado["Scout"].isin(filtro_scout)]
    if filtro_jugador:
        df_filtrado = df_filtrado[df_filtrado["Nombre"].isin(filtro_jugador)]
    if filtro_club:
        df_filtrado = df_filtrado[df_filtrado["Club"].isin(filtro_club)]
    if filtro_pos:
        df_filtrado = df_filtrado[df_filtrado["Posición"].isin(filtro_pos)]
    if filtro_linea:
        df_filtrado = df_filtrado[df_filtrado["Línea"].isin(filtro_linea)]
    if filtro_nac:
        df_filtrado = df_filtrado[df_filtrado["Nacionalidad"].isin(filtro_nac)]

    informes_filtrados = len(df_filtrado)
    jugadores_filtrados = df_filtrado["ID_Jugador"].nunique() if not df_filtrado.empty else 0
    scouts_filtrados = df_filtrado["Scout"].nunique() if not df_filtrado.empty else 0
    clubes_filtrados = df_filtrado["Club"].nunique() if not df_filtrado.empty else 0

    render_html_block(
        f"""
        <div class="alab-mini-grid">
            <div class="alab-mini-stat">
                <span class="alab-mini-label">Informes visibles</span>
                <span class="alab-mini-value">{informes_filtrados}</span>
                <span class="alab-mini-copy">Resultado actual luego de aplicar los filtros activos.</span>
            </div>
            <div class="alab-mini-stat">
                <span class="alab-mini-label">Jugadores</span>
                <span class="alab-mini-value">{jugadores_filtrados}</span>
                <span class="alab-mini-copy">Perfiles distintos presentes en el listado filtrado.</span>
            </div>
            <div class="alab-mini-stat">
                <span class="alab-mini-label">Scouts</span>
                <span class="alab-mini-value">{scouts_filtrados}</span>
                <span class="alab-mini-copy">Cantidad de observadores representados en la muestra.</span>
            </div>
            <div class="alab-mini-stat">
                <span class="alab-mini-label">Clubes</span>
                <span class="alab-mini-value">{clubes_filtrados}</span>
                <span class="alab-mini-copy">Instituciones incluidas dentro de la vista actual.</span>
            </div>
        </div>
        """
    )

    # =========================================================
    # TABLA PRINCIPAL (AgGrid) — DISEÑO ORIGINAL
    # =========================================================
    if not df_filtrado.empty:
        section_header("Informes disponibles")

        columnas = [
            "Fecha_Informe", "Nombre", "Club",
            "Línea", "Scout", "Equipos_Resultados", "Observaciones"
        ]

        df_detalle = df_filtrado.copy()

        try:
            df_detalle["Fecha_dt"] = pd.to_datetime(
                df_detalle["Fecha_Informe"],
                format="%d/%m/%Y",
                errors="coerce"
            )
            df_detalle = (
                df_detalle
                .sort_values("Fecha_dt", ascending=False)
            )
        except Exception:
            pass

        df_detalle = df_detalle.reset_index(drop=True)
        df_detalle["N°"] = df_detalle.index + 1

        df_tabla = df_detalle[[c for c in ["N°"] + columnas if c in df_detalle.columns]].copy()

        col_pag_1, col_pag_2, col_pag_3 = st.columns([1, 1, 3])
        with col_pag_1:
            page_size = st.selectbox(
                "Informes por página",
                [10, 15, 25, 50],
                index=1,
                key="ver_informes_page_size"
            )

        total_pages = max(1, (len(df_tabla) + page_size - 1) // page_size)

        with col_pag_2:
            pagina = st.number_input(
                "Página",
                min_value=1,
                max_value=total_pages,
                value=1,
                step=1,
                key="ver_informes_page"
            )

        inicio = (pagina - 1) * page_size
        fin = inicio + page_size

        with col_pag_3:
            st.caption(
                f"Mostrando {inicio + 1} a {min(fin, len(df_tabla))} de {len(df_tabla)} informes"
            )

        df_tabla_pagina = df_tabla.iloc[inicio:fin].copy()
        df_detalle_pagina = df_detalle.iloc[inicio:fin].copy()

        tabla_event = st.dataframe(
            df_tabla_pagina,
            use_container_width=True,
            hide_index=True,
            height=580,
            on_select="rerun",
            selection_mode="single-row",
            key=f"ver_informes_table_{pagina}_{page_size}"
        )

        selected_data = []
        selected_rows = []
        if tabla_event is not None:
            selected_rows = list(getattr(tabla_event.selection, "rows", []))

        if selected_rows:
            selected_idx = selected_rows[0]
            selected_data = [df_detalle_pagina.iloc[selected_idx].to_dict()]

        # A PARTIR DE ACÁ SIEMPRE ES list[dict]
        if len(selected_data) > 0:
            jugador_sel = selected_data[0]
            nombre_jug = jugador_sel.get("Nombre", "")
        else:
            st.info("Seleccioná un informe del listado para abrir la ficha completa del jugador.")


        # =========================================================
        # FICHA DEL JUGADOR
        # =========================================================
        if len(selected_data) > 0:

            jugador_sel = selected_data[0]
            nombre_jug = jugador_sel.get("Nombre", "")
            jugador_data = df_players[df_players["Nombre"] == nombre_jug]

            if not jugador_data.empty:
                j = jugador_data.iloc[0]

                st.markdown("---")
                section_header(
                    f"Ficha del jugador: {j['Nombre']}",
                )

                render_html_block(
                    f"""
                    <div class="alab-mini-grid">
                        <div class="alab-mini-stat">
                            <span class="alab-mini-label">Informe seleccionado</span>
                            <span class="alab-mini-value">{jugador_sel.get('Fecha_Informe', '-') or '-'}</span>
                            <span class="alab-mini-copy">Fecha del registro abierto actualmente en la tabla.</span>
                        </div>
                        <div class="alab-mini-stat">
                            <span class="alab-mini-label">Scout</span>
                            <span class="alab-mini-value">{jugador_sel.get('Scout', '-') or '-'}</span>
                            <span class="alab-mini-copy">Observador responsable del informe activo.</span>
                        </div>
                        <div class="alab-mini-stat">
                            <span class="alab-mini-label">Línea</span>
                            <span class="alab-mini-value">{jugador_sel.get('Línea', '-') or '-'}</span>
                            <span class="alab-mini-copy">Criterio o estado asignado en la última evaluación visible.</span>
                        </div>
                        <div class="alab-mini-stat">
                            <span class="alab-mini-label">Partido</span>
                            <span class="alab-mini-value">{jugador_sel.get('Fecha_Partido', '-') or '-'}</span>
                            <span class="alab-mini-copy">Referencia del encuentro asociado al informe seleccionado.</span>
                        </div>
                    </div>
                    """
                )

                ficha_cols = st.columns(4)
                with ficha_cols[0]:
                    st.metric("Club", j.get("Club", "-"))
                with ficha_cols[1]:
                    st.metric("Posición", j.get("Posición", "-"))
                with ficha_cols[2]:
                    st.metric("Edad", calcular_edad(j.get("Fecha_Nac")))
                with ficha_cols[3]:
                    st.metric("Informes", len(df_reports[df_reports["ID_Jugador"] == j["ID_Jugador"]]))

                col1, col2 = st.columns([1.1, 1.9])

                with col1:
                    foto_url = str(j.get("URL_Foto", "") or "")
                    if foto_url.startswith("http"):
                        st.image(foto_url, width=150)

                    instagram_url = str(j.get("Instagram", "") or "")
                    perfil_url = str(j.get("URL_Perfil", "") or "")
                    video_url = str(j.get("video_url", "") or "")

                    if instagram_url.startswith("http"):
                        st.markdown(f"[📸 Instagram]({instagram_url})")

                    if perfil_url.startswith("http"):
                        st.markdown(f"[🌐 Perfil externo]({perfil_url})")

                    if video_url.startswith("http"):
                        st.markdown(f"[🎬 Ver video]({video_url})")

                with col2:
                    descripcion = str(j.get("Descripcion", "") or "").strip()
                    segunda_nacionalidad = j.get("Segunda_Nacionalidad", "") or "No informada"
                    caracteristica = j.get("Caracteristica", "-") or "-"
                    fin_contrato = j.get("Fecha_Fin_Contrato", "-") or "-"
                    nombre_wyscout = j.get("nombre_wyscout", "-") or "-"

                    render_html_block(
                        f"""
                        <div class="alab-player-panel">
                            <div class="alab-player-panel-title">Perfil general</div>
                            <div class="alab-badge-row">
                                <span class="alab-badge alab-badge-muted">{j.get('Posición', '-')}</span>
                                <span class="alab-badge alab-badge-muted">{j.get('Liga', '-')}</span>
                                <span class="alab-badge alab-badge-muted">{j.get('Pie_Hábil', '-')}</span>
                            </div>
                            <div class="alab-detail-grid">
                                <div class="alab-detail-item">
                                    <span class="alab-detail-label">Club</span>
                                    <span class="alab-detail-value">{j.get('Club', '-')}</span>
                                </div>
                                <div class="alab-detail-item">
                                    <span class="alab-detail-label">Altura</span>
                                    <span class="alab-detail-value">{j.get('Altura', '-')} cm</span>
                                </div>
                                <div class="alab-detail-item">
                                    <span class="alab-detail-label">Nacionalidad</span>
                                    <span class="alab-detail-value">{j.get('Nacionalidad', '-')}</span>
                                </div>
                                <div class="alab-detail-item">
                                    <span class="alab-detail-label">Segunda nacionalidad</span>
                                    <span class="alab-detail-value">{segunda_nacionalidad}</span>
                                </div>
                                <div class="alab-detail-item">
                                    <span class="alab-detail-label">Fin de contrato</span>
                                    <span class="alab-detail-value">{fin_contrato}</span>
                                </div>
                                <div class="alab-detail-item">
                                    <span class="alab-detail-label">Nombre Wyscout</span>
                                    <span class="alab-detail-value">{nombre_wyscout}</span>
                                </div>
                                <div class="alab-detail-item">
                                    <span class="alab-detail-label">Característica</span>
                                    <span class="alab-detail-value">{caracteristica}</span>
                                </div>
                            </div>
                        </div>
                        """
                    )

                    if descripcion:
                        section_note(descripcion)
                    else:
                        st.info("Este jugador no tiene descripción cargada todavía.")

                # =========================================================
                # EXPORTAR PDF SIMPLE
                # =========================================================
                # EXPORTAR PDF COMPLETO (CON FOTO E INFORMACIÓN COMPLETA)
                # =========================================================
                if st.button("📝 Generar informe", key=f"pdf_{j['ID_Jugador']}"):
                    buffer = generar_pdf_reporte_completo(j, df_reports)
                    if buffer:
                        pdf_file_name = f"Reporte_Scouting_{str(j.get('Nombre', 'Jugador')).replace(' ', '_')}.pdf"
                        st.download_button(
                            "⬇️ Descargar PDF",
                            buffer,
                            file_name=pdf_file_name,
                            mime="application/pdf",
                            key=f"descarga_{j['ID_Jugador']}"
                        )

                # =========================================================
                # EXPANDER — EDITAR / ELIMINAR INFORMES
                # =========================================================
                informes_sel = df_reports[df_reports["ID_Jugador"] == j["ID_Jugador"]]

                for idx, inf in enumerate(informes_sel.itertuples()):
                    titulo = f"{inf.Fecha_Partido} | Scout: {inf.Scout} | Línea: {inf.Línea}"

                    with st.expander(titulo):
                        with st.form(f"form_edit_{inf.ID_Informe}_{idx}"):

                            nuevo_scout = st.text_input("Scout", inf.Scout)
                            nueva_fecha = st.text_input("Fecha del partido", inf.Fecha_Partido)
                            nuevos_equipos = st.text_input("Equipos y resultado", inf.Equipos_Resultados)

                            opciones_linea = [
                                "Exponencial", "Destacado",
                                "Acorde", "Desarrollo",
                                "En observación"
                            ]

                            nueva_linea = st.selectbox(
                                "Línea",
                                opciones_linea,
                                index=opciones_linea.index(inf.Línea)
                                if inf.Línea in opciones_linea else 2
                            )

                            nuevas_obs = st.text_area(
                                "Observaciones",
                                inf.Observaciones,
                                height=120
                            )

                            guardar = st.form_submit_button("💾 Guardar cambios")

                            if guardar:
                                try:
                                    ws_inf = obtener_hoja("Informes")

                                    # Leer hoja real
                                    data_sheet = ws_inf.get_all_records()
                                    df_sheet = pd.DataFrame(data_sheet)

                                    # Buscar fila real por ID
                                    match = df_sheet[
                                        df_sheet["ID_Informe"].astype(str) == str(inf.ID_Informe)
                                    ]

                                    if not match.empty:

                                        row_index = match.index[0] + 2  # +2 porque fila 1 es encabezado

                                        fila_actual = match.copy()

                                        # Aplicar cambios
                                        fila_actual["Scout"] = nuevo_scout
                                        fila_actual["Fecha_Partido"] = nueva_fecha
                                        fila_actual["Equipos_Resultados"] = nuevos_equipos
                                        fila_actual["Línea"] = nueva_linea
                                        fila_actual["Observaciones"] = nuevas_obs

                                        # Actualizar SOLO esa fila
                                        ws_inf.update(
                                            f"A{row_index}:AB{row_index}",
                                            [fila_actual.values.tolist()[0]]
                                        )

                                        st.cache_data.clear()
                                        st.toast("✓ Informe actualizado correctamente", icon="✅")
                                        st.rerun()
                                    else:
                                        st.error("No se encontró el informe en la hoja.")

                                except Exception as e:
                                    st.error(f"⚠️ Error al actualizar el informe: {e}")

                            st.markdown("---")

                            confirmar = st.checkbox(
                                "Confirmar eliminación del informe",
                                key=f"del_chk_{inf.ID_Informe}"
                            )

                            eliminar = st.form_submit_button(
                                "🗑️ Eliminar informe",
                                disabled=not confirmar
                            )

                            if eliminar:
                                try:
                                    eliminar_por_id(
                                        nombre_hoja="Informes",
                                        id_col="ID_Informe",
                                        id_valor=inf.ID_Informe
                                    )
                                    st.cache_data.clear()
                                    st.session_state["toast_eliminado_informe"] = True
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"⚠️ Error al eliminar el informe: {e}")
    else:
        st.info("No hay informes que coincidan con los filtros actuales.")

    # Mostrar toast persistente si corresponde (eliminación de informe)
    if st.session_state.get("toast_eliminado_informe"):
        st.toast("🗑️ Informe eliminado correctamente", icon="🗑️")
        st.session_state["toast_eliminado_informe"] = False


# =========================================================
# BLOQUE 5 / 5 — Lista corta táctica
# =========================================================

if st.session_state["menu"] == "Lista corta":
    # -----------------------------------------------------
    # DATASETS
    # -----------------------------------------------------
    df_short = df_short_user.copy()          # decisiones (todas; privacidad luego)
    df_players = df_players_all.copy()       # base completa de jugadores

    if df_short.empty:
        st.info("No hay jugadores cargados en la lista corta actualmente.")
        st.stop()

    # =========================================================
    # FILTRO DE PRIVACIDAD POR USUARIO
    # =========================================================
    if CURRENT_ROLE not in ["admin"]:
        df_short = df_short[df_short["Agregado_Por"] == CURRENT_USER]

    # Cortar referencia (evita SettingWithCopyWarning)
    df_short = df_short.copy()

    ultimo_mov_short = "-"
    if "Fecha_Agregado" in df_short.columns and not df_short.empty:
        fechas_short = pd.to_datetime(df_short["Fecha_Agregado"], errors="coerce", dayfirst=True)
        if fechas_short.notna().any():
            ultimo_mov_short = fechas_short.max().strftime("%d/%m/%Y")

    alcance_short = "Vista global" if CURRENT_ROLE == "admin" else "Tu shortlist"

    render_html_block(
        f"""
        <div class="alab-dashboard-hero">
            <div class="alab-dashboard-hero-kicker">Shortlist</div>
            <h1 class="alab-dashboard-hero-title">Lista corta</h1>
            <div class="alab-dashboard-chip-row">
                <span class="alab-dashboard-chip"><strong>Alcance</strong> {alcance_short}</span>
                <span class="alab-dashboard-chip"><strong>Registros</strong> {len(df_short)}</span>
                <span class="alab-dashboard-chip"><strong>Último movimiento</strong> {ultimo_mov_short}</span>
            </div>
        </div>
        """
    )

    # =========================================================
    # NORMALIZAR FECHA / AÑO / SEMESTRE (LISTA CORTA)
    # =========================================================
    if "Fecha_Agregado" not in df_short.columns:
        df_short["Fecha_Agregado"] = None

    df_short["Fecha_dt"] = pd.to_datetime(
        df_short["Fecha_Agregado"],
        errors="coerce",
        dayfirst=True
    )

    df_short["Año"] = df_short["Fecha_dt"].dt.year.astype("Int64")

    df_short["Semestre"] = df_short["Fecha_dt"].dt.month.apply(
        lambda m: "1º" if m <= 6 else "2º" if pd.notna(m) else ""
    )

    # =========================================================
    # 🔧 AGREGADO 1 / 2 — DEFAULT AÑO + SEMESTRE ACTUAL
    # =========================================================
    hoy = datetime.today()
    anio_actual = hoy.year
    semestre_actual = "1º" if hoy.month <= 6 else "2º"

    opciones_anio = (
        df_short["Año"]
        .dropna()
        .astype(int)
        .unique()
        .tolist()
    )

    if anio_actual in opciones_anio:
        default_anio = anio_actual
    else:
        default_anio = max(opciones_anio) if opciones_anio else ""

    default_semestre = semestre_actual

    # =========================================================
    # FILTROS
    # =========================================================
    section_header("Filtros")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        filtro_scout = st.selectbox(
            "Scout",
            [""] + sorted(df_short["Agregado_Por"].dropna().unique())
        )

    with col2:
        filtro_liga = st.selectbox(
            "Liga",
            [""] + sorted(df_players["Liga"].dropna().unique())
        )

    with col3:
        filtro_nac = st.selectbox(
            "Nacionalidad",
            [""] + sorted(df_players["Nacionalidad"].dropna().unique())
        )

    with col4:
        filtro_anio = st.selectbox(
            "Año",
            [""] + sorted(opciones_anio, reverse=True),
            index=(
                sorted(opciones_anio, reverse=True).index(default_anio) + 1
                if default_anio in opciones_anio else 0
            )
        )

    with col5:
        filtro_sem = st.selectbox(
            "Semestre",
            ["", "1º", "2º"],
            index=1 if default_semestre == "1º" else 2
        )

    with col6:
        filtro_promesa = st.selectbox(
            "Promesa",
            ["", "Sí", "No"]
        )

    # =========================================================
    # APLICAR FILTROS
    # =========================================================
    df_filtrado = df_short.copy()

    if filtro_scout:
        df_filtrado = df_filtrado[df_filtrado["Agregado_Por"] == filtro_scout]

    if filtro_liga:
        ids_liga = (
            df_players[df_players["Liga"] == filtro_liga]["ID_Jugador"]
            .astype(str)
        )
        df_filtrado = df_filtrado[
            df_filtrado["ID_Jugador"].astype(str).isin(ids_liga)
        ]

    if filtro_nac:
        ids_nac = (
            df_players[df_players["Nacionalidad"] == filtro_nac]["ID_Jugador"]
            .astype(str)
        )
        df_filtrado = df_filtrado[
            df_filtrado["ID_Jugador"].astype(str).isin(ids_nac)
        ]

    if filtro_anio:
        df_filtrado = df_filtrado[df_filtrado["Año"] == int(filtro_anio)]

    if filtro_sem:
        df_filtrado = df_filtrado[df_filtrado["Semestre"] == filtro_sem]

    if filtro_promesa == "Sí":
        df_filtrado = df_filtrado[
            df_filtrado["Posición"].str.contains("Promesa", case=False, na=False)
        ]
    elif filtro_promesa == "No":
        df_filtrado = df_filtrado[
            ~df_filtrado["Posición"].str.contains("Promesa", case=False, na=False)
        ]

    df_filtrado_vista = (
        df_filtrado
        .sort_values("Fecha_dt", ascending=False, na_position="last")
        .drop_duplicates(subset=["ID_Jugador"], keep="first")
        .copy()
    )

    total_jugadores = len(df_filtrado_vista)

    periodo_activo = "Todos los períodos"
    if filtro_anio and filtro_sem:
        periodo_activo = f"{filtro_sem} {filtro_anio}"
    elif filtro_anio:
        periodo_activo = f"Año {filtro_anio}"
    elif filtro_sem:
        periodo_activo = f"Semestre {filtro_sem}"

    render_html_block(
        f"""
        <div class="alab-mini-grid">
            <div class="alab-mini-stat">
                <span class="alab-mini-label">Jugadores filtrados</span>
                <span class="alab-mini-value">{total_jugadores}</span>
                <span class="alab-mini-copy">Perfiles visibles en la estructura táctica actual.</span>
            </div>
            <div class="alab-mini-stat">
                <span class="alab-mini-label">Scouts representados</span>
                <span class="alab-mini-value">{df_filtrado['Agregado_Por'].nunique()}</span>
                <span class="alab-mini-copy">Cantidad de observadores con presencia en la vista filtrada.</span>
            </div>
            <div class="alab-mini-stat">
                <span class="alab-mini-label">Posiciones cubiertas</span>
                <span class="alab-mini-value">{df_filtrado_vista['Posición'].nunique()}</span>
                <span class="alab-mini-copy">Diversidad posicional disponible dentro del 4-2-3-1.</span>
            </div>
            <div class="alab-mini-stat">
                <span class="alab-mini-label">Período activo</span>
                <span class="alab-mini-value">{periodo_activo}</span>
                <span class="alab-mini-copy">Ventana temporal hoy aplicada sobre la shortlist.</span>
            </div>
        </div>
        """
    )

    section_header("Vista táctica 4-2-3-1")

    # =========================================================
    # CSS TARJETAS
    # =========================================================
    # =========================================================
    # SISTEMA 4-2-3-1
    # =========================================================
    sistema = {
        "Arqueros": ["Arquero"],
        "Defensas": [
            "Lateral derecho",
            "Defensa central derecho",
            "Defensa central izquierdo",
            "Lateral izquierdo",
        ],
        "Mediocampistas defensivos": [
            "Mediocampista mixto",
            "Mediocampista defensivo",
        ],
        "Mediocampistas ofensivos": [
            "Extremo derecho",
            "Mediocampista ofensivo",
            "Extremo izquierdo",
        ],
        "Delanteros": ["Delantero centro"],
    }

    # =========================================================
    # RENDER DE JUGADORES
    # =========================================================
    for linea, posiciones in sistema.items():
        jugadores_linea = df_filtrado_vista[df_filtrado_vista["Posición"].isin(posiciones)]
        if jugadores_linea.empty:
            continue

        cantidad = len(jugadores_linea)
        with st.expander(f"{linea} ({cantidad})", expanded=True):

            if linea in ["Arqueros", "Delanteros"]:
                jugadores_lista = list(jugadores_linea.iterrows())
                for fila in range(0, len(jugadores_lista), 5):
                    fila_jugadores = jugadores_lista[fila:fila + 5]
                    fila_cols = st.columns(len(fila_jugadores))
                    for fcol, (_, row) in zip(fila_cols, fila_jugadores):
                        with fcol:
                            url_foto = str(row.get("URL_Foto", "")).strip()
                            if not url_foto.startswith("http"):
                                url_foto = "https://via.placeholder.com/60"

                            partes = str(row.get("Nombre", "")).split()
                            nombre = partes[0] if partes else "Sin nombre"
                            apellido = partes[-1] if len(partes) > 1 else ""

                            edad = row.get("Edad", "-")
                            altura = row.get("Altura", "-")
                            club = row.get("Club", "-")
                            url_perfil = str(row.get("URL_Perfil", ""))

                            link_html = (
                                f"<div class='player-link'><a href='{url_perfil}' target='_blank'>Ver perfil</a></div>"
                                if url_perfil.startswith("http") else ""
                            )

                            st.markdown(
                                f"""
                                <div class="player-card alab-player-card">
                                    <img src="{url_foto}" class="player-photo alab-player-photo"/>
                                    <div class="player-info">
                                        <h5 class="alab-player-name">{nombre} {apellido}</h5>
                                        <p class="alab-player-copy">{club}</p>
                                        <p class="alab-player-copy">Edad: {edad} | Altura: {altura} cm</p>
                                        {link_html}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

            else:
                cols = st.columns(len(posiciones))
                for i, pos in enumerate(posiciones):
                    jugadores_pos = jugadores_linea[jugadores_linea["Posición"] == pos]
                    with cols[i]:
                        st.markdown(
                            f"<div class='line-title alab-line-title'>{pos}</div>",
                            unsafe_allow_html=True
                        )

                        if jugadores_pos.empty:
                            st.markdown(
                                "<div class='alab-empty-slot'>— Vacante —</div>",
                                unsafe_allow_html=True
                            )
                            continue

                        jugadores_lista = list(jugadores_pos.iterrows())
                        salto = 2 if "Mediocampista" in pos else 1

                        for fila in range(0, len(jugadores_lista), salto):
                            fila_jugadores = jugadores_lista[fila:fila + salto]
                            fila_cols = st.columns(len(fila_jugadores))
                            for fcol, (_, row) in zip(fila_cols, fila_jugadores):
                                with fcol:
                                    url_foto = str(row.get("URL_Foto", "")).strip()
                                    if not url_foto.startswith("http"):
                                        url_foto = "https://via.placeholder.com/60"

                                    partes = str(row.get("Nombre", "")).split()
                                    nombre = partes[0] if partes else "Sin nombre"
                                    apellido = partes[-1] if len(partes) > 1 else ""

                                    edad = row.get("Edad", "-")
                                    altura = row.get("Altura", "-")
                                    club = row.get("Club", "-")
                                    url_perfil = str(row.get("URL_Perfil", ""))

                                    link_html = (
                                        f"<div class='player-link'><a href='{url_perfil}' target='_blank'>Ver perfil</a></div>"
                                        if url_perfil.startswith("http") else ""
                                    )

                                    st.markdown(
                                        f"""
                                        <div class="player-card alab-player-card">
                                            <img src="{url_foto}" class="player-photo alab-player-photo"/>
                                            <div class="player-info">
                                                <h5 class="alab-player-name">{nombre} {apellido}</h5>
                                                <p class="alab-player-copy">{club}</p>
                                                <p class="alab-player-copy">Edad: {edad} | Altura: {altura} cm</p>
                                                {link_html}
                                            </div>
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )

    # =========================================================
    # GESTOR DE LISTA CORTA — Eliminación
    # =========================================================
    st.markdown("---")
    section_header("Gestor de lista corta")

    busqueda = st.text_input("Buscar jugador para eliminar (por nombre o club)")

    if busqueda:
        df_busqueda = df_filtrado[
            df_filtrado["Nombre"].str.contains(busqueda, case=False, na=False) |
            df_filtrado["Club"].str.contains(busqueda, case=False, na=False)
        ]
    else:
        df_busqueda = df_filtrado.copy()

    if df_busqueda.empty:
        st.info("No se encontraron jugadores que coincidan con la búsqueda.")
    else:
        st.dataframe(
            df_busqueda[["Nombre", "Posición", "Club", "Agregado_Por"]],
            use_container_width=True,
            hide_index=True
        )

        jugador_sel = st.selectbox(
            "Seleccionar jugador a eliminar",
            [""] + sorted(df_busqueda["Nombre"].unique())
        )

        if jugador_sel:
            jugador_row = df_busqueda[df_busqueda["Nombre"] == jugador_sel].iloc[0]
            st.warning(f"⚠️ Vas a eliminar a **{jugador_sel}** de TU lista corta.")
            confirmar = st.checkbox("Confirmar eliminación")

            if st.button("🗑️ Eliminar jugador", type="primary", disabled=not confirmar):
                try:
                    ws_short = obtener_hoja("Lista corta")
                    data_short = ws_short.get_all_records()
                    df_short_local = pd.DataFrame(data_short)

                    fila = df_short_local.index[
                        (df_short_local["ID_Jugador"].astype(str) == str(jugador_row["ID_Jugador"])) &
                        (df_short_local["Agregado_Por"] == CURRENT_USER)
                    ]

                    if not fila.empty:
                        df_short_local = df_short_local.drop(fila[0])
                        ws_short.clear()
                        ws_short.update(
                            [df_short_local.columns.values.tolist()] +
                            df_short_local.values.tolist()
                        )
                        st.toast(
                            f"🗑️ Jugador {jugador_sel} eliminado correctamente de TU lista.",
                            icon="🗑️"
                        )
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.warning("⚠️ No se encontró el jugador en tu lista corta.")
                except Exception as e:
                    st.error(f"⚠️ Error al eliminar: {e}")


# =========================================================
# 🕐 BLOQUE 6 / 6 — Agenda de Seguimientos — ScoutingApp PRO
# =========================================================
# - Versión FINAL BLINDADA (2025)
# - Sin errores JSON, sin borrado de hojas, con backup automático
# - Cards en filas de 5 columnas, con etiquetas dinámicas y hover
# =========================================================

if st.session_state["menu"] == "Agenda":
    import os
    import pandas as pd
    from datetime import datetime, timedelta

    df_players = df_players_all.copy()

    section_header(
        "Agenda de seguimiento",
        eyebrow="Planificación",
        caption="Organizá prioridades de observación, controlá vencimientos y programá próximos seguimientos en un solo panel.",
        centered=True,
    )

    # =========================================================
    # CSS PERSONALIZADO
    # =========================================================
    # =========================================================
    # CARGA / CREACIÓN DE HOJA "Agenda"
    # =========================================================
    columnas = ["ID_Jugador", "Nombre", "Scout", "Fecha_Revisar", "Motivo", "Visto"]

    try:
        ws = obtener_hoja("Agenda", columnas)
        data = ws.get_all_records()
        df_agenda = pd.DataFrame(data)
    except Exception as e:
        st.warning("⚠️ No existía la hoja 'Agenda'. Se creará automáticamente en la base de datos.")
        try:
            ws = obtener_hoja("Agenda", columnas)
            ws.append_row(columnas)
            df_agenda = pd.DataFrame(columns=columnas)
        except Exception as err:
            st.error(f"❌ No se pudo crear la hoja Agenda: {err}")
            st.stop()

    if df_agenda.empty:
        df_agenda = pd.DataFrame(columns=columnas)

    df_agenda["Fecha_Revisar"] = pd.to_datetime(df_agenda["Fecha_Revisar"], errors="coerce")
    df_agenda["Visto"] = df_agenda["Visto"].astype(str).str.lower().isin(["si", "sí", "true", "1"])

    hoy = pd.Timestamp(datetime.now().date())
    pendientes = df_agenda[df_agenda["Visto"] == False]
    vistos = df_agenda[df_agenda["Visto"] == True]
    vencidos = pendientes[pendientes["Fecha_Revisar"] < hoy].shape[0]
    para_hoy = pendientes[pendientes["Fecha_Revisar"] == hoy].shape[0]
    proximos = pendientes[
        (pendientes["Fecha_Revisar"] > hoy) &
        (pendientes["Fecha_Revisar"] <= hoy + pd.Timedelta(days=7))
    ].shape[0]

    agenda_cols = st.columns(4)
    with agenda_cols[0]:
        st.metric("Pendientes", len(pendientes))
    with agenda_cols[1]:
        st.metric("Vencidos", vencidos)
    with agenda_cols[2]:
        st.metric("Para hoy", para_hoy)
    with agenda_cols[3]:
        st.metric("Próximos 7 días", proximos)

    # =========================================================
    # FUNCIÓN DE BACKUP LOCAL
    # =========================================================
    def backup_local(df):
        try:
            df.to_csv("agenda_backup.csv", index=False, encoding="utf-8")
        except Exception:
            pass

    # =========================================================
    # FUNCIÓN: MARCAR VISTO (segura y serializable)
    # =========================================================
    def marcar_visto(nombre):
        df_agenda.loc[df_agenda["Nombre"] == nombre, "Visto"] = "Sí"

        # Convertir fechas a texto antes de enviar
        df_tmp = df_agenda.copy()
        if "Fecha_Revisar" in df_tmp.columns:
            df_tmp["Fecha_Revisar"] = df_tmp["Fecha_Revisar"].astype(str)

        backup_local(df_tmp)

        try:
            ws.update([df_tmp.columns.values.tolist()] + df_tmp.fillna("").values.tolist())
            st.toast(f"✅ {nombre} marcado como visto.", icon="✅")
            st.cache_data.clear()
            st.rerun()
        except Exception as e:
            st.error(f"⚠️ Error al actualizar seguimiento: {e}")

    # =========================================================
    # FUNCIÓN: GUARDAR NUEVO (con backup)
    # =========================================================
    def guardar_nuevo(id_jugador, nombre, scout, fecha, motivo):
        nueva = [id_jugador, nombre, scout, fecha.strftime("%Y-%m-%d"), motivo, "Pendiente"]
        try:
            ws.append_row(nueva)
            df_local = pd.concat([df_agenda, pd.DataFrame([{
                "ID_Jugador": id_jugador,
                "Nombre": nombre,
                "Scout": scout,
                "Fecha_Revisar": fecha.strftime("%Y-%m-%d"),
                "Motivo": motivo,
                "Visto": "Pendiente"
            }])], ignore_index=True)
            backup_local(df_local)
            st.success(f"✅ Seguimiento agendado para {nombre} el {fecha.strftime('%d/%m/%Y')}")
            st.cache_data.clear()
            st.rerun()
        except Exception as e:
            st.error(f"⚠️ Error al guardar seguimiento: {e}")

    # =========================================================
    # BLOQUE PENDIENTES (máx 5 columnas por fila)
    # =========================================================
    with st.expander("🕐 Seguimientos pendientes", expanded=True):
        if pendientes.empty:
            st.info("No hay seguimientos pendientes.")
        else:
            jugadores_lista = list(pendientes.sort_values("Fecha_Revisar").iterrows())
            for i in range(0, len(jugadores_lista), 5):
                fila = jugadores_lista[i:i+5]
                cols = st.columns(len(fila))
                for col, (_, row) in zip(cols, fila):
                    nombre, scout, fecha, motivo = row["Nombre"], row["Scout"], row["Fecha_Revisar"], row["Motivo"]
                    if pd.isnull(fecha): continue
                    dias = (fecha - hoy).days
                    if dias < 0: label = "<span class='label alab-badge alab-badge-vencido'>Vencido</span>"
                    elif dias == 0: label = "<span class='label alab-badge alab-badge-hoy'>Hoy</span>"
                    elif dias <= 7: label = f"<span class='label alab-badge alab-badge-proximo'>En {dias} días</span>"
                    else: label = f"<span class='label alab-badge alab-badge-futuro'>En {dias} días</span>"

                    with col:
                        st.markdown(f"""
                        <div class='card alab-card alab-agenda-card'>
                            {label}
                            <h5>{nombre}</h5>
                            <p>Scout: {scout}</p>
                            <p>📅 {fecha.strftime('%d/%m/%Y')}</p>
                            <p><i>{motivo}</i></p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.button("👁 Marcar visto", key=f"mark_{nombre}_{i}", on_click=marcar_visto, args=(nombre,))

    # =========================================================
    # BLOQUE YA VISTOS (máx 5 columnas por fila)
    # =========================================================
    with st.expander("👁 Seguimientos ya vistos", expanded=False):
        if vistos.empty:
            st.info("No hay jugadores vistos aún.")
        else:
            jugadores_lista = list(vistos.sort_values("Fecha_Revisar").iterrows())
            for i in range(0, len(jugadores_lista), 5):
                fila = jugadores_lista[i:i+5]
                cols = st.columns(len(fila))
                for col, (_, row) in zip(cols, fila):
                    nombre, scout, fecha, motivo = row["Nombre"], row["Scout"], row["Fecha_Revisar"], row["Motivo"]
                    if pd.isnull(fecha): continue
                    with col:
                        st.markdown(f"""
                        <div class='card visto alab-card alab-card-seen alab-agenda-card'>
                            <span class='label alab-badge alab-badge-futuro'>Visto</span>
                            <h5>{nombre}</h5>
                            <p>Scout: {scout}</p>
                            <p>📅 {fecha.strftime('%d/%m/%Y')}</p>
                            <p><i>{motivo}</i></p>
                        </div>
                        """, unsafe_allow_html=True)

    # =========================================================
    # FORMULARIO NUEVO SEGUIMIENTO
    # =========================================================
    st.markdown("---")
    with st.expander("➕ Agendar nuevo seguimiento", expanded=False):
        jugadores_dict = {row["Nombre"]: row["ID_Jugador"] for _, row in df_players.iterrows()}
        col1, col2 = st.columns(2)
        with col1:
            jugador_sel = st.selectbox("Seleccioná un jugador", [""] + list(jugadores_dict.keys()))
            scout = st.text_input("Scout responsable", value=CURRENT_USER)
        with col2:
            fecha_rev = st.date_input("Fecha de revisión", value=datetime.now().date() + timedelta(days=7))
            motivo = st.text_area("Motivo del seguimiento", height=70)

        if jugador_sel and st.button("💾 Guardar seguimiento"):
            id_jugador = jugadores_dict[jugador_sel]
            guardar_nuevo(id_jugador, jugador_sel, scout, fecha_rev, motivo)

# =========================================================
# 🏠 PANEL GENERAL — ScoutingApp PRO (FINAL + CONSENSO)
# =========================================================
if st.session_state["menu"] == "Panel General":
    # =========================
    # DATA BASE
    # =========================
    df_players = df_players_user.copy()
    df_reports = df_reports_user.copy()
    df_short = df_short_user.copy()

    alcance_panel = "Vista total" if CURRENT_ROLE == "admin" else "Vista de scout"
    periodo_panel = f"Temporada {datetime.today().year}/{str(datetime.today().year + 1)[-2:]}"

    render_html_block(
        f"""
        <div class="alab-dashboard-hero">
            <div class="alab-dashboard-hero-kicker">Overview</div>
            <h1 class="alab-dashboard-hero-title">Panel General</h1>
            <div class="alab-dashboard-chip-row">
                <span class="alab-dashboard-chip"><strong>Rol</strong> {CURRENT_ROLE}</span>
                <span class="alab-dashboard-chip"><strong>Alcance</strong> {alcance_panel}</span>
                <span class="alab-dashboard-chip"><strong>Periodo</strong> {periodo_panel}</span>
            </div>
        </div>
        """
    )

    df_players["ID_Jugador"] = df_players["ID_Jugador"].astype(str)
    df_reports["ID_Jugador"] = df_reports["ID_Jugador"].astype(str)
    df_short["ID_Jugador"] = df_short["ID_Jugador"].astype(str)

    # =========================
    # FECHAS
    # =========================
    df_reports["Fecha_Informe_dt"] = pd.to_datetime(
        df_reports["Fecha_Informe"], errors="coerce", dayfirst=True
    )

    hoy = datetime.today()
    hace_30 = hoy - timedelta(days=30)

    # =========================
    # EDAD SEGURA
    # =========================
    def edad_segura(fecha):
        try:
            f = datetime.strptime(str(fecha), "%d/%m/%Y")
            return int((hoy - f).days / 365.25)
        except:
            return None

    df_players["Edad"] = df_players["Fecha_Nac"].apply(edad_segura)

    # =========================
    # MÉTRICAS LIMPIAS
    # =========================
    metricas = [
        "Controles","Perfiles","Pase_corto","Pase_largo","Pase_filtrado",
        "1v1_defensivo","Recuperacion","Intercepciones","Duelos_aereos",
        "Regate","Velocidad","Duelos_ofensivos",
        "Resiliencia","Liderazgo","Inteligencia_tactica",
        "Inteligencia_emocional","Posicionamiento","Vision_de_juego",
        "Movimientos_sin_pelota"
    ]

    for m in metricas:
        if m in df_reports.columns:
            df_reports[m] = (
                df_reports[m]
                .astype(str)
                .str.replace(",", ".", regex=False)
                .replace(["", "nan", "None", "-", "—"], 0)
                .astype(float)
            )
        else:
            df_reports[m] = 0.0

    # =========================
    # KPIs
    # =========================
    inicio_semestre = datetime(hoy.year, 1, 1) if hoy.month <= 6 else datetime(hoy.year, 7, 1)
    jugadores_sem = df_reports[df_reports["Fecha_Informe_dt"] >= inicio_semestre]["ID_Jugador"].nunique()
    informes_30 = df_reports[df_reports["Fecha_Informe_dt"] >= hace_30].shape[0]

    st.markdown(f"""
    <div class="kpi-container alab-kpi-grid">
        <div class="kpi-card alab-kpi"><div class="kpi-title alab-kpi-label">Jugadores evaluados</div><div class="kpi-value alab-kpi-value">{df_players["ID_Jugador"].nunique()}</div></div>
        <div class="kpi-card alab-kpi"><div class="kpi-title alab-kpi-label">Informes cargados</div><div class="kpi-value alab-kpi-value">{len(df_reports)}</div></div>
        <div class="kpi-card alab-kpi"><div class="kpi-title alab-kpi-label">Jugadores este semestre</div><div class="kpi-value alab-kpi-value">{jugadores_sem}</div></div>
        <div class="kpi-card alab-kpi"><div class="kpi-title alab-kpi-label">Informes últimos 30 días</div><div class="kpi-value alab-kpi-value">{informes_30}</div></div>
    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # ⭐ CONSENSO — LISTA CORTA
    # =====================================================
    section_header("Consenso en lista corta")

    df_short["Fecha_Agregado_dt"] = pd.to_datetime(
        df_short["Fecha_Agregado"], errors="coerce", dayfirst=True
    )

    col_c1, col_c2 = st.columns(2)

    with col_c1:
        filtro_anio = st.selectbox(
            "Año",
            ["Todos"] + sorted(df_short["Fecha_Agregado_dt"].dt.year.dropna().unique().tolist())
        )

    with col_c2:
        filtro_sem = st.selectbox(
            "Semestre",
            ["Todos", "1° semestre", "2° semestre"]
        )

    df_consenso = df_short.copy()

    if filtro_anio != "Todos":
        df_consenso = df_consenso[df_consenso["Fecha_Agregado_dt"].dt.year == filtro_anio]

    if filtro_sem != "Todos":
        if filtro_sem == "1° semestre":
            df_consenso = df_consenso[df_consenso["Fecha_Agregado_dt"].dt.month <= 6]
        else:
            df_consenso = df_consenso[df_consenso["Fecha_Agregado_dt"].dt.month >= 7]

    df_consenso = (
        df_consenso
        .groupby(["ID_Jugador","Nombre","Club","Posición"], as_index=False)
        .agg(Cantidad_Scouts=("Agregado_Por","nunique"))
    )

    df_consenso = df_consenso[df_consenso["Cantidad_Scouts"] > 1]

    consenso_total = len(df_consenso)
    consenso_max = int(df_consenso["Cantidad_Scouts"].max()) if not df_consenso.empty else 0

    render_html_block(
        f"""
        <div class="alab-mini-grid">
            <div class="alab-mini-stat">
                <span class="alab-mini-label">Jugadores con consenso</span>
                <span class="alab-mini-value">{consenso_total}</span>
                <span class="alab-mini-copy">Perfiles repetidos entre scouts en el periodo filtrado.</span>
            </div>
            <div class="alab-mini-stat">
                <span class="alab-mini-label">Pico de coincidencia</span>
                <span class="alab-mini-value">{consenso_max}</span>
                <span class="alab-mini-copy">Máxima cantidad de scouts coincidiendo sobre un mismo jugador.</span>
            </div>
        </div>
        """
    )

    if df_consenso.empty:
        st.info("No hay jugadores con consenso entre scouts.")
    else:
        st.dataframe(
            df_consenso.sort_values("Cantidad_Scouts", ascending=False),
            use_container_width=True,
            hide_index=True
        )

    # =====================================================
    # ⏰ SEGUIMIENTOS PRIORITARIOS VENCIDOS
    # =====================================================
    section_header("Seguimientos prioritarios vencidos")

    lineas_prioritarias = ["Exponencial", "Destacado", "En observación"]

    df_last = (
        df_reports
        .sort_values("Fecha_Informe_dt")
        .groupby("ID_Jugador")
        .last()
        .reset_index()
    )

    df_last = df_last[df_last["Línea"].isin(lineas_prioritarias)]
    df_last["Dias_sin_evaluar"] = (hoy - df_last["Fecha_Informe_dt"]).dt.days

    df_last = df_last[
        (df_last["Dias_sin_evaluar"] > 46) &
        (df_last["Dias_sin_evaluar"] <= 100)
    ]

    if CURRENT_ROLE != "admin":
        df_last = df_last[df_last["Scout"] == CURRENT_USER]

    df_alertas = df_last.merge(
        df_players[["ID_Jugador","Nombre","Club","Posición"]],
        on="ID_Jugador",
        how="left"
    )

    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
        filtro_pos = st.multiselect(
            "Posición",
            sorted(df_alertas["Posición"].dropna().unique().tolist())
        )

    with col_f2:
        filtro_linea = st.multiselect(
            "Línea",
            sorted(df_alertas["Línea"].dropna().unique().tolist())
        )

    with col_f3:
        filtro_dias = st.selectbox(
            "Días sin evaluar",
            ["Todos", "47–60", "61–80", "81–100"]
        )

    if filtro_pos:
        df_alertas = df_alertas[df_alertas["Posición"].isin(filtro_pos)]

    if filtro_linea:
        df_alertas = df_alertas[df_alertas["Línea"].isin(filtro_linea)]

    if filtro_dias != "Todos":
        rangos = {
            "47–60": (47, 60),
            "61–80": (61, 80),
            "81–100": (81, 100)
        }
        r = rangos[filtro_dias]
        df_alertas = df_alertas[
            (df_alertas["Dias_sin_evaluar"] >= r[0]) &
            (df_alertas["Dias_sin_evaluar"] <= r[1])
        ]

    alertas_total = len(df_alertas)
    alertas_media = int(round(df_alertas["Dias_sin_evaluar"].mean())) if not df_alertas.empty else 0
    lineas_activas = df_alertas["Línea"].nunique() if not df_alertas.empty else 0

    render_html_block(
        f"""
        <div class="alab-mini-grid">
            <div class="alab-mini-stat">
                <span class="alab-mini-label">Seguimientos vencidos</span>
                <span class="alab-mini-value">{alertas_total}</span>
                <span class="alab-mini-copy">Jugadores prioritarios que ya piden una nueva observación.</span>
            </div>
            <div class="alab-mini-stat">
                <span class="alab-mini-label">Demora promedio</span>
                <span class="alab-mini-value">{alertas_media} días</span>
                <span class="alab-mini-copy">Antigüedad media del último informe dentro del filtro actual.</span>
            </div>
            <div class="alab-mini-stat">
                <span class="alab-mini-label">Líneas activas</span>
                <span class="alab-mini-value">{lineas_activas}</span>
                <span class="alab-mini-copy">Cantidad de líneas de seguimiento afectadas.</span>
            </div>
        </div>
        """
    )

    if df_alertas.empty:
        st.success("No hay seguimientos prioritarios vencidos.")
    else:
        st.dataframe(
            df_alertas[["Nombre","Club","Posición","Línea","Fecha_Informe","Dias_sin_evaluar"]],
            use_container_width=True,
            hide_index=True
        )

    # =========================
    # CONTRATOS POR VENCER
    # =========================
    if "Fecha_Fin_Contrato" in df_players.columns:

        df_c = df_players.copy()
        df_c["Fecha_Fin_dt"] = pd.to_datetime(df_c["Fecha_Fin_Contrato"], errors="coerce", dayfirst=True)
        df_c = df_c.dropna(subset=["Fecha_Fin_dt"])

        lim6 = hoy + timedelta(days=180)
        lim12 = hoy + timedelta(days=365)

        df6 = df_c[df_c["Fecha_Fin_dt"] <= lim6]
        df12 = df_c[(df_c["Fecha_Fin_dt"] > lim6) & (df_c["Fecha_Fin_dt"] <= lim12)]
        proximidad_min = (df6["Fecha_Fin_dt"].min() - hoy).days if not df6.empty else None

        section_header(
            "Contratos por vencer",
        )

        render_html_block(
            f"""
            <div class="alab-mini-grid">
                <div class="alab-mini-stat">
                    <span class="alab-mini-label">Ventana inmediata</span>
                    <span class="alab-mini-value">{len(df6)}</span>
                    <span class="alab-mini-copy">Jugadores con finalización contractual dentro de los próximos 6 meses.</span>
                </div>
                <div class="alab-mini-stat">
                    <span class="alab-mini-label">Ventana ampliada</span>
                    <span class="alab-mini-value">{len(df12)}</span>
                    <span class="alab-mini-copy">Casos que vencen entre 6 y 12 meses y merecen seguimiento comercial.</span>
                </div>
                <div class="alab-mini-stat">
                    <span class="alab-mini-label">Próximo vencimiento</span>
                    <span class="alab-mini-value">{"-" if proximidad_min is None else f'{proximidad_min} días'}</span>
                    <span class="alab-mini-copy">Referencia del contrato más cercano detectado en la base actual.</span>
                </div>
            </div>
            """
        )

        c1, c2 = st.columns(2)
        with c1: st.metric("🔴 ≤ 6 meses", len(df6))
        with c2: st.metric("🟡 ≤ 12 meses", len(df12))

        if not df6.empty or not df12.empty:
            st.dataframe(
                pd.concat([df6, df12]).sort_values("Fecha_Fin_dt")[
                    ["Nombre","Club","Posición","Fecha_Fin_Contrato"]
                ],
                use_container_width=True,
                hide_index=True
            )

    # =========================
    # TOPS POR POSICIÓN
    # =========================
    df_scores = (
        df_reports
        .groupby("ID_Jugador")[metricas]
        .mean()
        .mean(axis=1)
        .reset_index(name="Score")
        .merge(
            df_players[["ID_Jugador","Nombre","Posición"]],
            on="ID_Jugador",
            how="left"
        )
        .sort_values("Score", ascending=False)
    )

    def render_top(df, titulo):
        st.markdown(f"<div class='panel-title alab-panel-title'>{titulo}</div>", unsafe_allow_html=True)
        if df.empty:
            st.info("Sin datos")
            return
        for i, r in enumerate(df.head(5).itertuples(), 1):
            st.markdown(f"""
            <div class='rank-card alab-rank-card'>
                <div class='rank-left alab-rank-left'>
                    <div class='rank-num alab-rank-num'>#{i}</div>
                    <div class='rank-name alab-rank-name'>{r.Nombre}</div>
                </div>
                <div class='rank-score alab-rank-score'>{round(r.Score,2)}</div>
            </div>
            """, unsafe_allow_html=True)

    posiciones = [
        ("Arquero","🧤 Arqueros"),
        ("Lateral derecho","➡️ Laterales derechos"),
        ("Defensa central derecho","🛡️ Centrales derechos"),
        ("Defensa central izquierdo","🛡️ Centrales izquierdos"),
        ("Lateral izquierdo","⬅️ Laterales izquierdos"),
        ("Mediocampista defensivo","🔒 Volantes defensivos"),
        ("Mediocampista mixto","🔄 Volantes mixtos"),
        ("Mediocampista ofensivo","🎯 Volantes ofensivos"),
        ("Extremo derecho","⚡ Extremos derechos"),
        ("Extremo izquierdo","⚡ Extremos izquierdos"),
        ("Delantero centro","🎯 Delanteros centro"),
    ]

    cobertura_posiciones = df_scores["Posición"].nunique() if not df_scores.empty else 0
    mejor_score = round(df_scores["Score"].max(), 2) if not df_scores.empty else 0

    section_header("Top 5 por posición")
    render_html_block(
        f"""
        <div class="alab-mini-grid">
            <div class="alab-mini-stat">
                <span class="alab-mini-label">Posiciones con ranking</span>
                <span class="alab-mini-value">{cobertura_posiciones}</span>
                <span class="alab-mini-copy">Roles con volumen suficiente de informes para ordenar perfiles.</span>
            </div>
            <div class="alab-mini-stat">
                <span class="alab-mini-label">Mejor score actual</span>
                <span class="alab-mini-value">{mejor_score}</span>
                <span class="alab-mini-copy">Puntaje promedio más alto del universo evaluado.</span>
            </div>
        </div>
        """
    )
    cols = st.columns(4)
    for i, (pos, titulo) in enumerate(posiciones):
        with cols[i % 4]:
            render_top(df_scores[df_scores["Posición"] == pos], titulo)

    # =========================
    # COMPARADOR DE JUGADORES
    # =========================
    section_header("Comparador de jugadores")

    col_f1, col_f2, col_f3 = st.columns(3)

    opciones_pos = sorted(df_players["Posición"].dropna().astype(str).unique().tolist())
    opciones_pie = sorted(df_players["Pie_Hábil"].dropna().astype(str).unique().tolist())

    with col_f1:
        filtro_pos = st.selectbox("Posición", ["Todas"] + opciones_pos)
    with col_f2:
        filtro_pie = st.selectbox("Pie hábil", ["Todos"] + opciones_pie)
    with col_f3:
        edad_min, edad_max = st.slider("Edad", 15, 45, (18, 35))

    df_base = df_players.copy()
    if filtro_pos != "Todas":
        df_base = df_base[df_base["Posición"] == filtro_pos]
    if filtro_pie != "Todos":
        df_base = df_base[df_base["Pie_Hábil"] == filtro_pie]

    df_base = df_base[(df_base["Edad"] >= edad_min) & (df_base["Edad"] <= edad_max)]

    render_html_block(
        f"""
        <div class="alab-mini-grid">
            <div class="alab-mini-stat">
                <span class="alab-mini-label">Base comparable</span>
                <span class="alab-mini-value">{df_base['ID_Jugador'].nunique()}</span>
                <span class="alab-mini-copy">Jugadores disponibles según posición, pie hábil y franja etaria.</span>
            </div>
            <div class="alab-mini-stat">
                <span class="alab-mini-label">Selección recomendada</span>
                <span class="alab-mini-value">2 a 6</span>
                <span class="alab-mini-copy">Rango óptimo para comparar métricas sin perder legibilidad.</span>
            </div>
        </div>
        """
    )

    opciones_cmp = {f"{r.Nombre} ({r.Club})": r.ID_Jugador for r in df_base.itertuples()}

    seleccionados = st.multiselect(
        "Seleccioná de 2 a 6 jugadores",
        list(opciones_cmp.keys()),
        max_selections=6
    )

    if 2 <= len(seleccionados) <= 6:
        ids = [opciones_cmp[n] for n in seleccionados]

        df_cmp = (
            df_reports[df_reports["ID_Jugador"].isin(ids)]
            .groupby("ID_Jugador")[metricas]
            .mean()
            .reset_index()
            .merge(
                df_players[["ID_Jugador","Nombre","Posición","Edad","Club","Pie_Hábil"]],
                on="ID_Jugador",
                how="left"
            )
        )

        df_cmp["Score"] = df_cmp[metricas].mean(axis=1).round(2)
        df_cmp = df_cmp.sort_values("Score", ascending=False)

        mejor_perfil = df_cmp.iloc[0]["Nombre"] if not df_cmp.empty else "-"
        score_medio_cmp = round(df_cmp["Score"].mean(), 2) if not df_cmp.empty else 0
        clubes_cmp = df_cmp["Club"].nunique() if not df_cmp.empty else 0
        edad_media_cmp = int(round(df_cmp["Edad"].mean())) if df_cmp["Edad"].notna().any() else 0

        render_html_block(
            f"""
            <div class="alab-mini-grid">
                <div class="alab-mini-stat">
                    <span class="alab-mini-label">Perfiles comparados</span>
                    <span class="alab-mini-value">{len(df_cmp)}</span>
                    <span class="alab-mini-copy">Selección activa dentro del universo filtrado.</span>
                </div>
                <div class="alab-mini-stat">
                    <span class="alab-mini-label">Score medio</span>
                    <span class="alab-mini-value">{score_medio_cmp}</span>
                    <span class="alab-mini-copy">Promedio general de la muestra comparada.</span>
                </div>
                <div class="alab-mini-stat">
                    <span class="alab-mini-label">Perfil líder</span>
                    <span class="alab-mini-value">{mejor_perfil}</span>
                    <span class="alab-mini-copy">Jugador con mayor score sintético entre los seleccionados.</span>
                </div>
                <div class="alab-mini-stat">
                    <span class="alab-mini-label">Contexto</span>
                    <span class="alab-mini-value">{clubes_cmp} clubes · {edad_media_cmp} años</span>
                    <span class="alab-mini-copy">Diversidad de origen y edad promedio del grupo analizado.</span>
                </div>
            </div>
            """
        )

        fig_cmp = px.bar(
            df_cmp,
            x="Nombre",
            y="Score",
            color="Posición",
            text="Score",
            title="Comparación sintética de perfiles",
        )
        fig_cmp.update_traces(textposition="outside")
        fig_cmp.update_layout(showlegend=False, yaxis_title="Score", xaxis_title="")
        apply_glass_plotly(fig_cmp)
        st.plotly_chart(fig_cmp, use_container_width=True)

        st.dataframe(
            df_cmp[["Nombre","Club","Posición","Pie_Hábil","Edad","Score"] + metricas],
            use_container_width=True,
            hide_index=True
        )
    elif len(seleccionados) == 1:
        st.info("Seleccioná al menos 2 jugadores para habilitar la comparación.")
    else:
        st.info("Elegí entre 2 y 6 jugadores para ver el comparador completo.")

# =========================================================
# 🧭 PANEL SCOUTS — BLOQUE ESTABLE Y COHERENTE
# =========================================================
if st.session_state["menu"] == "Panel Scouts":

    # -----------------------------------------------------
    # 🔐 CONTROL DE ACCESO
    # -----------------------------------------------------
    if CURRENT_ROLE not in ["admin", "scout"]:
        st.warning("⛔ No tenés permisos para acceder a este panel.")
        st.stop()

    section_header(
        "Panel de control de scouts",
        eyebrow="Rendimiento",
        caption="Seguimiento de actividad, carga de informes y distribución de decisiones por período.",
        centered=True,
    )

    # -----------------------------------------------------
    # 📦 DATA BASE (YA FILTRADA POR USUARIO)
    # -----------------------------------------------------
    df_reports = df_reports_user.copy()
    df_players = df_players_user.copy()

    if df_reports.empty:
        st.info("No hay informes disponibles.")
        st.stop()

    # -----------------------------------------------------
    # 🧹 NORMALIZACIÓN BÁSICA
    # -----------------------------------------------------
    df_reports["Scout"] = df_reports["Scout"].astype(str).str.strip()
    df_reports["ID_Jugador"] = df_reports["ID_Jugador"].astype(str)
    df_players["ID_Jugador"] = df_players["ID_Jugador"].astype(str)

    # -----------------------------------------------------
    # 🕒 FECHAS
    # -----------------------------------------------------
    df_reports["Fecha_dt"] = pd.to_datetime(
        df_reports["Fecha_Informe"],
        errors="coerce",
        dayfirst=True
    )

    df_reports["Año"] = df_reports["Fecha_Informe"].astype(str).str[-4:]
    df_reports["Mes_num"] = df_reports["Fecha_dt"].dt.month
    df_reports["Semestre"] = df_reports["Mes_num"].apply(
        lambda m: "1º" if m and m <= 6 else "2º"
    )
    df_reports["Mes"] = df_reports["Fecha_dt"].dt.strftime("%Y-%m")

    # -----------------------------------------------------
    # 🔗 MERGE CON JUGADORES
    # -----------------------------------------------------
    df = df_reports.merge(
        df_players[["ID_Jugador", "Posición", "Liga"]],
        on="ID_Jugador",
        how="left"
    )
    df["Posición"] = (
        df["Posición"]
        .fillna("Sin posición")
        .astype(str)
        .str.strip()
        .replace({"": "Sin posición", "nan": "Sin posición", "None": "Sin posición", "undefined": "Sin posición"})
    )

    # -----------------------------------------------------
    # 🔎 FILTROS
    # -----------------------------------------------------
    section_header(
        "Filtros del período",
        eyebrow="Segmentación",
        caption="Definí año, semestre y scout para evaluar rendimiento y volumen con más precisión.",
    )

    f1, f2, f3 = st.columns(3)

    with f1:
        filtro_anio = st.multiselect(
            "Año",
            sorted(df["Año"].dropna().unique(), reverse=True)
        )

    with f2:
        filtro_sem = st.multiselect("Semestre", ["1º", "2º"])

    with f3:
        if CURRENT_ROLE == "admin":
            filtro_scout = st.multiselect(
                "Scout",
                sorted(df["Scout"].dropna().unique())
            )
        else:
            filtro_scout = []

    # -----------------------------------------------------
    # 🎯 DATAFRAME FINAL
    # -----------------------------------------------------
    df_f = df.copy()

    if filtro_anio:
        df_f = df_f[df_f["Año"].isin(filtro_anio)]
    if filtro_sem:
        df_f = df_f[df_f["Semestre"].isin(filtro_sem)]
    if filtro_scout:
        df_f = df_f[df_f["Scout"].isin(filtro_scout)]

    # -----------------------------------------------------
    # 📊 KPIs
    # -----------------------------------------------------
    section_header(
        "Actividad del período",
        eyebrow="KPIs",
        caption="Resumen ejecutivo del volumen operativo generado por el conjunto filtrado.",
    )

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("📝 Informes", len(df_f))
    k2.metric("👤 Scouts activos", df_f["Scout"].nunique())
    k3.metric("🎯 Jugadores", df_f["ID_Jugador"].nunique())
    k4.metric("🏟️ Ligas", df_f["Liga"].nunique())

    # -----------------------------------------------------
    # 🏆 RANKING
    # -----------------------------------------------------
    pesos = {
        "Exponencial": 3,
        "Destacado": 2,
        "Acorde": 1
    }

    df_rank = df_f.copy()
    df_rank["Peso"] = df_rank["Línea"].map(pesos).fillna(0.5)

    ranking = (
        df_rank.groupby("Scout")
        .agg(
            Informes=("ID_Jugador", "count"),
            Jugadores=("ID_Jugador", "nunique"),
            Calidad=("Peso", "sum")
        )
        .reset_index()
    )

    ranking["Score"] = (ranking["Calidad"] / ranking["Informes"]).round(2)
    ranking = ranking.sort_values(["Score", "Informes"], ascending=False)

    section_header(
        "Ranking de scouts",
        eyebrow="Comparativa",
        caption="El score pondera cantidad de informes y calidad relativa según la línea asignada en cada observación.",
    )
    st.dataframe(ranking, use_container_width=True)

    # -----------------------------------------------------
    # 📈 GRÁFICOS
    # -----------------------------------------------------
    section_header(
        "Visualizaciones del período",
        eyebrow="Tendencias",
        caption="Lectura temporal y distributiva del trabajo de scouting, presentada en pares de gráficos para contraste rápido.",
    )
    col1, col2 = st.columns(2)

    with col1:
        section_header("Evolución mensual total")

        total_mes = (
            df_f.groupby("Mes")
            .size()
            .reset_index(name="Informes")
            .sort_values("Mes")
        )

        fig = px.line(total_mes, x="Mes", y="Informes", markers=True)
        fig = apply_glass_plotly(fig)
        st.plotly_chart(fig, use_container_width=True)

        section_header("Observaciones por posición")

        pos_df = df_f["Posición"].value_counts().reset_index()
        pos_df.columns = ["Posición", "Cantidad"]

        fig = px.pie(pos_df, names="Posición", values="Cantidad", hole=0.45)
        fig.update_traces(
            textinfo="percent",
            textposition="inside",
            hovertemplate="%{label}<br>Informes: %{value}<br>Participación: %{percent}<extra></extra>",
        )
        fig = apply_glass_plotly(fig)
        fig.update_layout(legend_title_text="")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_header("Evolución mensual por scout")

        scout_mes = (
            df_f.groupby(["Mes", "Scout"])
            .size()
            .reset_index(name="Informes")
            .sort_values("Mes")
        )

        fig = px.line(
            scout_mes,
            x="Mes",
            y="Informes",
            color="Scout",
            markers=True
        )
        fig = apply_glass_plotly(fig)
        st.plotly_chart(fig, use_container_width=True)

        section_header("Informes por scout")

        bar_df = (
            df_f.groupby("Scout")
            .size()
            .reset_index(name="Informes")
        )

        fig = px.bar(bar_df, x="Scout", y="Informes", text="Informes")
        fig = apply_glass_plotly(fig)
        st.plotly_chart(fig, use_container_width=True)

    # -----------------------------------------------------
    # 🎯 DISTRIBUCIÓN DE DECISIONES
    # -----------------------------------------------------
    section_header(
        "Distribución de decisiones por scout",
        eyebrow="Matriz",
        caption="Vista compacta para comparar cómo se reparte cada línea de decisión entre los scouts activos.",
    )

    tabla_lineas = (
        df_f.groupby(["Scout", "Línea"])
        .size()
        .reset_index(name="Cantidad")
        .pivot(index="Scout", columns="Línea", values="Cantidad")
        .fillna(0)
        .astype(int)
    )

    st.dataframe(tabla_lineas, use_container_width=True)
# =========================================================
# CIERRE PROFESIONAL (footer)
# =========================================================
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;color:#5a9a7c;margin-top:30px;">
    <h4>ScoutingApp Profesional v2.3</h4>
    <p>Usuario activo: <strong>{CURRENT_USER}</strong> ({CURRENT_ROLE})</p>
    <p style="color:gray;font-size:13px;">
        Área de Scouting Profesional
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align:center;color:gray;font-size:12px;'>© 2025 · EOC · ScoutingApp Profesional</p>",
    unsafe_allow_html=True
)

