"""
extractor.py
Extrae variables remuneracionales y operacionales de contratos colectivos
de pilotos en Chile usando pdfplumber + heurísticas de lenguaje natural.
"""

import re
import pdfplumber
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class TipoVariable(Enum):
    REMUNERACIONAL = "Remuneracional"
    OPERACIONAL = "Operacional"
    BONO_ONE_TIME = "Bono One-Time"
    INDEMNIZACION = "Indemnización"
    INCREMENTO = "Incremento"


class Recurrencia(Enum):
    MENSUAL = "Mensual"
    ANUAL = "Anual"
    ONE_TIME = "One-Time"
    EVENTO = "Por Evento"
    DESCONOCIDA = "Desconocida"


@dataclass
class VariableContrato:
    nombre: str
    tipo: TipoVariable
    recurrencia: Recurrencia
    valor_libro: Optional[float]          # extraído del PDF
    valor_actual: Optional[float]         # editable por usuario (inicia igual a libro)
    valor_nuevo: Optional[float]          # propuesta negociación
    aplica_capitanes: bool = True
    aplica_primer_oficial: bool = True
    tramos_antiguedad: dict = field(default_factory=dict)   # {tramo: valor}
    unidad: str = "CLP"
    nota_operacional: Optional[str] = None   # estimación headcount si es operacional
    aplica_incremento_real: bool = False     # si el % de incremento real se aplica
    clausula_referencia: Optional[str] = None
    es_nuevo_beneficio: bool = False


# ─────────────────────────────────────────────
# Patrones de extracción
# ─────────────────────────────────────────────

PATRONES_REMUNERACION = [
    # Bonos con monto explícito
    r'(?P<nombre>bono\s+[\w\s]+?)\s*[:\-–]\s*\$?\s*(?P<valor>[\d\.,]+)',
    r'(?P<nombre>asignaci[oó]n\s+[\w\s]+?)\s*[:\-–]\s*\$?\s*(?P<valor>[\d\.,]+)',
    r'(?P<nombre>gratificaci[oó]n\s+[\w\s]+?)\s*[:\-–]\s*\$?\s*(?P<valor>[\d\.,]+)',
    r'(?P<nombre>premio\s+[\w\s]+?)\s*[:\-–]\s*\$?\s*(?P<valor>[\d\.,]+)',
    r'(?P<nombre>viático\s+[\w\s]+?)\s*[:\-–]\s*\$?\s*(?P<valor>[\d\.,]+)',
    r'(?P<nombre>hora\s+extra[\w\s]*?)\s*[:\-–]\s*\$?\s*(?P<valor>[\d\.,]+)',
    r'(?P<nombre>colaci[oó]n[\w\s]*?)\s*[:\-–]\s*\$?\s*(?P<valor>[\d\.,]+)',
    r'(?P<nombre>movilizaci[oó]n[\w\s]*?)\s*[:\-–]\s*\$?\s*(?P<valor>[\d\.,]+)',
    # Porcentajes sobre sueldo base
    r'(?P<nombre>[\w\s]+?)\s+(?P<valor>[\d]+(?:,\d+)?)\s*%\s*(?:del\s+)?sueldo\s+base',
    # Valores en UTM / UF
    r'(?P<nombre>[\w\s]+?)\s*[:\-–]\s*(?P<valor>[\d\.,]+)\s*(?P<unidad>UTM|UF)',
]

PATRONES_OPERACIONAL = [
    r'descanso\s+[\w\s]*',
    r'días?\s+libre[s]?\s+[\w\s]*',
    r'horario[s]?\s+bloqueado[s]?',
    r'límite[s]?\s+de\s+horas?\s+de\s+vuelo',
    r'período[s]?\s+de\s+descanso',
    r'rotaci[oó]n[\s\w]*',
    r'turno[s]?\s+[\w\s]*',
    r'rest[o]?\s+[\w\s]*',
    r'FDP\s+[\w\s]*',        # Flight Duty Period
    r'FT\s+[\w\s]*',         # Flight Time
    r'standby[\s\w]*',
    r'reserva[\s\w]*disponibilidad',
    r'licencia[\s\w]*',
    r'permisos?\s+[\w\s]*',
]

PATRONES_INCREMENTO = [
    r'incremento\s+real\s+de\s+(?:remuneraciones?\s+)?(?:de\s+)?(?P<valor>[\d]+(?:[,\.]\d+)?)\s*%',
    r'aumento\s+real\s+(?:de\s+)?(?P<valor>[\d]+(?:[,\.]\d+)?)\s*%',
    r'reajuste\s+real\s+(?:de\s+)?(?P<valor>[\d]+(?:[,\.]\d+)?)\s*%',
    r'(?P<valor>[\d]+(?:[,\.]\d+)?)\s*%\s*(?:de\s+)?incremento\s+real',
]

PATRONES_ANTIGUEDAD = [
    r'(?P<desde>\d+)\s*(?:a\s+(?P<hasta>\d+)|o\s+más)\s*años?\s+de\s+(?:servicio|antigüedad)',
    r'tramo\s+(?P<tramo>\w+)\s*:\s*(?:de\s+)?(?P<desde>\d+)\s*a\s*(?P<hasta>\d+)\s*años?',
    r'(?:hasta|menos\s+de)\s+(?P<hasta>\d+)\s*años?\s+de\s+(?:servicio|antigüedad)',
]

PALABRAS_BONO_TERMINO = [
    'bono de término', 'bono término', 'bono de negociación',
    'bono negociación', 'bono de cierre', 'bono fin de negociación',
    'bono por término'
]

PALABRAS_INDEMNIZACION = [
    'indemnización por años de servicio', 'indemnización años servicio',
    'años de servicio', 'indemnización legal', 'indemnización convencional'
]


def limpiar_valor(valor_str: str) -> Optional[float]:
    """Convierte string de valor monetario a float."""
    if not valor_str:
        return None
    # Remover puntos de miles y reemplazar coma decimal
    limpio = re.sub(r'[^\d,\.]', '', valor_str)
    # Formato chileno: 1.000.000 o 1.000.000,50
    limpio = limpio.replace('.', '').replace(',', '.')
    try:
        return float(limpio)
    except ValueError:
        return None


def normalizar_nombre(nombre: str) -> str:
    """Normaliza y limpia el nombre de una variable."""
    nombre = re.sub(r'\s+', ' ', nombre).strip()
    nombre = nombre.strip(':-–').strip()
    return nombre.title()


def extraer_tramos_antiguedad(texto_clausula: str) -> dict:
    """Extrae tramos de antigüedad de una cláusula."""
    tramos = {}
    lines = texto_clausula.split('\n')
    for line in lines:
        # Buscar patrones como "0-5 años: $X" o "Más de 10 años: $X"
        m = re.search(
            r'(\d+)\s*[-–a]\s*(\d+)\s*años?.{0,30}\$?\s*([\d\.,]+)',
            line, re.IGNORECASE
        )
        if m:
            tramo = f"{m.group(1)}-{m.group(2)} años"
            valor = limpiar_valor(m.group(3))
            if valor:
                tramos[tramo] = valor
            continue
        m = re.search(
            r'(?:más\s+de|sobre|desde)\s+(\d+)\s*años?.{0,30}\$?\s*([\d\.,]+)',
            line, re.IGNORECASE
        )
        if m:
            tramo = f"+{m.group(1)} años"
            valor = limpiar_valor(m.group(2))
            if valor:
                tramos[tramo] = valor
    return tramos


def detectar_cargo(texto: str) -> tuple[bool, bool]:
    """Detecta si una cláusula aplica a capitán, primer oficial o ambos."""
    texto_lower = texto.lower()
    tiene_capitan = any(p in texto_lower for p in ['capitán', 'capitan', 'comandante'])
    tiene_fo = any(p in texto_lower for p in ['primer oficial', 'co-piloto', 'copiloto', 'first officer', 'f/o'])
    # Si no menciona ninguno, aplica a ambos
    if not tiene_capitan and not tiene_fo:
        return True, True
    return tiene_capitan, tiene_fo


def detectar_recurrencia(texto: str) -> Recurrencia:
    """Detecta la recurrencia de un beneficio."""
    texto_lower = texto.lower()
    if any(p in texto_lower for p in ['mensual', 'cada mes', 'por mes']):
        return Recurrencia.MENSUAL
    if any(p in texto_lower for p in ['anual', 'cada año', 'por año', 'al año']):
        return Recurrencia.ANUAL
    if any(p in texto_lower for p in ['por evento', 'por vuelo', 'por turno', 'por jornada']):
        return Recurrencia.EVENTO
    return Recurrencia.DESCONOCIDA


def extraer_variables_pdf(pdf_path: str) -> tuple[list[VariableContrato], str]:
    """
    Extrae todas las variables del PDF.
    Retorna (lista de variables, texto completo extraído).
    """
    variables = []
    texto_completo = []
    nombres_vistos = set()

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            texto = page.extract_text()
            if texto:
                texto_completo.append(texto)

    texto_total = '\n'.join(texto_completo)

    # ── 1. Buscar incremento real ──────────────────────────────────────────
    for patron in PATRONES_INCREMENTO:
        for m in re.finditer(patron, texto_total, re.IGNORECASE):
            valor_str = m.group('valor').replace(',', '.')
            try:
                pct = float(valor_str)
            except ValueError:
                continue
            nombre = "Incremento Real de Remuneraciones"
            if nombre not in nombres_vistos:
                nombres_vistos.add(nombre)
                # Buscar contexto de 300 chars
                inicio = max(0, m.start() - 100)
                fin = min(len(texto_total), m.end() + 200)
                contexto = texto_total[inicio:fin]
                cap, fo = detectar_cargo(contexto)
                variables.append(VariableContrato(
                    nombre=nombre,
                    tipo=TipoVariable.INCREMENTO,
                    recurrencia=Recurrencia.ANUAL,
                    valor_libro=pct,
                    valor_actual=pct,
                    valor_nuevo=pct,
                    aplica_capitanes=cap,
                    aplica_primer_oficial=fo,
                    unidad="%",
                    aplica_incremento_real=False,
                    clausula_referencia=contexto[:200].strip(),
                ))

    # ── 2. Buscar bono de término de negociación ───────────────────────────
    for keyword in PALABRAS_BONO_TERMINO:
        for m in re.finditer(re.escape(keyword), texto_total, re.IGNORECASE):
            inicio = max(0, m.start() - 50)
            fin = min(len(texto_total), m.end() + 300)
            contexto = texto_total[inicio:fin]
            # Buscar valor en el contexto
            vm = re.search(r'\$?\s*([\d\.,]+)', contexto)
            valor = limpiar_valor(vm.group(1)) if vm else None
            nombre = "Bono De Término De Negociación"
            if nombre not in nombres_vistos:
                nombres_vistos.add(nombre)
                cap, fo = detectar_cargo(contexto)
                tramos = extraer_tramos_antiguedad(contexto)
                variables.append(VariableContrato(
                    nombre=nombre,
                    tipo=TipoVariable.BONO_ONE_TIME,
                    recurrencia=Recurrencia.ONE_TIME,
                    valor_libro=valor,
                    valor_actual=valor,
                    valor_nuevo=valor,
                    aplica_capitanes=cap,
                    aplica_primer_oficial=fo,
                    tramos_antiguedad=tramos,
                    aplica_incremento_real=False,
                    clausula_referencia=contexto[:200].strip(),
                ))
            break

    # ── 3. Buscar indemnizaciones ──────────────────────────────────────────
    for keyword in PALABRAS_INDEMNIZACION:
        for m in re.finditer(re.escape(keyword), texto_total, re.IGNORECASE):
            inicio = max(0, m.start() - 50)
            fin = min(len(texto_total), m.end() + 400)
            contexto = texto_total[inicio:fin]
            nombre = "Indemnización Por Años De Servicio"
            if nombre not in nombres_vistos:
                nombres_vistos.add(nombre)
                cap, fo = detectar_cargo(contexto)
                tramos = extraer_tramos_antiguedad(contexto)
                variables.append(VariableContrato(
                    nombre=nombre,
                    tipo=TipoVariable.INDEMNIZACION,
                    recurrencia=Recurrencia.ONE_TIME,
                    valor_libro=None,
                    valor_actual=None,
                    valor_nuevo=None,
                    aplica_capitanes=cap,
                    aplica_primer_oficial=fo,
                    tramos_antiguedad=tramos,
                    aplica_incremento_real=False,
                    clausula_referencia=contexto[:200].strip(),
                    nota_operacional="Declarada. No se costea en este modelo.",
                ))
            break

    # ── 4. Buscar variables remuneracionales con valor ─────────────────────
    for patron in PATRONES_REMUNERACION:
        for m in re.finditer(patron, texto_total, re.IGNORECASE):
            nombre_raw = m.group('nombre') if 'nombre' in m.groupdict() else ''
            nombre = normalizar_nombre(nombre_raw)
            if not nombre or len(nombre) < 4:
                continue
            # Evitar duplicados con bono de término e indemnización
            if any(k in nombre.lower() for k in ['término', 'termino', 'negociaci', 'indemnizaci', 'incremento']):
                continue
            if nombre in nombres_vistos:
                continue
            nombres_vistos.add(nombre)

            valor_str = m.group('valor') if 'valor' in m.groupdict() else None
            unidad_raw = m.group('unidad') if 'unidad' in m.groupdict() else 'CLP'
            valor = limpiar_valor(valor_str)

            inicio = max(0, m.start() - 100)
            fin = min(len(texto_total), m.end() + 400)
            contexto = texto_total[inicio:fin]

            cap, fo = detectar_cargo(contexto)
            recurrencia = detectar_recurrencia(contexto)
            tramos = extraer_tramos_antiguedad(contexto)

            # ¿Aplica incremento real? Solo si el contrato menciona que se aplica sobre este concepto
            aplica_inc = bool(re.search(
                r'increment[ao]\s+real.{0,100}' + re.escape(nombre_raw[:10]),
                texto_total, re.IGNORECASE
            ))

            variables.append(VariableContrato(
                nombre=nombre,
                tipo=TipoVariable.REMUNERACIONAL,
                recurrencia=recurrencia,
                valor_libro=valor,
                valor_actual=valor,
                valor_nuevo=valor,
                aplica_capitanes=cap,
                aplica_primer_oficial=fo,
                tramos_antiguedad=tramos,
                unidad=unidad_raw or 'CLP',
                aplica_incremento_real=aplica_inc,
                clausula_referencia=contexto[:200].strip(),
            ))

    # ── 5. Buscar variables operacionales ─────────────────────────────────
    for patron in PATRONES_OPERACIONAL:
        for m in re.finditer(patron, texto_total, re.IGNORECASE):
            inicio = max(0, m.start() - 30)
            fin = min(len(texto_total), m.end() + 300)
            contexto = texto_total[inicio:fin]
            # Extraer primera línea como nombre
            primera_linea = contexto.split('\n')[0][:80]
            nombre = normalizar_nombre(primera_linea)
            if not nombre or nombre in nombres_vistos or len(nombre) < 5:
                continue
            nombres_vistos.add(nombre)

            cap, fo = detectar_cargo(contexto)
            # Buscar valor numérico (horas, días, etc.)
            vm = re.search(r'(\d+(?:[,\.]\d+)?)\s*(horas?|días?|minutos?)', contexto, re.IGNORECASE)
            valor = float(vm.group(1).replace(',', '.')) if vm else None
            unidad = vm.group(2) if vm else 'N/A'

            nota = estimar_efecto_operacional(nombre, contexto)

            variables.append(VariableContrato(
                nombre=nombre,
                tipo=TipoVariable.OPERACIONAL,
                recurrencia=Recurrencia.MENSUAL,
                valor_libro=valor,
                valor_actual=valor,
                valor_nuevo=valor,
                aplica_capitanes=cap,
                aplica_primer_oficial=fo,
                unidad=unidad,
                nota_operacional=nota,
                aplica_incremento_real=False,
                clausula_referencia=contexto[:200].strip(),
            ))

    return variables, texto_total


# ─────────────────────────────────────────────
# Estimación de efecto operacional en headcount
# ─────────────────────────────────────────────

# Parámetros industria aérea Chile (valores promedio de referencia)
PARAMS_INDUSTRIA = {
    "horas_vuelo_mes_capitan": 75,        # horas/mes promedio capitán
    "horas_vuelo_mes_fo": 80,             # horas/mes promedio primer oficial
    "horas_fdp_max_dia": 12,              # FDP máximo legal (DAN 91)
    "dias_servicio_mes": 20,              # días de servicio al mes
    "ratio_reserva": 0.15,                # 15% de la dotación en reserva
    "costo_hora_capitan_clp": 85_000,     # costo/hora aproximado capitán
    "costo_hora_fo_clp": 55_000,          # costo/hora aproximado FO
    "sueldo_base_capitan": 4_500_000,     # sueldo base referencial
    "sueldo_base_fo": 2_800_000,          # sueldo base referencial FO
}


def estimar_efecto_operacional(nombre: str, contexto: str) -> str:
    """
    Estima el efecto en headcount o costo de una variable operacional
    usando parámetros de la industria aérea chilena.
    """
    nombre_lower = nombre.lower()
    contexto_lower = contexto.lower()

    # Detectar valores numéricos en contexto
    nums = re.findall(r'(\d+(?:[,\.]\d+)?)\s*(horas?|días?|minutos?)', contexto, re.IGNORECASE)

    if any(p in nombre_lower for p in ['descanso', 'rest', 'días libre', 'día libre']):
        if nums:
            valor = float(nums[0][0].replace(',', '.'))
            unidad = nums[0][1].lower()
            if 'hora' in unidad:
                # Más horas de descanso → menos disponibilidad → más headcount
                reduccion_pct = valor / (PARAMS_INDUSTRIA['horas_fdp_max_dia'] * PARAMS_INDUSTRIA['dias_servicio_mes'] * 24 / PARAMS_INDUSTRIA['horas_fdp_max_dia'])
                return (
                    f"Estimación: aumentar descanso mínimo en {valor:.0f} horas reduce "
                    f"disponibilidad operativa ~{reduccion_pct*100:.1f}%. "
                    f"En una dotación de 100 pilotos, equivale a ~{max(1, int(100 * reduccion_pct))} "
                    f"pilotos adicionales de headcount efectivo. "
                    f"Parámetro: FDP máx {PARAMS_INDUSTRIA['horas_fdp_max_dia']}h (DAN 91 Chile)."
                )
        return (
            "Estimación: cada día adicional de descanso mensual reduce disponibilidad ~5%. "
            "En dotación de 100 pilotos ≈ 5 pilotos equivalentes de headcount adicional."
        )

    if any(p in nombre_lower for p in ['horario bloqueado', 'bloqueo', 'no programar']):
        return (
            "Estimación: bloquear franjas horarias reduce productividad de programación. "
            "Impacto típico en aerolíneas regionales Chile: +3-8% sobre dotación mínima operativa, "
            "dependiendo del porcentaje de vuelos en franja bloqueada."
        )

    if any(p in nombre_lower for p in ['standby', 'reserva', 'disponibilidad']):
        return (
            f"Estimación: cada piloto en standby tiene disponibilidad efectiva ~{PARAMS_INDUSTRIA['ratio_reserva']*100:.0f}% "
            f"respecto a uno en línea. "
            f"Aumentar cobertura de standby en 1 posición diaria requiere "
            f"~{int(1/PARAMS_INDUSTRIA['ratio_reserva'])} pilotos adicionales en el pool de reserva."
        )

    if any(p in nombre_lower for p in ['hora de vuelo', 'fdp', 'flight duty', 'límite']):
        if nums:
            valor = float(nums[0][0].replace(',', '.'))
            # Reducción de FDP máx → más pilotos para cubrir mismos vuelos
            actual = PARAMS_INDUSTRIA['horas_fdp_max_dia']
            if valor < actual:
                factor = actual / valor
                return (
                    f"Estimación: reducir FDP máximo de {actual:.0f}h a {valor:.0f}h "
                    f"implica factor de cobertura ×{factor:.2f}. "
                    f"En dotación de 100 pilotos, requeriría ~{int(100 * (factor - 1))} pilotos adicionales."
                )
        return (
            "Estimación: reducción de límite de horas de vuelo aumenta headcount requerido. "
            "Referencia: límite actual DAN 91 Chile = 900 horas/año."
        )

    if any(p in nombre_lower for p in ['licencia', 'permiso', 'vacacion']):
        if nums:
            valor = float(nums[0][0].replace(',', '.'))
            dias_laborables_ano = 240
            reduccion = valor / dias_laborables_ano
            return (
                f"Estimación: {valor:.0f} días adicionales de licencia/año = "
                f"{reduccion*100:.1f}% de reducción de disponibilidad anual. "
                f"En dotación de 100 pilotos ≈ {max(1, int(100 * reduccion))} pilotos equivalentes."
            )
        return "Estimación: cada día adicional de licencia anual ≈ 0.4% reducción en disponibilidad."

    # Genérico
    return (
        "Variable operacional identificada. "
        "Se requiere contexto adicional para estimar efecto en headcount. "
        "Ingrese manualmente el efecto estimado en la tabla."
    )
