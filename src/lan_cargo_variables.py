"""
lan_cargo_variables.py
Variables del Contrato Colectivo LAN Cargo S.A. — Vigencia 01-sep-2023 al 31-ago-2026
Todos los valores están precargados con sus valores libro del contrato.
"""

from extractor import VariableContrato, TipoVariable, Recurrencia


# ─────────────────────────────────────────────────────────────────────────────
# TABLAS DE COMPONENTE VARIABLE (HBT) — Cláusula Cuarta N°2
# Valor mensual según tramo de horas voladas
# ─────────────────────────────────────────────────────────────────────────────

TABLA_HBT_CAPITAN = {
    # (horas_min, horas_max): (Nivel A, Nivel B, Nivel C)
    (59,   68.9): (876_873,   843_147,   809_421),
    (69,   78.9): (1_198_250, 1_152_163, 1_106_076),
    (79,   81.9): (1_976_219, 1_900_210, 1_824_201),
    (82,   82.9): (2_089_056, 2_008_707, 1_928_358),
    (83,   83.9): (2_201_894, 2_117_205, 2_032_516),
    (84,   84.9): (2_314_731, 2_225_702, 2_136_674),
    (85,   85.9): (2_427_569, 2_334_200, 2_240_831),
    (86,   86.9): (2_540_406, 2_442_697, 2_344_989),
    (87,   87.9): (2_653_243, 2_551_195, 2_449_146),
    (88,   88.9): (2_766_081, 2_659_692, 2_553_304),
    (89,   999):  (2_883_849, 2_772_931, 2_662_013),
}

TABLA_HBT_FO = {
    (59,   68.9): (768_950,   739_375,   665_438),
    (69,   78.9): (982_706,   944_909,   850_419),
    (79,   81.9): (1_196_461, 1_150_443, 1_035_400),
    (82,   82.9): (1_265_585, 1_216_909, 1_097_941),
    (83,   83.9): (1_334_709, 1_283_374, 1_160_482),
    (84,   84.9): (1_403_834, 1_349_840, 1_223_023),
    (85,   85.9): (1_472_958, 1_416_305, 1_285_563),
    (86,   86.9): (1_542_082, 1_482_771, 1_348_104),
    (87,   87.9): (1_611_206, 1_549_236, 1_410_645),
    (88,   88.9): (1_680_330, 1_615_702, 1_473_186),
    (89,   999):  (1_749_455, 1_682_167, 1_535_727),
}


def hbt_a_valor(horas: float, tabla: dict, nivel_idx: int) -> int:
    """Retorna el valor mensual de componente variable para las horas dadas."""
    for (h_min, h_max), valores in tabla.items():
        if h_min <= horas <= h_max:
            return valores[nivel_idx]
    if horas < 59:
        return 0
    return list(tabla.values())[-1][nivel_idx]


def calcular_componente_variable(
    horas_cap_a: float, horas_cap_b: float, horas_cap_c: float,
    horas_fo_a: float, horas_fo_b: float, horas_fo_c: float,
    horas_fo_subc: float,
) -> dict:
    """
    Retorna dict con valor mensual de componente variable por nivel.
    Se usa desde la app para precalcular los valores según horas ingresadas.
    """
    return {
        "CAP Nivel A": hbt_a_valor(horas_cap_a, TABLA_HBT_CAPITAN, 0),
        "CAP Nivel B": hbt_a_valor(horas_cap_b, TABLA_HBT_CAPITAN, 1),
        "CAP Nivel C": hbt_a_valor(horas_cap_c, TABLA_HBT_CAPITAN, 2),
        "FO Nivel A":  hbt_a_valor(horas_fo_a,  TABLA_HBT_FO, 0),
        "FO Nivel B":  hbt_a_valor(horas_fo_b,  TABLA_HBT_FO, 1),
        "FO Nivel C":  hbt_a_valor(horas_fo_c,  TABLA_HBT_FO, 2),
        "FO Sub-C":    hbt_a_valor(horas_fo_subc, TABLA_HBT_FO, 2),
    }


def cargar_variables_lan_cargo(
    horas_cap_a=75.0, horas_cap_b=75.0, horas_cap_c=75.0,
    horas_fo_a=75.0,  horas_fo_b=75.0,  horas_fo_c=75.0,
    horas_fo_subc=70.0,
) -> list:
    """
    Retorna lista de variables del contrato LAN Cargo.
    Los valores de componente variable se calculan según las horas promedio ingresadas.
    """
    variables = []

    cv = calcular_componente_variable(
        horas_cap_a, horas_cap_b, horas_cap_c,
        horas_fo_a, horas_fo_b, horas_fo_c, horas_fo_subc,
    )

    # ─────────────────────────────────────────────────────────────────
    # 1. SUELDOS BASE — Cláusula Cuarta N°1
    # ─────────────────────────────────────────────────────────────────

    variables.append(VariableContrato(
        nombre="Sueldo Base — Capitán",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=8_862_076,
        valor_actual=8_862_076,
        valor_nuevo=8_862_076,
        aplica_capitanes=True,
        aplica_primer_oficial=False,
        tramos_antiguedad={
            "Nivel A (≥20 años)":   8_862_076,
            "Nivel B (13-19 años)": 8_521_227,
            "Nivel C (<13 años)":   8_180_376,
        },
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Cuarta N°1.1 — Vigente desde oct 2023",
    ))

    variables.append(VariableContrato(
        nombre="Sueldo Base — Primer Oficial (ingreso pre mayo 2018)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=5_317_245,
        valor_actual=5_317_245,
        valor_nuevo=5_317_245,
        aplica_capitanes=False,
        aplica_primer_oficial=True,
        tramos_antiguedad={
            "Nivel A (≥8 años)":  5_317_245,
            "Nivel B (4-7 años)": 5_112_736,
            "Nivel C (<4 años)":  4_810_841,
        },
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Cuarta N°1.2.1 — Vigente desde oct 2023",
    ))

    variables.append(VariableContrato(
        nombre="Sueldo Base — Primer Oficial (ingreso desde mayo 2018)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=5_317_245,
        valor_actual=5_317_245,
        valor_nuevo=5_317_245,
        aplica_capitanes=False,
        aplica_primer_oficial=True,
        tramos_antiguedad={
            "Nivel A (≥7 años)":  5_317_245,
            "Nivel B (6-7 años)": 5_112_736,
            "Nivel C (4-6 años)": 4_810_841,
        },
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Cuarta N°1.2.2 — Vigente desde oct 2023",
    ))

    variables.append(VariableContrato(
        nombre="Sueldo Base — Primer Oficial Sub-C (<4 años, Nivel 1 año 3)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=3_577_672,
        valor_actual=3_577_672,
        valor_nuevo=3_577_672,
        aplica_capitanes=False,
        aplica_primer_oficial=True,
        tramos_antiguedad={
            "0 años Nivel 1": 1_917_929,
            "0 años Nivel 2": 2_508_058,
            "0 años Nivel 3": 2_803_125,
            "1 año Nivel 1":  3_039_177,
            "1 año Nivel 2":  3_393_257,
            "1 año Nivel 3":  3_688_322,
            "2 años Nivel 1": 3_577_672,
            "2 años Nivel 2": 3_983_387,
            "2 años Nivel 3": 4_278_455,
            "3 años Nivel 1": 4_810_841,
        },
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Cuarta N°1.2.3 — FO Sub-C",
        nota_operacional="Tabla de progresión Sub-C. El valor libro muestra el tramo 2 años Nivel 1. Ajusta los tramos según distribución real de la dotación Sub-C.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 2. COMPONENTE VARIABLE HBT — Cláusula Cuarta N°2
    # Calculado según horas promedio ingresadas por el usuario
    # ─────────────────────────────────────────────────────────────────

    variables.append(VariableContrato(
        nombre="Componente Variable HBT — Capitán",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=cv["CAP Nivel A"],
        valor_actual=cv["CAP Nivel A"],
        valor_nuevo=cv["CAP Nivel A"],
        aplica_capitanes=True,
        aplica_primer_oficial=False,
        tramos_antiguedad={
            "Nivel A":  cv["CAP Nivel A"],
            "Nivel B":  cv["CAP Nivel B"],
            "Nivel C":  cv["CAP Nivel C"],
        },
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Cuarta N°2.1 — Wide Body",
        nota_operacional=f"Calculado para {horas_cap_a:.0f}h promedio CAP-A / {horas_cap_b:.0f}h CAP-B / {horas_cap_c:.0f}h CAP-C. Ajusta las horas en la sección de configuración HBT.",
    ))

    variables.append(VariableContrato(
        nombre="Componente Variable HBT — Primer Oficial",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=cv["FO Nivel A"],
        valor_actual=cv["FO Nivel A"],
        valor_nuevo=cv["FO Nivel A"],
        aplica_capitanes=False,
        aplica_primer_oficial=True,
        tramos_antiguedad={
            "Nivel A":  cv["FO Nivel A"],
            "Nivel B":  cv["FO Nivel B"],
            "Nivel C":  cv["FO Nivel C"],
            "Sub-C":    cv["FO Sub-C"],
        },
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Cuarta N°2.2 — Wide Body",
        nota_operacional=f"Calculado para {horas_fo_a:.0f}h promedio FO-A / {horas_fo_b:.0f}h FO-B / {horas_fo_c:.0f}h FO-C / {horas_fo_subc:.0f}h Sub-C.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 3. GRATIFICACIÓN LEGAL — Cláusula Cuarta N°3
    # 25% de lo pagado, tope 4.75 IMM = ~$270.000 mensual aprox.
    # Se paga mensualmente como anticipo
    # ─────────────────────────────────────────────────────────────────

    variables.append(VariableContrato(
        nombre="Gratificación Legal (tope 4.75 IMM = ~$270.200 mensual)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=270_200,
        valor_actual=270_200,
        valor_nuevo=270_200,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Cuarta N°3 — Art. 50 Código del Trabajo",
        nota_operacional="Tope = 4.75 × IMM (Ingreso Mínimo Mensual). Valor referencial calculado sobre IMM $570.000 (2024). Actualizar si cambia el IMM.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 4. ASIGNACIÓN DE ANTIGÜEDAD — Cláusula Cuarta N°4
    # ─────────────────────────────────────────────────────────────────

    variables.append(VariableContrato(
        nombre="Asignación Antigüedad — Capitán (desde año 9, 1%/año, máx 30%)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=88_621,
        valor_actual=88_621,
        valor_nuevo=88_621,
        aplica_capitanes=True,
        aplica_primer_oficial=False,
        tramos_antiguedad={
            "9 años (1%)":  88_621,
            "10 años (2%)": 177_242,
            "15 años (7%)": 620_345,
            "20 años (12%)": 1_063_449,
            "25 años (17%)": 1_506_553,
            "30 años (22%)": 1_949_657,
        },
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Cuarta N°4.1",
        nota_operacional="1% del promedio de remuneración por cada año desde el año 9. Máximo 30%. Valores referenciales calculados sobre sueldo base Nivel A $8.862.076. Ajustar según distribución real de antigüedad.",
    ))

    variables.append(VariableContrato(
        nombre="Asignación Antigüedad — Primer Oficial (desde año 2, escalonada, máx 9%)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=53_172,
        valor_actual=53_172,
        valor_nuevo=53_172,
        aplica_capitanes=False,
        aplica_primer_oficial=True,
        tramos_antiguedad={
            "2 años (1%)":  53_172,
            "3 años (1.5%)": 79_758,
            "4 años (2%)":   106_344,
            "5 años (3%)":   159_516,
            "8 años (6%)":   319_034,
            "9 años (7%)":   372_207,
            "≥10 años (max 9%)": 478_552,
        },
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Cuarta N°4.2",
        nota_operacional="Escala: 1% año 2, 1.5% año 3, 2% año 4, luego +1%/año hasta máx 9% (o 25% si no asciende con ≥12 años). Valores referenciales sobre sueldo base FO Nivel A $5.317.245.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 5. MOVILIZACIÓN — Cláusula Undécima
    # ─────────────────────────────────────────────────────────────────

    variables.append(VariableContrato(
        nombre="Asignación Sustitutiva de Movilización (líquido mensual)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=205_837,
        valor_actual=205_837,
        valor_nuevo=205_837,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Undécima N°2 — $205.837 líquidos",
        nota_operacional="Solo aplica a pilotos que renuncian a la movilización provista. Ajustar N° de beneficiarios en la dotación según elección real.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 6. ASIGNACIONES ANUALES / ESPECIALES — Cláusula Sexta
    # ─────────────────────────────────────────────────────────────────

    variables.append(VariableContrato(
        nombre="Asignación Septiembre",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.ANUAL,
        valor_libro=94_688,
        valor_actual=94_688,
        valor_nuevo=94_688,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Sexta letra b) — $94.688 brutos + $21.044 por carga familiar",
        nota_operacional="$94.688 base + $21.044 por cada carga familiar reconocida. El valor libro es el base sin cargas. Ajustar si se quiere modelar con cargas promedio.",
    ))

    variables.append(VariableContrato(
        nombre="Asignación Navidad",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.ANUAL,
        valor_libro=165_656,
        valor_actual=165_656,
        valor_nuevo=165_656,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Sexta letra c) — $165.656 brutos, pagado antes del 24 dic",
    ))

    variables.append(VariableContrato(
        nombre="Asignación Escolaridad — Universitaria/Técnica (por hijo/año)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.ANUAL,
        valor_libro=272_693,
        valor_actual=272_693,
        valor_nuevo=272_693,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Sexta letra a)",
        nota_operacional="Tramos: Parvulario $105.209 / Básica $136.350 / Media $146.450 / Universitaria $272.693. El valor libro es el tramo más alto. Costear según distribución real de hijos.",
    ))

    variables.append(VariableContrato(
        nombre="Asignación Matrimonio (primera vez)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.EVENTO,
        valor_libro=94_138,
        valor_actual=94_138,
        valor_nuevo=94_138,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Sexta letra e) — $94.138 brutos",
        nota_operacional="Pago por evento. Para costear, ingresar número estimado de matrimonios al año en la dotación.",
    ))

    variables.append(VariableContrato(
        nombre="Asignación Hijo Discapacitado (anual por hijo)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.ANUAL,
        valor_libro=430_511,
        valor_actual=430_511,
        valor_nuevo=430_511,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Sexta letra f) — $430.511 brutos anuales",
        nota_operacional="Requiere certificado SENADIS. Pagado en abril. Ajustar número de beneficiarios.",
    ))

    variables.append(VariableContrato(
        nombre="Asignación Instructor Evaluador — IE (mensual)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=1_462_399,
        valor_actual=1_462_399,
        valor_nuevo=1_462_399,
        aplica_capitanes=True,
        aplica_primer_oficial=False,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Sexta letra g) — $1.462.399 brutos mensuales",
        nota_operacional="Solo mientras mantenga la designación de IE. Ajustar N° de IEs en dotación lateral.",
    ))

    variables.append(VariableContrato(
        nombre="Asignación Instructor de Vuelo (mensual)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=572_102,
        valor_actual=572_102,
        valor_nuevo=572_102,
        aplica_capitanes=True,
        aplica_primer_oficial=False,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Sexta letra h) — $572.102 brutos mensuales",
    ))

    variables.append(VariableContrato(
        nombre="Asignación Asesor (mensual)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=746_687,
        valor_actual=746_687,
        valor_nuevo=746_687,
        aplica_capitanes=True,
        aplica_primer_oficial=False,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Sexta letra j) — $746.687 brutos mensuales",
    ))

    variables.append(VariableContrato(
        nombre="Asignación Tutor (por vuelo de instrucción)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.EVENTO,
        valor_libro=80_636,
        valor_actual=80_636,
        valor_nuevo=80_636,
        aplica_capitanes=True,
        aplica_primer_oficial=False,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Sexta letra k) — $80.636 brutos por vuelo",
        nota_operacional="Por vuelo de instrucción efectivo. Para costear, ingresar número estimado de vuelos de instrucción al año.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 7. BONO FERIADO LEGAL — Cláusula Séptima N°4
    # 3.33% de remuneración por día de vacaciones, máx 15 días/año
    # ─────────────────────────────────────────────────────────────────

    variables.append(VariableContrato(
        nombre="Bono Feriado Legal (3.33%/día vacaciones, máx 15 días/año)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.ANUAL,
        valor_libro=444_503,
        valor_actual=444_503,
        valor_nuevo=444_503,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Séptima N°4",
        nota_operacional="Valor libro = 3.33% × $8.862.076 × 15 días = $443.103 (CAP Nivel A). Ajustar por nivel y horas promedio.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 8. SALA CUNA — Cláusula Duodécima
    # ─────────────────────────────────────────────────────────────────

    variables.append(VariableContrato(
        nombre="Sala Cuna (máx $242.856 mensual por trabajadora con hijo <2 años)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=242_856,
        valor_actual=242_856,
        valor_nuevo=242_856,
        aplica_capitanes=False,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Duodécima N°2.2.3 — $242.856 brutos mensuales máximo",
        nota_operacional="Solo trabajadoras con hijos menores de 2 años. Ajustar número de beneficiarias en dotación.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 9. COMPENSACIONES DE JORNADA — Cláusula Tercera
    # ─────────────────────────────────────────────────────────────────

    variables.append(VariableContrato(
        nombre="Bono Turno en Exceso (2.5%/turno sobre 3 al mes)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.EVENTO,
        valor_libro=221_552,
        valor_actual=221_552,
        valor_nuevo=221_552,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Tercera I, N°6 — 2.5% de remuneración por turno adicional",
        nota_operacional="Valor libro = 2.5% × $8.862.076 (CAP Nivel A). Los primeros 3 turnos/mes no generan pago. A partir del 4° turno se paga por cada uno.",
    ))

    variables.append(VariableContrato(
        nombre="Bono Secuencia 9-10 Días Consecutivos (3.3% por evento)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.EVENTO,
        valor_libro=292_448,
        valor_actual=292_448,
        valor_nuevo=292_448,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Tercera I, N°7 — 3.3% remuneración por cada secuencia",
        nota_operacional="Valor libro = 3.3% × $8.862.076 (CAP Nivel A). Solo aplica a vuelos en aviones cargueros.",
    ))

    variables.append(VariableContrato(
        nombre="Compensación Feriado Trabajado (6.6% remuneración por día)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.EVENTO,
        valor_libro=584_897,
        valor_actual=584_897,
        valor_nuevo=584_897,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Tercera I, N°8 — 6.6% remuneración por día feriado trabajado",
        nota_operacional="Valor libro = 6.6% × $8.862.076 (CAP Nivel A). En Chile hay ~15 días feriados anuales.",
    ))

    variables.append(VariableContrato(
        nombre="Compensación Noches Fuera de Base (3.33%/noche 17 y 18)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.EVENTO,
        valor_libro=295_107,
        valor_actual=295_107,
        valor_nuevo=295_107,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Tercera I, N°9 — 3.33% remuneración por noche 17 y 18",
        nota_operacional="Valor libro = 3.33% × $8.862.076. Solo aplica a partir de la noche 17 fuera de base (máx noche 18). Opera principalmente en rutas largas.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 10. LIBRES AFECTADOS — Cláusula Octava
    # ─────────────────────────────────────────────────────────────────

    variables.append(VariableContrato(
        nombre="Compensación Libre Tocado (3.3% remuneración por evento)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.EVENTO,
        valor_libro=292_448,
        valor_actual=292_448,
        valor_nuevo=292_448,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Octava N°2 — 3.3% remuneración por PSV que toca día libre",
        nota_operacional="Valor libro = 3.3% × $8.862.076. Frecuencia típica LAN Cargo carguero: 1-2 eventos/mes por piloto en rutas largas.",
    ))

    variables.append(VariableContrato(
        nombre="Compensación Libre Tocado Bloque 106h — PSV desde 04:00 (5%)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.EVENTO,
        valor_libro=443_104,
        valor_actual=443_104,
        valor_nuevo=443_104,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Octava N°2.3.1.3 — 5% cuando PSV termina desde las 04:00 del bloque 106h",
        nota_operacional="Valor libro = 5% × $8.862.076. Se activa cuando el vuelo termina a partir de las 04:00 del primer día del bloque de descanso mensual.",
    ))

    variables.append(VariableContrato(
        nombre="Viático Festivos Especiales — 24 y 31 dic (USD$100 por día)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.EVENTO,
        valor_libro=100,
        valor_actual=100,
        valor_nuevo=100,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        unidad="USD",
        clausula_referencia="Cláusula Octava N°1 — USD$100 por día (24 y/o 31 dic) fuera de base",
        nota_operacional="USD 100 por cada día festivo especial operando fuera de base. Máximo 2 eventos/año.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 11. BONIFICACIÓN INCAPACIDAD LABORAL — Cláusula Décimo Octava
    # ─────────────────────────────────────────────────────────────────

    variables.append(VariableContrato(
        nombre="Bonificación Incapacidad Laboral (diferencia subsidio-remuneración)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.EVENTO,
        valor_libro=296_000,
        valor_actual=296_000,
        valor_nuevo=296_000,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Décimo Octava",
        nota_operacional="Empresa paga diferencia entre subsidio (~60% remuneración) y remuneración líquida diaria. Valor libro estimado = 40% diferencia × remuneración diaria CAP. Ajustar según días promedio de licencia al año.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 12. SEGUROS — Cláusula Vigésima
    # ─────────────────────────────────────────────────────────────────

    variables.append(VariableContrato(
        nombre="Seguro Catastrófico de Salud (UF 35.000/beneficiario, deducible UF 100)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.ANUAL,
        valor_libro=180_000,
        valor_actual=180_000,
        valor_nuevo=180_000,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Vigésima N°1 — Prima pagada por la empresa",
        nota_operacional="Prima anual referencial estimada. Ingresar el valor real de la prima negociada con la aseguradora.",
    ))

    variables.append(VariableContrato(
        nombre="Seguro de Vida (UF 2.500 muerte natural / UF 5.000 accidental)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.ANUAL,
        valor_libro=60_000,
        valor_actual=60_000,
        valor_nuevo=60_000,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Vigésima N°2 — Prima pagada por la empresa",
        nota_operacional="Prima anual referencial estimada. Ingresar valor real.",
    ))

    variables.append(VariableContrato(
        nombre="Seguro Accidente de Aviación (USD$75.000 / USD$100.000 ferry)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.ANUAL,
        valor_libro=120_000,
        valor_actual=120_000,
        valor_nuevo=120_000,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Vigésima N°3 — Prima pagada por la empresa",
        nota_operacional="Prima anual referencial estimada. Ingresar valor real.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 13. BONO GESTIÓN ANUAL — Cláusula Vigésima Primera
    # ─────────────────────────────────────────────────────────────────

    variables.append(VariableContrato(
        nombre="Bono Gestión Anual (target 2 remuneraciones, pagado en marzo)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.ANUAL,
        valor_libro=17_724_152,
        valor_actual=17_724_152,
        valor_nuevo=17_724_152,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        tramos_antiguedad={
            "Capitán Nivel A":  17_724_152,
            "Capitán Nivel B":  17_042_454,
            "FO Nivel A":       10_634_490,
            "FO Nivel B":       10_225_472,
        },
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Vigésima Primera — Target 2 remuneraciones, pagado en marzo",
        nota_operacional="Valor libro = 2 × sueldo base CAP Nivel A. Condicional: sin accidentes LATAM + utilidades + metas Safety/OTP/Fuel. Ajustar probabilidad de pago según expectativa.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 14. VIÁTICOS — Cláusula Vigésima Segunda
    # ─────────────────────────────────────────────────────────────────

    variables.append(VariableContrato(
        nombre="Viáticos Américas (USD$65/día fuera de base)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.EVENTO,
        valor_libro=65,
        valor_actual=65,
        valor_nuevo=65,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        unidad="USD",
        clausula_referencia="Cláusula Vigésima Segunda — USD$65 Américas / USD$70 NY / USD$80 Europa / USD$85 África-Asia",
        nota_operacional="No constituye remuneración. Para costear, ingresar noches promedio fuera de base por piloto al mes.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 15. INCREMENTO REAL — Cláusula Vigésima Séptima N°1
    # ─────────────────────────────────────────────────────────────────

    variables.append(VariableContrato(
        nombre="Incremento Real (1% ene-2024, 1% ago-2024, 1% ago-2025, 1% ago-2026)",
        tipo=TipoVariable.INCREMENTO,
        recurrencia=Recurrencia.ANUAL,
        valor_libro=1.0,
        valor_actual=1.0,
        valor_nuevo=1.0,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        unidad="%",
        clausula_referencia="Cláusula Vigésima Séptima N°1 — Aplica sobre sueldo base y valor de horas",
        nota_operacional="4 cuotas de 1% cada una. Adicional al IPC semestral. Aplica solo sobre sueldo base (Cláusula 4 N°1) y componente variable HBT (N°2). El IPC está excluido del costeo.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 16. BONO ITP — Cláusula Vigésima Séptima N°3 (ONE-TIME)
    # ─────────────────────────────────────────────────────────────────

    variables.append(VariableContrato(
        nombre="Bono ITP — Instrucción Periódica Terrestre (one-time, ene-2024)",
        tipo=TipoVariable.BONO_ONE_TIME,
        recurrencia=Recurrencia.ONE_TIME,
        valor_libro=2_625_000,
        valor_actual=2_625_000,
        valor_nuevo=2_625_000,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        tramos_antiguedad={
            "Capitán":         2_625_000,
            "Primer Oficial":  1_575_000,
        },
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Vigésima Séptima N°3 — Pagado en enero 2024, no reajustable",
        nota_operacional="Ya pagado en enero 2024. Se incluye como referencia histórica para cálculo punta a punta. No se repite durante la vigencia del contrato.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 17. BONO TÉRMINO NEGOCIACIÓN — Cláusula Vigésima Séptima N°2 (ONE-TIME)
    # ─────────────────────────────────────────────────────────────────

    variables.append(VariableContrato(
        nombre="Bono Término Negociación Colectiva (one-time, oct-2023)",
        tipo=TipoVariable.BONO_ONE_TIME,
        recurrencia=Recurrencia.ONE_TIME,
        valor_libro=17_724_152,
        valor_actual=17_724_152,
        valor_nuevo=17_724_152,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        tramos_antiguedad={
            "Capitán Nivel A (2 rem)":  17_724_152,
            "Capitán Nivel B (2 rem)":  17_042_454,
            "FO Nivel A (2 rem)":       10_634_490,
            "FO Sub-C (2 rem +25%)":    9_520_000,
        },
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Vigésima Séptima N°2 — 2 remuneraciones, pagado oct 2023",
        nota_operacional="Ya pagado en octubre 2023. Incluido como referencia. Valor libro = 2 × sueldo base CAP Nivel A. No forma parte del piso de la próxima negociación.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 18. INDEMNIZACIONES — Cláusula Décimo Quinta
    # ─────────────────────────────────────────────────────────────────

    variables.append(VariableContrato(
        nombre="Indemnización por Años de Servicio (30 días/año, tope 330 días)",
        tipo=TipoVariable.INDEMNIZACION,
        recurrencia=Recurrencia.ONE_TIME,
        valor_libro=None, valor_actual=None, valor_nuevo=None,
        aplica_capitanes=True, aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Décimo Quinta N°1",
        nota_operacional="Declarada. No se costea. 30 días × años de servicio, tope 330 días. Sin tope UF 90. Base de cálculo: Cláusula Cuarta N°5.",
    ))

    variables.append(VariableContrato(
        nombre="Indemnización por Pérdida de Licencia de Vuelo (12 meses adicionales)",
        tipo=TipoVariable.INDEMNIZACION,
        recurrencia=Recurrencia.ONE_TIME,
        valor_libro=None, valor_actual=None, valor_nuevo=None,
        aplica_capitanes=True, aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Décimo Quinta N°4",
        nota_operacional="Declarada. No se costea. Mantención contrato 12 meses o indemnización adicional equivalente.",
    ))

    variables.append(VariableContrato(
        nombre="Indemnización Fallecimiento / Renuncia desde 60 años",
        tipo=TipoVariable.INDEMNIZACION,
        recurrencia=Recurrencia.ONE_TIME,
        valor_libro=None, valor_actual=None, valor_nuevo=None,
        aplica_capitanes=True, aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Décimo Quinta N°2",
        nota_operacional="Declarada. No se costea. Mismas condiciones N°1, aplica por fallecimiento o renuncia voluntaria desde los 60 años.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 19. VARIABLES OPERACIONALES — Cláusulas Tercera y Octava
    # ─────────────────────────────────────────────────────────────────

    variables.append(VariableContrato(
        nombre="[OPERACIONAL] Restricción Zona Roja (máx 2 noches consecutivas 00:30-05:30)",
        tipo=TipoVariable.OPERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=2, valor_actual=2, valor_nuevo=2,
        aplica_capitanes=True, aplica_primer_oficial=True,
        unidad="noches", aplica_incremento_real=False,
        clausula_referencia="Cláusula Tercera I, N°5",
        nota_operacional="Máximo 2 noches consecutivas en Zona Roja (00:30-05:30). Limita eficiencia en rutas cargueras nocturnas (GRU, EZE, MIA). Estimación: reduce disponibilidad nocturna ~30-40%. En 112 pilotos, equivale a necesitar 3-5 pilotos adicionales para misma operación nocturna.",
    ))

    variables.append(VariableContrato(
        nombre="[OPERACIONAL] Turno/Retén (máx 12h, 3 turnos/mes sin costo adicional)",
        tipo=TipoVariable.OPERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=3, valor_actual=3, valor_nuevo=3,
        aplica_capitanes=True, aplica_primer_oficial=True,
        unidad="turnos", aplica_incremento_real=False,
        clausula_referencia="Cláusula Tercera I, N°6",
        nota_operacional="3 turnos/mes incluidos sin pago. A partir del 4° turno se paga 2.5%/turno. Cada punto porcentual de dotación en standby adicional ≈ 1 piloto más.",
    ))

    variables.append(VariableContrato(
        nombre="[OPERACIONAL] Descanso 106h Mensual (bloque obligatorio con sáb-dom)",
        tipo=TipoVariable.OPERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=106, valor_actual=106, valor_nuevo=106,
        aplica_capitanes=True, aplica_primer_oficial=True,
        unidad="horas", aplica_incremento_real=False,
        clausula_referencia="Cláusula Octava (Art. 152 ter K Código del Trabajo)",
        nota_operacional="106h continuas de descanso mensual obligatorio (incluye sáb-dom). Bloquea ~14.7% del mes. Estimación: obliga a mantener ~15% de buffer adicional de dotación para operación carguera continua.",
    ))

    variables.append(VariableContrato(
        nombre="[OPERACIONAL] Publicación Rol (día 25 mes anterior, inmodificable 60 días antes vacaciones)",
        tipo=TipoVariable.OPERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=25, valor_actual=25, valor_nuevo=25,
        aplica_capitanes=True, aplica_primer_oficial=True,
        unidad="días", aplica_incremento_real=False,
        clausula_referencia="Cláusula Tercera I, N°1 y Séptima N°1",
        nota_operacional="Rol publicado el día 25. Vacaciones inmodificables con 60 días de anticipación. Reduce flexibilidad de programación y aumenta necesidad de standby.",
    ))

    variables.append(VariableContrato(
        nombre="[OPERACIONAL] Bloqueo Simulador Post-Vacaciones (5 días corridos)",
        tipo=TipoVariable.OPERACIONAL,
        recurrencia=Recurrencia.ANUAL,
        valor_libro=5, valor_actual=5, valor_nuevo=5,
        aplica_capitanes=True, aplica_primer_oficial=True,
        unidad="días", aplica_incremento_real=False,
        clausula_referencia="Cláusula Séptima N°3",
        nota_operacional="No se puede programar simulador en los 5 días después de vacaciones ≥10 días hábiles. Con 112 pilotos en temporada alta puede bloquear ~10-15% capacidad de simulador.",
    ))

    variables.append(VariableContrato(
        nombre="[OPERACIONAL] Regreso de Descanso (no antes de 06:00 post día libre)",
        tipo=TipoVariable.OPERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=6, valor_actual=6, valor_nuevo=6,
        aplica_capitanes=True, aplica_primer_oficial=True,
        unidad="horas", aplica_incremento_real=False,
        clausula_referencia="Cláusula Tercera I, N°4",
        nota_operacional="No se puede iniciar PSV antes de las 06:00 después de un día libre (excepción: lunes post domingo desde 03:00). Impacta principalmente rutas nocturnas a GRU y EZE.",
    ))

    return variables
