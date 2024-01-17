import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# Crear el DataFrame en Streamlit
data = {
    'Columna 1': range(1, 21),
    'Columna 2': range(21, 41),
    'Columna 3': range(41, 61),
    'Columna 4': range(61, 81),
    'Columna 5': range(81, 101),
    'Columna 6': range(101, 121),
    'Columna 7': range(121, 141)
}

df = pd.DataFrame(data)

# Mostrar el DataFrame en Streamlit
st.dataframe(df)

# Generar PDF con el DataFrame y fecha/hora como título
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Obtener fecha y hora actual para el título
now = datetime.now()
fecha_hora = now.strftime("%Y-%m-%d %H")

pdf.set_title(f"DataFrame - {fecha_hora}")

# Escribir el título en el PDF
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, txt=f"DataFrame - {fecha_hora}", ln=True, align="C")
pdf.ln(10)

# Obtener anchos de columna dinámicos basados en el contenido
col_widths = []
for col in df.columns:
    col_widths.append(pdf.get_string_width(col) -2 )  # Ancho de cada columna basado en el encabezado

for _, row in df.iterrows():
    for i, value in enumerate(row):
        cell_width = pdf.get_string_width(str(value)) -2   # Ancho de celda basado en el contenido
        if cell_width > col_widths[i]:
            col_widths[i] = cell_width  # Si el ancho de la celda es mayor, ajustar el ancho de columna

# Agregar el DataFrame al PDF con líneas de tabla y celdas ajustadas al contenido
pdf.set_font("Arial", size=10)
for i, col in enumerate(df.columns):
    pdf.cell(col_widths[i], 10, str(col), border=1, align='C')
pdf.ln()

pdf.set_font("Arial", size=8)
for _, row in df.iterrows():
    for i, value in enumerate(row):
        pdf.cell(col_widths[i], 10, str(value), border=1, align='C')
    pdf.ln()

# Guardar el PDF
pdf_output = f"DataFrame_{fecha_hora}.pdf"
pdf.output(pdf_output)
st.success(f"Se ha generado el PDF: {pdf_output}")
