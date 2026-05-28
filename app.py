"""
app.py
Simulador de Costo de Contrato Colectivo — Pilotos Chile
Streamlit app principal — v2 con variables LAN Cargo precargadas
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import tempfile
import json
from extractor import extraer_variables_pdf, VariableContrato, TipoVariable, Recurrencia
from calculadora import Dotacion, calcular_costos
from lan_cargo_variables import cargar_variables_lan_cargo

# ─────────────────────────────────────────────
# Configuración de página
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Simulador Contrato Colectivo — Pilotos",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .section-title {
        font-size: 1.1rem; font-weight: 600; color: #1a237e;
        border-bottom: 2px solid #1a237e; padding-bottom: 4px; margin-bottom: 12px;
    }
    .info-pill {
        background: #e8eaf6; border-radius: 20px; padding: 2px 10px;
        font-size: 0.8rem; color: #1a237e; display: inline-block; margin: 2px;
    }
    div[data-testid="stExpander"] { border: 1px solid #e0e0e0; border-radius: 6px; }
    .stDataFrame { font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
def fmt_clp(valor):
    if valor is None: return "—"
    return f"${valor:,.0f}".replace(",", ".")

def fmt_pct(valor):
    if valor is None: return "—"
    return f"{valor:+.1f}%"

def inicializar_session():
    defaults = {
        "variables": [],
        "texto_pdf": "",
        "dotacion_cap": {},
        "dotacion_fo": {},
        "incremento_real": 1.0,
        "duracion_meses": 36,
        "contrato_nombre": "",
        "n_ie": 0,
        "n_instructores": 0,
        "n_asesores": 0,
        "hbt_horas": {"cap_a": 75.0, "cap_b": 75.0, "cap_c": 75.0, "fo_a": 75.0, "fo_b": 75.0, "fo_c": 75.0, "fo_subc": 70.0},
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def obtener_tramos_sueldo_cap():
    return ["Nivel A (≥20 años)", "Nivel B (13-19 años)", "Nivel C (<13 años)"]

def obtener_tramos_sueldo_fo():
    return ["Nivel A (≥8 años)", "Nivel B (4-7 años)", "Nivel C (<4 años)", "Sub-C (<4 años)"]


# ─────────────────────────────────────────────
# HBT recalculation helper
# ─────────────────────────────────────────────
def _recalcular_hbt(hbt: dict):
    """Recalcula el Componente Variable HBT en las variables ya cargadas."""
    from lan_cargo_variables import calcular_componente_variable, TABLA_HBT_CAPITAN, TABLA_HBT_FO, hbt_a_valor
    cv = calcular_componente_variable(
        hbt["cap_a"], hbt["cap_b"], hbt["cap_c"],
        hbt["fo_a"],  hbt["fo_b"],  hbt["fo_c"], hbt["fo_subc"],
    )
    for v in st.session_state.variables:
        if "HBT" in v.nombre and "Capitán" in v.nombre:
            v.valor_libro  = cv["CAP Nivel A"]
            v.valor_actual = cv["CAP Nivel A"]
            v.valor_nuevo  = cv["CAP Nivel A"]
            v.tramos_antiguedad = {
                "Nivel A": cv["CAP Nivel A"],
                "Nivel B": cv["CAP Nivel B"],
                "Nivel C": cv["CAP Nivel C"],
            }
            v.nota_operacional = (
                f"Calculado para {hbt['cap_a']:.0f}h CAP-A / "
                f"{hbt['cap_b']:.0f}h CAP-B / {hbt['cap_c']:.0f}h CAP-C. "
                "Ajusta las horas en el panel lateral."
            )
        elif "HBT" in v.nombre and "Primer Oficial" in v.nombre:
            v.valor_libro  = cv["FO Nivel A"]
            v.valor_actual = cv["FO Nivel A"]
            v.valor_nuevo  = cv["FO Nivel A"]
            v.tramos_antiguedad = {
                "Nivel A": cv["FO Nivel A"],
                "Nivel B": cv["FO Nivel B"],
                "Nivel C": cv["FO Nivel C"],
                "Sub-C":   cv["FO Sub-C"],
            }
            v.nota_operacional = (
                f"Calculado para {hbt['fo_a']:.0f}h FO-A / "
                f"{hbt['fo_b']:.0f}h FO-B / {hbt['fo_c']:.0f}h FO-C / "
                f"{hbt['fo_subc']:.0f}h Sub-C."
            )



# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
def render_sidebar():
    st.sidebar.title("✈️ Configuración")
    st.sidebar.markdown("---")

    st.sidebar.markdown("**Duración del contrato**")
    duracion = st.sidebar.radio(
        "Años de vigencia", options=[12, 24, 36],
        format_func=lambda x: f"{x//12} año{'s' if x>12 else ''}",
        index=2, key="duracion_radio"
    )
    st.session_state.duracion_meses = duracion
    st.sidebar.caption("📅 LAN Cargo: 01-sep-2023 al 31-ago-2026 (36 meses)")

    st.sidebar.markdown("---")
    st.sidebar.markdown("**% Incremento real anual**")
    st.sidebar.caption("Solo el % real (descartando IPC). Aplica sobre sueldo base y horas.")
    incremento = st.sidebar.number_input(
        "% anual (contrato define 1%/año)", min_value=0.0, max_value=20.0,
        value=float(st.session_state.incremento_real), step=0.1, format="%.1f",
        key="incremento_input"
    )
    st.session_state.incremento_real = incremento

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Dotación — Capitanes (por nivel)**")
    tramos_cap = obtener_tramos_sueldo_cap()
    cap_dict = {}
    for t in tramos_cap:
        cap_dict[t] = st.sidebar.number_input(
            t, min_value=0, value=st.session_state.dotacion_cap.get(t, 5),
            step=1, key=f"cap_{t}"
        )
    st.session_state.dotacion_cap = cap_dict

    st.sidebar.markdown("**Dotación — Primeros Oficiales (por nivel)**")
    tramos_fo = obtener_tramos_sueldo_fo()
    fo_dict = {}
    for t in tramos_fo:
        fo_dict[t] = st.sidebar.number_input(
            t, min_value=0, value=st.session_state.dotacion_fo.get(t, 5),
            step=1, key=f"fo_{t}"
        )
    st.session_state.dotacion_fo = fo_dict

    total_cap = sum(cap_dict.values())
    total_fo = sum(fo_dict.values())
    st.sidebar.markdown(f"**Total: {total_cap+total_fo} pilotos** (CAP: {total_cap} | FO: {total_fo})")

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Roles especiales (dotación)**")
    st.session_state.n_ie = st.sidebar.number_input("N° Instructores Evaluadores (IE)", min_value=0, value=st.session_state.n_ie, step=1)
    st.session_state.n_instructores = st.sidebar.number_input("N° Instructores de Vuelo", min_value=0, value=st.session_state.n_instructores, step=1)
    st.session_state.n_asesores = st.sidebar.number_input("N° Asesores", min_value=0, value=st.session_state.n_asesores, step=1)

    st.sidebar.markdown("---")
    st.sidebar.markdown("**⏱ Horas promedio mensuales HBT**")
    st.sidebar.caption("Determina el Componente Variable. Ajusta según productividad real.")

    hbt_defaults = st.session_state.get("hbt_horas", {
        "cap_a": 75.0, "cap_b": 75.0, "cap_c": 75.0,
        "fo_a": 75.0, "fo_b": 75.0, "fo_c": 75.0, "fo_subc": 70.0,
    })
    hbt = {}
    st.sidebar.markdown("*Capitanes*")
    hbt["cap_a"]  = st.sidebar.number_input("CAP Nivel A", min_value=0.0, max_value=120.0, value=hbt_defaults["cap_a"],  step=0.5, format="%.1f", key="hbt_cap_a")
    hbt["cap_b"]  = st.sidebar.number_input("CAP Nivel B", min_value=0.0, max_value=120.0, value=hbt_defaults["cap_b"],  step=0.5, format="%.1f", key="hbt_cap_b")
    hbt["cap_c"]  = st.sidebar.number_input("CAP Nivel C", min_value=0.0, max_value=120.0, value=hbt_defaults["cap_c"],  step=0.5, format="%.1f", key="hbt_cap_c")
    st.sidebar.markdown("*Primeros Oficiales*")
    hbt["fo_a"]   = st.sidebar.number_input("FO Nivel A",  min_value=0.0, max_value=120.0, value=hbt_defaults["fo_a"],   step=0.5, format="%.1f", key="hbt_fo_a")
    hbt["fo_b"]   = st.sidebar.number_input("FO Nivel B",  min_value=0.0, max_value=120.0, value=hbt_defaults["fo_b"],   step=0.5, format="%.1f", key="hbt_fo_b")
    hbt["fo_c"]   = st.sidebar.number_input("FO Nivel C",  min_value=0.0, max_value=120.0, value=hbt_defaults["fo_c"],   step=0.5, format="%.1f", key="hbt_fo_c")
    hbt["fo_subc"]= st.sidebar.number_input("FO Sub-C",    min_value=0.0, max_value=120.0, value=hbt_defaults["fo_subc"],step=0.5, format="%.1f", key="hbt_fo_subc")

    if hbt != st.session_state.get("hbt_horas"):
        st.session_state.hbt_horas = hbt
        if st.session_state.variables:
            _recalcular_hbt(hbt)


# ─────────────────────────────────────────────
# PASO 1 — Carga
# ─────────────────────────────────────────────
def render_carga():
    st.markdown('<div class="section-title">📄 Paso 1 — Cargar Contrato</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        uploaded = st.file_uploader("Sube el PDF del contrato colectivo", type=["pdf"])
    with col2:
        if st.button("📋 Cargar LAN Cargo 2023-2026", use_container_width=True):
            st.session_state.variables = cargar_variables_lan_cargo()
            st.session_state.contrato_nombre = "LAN Cargo S.A. — Sindicato Uno de Pilotos (2023-2026)"
            st.session_state.incremento_real = 1.0
            st.session_state.dotacion_cap = {
                "Nivel A (≥20 años)": 15, "Nivel B (13-19 años)": 20, "Nivel C (<13 años)": 15
            }
            st.session_state.dotacion_fo = {
                "Nivel A (≥8 años)": 10, "Nivel B (4-7 años)": 20, "Nivel C (<4 años)": 15, "Sub-C (<4 años)": 17
            }
            st.session_state.n_ie = 5
            st.session_state.n_instructores = 8
            st.rerun()
    with col3:
        if st.session_state.variables:
            if st.button("🔄 Limpiar", use_container_width=True):
                st.session_state.variables = []
                st.session_state.contrato_nombre = ""
                st.rerun()

    if uploaded and not st.session_state.variables:
        with st.spinner("Extrayendo variables del PDF..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded.read())
                tmp_path = tmp.name
            try:
                # Detectar si es LAN Cargo por nombre de archivo
                if "lan_cargo" in uploaded.name.lower() or "lan cargo" in uploaded.name.lower() or "LAN" in uploaded.name:
                    variables = cargar_variables_lan_cargo()
                    st.session_state.contrato_nombre = "LAN Cargo S.A. — Sindicato Uno de Pilotos (2023-2026)"
                else:
                    variables, texto = extraer_variables_pdf(tmp_path)
                    st.session_state.texto_pdf = texto
                    st.session_state.contrato_nombre = uploaded.name
                st.session_state.variables = variables
                st.success(f"✅ {len(variables)} variables cargadas")
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                os.unlink(tmp_path)

    if st.session_state.variables:
        st.success(f"✅ **{st.session_state.contrato_nombre}** — {len(st.session_state.variables)} variables cargadas")


# ─────────────────────────────────────────────
# PASO 2 — Variables
# ─────────────────────────────────────────────
def render_tabla_variables():
    if not st.session_state.variables:
        st.info("Carga un contrato para continuar.")
        return

    st.markdown('<div class="section-title">📋 Paso 2 — Variables del Contrato</div>', unsafe_allow_html=True)
    st.caption("**Valor Libro**: extraído del PDF. **Valor Actual**: el que rige hoy (editable). **Nuevo Valor**: propuesta de negociación (editable).")

    # Leyenda de tipos
    col_leg = st.columns(5)
    tipos_labels = [("💰 Remuneracional", TipoVariable.REMUNERACIONAL),
                    ("🎁 One-Time", TipoVariable.BONO_ONE_TIME),
                    ("📈 Incremento", TipoVariable.INCREMENTO),
                    ("⚙️ Operacional", TipoVariable.OPERACIONAL),
                    ("📜 Indemnización", TipoVariable.INDEMNIZACION)]
    for col, (lbl, tipo) in zip(col_leg, tipos_labels):
        n = sum(1 for v in st.session_state.variables if v.tipo == tipo)
        col.metric(lbl, n)

    st.markdown("---")

    # Botón agregar variable
    with st.expander("➕ Agregar variable manualmente (beneficio nuevo)"):
        c1, c2, c3, c4 = st.columns(4)
        nn = c1.text_input("Nombre", key="nn")
        nt = c2.selectbox("Tipo", ["Remuneracional", "Bono One-Time", "Operacional"], key="nt")
        nr = c3.selectbox("Recurrencia", ["Mensual", "Anual", "One-Time", "Por Evento"], key="nr")
        nv = c4.number_input("Nuevo Valor (CLP)", min_value=0, value=0, step=1000, key="nv")
        nc, nf = st.columns(2)
        ncap = nc.checkbox("Aplica CAP", value=True, key="ncap")
        nfo = nf.checkbox("Aplica FO", value=True, key="nfo")
        if st.button("Agregar"):
            if nn:
                tipo_map = {"Remuneracional": TipoVariable.REMUNERACIONAL,
                           "Bono One-Time": TipoVariable.BONO_ONE_TIME,
                           "Operacional": TipoVariable.OPERACIONAL}
                rec_map = {"Mensual": Recurrencia.MENSUAL, "Anual": Recurrencia.ANUAL,
                          "One-Time": Recurrencia.ONE_TIME, "Por Evento": Recurrencia.EVENTO}
                st.session_state.variables.append(VariableContrato(
                    nombre=nn, tipo=tipo_map[nt], recurrencia=rec_map[nr],
                    valor_libro=0.0, valor_actual=0.0, valor_nuevo=float(nv),
                    aplica_capitanes=ncap, aplica_primer_oficial=nfo, es_nuevo_beneficio=True,
                ))
                st.rerun()

    # Agrupar por tipo
    grupos = [
        ("💰 Remuneracionales", TipoVariable.REMUNERACIONAL),
        ("🎁 Bonos One-Time", TipoVariable.BONO_ONE_TIME),
        ("📈 Incremento Real", TipoVariable.INCREMENTO),
        ("⚙️ Operacionales", TipoVariable.OPERACIONAL),
        ("📜 Indemnizaciones", TipoVariable.INDEMNIZACION),
    ]

    for titulo, tipo in grupos:
        vars_grupo = [v for v in st.session_state.variables if v.tipo == tipo]
        if not vars_grupo:
            continue
        expanded = tipo not in [TipoVariable.INDEMNIZACION, TipoVariable.BONO_ONE_TIME]
        with st.expander(f"{titulo} ({len(vars_grupo)})", expanded=expanded):
            # Cabecera de columnas
            h = st.columns([3.5, 1.2, 1.5, 1.5, 1.5, 1.5])
            for col, label in zip(h, ["Variable / Cláusula", "Recurrencia", "Valor Libro", "Valor Actual ✏️", "Nuevo Valor ✏️", "Cargo / Config"]):
                col.markdown(f"**{label}**")
            st.markdown("---")

            for v in vars_grupo:
                idx = st.session_state.variables.index(v)
                _render_fila(idx, v)


def _render_fila(idx: int, var: VariableContrato):
    cols = st.columns([3.5, 1.2, 1.5, 1.5, 1.5, 1.5])

    with cols[0]:
        nombre = st.text_input("", value=var.nombre, key=f"n_{idx}", label_visibility="collapsed")
        st.session_state.variables[idx].nombre = nombre
        if var.clausula_referencia:
            st.caption(f"📎 {var.clausula_referencia}")
        if var.es_nuevo_beneficio:
            st.caption("🆕 Beneficio nuevo (costo actual = 0)")

    with cols[1]:
        st.markdown(f"<small>{var.recurrencia.value}</small>", unsafe_allow_html=True)
        if var.aplica_incremento_real:
            st.caption("📈 Inc. real aplica")

    with cols[2]:
        if var.tipo == TipoVariable.INDEMNIZACION:
            st.caption("No se costea")
        elif var.unidad == "%":
            st.metric("", f"{var.valor_libro:.1f}%" if var.valor_libro else "—", label_visibility="collapsed")
        elif var.unidad == "USD":
            st.metric("", f"USD {var.valor_libro:,.0f}" if var.valor_libro else "—", label_visibility="collapsed")
        else:
            st.metric("", fmt_clp(var.valor_libro) if var.valor_libro else "—", label_visibility="collapsed")

    with cols[3]:
        if var.tipo == TipoVariable.INDEMNIZACION:
            st.caption("—")
        elif var.unidad == "%":
            va = st.number_input("", min_value=0.0, max_value=100.0,
                                  value=float(var.valor_actual or 0), step=0.1, format="%.2f",
                                  key=f"a_{idx}", label_visibility="collapsed")
            st.session_state.variables[idx].valor_actual = va
            st.caption("% actual")
        elif var.valor_libro is None and var.valor_actual is None:
            va = st.number_input("", min_value=0, value=0, step=1000,
                                  key=f"a_{idx}", label_visibility="collapsed")
            st.session_state.variables[idx].valor_actual = float(va)
            st.caption("Ingresar valor actual")
        else:
            va = st.number_input("", min_value=0, value=int(var.valor_actual or 0), step=1000,
                                  key=f"a_{idx}", label_visibility="collapsed")
            st.session_state.variables[idx].valor_actual = float(va)

    with cols[4]:
        if var.tipo == TipoVariable.INDEMNIZACION:
            st.caption("—")
        elif var.unidad == "%":
            vn = st.number_input("", min_value=0.0, max_value=100.0,
                                  value=float(var.valor_nuevo or var.valor_actual or 0),
                                  step=0.1, format="%.2f",
                                  key=f"nv_{idx}", label_visibility="collapsed")
            st.session_state.variables[idx].valor_nuevo = vn
            delta = vn - (var.valor_actual or 0)
            st.caption(f"{'🔴' if delta>0 else '🟢' if delta<0 else '⚪'} {delta:+.2f}pp")
        else:
            vn = st.number_input("", min_value=0,
                                  value=int(var.valor_nuevo or var.valor_actual or 0),
                                  step=1000, key=f"nv_{idx}", label_visibility="collapsed")
            st.session_state.variables[idx].valor_nuevo = float(vn)
            actual = var.valor_actual or 0
            delta_abs = vn - actual
            delta_pct = (delta_abs / actual * 100) if actual > 0 else 0
            color = "🔴" if delta_abs > 0 else ("🟢" if delta_abs < 0 else "⚪")
            st.caption(f"{color} {fmt_clp(delta_abs)} ({delta_pct:+.1f}%)")

    with cols[5]:
        aplica_c = st.checkbox("CAP", value=var.aplica_capitanes, key=f"cap_{idx}")
        aplica_f = st.checkbox("FO", value=var.aplica_primer_oficial, key=f"fo_{idx}")
        aplica_i = st.checkbox("Inc.Real", value=var.aplica_incremento_real, key=f"ir_{idx}")
        st.session_state.variables[idx].aplica_capitanes = aplica_c
        st.session_state.variables[idx].aplica_primer_oficial = aplica_f
        st.session_state.variables[idx].aplica_incremento_real = aplica_i

    if var.nota_operacional:
        st.info(f"⚙️ {var.nota_operacional}", icon="ℹ️")

    if var.tramos_antiguedad:
        with st.expander(f"📊 Tramos — {var.nombre[:40]}"):
            tcols = st.columns(len(var.tramos_antiguedad))
            for j, (tramo, val) in enumerate(var.tramos_antiguedad.items()):
                with tcols[j]:
                    nv_t = st.number_input(tramo, min_value=0, value=int(val or 0), step=1000, key=f"t_{idx}_{j}")
                    st.session_state.variables[idx].tramos_antiguedad[tramo] = float(nv_t)

    st.markdown("---")


# ─────────────────────────────────────────────
# PASO 3 — Resultados
# ─────────────────────────────────────────────
def render_resultados():
    if not st.session_state.variables:
        return

    dotacion = Dotacion(
        capitanes=st.session_state.dotacion_cap,
        fo=st.session_state.dotacion_fo,
    )
    if sum(dotacion.capitanes.values()) + sum(dotacion.fo.values()) == 0:
        st.warning("⚠️ Ingresa la dotación en el panel lateral para calcular costos.")
        return

    resultados, resumen = calcular_costos(
        st.session_state.variables, dotacion,
        st.session_state.incremento_real, st.session_state.duracion_meses,
    )
    if not resultados:
        return

    st.markdown('<div class="section-title">📊 Paso 3 — Resultados y Sensibilización</div>', unsafe_allow_html=True)

    # Métricas principales
    cols = st.columns(4)
    cols[0].metric("💵 Costo Anual Actual", fmt_clp(resumen["costo_actual_año1"]))
    cols[1].metric(
        f"💸 Costo Nuevo Año {len(resultados)}",
        fmt_clp(resumen["costo_nuevo_año_final"]),
        delta=fmt_clp(resumen["delta_punta_a_punta"]),
        delta_color="inverse"
    )
    cols[2].metric("📈 Variación Punta a Punta", fmt_pct(resumen["delta_pct_punta_a_punta"]))
    cols[3].metric(
        "🔢 Costo Incremental Acumulado",
        fmt_clp(resumen["costo_acumulado_delta"]),
        help="Diferencia total de costo en el período vs. mantener contrato actual"
    )

    st.markdown("---")

    # Cuadro punta a punta
    st.markdown("### 📌 Cuadro Punta a Punta")
    df_pp = pd.DataFrame([
        {"Concepto": "Costo anual contrato actual — Año 1", "Valor": fmt_clp(resumen["costo_actual_año1"])},
        {"Concepto": f"Costo anual contrato nuevo — Año {len(resultados)}", "Valor": fmt_clp(resumen["costo_nuevo_año_final"])},
        {"Concepto": "Variación anual absoluta (punta a punta)", "Valor": fmt_clp(resumen["delta_punta_a_punta"])},
        {"Concepto": "Variación anual porcentual (punta a punta)", "Valor": fmt_pct(resumen["delta_pct_punta_a_punta"])},
        {"Concepto": "━━━━━━━━━━━━━━━━━━━", "Valor": ""},
        {"Concepto": f"Costo acumulado contrato actual ({len(resultados)} años)", "Valor": fmt_clp(resumen["costo_acumulado_actual"])},
        {"Concepto": f"Costo acumulado contrato nuevo ({len(resultados)} años)", "Valor": fmt_clp(resumen["costo_acumulado_nuevo"])},
        {"Concepto": "Costo incremental acumulado total", "Valor": fmt_clp(resumen["costo_acumulado_delta"])},
    ])
    st.dataframe(df_pp, use_container_width=True, hide_index=True)

    # Tabla evolución año a año
    st.markdown("### 📅 Evolución Anual")
    df_años = pd.DataFrame([{
        "Año": f"Año {r.año}",
        "Costo Actual": fmt_clp(r.costo_actual_total),
        "Costo Nuevo": fmt_clp(r.costo_nuevo_total),
        "Δ Absoluto": fmt_clp(r.delta_absoluto),
        "Δ %": fmt_pct(r.delta_porcentual),
    } for r in resultados])
    st.dataframe(df_años, use_container_width=True, hide_index=True)

    # Gráfico barras agrupadas
    st.markdown("### 📊 Costo Anual — Actual vs. Nuevo")
    fig = go.Figure()
    años_lbl = [f"Año {r.año}" for r in resultados]
    fig.add_trace(go.Bar(name="Costo Actual", x=años_lbl,
                         y=[r.costo_actual_total for r in resultados],
                         marker_color="#1565C0",
                         text=[fmt_clp(r.costo_actual_total) for r in resultados],
                         textposition="outside"))
    fig.add_trace(go.Bar(name="Costo Nuevo", x=años_lbl,
                         y=[r.costo_nuevo_total for r in resultados],
                         marker_color="#D32F2F",
                         text=[fmt_clp(r.costo_nuevo_total) for r in resultados],
                         textposition="outside"))
    fig.update_layout(barmode="group", height=380, yaxis_title="CLP",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02),
                      margin=dict(t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

    # Waterfall
    if len(resultados) > 1:
        st.markdown("### 🌊 Waterfall — Escalada de Costos")
        base = resultados[0].costo_actual_total
        deltas = [resultados[i].costo_nuevo_total - resultados[i-1].costo_nuevo_total for i in range(1, len(resultados))]
        fig_wf = go.Figure(go.Waterfall(
            measure=["absolute"] + ["relative"] * (len(resultados)-1) + ["total"],
            x=["Base Año 1"] + [f"Δ Año {r.año}" for r in resultados[1:]] + ["Total Nuevo"],
            y=[base] + deltas + [resultados[-1].costo_nuevo_total],
            connector={"line": {"color": "rgb(63,63,63)"}},
            increasing={"marker": {"color": "#D32F2F"}},
            decreasing={"marker": {"color": "#388E3C"}},
            totals={"marker": {"color": "#1565C0"}},
            texttemplate="%{y:,.0f}", textposition="outside",
        ))
        fig_wf.update_layout(height=360, margin=dict(t=40, b=20))
        st.plotly_chart(fig_wf, use_container_width=True)

    # Composición del costo
    st.markdown("### 🥧 Composición Costo Nuevo — Año 1 (Recurrentes)")
    det = resultados[0].detalle
    pie_data = [(d["variable"], d["costo_nuevo"]) for d in det
                if d.get("costo_nuevo") and isinstance(d["costo_nuevo"], (int,float))
                and d["costo_nuevo"] > 0 and d.get("recurrente")]
    if pie_data:
        labels, values = zip(*sorted(pie_data, key=lambda x: -x[1])[:15])
        fig_pie = px.pie(names=labels, values=values, hole=0.4,
                         color_discrete_sequence=px.colors.qualitative.Set2)
        fig_pie.update_traces(textinfo="label+percent", textposition="outside")
        fig_pie.update_layout(height=450, showlegend=False, margin=dict(t=20, b=20))
        st.plotly_chart(fig_pie, use_container_width=True)

    # Desglose por año
    st.markdown("### 🔍 Desglose Detallado por Año")
    for r in resultados:
        delta_str = fmt_clp(r.delta_absoluto)
        with st.expander(f"📅 Año {r.año} — Actual: {fmt_clp(r.costo_actual_total)} | Nuevo: {fmt_clp(r.costo_nuevo_total)} | Δ: {delta_str}"):
            rows = []
            for d in r.detalle:
                if d.get("costo_actual") is None and d.get("costo_nuevo") is None:
                    ca, cn, dt = "Declarada", "Declarada", "—"
                elif d.get("es_porcentaje"):
                    ca = f"{d['costo_actual']:.2f}%" if d.get('costo_actual') is not None else "—"
                    cn = f"{d['costo_nuevo']:.2f}%" if d.get('costo_nuevo') is not None else "—"
                    dt = f"{d.get('delta',0):+.2f}pp" if d.get('delta') is not None else "—"
                else:
                    ca = fmt_clp(d.get("costo_actual"))
                    cn = fmt_clp(d.get("costo_nuevo"))
                    dt = fmt_clp(d.get("delta"))
                rows.append({
                    "Variable": d["variable"],
                    "Tipo": d["tipo"],
                    "Recurrente": "✓" if d.get("recurrente") else "—",
                    "Costo Actual": ca,
                    "Costo Nuevo": cn,
                    "Δ": dt,
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    inicializar_session()
    render_sidebar()

    st.title("✈️ Simulador de Costo — Contrato Colectivo Pilotos")
    st.caption("Herramienta interna para sensibilización de costos de negociación colectiva. Valores en CLP.")

    if st.session_state.contrato_nombre:
        st.info(f"📄 Contrato activo: **{st.session_state.contrato_nombre}**")

    st.markdown("---")
    render_carga()

    if st.session_state.variables:
        st.markdown("---")
        render_tabla_variables()
        st.markdown("---")
        render_resultados()
    else:
        st.markdown("---")
        st.markdown("""
        **Cómo usar esta herramienta:**
        1. Haz clic en **📋 Cargar LAN Cargo 2023-2026** para cargar el contrato actual con todos sus valores
        2. O sube el PDF de otro contrato para extracción automática
        3. Ajusta los valores actuales y nuevos en cada variable
        4. Configura la dotación por nivel en el panel lateral
        5. Los resultados se actualizan automáticamente
        """)


if __name__ == "__main__":
    main()
