"""
calculadora.py
Motor de cálculo de costos del contrato colectivo.
Calcula costo actual vs nuevo costo, año a año (3 años).
"""

from dataclasses import dataclass
from typing import Optional
from extractor import VariableContrato, TipoVariable, Recurrencia


@dataclass
class Dotacion:
    """Dotación de pilotos por cargo y tramo de antigüedad."""
    capitanes: dict   # {tramo: cantidad}  ej. {"0-5 años": 10, "6-10 años": 15}
    fo: dict          # {tramo: cantidad}


@dataclass
class ResultadoAnual:
    año: int
    costo_actual_total: float
    costo_nuevo_total: float
    delta_absoluto: float
    delta_porcentual: float
    detalle: list  # lista de dicts con desglose por variable


def calcular_dotacion_total(dotacion: Dotacion) -> tuple[int, int]:
    """Retorna (total capitanes, total FO)."""
    return sum(dotacion.capitanes.values()), sum(dotacion.fo.values())


def valor_con_incremento(valor_base: float, pct_incremento: float, año: int) -> float:
    """Aplica incremento real compuesto por N años."""
    return valor_base * ((1 + pct_incremento / 100) ** año)


def costo_variable_por_año(
    var: VariableContrato,
    dotacion: Dotacion,
    incremento_real_pct: float,
    usar_nuevo_valor: bool,
    año: int,  # 1, 2 o 3
) -> float:
    """
    Calcula el costo anual de una variable para la dotación dada.
    Retorna costo en CLP.
    """
    # Variables no costeadas
    if var.tipo == TipoVariable.INDEMNIZACION:
        return 0.0
    if var.tipo == TipoVariable.OPERACIONAL and var.valor_libro is None:
        return 0.0

    # Valor base según modo
    valor_base = var.valor_nuevo if usar_nuevo_valor else var.valor_actual
    if valor_base is None:
        return 0.0

    # Incremento real compuesto (solo si aplica y años > 0)
    if var.aplica_incremento_real and año > 0:
        valor_base = valor_con_incremento(valor_base, incremento_real_pct, año)

    # Unidad: si es % no tiene costo directo (es multiplicador de otro concepto)
    if var.unidad == '%':
        return 0.0

    total_cap, total_fo = calcular_dotacion_total(dotacion)

    # ── Cálculo según tramos de antigüedad ────────────────────────────────
    if var.tramos_antiguedad:
        costo = 0.0
        if var.aplica_capitanes:
            for tramo, n_personas in dotacion.capitanes.items():
                valor_tramo = var.tramos_antiguedad.get(tramo, valor_base)
                if var.aplica_incremento_real and año > 0:
                    valor_tramo = valor_con_incremento(valor_tramo, incremento_real_pct, año)
                costo += valor_tramo * n_personas * multiplicador_recurrencia(var.recurrencia)
        if var.aplica_primer_oficial:
            for tramo, n_personas in dotacion.fo.items():
                valor_tramo = var.tramos_antiguedad.get(tramo, valor_base)
                if var.aplica_incremento_real and año > 0:
                    valor_tramo = valor_con_incremento(valor_tramo, incremento_real_pct, año)
                costo += valor_tramo * n_personas * multiplicador_recurrencia(var.recurrencia)
        return costo

    # ── Sin tramos: valor plano por persona ───────────────────────────────
    n_aplica = 0
    if var.aplica_capitanes:
        n_aplica += total_cap
    if var.aplica_primer_oficial:
        n_aplica += total_fo

    return valor_base * n_aplica * multiplicador_recurrencia(var.recurrencia)


def multiplicador_recurrencia(recurrencia: Recurrencia) -> float:
    """Convierte recurrencia a multiplicador anual."""
    mapping = {
        Recurrencia.MENSUAL: 12,
        Recurrencia.ANUAL: 1,
        Recurrencia.ONE_TIME: 1,   # se trata por separado
        Recurrencia.EVENTO: 12,    # asume 1 evento/mes por defecto
        Recurrencia.DESCONOCIDA: 12,
    }
    return mapping.get(recurrencia, 12)


def es_recurrente(var: VariableContrato) -> bool:
    """Determina si una variable es recurrente para el cálculo anual."""
    return var.tipo != TipoVariable.BONO_ONE_TIME and var.recurrencia != Recurrencia.ONE_TIME


def calcular_costos(
    variables: list[VariableContrato],
    dotacion: Dotacion,
    incremento_real_pct: float,
    duracion_meses: int = 36,
) -> tuple[list[ResultadoAnual], dict]:
    """
    Calcula los costos año a año para el contrato.
    Retorna (resultados por año, resumen punta a punta).
    """
    años = duracion_meses // 12  # máximo 3
    resultados = []

    for año in range(1, años + 1):
        detalle = []
        costo_actual_total = 0.0
        costo_nuevo_total = 0.0

        for var in variables:
            # Bono one-time solo en año 1
            if var.tipo == TipoVariable.BONO_ONE_TIME and año > 1:
                detalle.append({
                    "variable": var.nombre,
                    "tipo": var.tipo.value,
                    "recurrente": False,
                    "costo_actual": 0.0,
                    "costo_nuevo": 0.0,
                    "delta": 0.0,
                    "nota": "One-time (solo año 1)",
                })
                continue

            # Indemnizaciones: declaradas, no costeadas
            if var.tipo == TipoVariable.INDEMNIZACION:
                detalle.append({
                    "variable": var.nombre,
                    "tipo": var.tipo.value,
                    "recurrente": False,
                    "costo_actual": None,
                    "costo_nuevo": None,
                    "delta": None,
                    "nota": "Declarada. No se costea.",
                })
                continue

            # Incremento real: se refleja como porcentaje, no como costo directo
            if var.tipo == TipoVariable.INCREMENTO:
                detalle.append({
                    "variable": var.nombre,
                    "tipo": var.tipo.value,
                    "recurrente": True,
                    "costo_actual": var.valor_actual,
                    "costo_nuevo": var.valor_nuevo,
                    "delta": (var.valor_nuevo or 0) - (var.valor_actual or 0),
                    "nota": f"% aplicado sobre conceptos definidos. Año {año}.",
                    "es_porcentaje": True,
                })
                continue

            c_actual = costo_variable_por_año(var, dotacion, incremento_real_pct, False, año - 1)
            # Costo nuevo: usa nuevo valor + incremento real acumulado
            c_nuevo = costo_variable_por_año(var, dotacion, incremento_real_pct, True, año - 1)

            delta = c_nuevo - c_actual

            if es_recurrente(var):
                costo_actual_total += c_actual
                costo_nuevo_total += c_nuevo

            detalle.append({
                "variable": var.nombre,
                "tipo": var.tipo.value,
                "recurrente": es_recurrente(var),
                "costo_actual": c_actual,
                "costo_nuevo": c_nuevo,
                "delta": delta,
                "nota": var.nota_operacional or "",
                "es_porcentaje": False,
            })

        delta_abs = costo_nuevo_total - costo_actual_total
        delta_pct = (delta_abs / costo_actual_total * 100) if costo_actual_total > 0 else 0.0

        resultados.append(ResultadoAnual(
            año=año,
            costo_actual_total=costo_actual_total,
            costo_nuevo_total=costo_nuevo_total,
            delta_absoluto=delta_abs,
            delta_porcentual=delta_pct,
            detalle=detalle,
        ))

    # ── Resumen punta a punta ──────────────────────────────────────────────
    if resultados:
        resumen = {
            "costo_actual_año1": resultados[0].costo_actual_total,
            "costo_nuevo_año_final": resultados[-1].costo_nuevo_total,
            "delta_punta_a_punta": resultados[-1].costo_nuevo_total - resultados[0].costo_actual_total,
            "delta_pct_punta_a_punta": (
                (resultados[-1].costo_nuevo_total - resultados[0].costo_actual_total)
                / resultados[0].costo_actual_total * 100
            ) if resultados[0].costo_actual_total > 0 else 0.0,
            "costo_acumulado_actual": sum(r.costo_actual_total for r in resultados),
            "costo_acumulado_nuevo": sum(r.costo_nuevo_total for r in resultados),
            "costo_acumulado_delta": sum(r.costo_nuevo_total for r in resultados) - sum(r.costo_actual_total for r in resultados),
        }
    else:
        resumen = {}

    return resultados, resumen
