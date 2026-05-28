"""
lan_cargo_variables.py
Variables extraídas manualmente del Contrato Colectivo LAN Cargo S.A. 
Vigencia: 01-sep-2023 al 31-ago-2026
"""

from extractor import VariableContrato, TipoVariable, Recurrencia

def cargar_variables_lan_cargo() -> list:
    """Retorna lista de variables del contrato LAN Cargo precargadas."""
    variables = []

    # ─────────────────────────────────────────────────────────────────
    # 1. SUELDOS BASE — Cláusula Cuarta N°1
    # ─────────────────────────────────────────────────────────────────

    # Capitán Wide Body
    variables.append(VariableContrato(
        nombre="Sueldo Base Capitán — Nivel A (≥20 años)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=8_862_076,
        valor_actual=8_862_076,
        valor_nuevo=8_862_076,
        aplica_capitanes=True,
        aplica_primer_oficial=False,
        tramos_antiguedad={"Nivel A (≥20 años)": 8_862_076, "Nivel B (13-19 años)": 8_521_227, "Nivel C (<13 años)": 8_180_376},
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Cuarta, N°1.1",
    ))

    # Primer Oficial (relación laboral previa al 1° mayo 2018)
    variables.append(VariableContrato(
        nombre="Sueldo Base Primer Oficial — Nivel A (≥8 años)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=5_317_245,
        valor_actual=5_317_245,
        valor_nuevo=5_317_245,
        aplica_capitanes=False,
        aplica_primer_oficial=True,
        tramos_antiguedad={"Nivel A (≥8 años)": 5_317_245, "Nivel B (4-7 años)": 5_112_736, "Nivel C (<4 años)": 4_810_841},
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Cuarta, N°1.2.1",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 2. COMPONENTE VARIABLE (Horas de Vuelo) — Cláusula Cuarta N°2
    # Valor referencial: tramo más frecuente (69-78.9 HBT)
    # ─────────────────────────────────────────────────────────────────
    variables.append(VariableContrato(
        nombre="Componente Variable HBT — Capitán Nivel A (69-78.9h)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=1_198_250,
        valor_actual=1_198_250,
        valor_nuevo=1_198_250,
        aplica_capitanes=True,
        aplica_primer_oficial=False,
        tramos_antiguedad={
            "Nivel A (69-78.9h)": 1_198_250,
            "Nivel B (69-78.9h)": 1_152_163,
            "Nivel C (69-78.9h)": 1_106_076,
        },
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Cuarta, N°2.1",
        nota_operacional="Valor referencial para tramo 69-78.9 HBT. Varía según horas voladas.",
    ))

    variables.append(VariableContrato(
        nombre="Componente Variable HBT — Primer Oficial Nivel A (69-78.9h)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=982_706,
        valor_actual=982_706,
        valor_nuevo=982_706,
        aplica_capitanes=False,
        aplica_primer_oficial=True,
        tramos_antiguedad={
            "Nivel A (69-78.9h)": 982_706,
            "Nivel B (69-78.9h)": 944_909,
            "Nivel C (69-78.9h)": 850_419,
        },
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Cuarta, N°2.2",
        nota_operacional="Valor referencial para tramo 69-78.9 HBT.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 3. ASIGNACIÓN DE ANTIGÜEDAD — Cláusula Cuarta N°4
    # ─────────────────────────────────────────────────────────────────
    variables.append(VariableContrato(
        nombre="Asignación de Antigüedad — Capitán (desde año 9, +1%/año, máx 30%)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=None,
        valor_actual=None,
        valor_nuevo=None,
        aplica_capitanes=True,
        aplica_primer_oficial=False,
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Cuarta, N°4.1",
        nota_operacional="1% del promedio de remuneración por año desde el año 9, máx 30%. Calcular según dotación real.",
    ))

    variables.append(VariableContrato(
        nombre="Asignación de Antigüedad — Primer Oficial (desde año 2, escalonada, máx 9%)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=None,
        valor_actual=None,
        valor_nuevo=None,
        aplica_capitanes=False,
        aplica_primer_oficial=True,
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Cuarta, N°4.2",
        nota_operacional="1% año 2, 1.5% año 3, 2% año 4+, máx 9% (25% si no asciende con ≥12 años).",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 4. ASIGNACIONES — Cláusula Sexta
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
        clausula_referencia="Cláusula Sexta, letra b)",
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
        clausula_referencia="Cláusula Sexta, letra c)",
    ))

    variables.append(VariableContrato(
        nombre="Asignación de Matrimonio (primera vez)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.EVENTO,
        valor_libro=94_138,
        valor_actual=94_138,
        valor_nuevo=94_138,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Sexta, letra e)",
        nota_operacional="Pago por evento. Costeo depende de frecuencia real.",
    ))

    variables.append(VariableContrato(
        nombre="Asignación por Hijo Discapacitado (anual por hijo)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.ANUAL,
        valor_libro=430_511,
        valor_actual=430_511,
        valor_nuevo=430_511,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Sexta, letra f)",
        nota_operacional="Se costea por número estimado de beneficiarios. Ingresar N° en dotación.",
    ))

    variables.append(VariableContrato(
        nombre="Asignación Instructor Evaluador (IE) — Mensual",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=1_462_399,
        valor_actual=1_462_399,
        valor_nuevo=1_462_399,
        aplica_capitanes=True,
        aplica_primer_oficial=False,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Sexta, letra g)",
        nota_operacional="Aplica solo mientras el piloto mantenga designación de IE.",
    ))

    variables.append(VariableContrato(
        nombre="Asignación Instructor de Vuelo — Mensual",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=572_102,
        valor_actual=572_102,
        valor_nuevo=572_102,
        aplica_capitanes=True,
        aplica_primer_oficial=False,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Sexta, letra h)",
    ))

    variables.append(VariableContrato(
        nombre="Asignación de Asesor — Mensual",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=746_687,
        valor_actual=746_687,
        valor_nuevo=746_687,
        aplica_capitanes=True,
        aplica_primer_oficial=False,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Sexta, letra j)",
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
        clausula_referencia="Cláusula Sexta, letra k)",
        nota_operacional="Pago por vuelo de instrucción efectivo.",
    ))

    variables.append(VariableContrato(
        nombre="Asignación de Escolaridad — Universitaria/Técnica (por hijo/año)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.ANUAL,
        valor_libro=272_693,
        valor_actual=272_693,
        valor_nuevo=272_693,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Sexta, letra a)",
        nota_operacional="Valores: Parvulario $105.209 / Básica $136.350 / Media $146.450 / Universitaria $272.693.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 5. VACACIONES — Cláusula Séptima
    # ─────────────────────────────────────────────────────────────────
    variables.append(VariableContrato(
        nombre="Bono Feriado Legal (3.33%/día, máx 15 días/año)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.ANUAL,
        valor_libro=None,
        valor_actual=None,
        valor_nuevo=None,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Séptima, N°4",
        nota_operacional="3.33% × remuneración × días de vacaciones efectivos (máx 15 días/año por piloto).",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 6. LIBRES AFECTADOS — Cláusula Octava
    # ─────────────────────────────────────────────────────────────────
    variables.append(VariableContrato(
        nombre="Compensación Libre Tocado (3.3% remuneración por evento)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.EVENTO,
        valor_libro=None,
        valor_actual=None,
        valor_nuevo=None,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Octava, N°2",
        nota_operacional="3.3% de la remuneración por cada período de servicio que toque un día libre. Frecuencia promedio industria: 1-2 veces/mes por piloto.",
    ))

    variables.append(VariableContrato(
        nombre="Compensación Libre Tocado 106h — PSV desde las 04:00 (5% remuneración)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.EVENTO,
        valor_libro=None,
        valor_actual=None,
        valor_nuevo=None,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Octava, N°2.3.1.3",
        nota_operacional="5% de la remuneración cuando PSV termina desde las 04:00 del primer día de bloque 106h.",
    ))

    variables.append(VariableContrato(
        nombre="Viático PSV en Festivos Especiales (24 y 31 dic, USD$100/día)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.EVENTO,
        valor_libro=100,
        valor_actual=100,
        valor_nuevo=100,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        unidad="USD",
        clausula_referencia="Cláusula Octava, N°1",
        nota_operacional="USD 100 por cada día festivo especial (24 y/o 31 diciembre) en que opere fuera de base.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 7. JORNADA — Compensaciones Cláusula Tercera
    # ─────────────────────────────────────────────────────────────────
    variables.append(VariableContrato(
        nombre="Bono Turno en Exceso (>3 turnos/mes, 2.5%/turno adicional)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.EVENTO,
        valor_libro=None,
        valor_actual=None,
        valor_nuevo=None,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Tercera, I, N°6",
        nota_operacional="2.5% de la remuneración por cada turno programado en exceso de 3 en el mes. Base cálculo cláusula 4 N°5.",
    ))

    variables.append(VariableContrato(
        nombre="Bono Secuencia 9-10 Días Consecutivos (3.3% por evento)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.EVENTO,
        valor_libro=None,
        valor_actual=None,
        valor_nuevo=None,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Tercera, I, N°7",
        nota_operacional="3.3% del promedio de remuneración por cada ocurrencia de secuencia de 9 o 10 días continuos de vuelo en carguero.",
    ))

    variables.append(VariableContrato(
        nombre="Compensación Feriado Trabajado (6.6% remuneración por día)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.EVENTO,
        valor_libro=None,
        valor_actual=None,
        valor_nuevo=None,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Tercera, I, N°8",
        nota_operacional="6.6% de la remuneración por cada día feriado efectivamente trabajado.",
    ))

    variables.append(VariableContrato(
        nombre="Compensación Noches Fuera de Base (noche 17 y 18, 3.33%/noche)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.EVENTO,
        valor_libro=None,
        valor_actual=None,
        valor_nuevo=None,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Tercera, I, N°9",
        nota_operacional="3.33% de la remuneración por cada noche fuera de base a partir de la noche 17 (máx noche 18). Opera principalmente en pilotos de carguero con rutas largas.",
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
        clausula_referencia="Cláusula Duodécima, N°2.2.3",
        nota_operacional="Aplica a trabajadoras con hijos menores de 2 años. Ingresar número estimado de beneficiarias.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 9. MOVILIZACIÓN — Cláusula Undécima
    # ─────────────────────────────────────────────────────────────────
    variables.append(VariableContrato(
        nombre="Asignación Mensual Sustitutiva de Movilización",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=205_837,
        valor_actual=205_837,
        valor_nuevo=205_837,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Undécima, N°2",
        nota_operacional="$205.837 líquidos para quienes renuncien a movilización provista. Solo aplica a pilotos que opten por este beneficio.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 10. BONIFICACIÓN POR INCAPACIDAD LABORAL — Cláusula Décimo Octava
    # ─────────────────────────────────────────────────────────────────
    variables.append(VariableContrato(
        nombre="Bonificación por Incapacidad Laboral (diferencia subsidio-remuneración)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.EVENTO,
        valor_libro=None,
        valor_actual=None,
        valor_nuevo=None,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Décimo Octava",
        nota_operacional="Empresa entera diferencia entre subsidio y remuneración líquida diaria. Costo depende de días de licencia médica promedio por año.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 11. SEGUROS — Cláusula Vigésima
    # ─────────────────────────────────────────────────────────────────
    variables.append(VariableContrato(
        nombre="Seguro Catastrófico de Salud (UF 35.000/beneficiario, deducible UF 100)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.ANUAL,
        valor_libro=None,
        valor_actual=None,
        valor_nuevo=None,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Vigésima, N°1",
        nota_operacional="Prima pagada por la empresa. Valor depende de negociación con aseguradora. Ingresar prima anual real.",
    ))

    variables.append(VariableContrato(
        nombre="Seguro de Vida (UF 2.500 muerte natural / UF 5.000 accidental)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.ANUAL,
        valor_libro=None,
        valor_actual=None,
        valor_nuevo=None,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Vigésima, N°2",
        nota_operacional="Prima anual pagada por la empresa. Ingresar valor real de prima.",
    ))

    variables.append(VariableContrato(
        nombre="Seguro Accidente de Aviación (USD$75.000 / USD$100.000 ferry)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.ANUAL,
        valor_libro=None,
        valor_actual=None,
        valor_nuevo=None,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Vigésima, N°3",
        nota_operacional="Prima anual pagada por la empresa. Ingresar valor real.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 12. BONO DE GESTIÓN ANUAL — Cláusula Vigésima Primera
    # ─────────────────────────────────────────────────────────────────
    variables.append(VariableContrato(
        nombre="Bono de Gestión Anual (target 2 remuneraciones, condicional)",
        tipo=TipoVariable.REMUNERACIONAL,
        recurrencia=Recurrencia.ANUAL,
        valor_libro=None,
        valor_actual=None,
        valor_nuevo=None,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=True,
        clausula_referencia="Cláusula Vigésima Primera",
        nota_operacional="Target = 2 remuneraciones. Condicional: sin accidentes LATAM + utilidades + metas Safety/OTP/Fuel. Pagado en marzo. Ingresar valor estimado según expectativa de cumplimiento.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 13. VIÁTICOS — Cláusula Vigésima Segunda
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
        clausula_referencia="Cláusula Vigésima Segunda",
        nota_operacional="USD 65/día en Américas, USD 70 Nueva York, USD 80 Europa, USD 85 África/Asia/Oceanía. No constituye remuneración.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 14. INCREMENTO REAL — Cláusula Vigésima Séptima N°1
    # ─────────────────────────────────────────────────────────────────
    variables.append(VariableContrato(
        nombre="Incremento Real de Remuneraciones (sobre sueldo base y horas)",
        tipo=TipoVariable.INCREMENTO,
        recurrencia=Recurrencia.ANUAL,
        valor_libro=1.0,
        valor_actual=1.0,
        valor_nuevo=1.0,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        unidad="%",
        clausula_referencia="Cláusula Vigésima Séptima, N°1",
        nota_operacional="1% en enero 2024, 1% agosto 2024, 1% agosto 2025, 1% agosto 2026. Aplica sobre sueldo base y valor de horas (Cláusula 4, N°1 y N°2). Adicional al IPC.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 15. BONO ITP — Cláusula Vigésima Séptima N°3 (ONE-TIME)
    # ─────────────────────────────────────────────────────────────────
    variables.append(VariableContrato(
        nombre="Bono ITP (Instrucción Periódica Terrestre) — One-Time 2024",
        tipo=TipoVariable.BONO_ONE_TIME,
        recurrencia=Recurrencia.ONE_TIME,
        valor_libro=2_625_000,
        valor_actual=2_625_000,
        valor_nuevo=2_625_000,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        tramos_antiguedad={"Capitán": 2_625_000, "Primer Oficial": 1_575_000},
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Vigésima Séptima, N°3",
        nota_operacional="Pagado en enero 2024. No reajustable por IPC. Capitán: $2.625.000 / FO: $1.575.000.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 16. BONO TÉRMINO DE NEGOCIACIÓN — Cláusula Vigésima Séptima N°2 (ONE-TIME)
    # ─────────────────────────────────────────────────────────────────
    variables.append(VariableContrato(
        nombre="Bono de Término de Negociación Colectiva — One-Time (oct 2023)",
        tipo=TipoVariable.BONO_ONE_TIME,
        recurrencia=Recurrencia.ONE_TIME,
        valor_libro=None,
        valor_actual=None,
        valor_nuevo=None,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Vigésima Séptima, N°2",
        nota_operacional="2 remuneraciones (sueldo base + antigüedad) vigentes a marzo 2020, actualizadas por IPC. Ya pagado en octubre 2023. Se incluye como referencia histórica.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 17. INDEMNIZACIONES — Cláusula Décimo Quinta
    # ─────────────────────────────────────────────────────────────────
    variables.append(VariableContrato(
        nombre="Indemnización por Años de Servicio (30 días/año, tope 330 días)",
        tipo=TipoVariable.INDEMNIZACION,
        recurrencia=Recurrencia.ONE_TIME,
        valor_libro=None,
        valor_actual=None,
        valor_nuevo=None,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Décimo Quinta, N°1",
        nota_operacional="Declarada. No se costea. 30 días por año de servicio, tope 330 días (post nov-1995). Base cálculo: Cláusula Cuarta N°5.",
    ))

    variables.append(VariableContrato(
        nombre="Indemnización por Pérdida de Licencia de Vuelo (12 meses adicionales)",
        tipo=TipoVariable.INDEMNIZACION,
        recurrencia=Recurrencia.ONE_TIME,
        valor_libro=None,
        valor_actual=None,
        valor_nuevo=None,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Décimo Quinta, N°4",
        nota_operacional="Declarada. No se costea. Mantención contrato 12 meses o indemnización adicional equivalente.",
    ))

    variables.append(VariableContrato(
        nombre="Indemnización por Fallecimiento / Renuncia desde 60 años",
        tipo=TipoVariable.INDEMNIZACION,
        recurrencia=Recurrencia.ONE_TIME,
        valor_libro=None,
        valor_actual=None,
        valor_nuevo=None,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Décimo Quinta, N°2",
        nota_operacional="Declarada. No se costea. Mismas condiciones que N°1, aplica también por fallecimiento o renuncia voluntaria desde los 60 años.",
    ))

    # ─────────────────────────────────────────────────────────────────
    # 18. VARIABLES OPERACIONALES — Cláusula Tercera y Octava
    # ─────────────────────────────────────────────────────────────────
    variables.append(VariableContrato(
        nombre="[OPERACIONAL] Restricción Zona Roja (máx 2 noches consecutivas 00:30-05:30)",
        tipo=TipoVariable.OPERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=2,
        valor_actual=2,
        valor_nuevo=2,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        unidad="noches",
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Tercera, I, N°5",
        nota_operacional="Límite de 2 noches consecutivas en Zona Roja (00:30-05:30). Restricción operacional que limita eficiencia de programación nocturna. Estimación: reduce disponibilidad nocturna ~30-40% para rutas cargueras de largo alcance (EZE, GRU, MIA). En dotación de 50 pilotos, equivale a necesidad de ~3-5 pilotos adicionales para cubrir misma operación nocturna.",
    ))

    variables.append(VariableContrato(
        nombre="[OPERACIONAL] Turno/Retén — máx 12h, máx 3 turnos/mes sin costo",
        tipo=TipoVariable.OPERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=3,
        valor_actual=3,
        valor_nuevo=3,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        unidad="turnos",
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Tercera, I, N°6",
        nota_operacional="3 turnos/mes incluidos. A partir del 4° turno se paga 2.5%/turno. Restricción: turno máx 12h, no consecutivo, no dentro del período de descanso. Estimación headcount: cada turno adicional pagado representa ~2.5% del costo mensual del piloto; si promedio de dotación supera 3 turnos, costo variable mensual aumenta directamente.",
    ))

    variables.append(VariableContrato(
        nombre="[OPERACIONAL] Descanso 106h mensual (bloque mensual obligatorio)",
        tipo=TipoVariable.OPERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=106,
        valor_actual=106,
        valor_nuevo=106,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        unidad="horas",
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Octava (Art. 152 ter K Código del Trabajo)",
        nota_operacional="106 horas continuas de descanso mensual obligatorio (incluye sábado y domingo). Limita la productividad mensual máxima. Estimación: de 720 horas/mes disponibles, ~106h están bloqueadas (14.7%). En operación de carguero con alta frecuencia nocturna, este bloque obliga a mantener ~15% de dotación adicional como buffer de cobertura.",
    ))

    variables.append(VariableContrato(
        nombre="[OPERACIONAL] Publicación Rol de Vuelo (día 25 mes anterior)",
        tipo=TipoVariable.OPERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=25,
        valor_actual=25,
        valor_nuevo=25,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        unidad="días",
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Tercera, I, N°1",
        nota_operacional="Restricción de programación: rol fijo publicado el día 25. Limita flexibilidad para ajustar según demanda operacional. No genera costo directo, pero reduce eficiencia de programación y aumenta necesidad de reserva (standby/turnos). Estimación: cada punto porcentual de reducción en eficiencia de programación equivale a ~1% de dotación adicional.",
    ))

    variables.append(VariableContrato(
        nombre="[OPERACIONAL] Bloqueo de Simulador Post-Vacaciones (5 días)",
        tipo=TipoVariable.OPERACIONAL,
        recurrencia=Recurrencia.ANUAL,
        valor_libro=5,
        valor_actual=5,
        valor_nuevo=5,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        unidad="días",
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Séptima, N°3",
        nota_operacional="La empresa no puede programar simulador en los 5 días corridos después del regreso de vacaciones (≥10 días hábiles). Impacto: retrasa recurrencias de licencia y puede generar cuellos de botella en planificación de simulador. Estimación: con 112 pilotos usando vacaciones en bloques de 2-3 semanas, esto puede bloquear ~10-15% de la capacidad de simulador en temporada alta.",
    ))

    variables.append(VariableContrato(
        nombre="[OPERACIONAL] Regreso de Días de Descanso (no antes de 06:00 post día libre)",
        tipo=TipoVariable.OPERACIONAL,
        recurrencia=Recurrencia.MENSUAL,
        valor_libro=6,
        valor_actual=6,
        valor_nuevo=6,
        aplica_capitanes=True,
        aplica_primer_oficial=True,
        unidad="horas",
        aplica_incremento_real=False,
        clausula_referencia="Cláusula Tercera, I, N°4",
        nota_operacional="No se puede iniciar PSV antes de las 06:00 a continuación de un día libre (excepción: lunes post domingo libre desde 03:00). Restricción de programación nocturna. Estimación: reduce disponibilidad de vuelos nocturnos de madrugada que requieren presentación antes de las 06:00, afectando principalmente rutas a EZE y GRU.",
    ))

    return variables
