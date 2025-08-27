from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from io import BytesIO
from django.db.models import Count, Avg
from .models import User, Career
from django.utils import timezone

#REPORTE CON XHTML2PDF - REPORTE DE TODOS LOS USUARIOS

# Función para insertar saltos de línea en emails largos
def break_long_words(text, max_len=20):
    #si el texto esta vacioo es None, retorna un string vacio
    if not text:
        return ''
    return ''.join(text[i:i+max_len] + ' ' for i in range(0, len(text), max_len))

def all_users_pdf_report(request):
    try:
        #obtener todos los usuarios
        users = User.objects.all().select_related('career').prefetch_related('clubs')
        
        # Procesar cada email para insertar saltos de línea
        for u in users:
            u.email_wrapped = break_long_words(u.email)

        # Contexto para usar en html
        context = {
            'users': users,
            'title': 'Reporte general de estudiantes',
            'generation_date': timezone.now().strftime('%d/%m/%Y'),
            'total_users': users.count(),
            'users_with_career': users.filter(career__isnull=False).count(),
            'users_without_career': users.filter(career__isnull=True).count(),
        }

        #Convierte el template html en string
        html_string = render_to_string('institute/reports/all_users_report.html', context)
        
        #Crea la respuesta http como pdf adjunto
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_general_estudiantes.pdf"'
        
        #general el pdf, convierte el html a pdf y lo guarda en response
        pisa_status = pisa.CreatePDF(html_string, dest=response, encoding='UTF-8')
        
        #verifica errores
        if pisa_status.err:
            return HttpResponse('Error al generar el PDF. Revisa consola para detalles.')
        
        #devuelve el pdf como response
        return response
        
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}')



#REPORTE CON REPORTLAB - REPORTE DE ESTUDIANTES POR CARRERA

def career_users_report(request):
    try:
        #Crear buffer para el pdf
        buffer = BytesIO()
        #almacena el pdf en memoria antes de enviarlo
        doc = SimpleDocTemplate(buffer, pagesize=A4)

        #lista vacia donde se almacenaran los elementos del pdf
        elements =[]

        #estilos
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1,  # Centrado
            textColor=colors.HexColor('#400147')
        )

        header_style = ParagraphStyle(
            'HeaderStyle',
            parent=styles['Heading2'],
            fontSize=12,
            spaceAfter=10,
            textColor=colors.HexColor('#2F1C4F')
        )

        #titulo de reporte
        elements.append(Paragraph('Reporte para estudiantes por carrera', title_style))
        elements.append(Paragraph(f'Generado el: {timezone.now().strftime("%d/%m/%Y")}', styles['Normal']))
        elements.append(Spacer(1, 20))

        #resumen general
        total_users= User.objects.count()
        users_with_career = User.objects.filter(career__isnull=False).count()
        users_without_career = User.objects.filter(career__isnull=True).count()

        summary_data = [
            ['Total de estudiantes', str(total_users)],
            ['Estudiantes con carrera asignada', str(users_with_career)],
            ['Estudiantes sin carrera asignada', str(users_without_career)]
        ]

        #crea una tabla para el resumen
        summary_table = Table(summary_data, colWidths=[200, 100])
        #estilos de la tabla
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2F1C4F')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        #agrega la tabla al documento
        elements.append(summary_table)
        elements.append(Spacer(1, 30))

        #Datos por carrera
        for career in Career.objects.all():
            users = career.user_set.all().select_related('career').prefetch_related('clubs')

            #si no hay usuarios en la carrera, salta a la siguiente
            if not users.exists():
                continue

            #encabezado de la carrera
            elements.append(Paragraph(f'Carrera: {career.name}', header_style))

            #estadisticas de la carrera, calcula total de usuarios y edad promedio
            stats = users.aggregate(
                total=Count('id'),
                avg_age=Avg('age')
            )

            avg_age = stats['avg_age'] or 0 # Manejo de None, si es None, asigna 0
            stats_text = f"Total de estudiantes: {stats['total']} | Edad promedio: {avg_age:.1f} años"

            #agrega las estadisticas al documento
            elements.append(Paragraph(stats_text, styles['Normal']))
            elements.append(Spacer(1, 10))

            #tabla de usuarios
            user_data = [['Nombre', 'Apellido', 'Edad', 'Email', 'Clubes']]

            #llenar datos de usuarios
            for i, user in enumerate(users, 1):
                # Obtener y formatear los nombres de los clubes
                clubs = ', '.join([club.name for club in user.clubs.all()]) or 'Sin clubes'

                user_data.append([
                    user.first_name,
                    user.last_name,
                    str(user.age),
                    user.email,
                    clubs
                ])

            #crear tabla
            table = Table(user_data, colWidths=[80, 80, 40, 150, 100])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2F1C4F')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))

            elements.append(table)
            elements.append(Spacer(1, 20))

        #Estudiantes sin carrera
        users_no_career = User.objects.filter(career__isnull=True).select_related('career').prefetch_related('clubs')
        if users_no_career.exists():
            #encabezado para estudiantes sin carrera
            elements.append(Paragraph('Estudiantes sin carrera asignada', header_style))
            elements.append(Spacer(1, 10))

            no_career_data = [['Nombre', 'Apellido', 'Edad', 'Email', 'Clubes']]

            #llenar datos de estudiantes sin carrera
            for i, user in enumerate(users_no_career, 1):
                no_career_data.append([
                    user.first_name,
                    user.last_name,
                    str(user.age),
                    user.email
                    , ', '.join([club.name for club in user.clubs.all()]) or 'Sin clubes'
                ])
            
            #crear tabla para estudiantes sin carrera
            table = Table(no_career_data, colWidths=[80, 80, 40, 150])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2F1C4F')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))

            #agrega la tabla al documento
            elements.append(table)
        
        #GENERAR PDF
        doc.title = "Reporte de Estudiantes por Carrera"
        doc.author = "Instituto"

        # Construye el PDF
        doc.build(elements)

        #crea respuesta http que contenddra un pdf
        response = HttpResponse(content_type='application/pdf')

        #lo descarga como archivo e indica el nombre del pdf
        response['Content-Disposition'] = 'attachment; filename="reporte_estudiantes_por_carrera.pdf"'

        #obtiene el contenido de buffer como bytes y response.write escribe esos bytes en la respuesta http
        response.write(buffer.getvalue())
        #cierra el buffer para liberar memoria
        buffer.close()

        return response
    
    except Exception as e:
        return HttpResponse(f'Error al generar el reporte: {str(e)}')