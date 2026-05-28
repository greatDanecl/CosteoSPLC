# ✈️ Simulador de Costo — Contrato Colectivo Pilotos

Herramienta interna para sensibilización de costos de negociación colectiva en aerolíneas chilenas.

## Funcionalidades

- 📄 Lectura automática de contratos colectivos en PDF (texto seleccionable)
- 🔍 Identificación automática de variables remuneracionales y operacionales
- ✏️ Edición de **Valor Libro** / **Valor Actual** / **Nuevo Valor** por variable
- 👥 Dotación por cargo (Capitán / Primer Oficial) y tramo de antigüedad
- 📊 Cálculo de costo actual vs. nuevo, año a año (máx. 36 meses)
- 📈 Cuadro punta a punta y gráficos de sensibilización
- ⚙️ Estimación de efecto en headcount para variables operacionales

## Reglas de negocio

- **IPC**: descartado del costeo (costo hundido)
- **Incremento real**: se aplica anualmente sobre conceptos definidos en el contrato
- **Bono de término de negociación**: one-time, excluido del cálculo anual recurrente
- **Indemnizaciones por año de servicio**: declaradas pero no costeadas

## Instalación local

```bash
git clone https://github.com/TU_USUARIO/contrato-colectivo.git
cd contrato-colectivo
pip install -r requirements.txt
streamlit run app.py
```

## Deploy en Streamlit Cloud

1. Sube el repositorio a GitHub (puede ser privado)
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu cuenta de GitHub
4. Selecciona el repositorio y el archivo `app.py`
5. Click en **Deploy**

La app estará disponible en `https://TU_APP.streamlit.app`

## Estructura del proyecto

```
contrato-colectivo/
├── app.py                  # App principal Streamlit
├── requirements.txt        # Dependencias Python
├── .streamlit/
│   └── config.toml         # Configuración de tema
└── src/
    ├── extractor.py         # Extracción de variables desde PDF
    └── calculadora.py       # Motor de cálculo de costos
```

## Variables detectadas automáticamente

### Remuneracionales
- Bonos (producción, turno, zona, antigüedad, etc.)
- Asignaciones (colación, movilización, viáticos, etc.)
- Gratificaciones
- Premios
- Horas extras

### Operacionales (con estimación de efecto en headcount)
- Períodos de descanso / días libres
- Límites FDP y horas de vuelo
- Standby y disponibilidad
- Horarios bloqueados para operación
- Rotaciones y turnos

### Especiales
- Incremento real de remuneraciones (% anual)
- Bono de término de negociación (one-time)
- Indemnizaciones por año de servicio (declarado, no costeado)

## Parámetros de referencia — Industria aérea Chile

| Parámetro | Valor |
|---|---|
| Horas vuelo/mes capitán | 75 h |
| Horas vuelo/mes primer oficial | 80 h |
| FDP máximo (DAN 91) | 12 h |
| Días de servicio/mes | 20 |
| Ratio de reserva | 15% |
