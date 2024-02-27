import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from io import BytesIO

# Función para exportar DataFrame a PDF
def export_to_pdf(df):
    # Crear un objeto BytesIO para almacenar el PDF
    pdf_buffer = BytesIO()
    # Crear un objeto SimpleDocTemplate para el PDF
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    # Obtener estilos de texto predefinidos
    styles = getSampleStyleSheet()

    # Convertir DataFrame a lista de listas para la tabla
    data = [df.columns.tolist()]  # Agregar una fila con los nombres de las variables

    for i, row in df.iterrows():
        # Contador de texto para la primera columna
        first_col_text = str(row[df.columns[0]])
        # Agregar \n cada 20 letras
        first_col_text = '\n'.join([first_col_text[j:j+20] for j in range(0, len(first_col_text), 20)])
        
        row_data = [first_col_text] + [str(row[col]) for col in df.columns[1:]]
        data.append(row_data)

    # Crear la tabla con los datos del DataFrame
    table = Table(data, repeatRows=1)

    # Establecer estilos para la tabla
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear el contenido al centro
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente en negrita para la primera fila (encabezado)
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Agregar espacio inferior a la primera fila
        ('GRID', (0, 0), (-1, -1), 1, 'black'),  # Agregar bordes a la tabla
        ('SPACEAFTER', (0, 0), (-1, -1), 6)  # Espacio después de cada fila
    ]))

    # Construir el PDF con la tabla
    doc.build([table])

    # Obtener el contenido del BytesIO
    pdf_content = pdf_buffer.getvalue()
    # Cerrar el BytesIO
    pdf_buffer.close()

    return pdf_content

# Crear datos de ejemplo
data = {
    'Nombre': ['Juan', 'María', 'Carlos con un texto muy largo que necesita ser dividido en varias líneas'],
    'Edad': [25, 30, 22],
    'Ciudad': ['Ciudad A', 'Ciudad B', 'Ciudad C\nLínea adicional\nOtra línea']
}

# Crear DataFrame a partir de los datos
df = pd.DataFrame(data)

# Configurar Streamlit
st.title('Tabla Exportable a PDF')

# Mostrar la tabla en Streamlit
st.table(df)

# Botón para exportar a PDF y descargar
if st.button('Exportar a PDF y Descargar'):
    # Llamar a la función para exportar DataFrame a PDF
    pdf_content = export_to_pdf(df)
    # Descargar el PDF
    st.download_button('Descargar PDF', pdf_content, file_name='tabla_exportada.pdf', key='download_button')
    # Mensaje de éxito
    st.success('Tabla exportada y PDF descargado exitosamente.')
