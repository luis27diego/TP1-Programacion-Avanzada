from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os
from datetime import datetime
from typing import List, Dict

class GameReportPDF:
    def __init__(self, output_dir: str = "static/reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def _create_title_style(self):
        """Crea estilo para títulos principales"""
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=getSampleStyleSheet()['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        return title_style
    
    def _create_subtitle_style(self):
        """Crea estilo para subtítulos"""
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=getSampleStyleSheet()['Heading2'],
            fontSize=16,
            spaceAfter=20,
            alignment=TA_LEFT,
            textColor=colors.darkgreen
        )
        return subtitle_style
    
    def _create_normal_style(self):
        """Crea estilo para texto normal"""
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=getSampleStyleSheet()['Normal'],
            fontSize=12,
            spaceAfter=12,
            alignment=TA_LEFT
        )
        return normal_style
    
    def _create_table_style(self):
        """Crea estilo para tablas"""
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
        return table_style
    
    def generate_report(self, games: List[Dict], charts_paths: Dict[str, str]) -> str:
        """Genera un reporte PDF completo con gráficas y estadísticas"""
        if not games:
            return None
            
        # Crear nombre del archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reporte_trivia_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Crear documento PDF
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []
        
        # Estilos
        title_style = self._create_title_style()
        subtitle_style = self._create_subtitle_style()
        normal_style = self._create_normal_style()
        table_style = self._create_table_style()
        
        # Título principal
        title = Paragraph("🎬 Reporte de Trivia de Películas", title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Información del reporte
        report_info = f"Generado el: {datetime.now().strftime('%d/%m/%Y a las %H:%M')}"
        info_para = Paragraph(report_info, normal_style)
        story.append(info_para)
        story.append(Spacer(1, 30))
        
        # Resumen ejecutivo
        subtitle1 = Paragraph("📊 Resumen Ejecutivo", subtitle_style)
        story.append(subtitle1)
        
        total_games = len(games)
        unique_players = len(set(game['username'] for game in games))
        
        summary_text = f"""
        Este reporte presenta un análisis completo de la actividad del juego Trivia de Películas.
        
        • Total de partidas jugadas: {total_games}
        • Total de jugadores únicos: {unique_players}
        • Período analizado: Desde el primer juego hasta la fecha actual
        """
        
        summary_para = Paragraph(summary_text, normal_style)
        story.append(summary_para)
        story.append(Spacer(1, 30))
        
        # Gráfica de líneas
        if charts_paths.get('line_chart') and os.path.exists(charts_paths['line_chart']):
            subtitle2 = Paragraph("📈 Evolución de Aciertos y Desaciertos por Fecha", subtitle_style)
            story.append(subtitle2)
            
            line_chart_img = Image(charts_paths['line_chart'], width=7*inch, height=5*inch)
            story.append(line_chart_img)
            story.append(Spacer(1, 20))
            
            line_chart_desc = Paragraph(
                "Esta gráfica muestra la evolución temporal de los aciertos y desaciertos "
                "a lo largo del tiempo, permitiendo identificar tendencias y patrones "
                "en el rendimiento de los jugadores.",
                normal_style
            )
            story.append(line_chart_desc)
            story.append(Spacer(1, 30))
        
        # Gráfica circular
        if charts_paths.get('pie_chart') and os.path.exists(charts_paths['pie_chart']):
            subtitle3 = Paragraph("🥧 Distribución Total de Aciertos y Desaciertos", subtitle_style)
            story.append(subtitle3)
            
            pie_chart_img = Image(charts_paths['pie_chart'], width=6*inch, height=5*inch)
            story.append(pie_chart_img)
            story.append(Spacer(1, 20))
            
            pie_chart_desc = Paragraph(
                "Esta gráfica circular muestra la distribución porcentual total de "
                "aciertos versus desaciertos acumulados por todos los jugadores.",
                normal_style
            )
            story.append(pie_chart_desc)
            story.append(Spacer(1, 30))
        
        # Tabla de resultados recientes
        subtitle4 = Paragraph("📋 Últimos 10 Juegos", subtitle_style)
        story.append(subtitle4)
        
        # Preparar datos de la tabla
        table_data = [['#', 'Jugador', 'Puntuación', 'Frases', 'Fecha']]
        
        # Tomar los últimos 10 juegos
        recent_games = games[-10:] if len(games) > 10 else games
        
        for i, game in enumerate(recent_games, 1):
            table_data.append([
                str(i),
                game['username'],
                game['score'],
                str(game['num_phrases']),
                game['start_time']
            ])
        
        # Crear tabla
        table = Table(table_data, colWidths=[0.5*inch, 1.5*inch, 1*inch, 0.8*inch, 1.2*inch])
        table.setStyle(table_style)
        story.append(table)
        story.append(Spacer(1, 30))
        
        # Estadísticas adicionales
        subtitle5 = Paragraph("📈 Estadísticas Detalladas", subtitle_style)
        story.append(subtitle5)
        
        # Calcular estadísticas
        total_phrases = sum(game['num_phrases'] for game in games)
        total_aciertos = 0
        total_desaciertos = 0
        
        for game in games:
            try:
                aciertos, total = map(int, game['score'].split('/'))
                total_aciertos += aciertos
                total_desaciertos += (total - aciertos)
            except:
                continue
        
        if total_aciertos + total_desaciertos > 0:
            porcentaje_aciertos = (total_aciertos / (total_aciertos + total_desaciertos)) * 100
        else:
            porcentaje_aciertos = 0
        
        stats_text = f"""
        • Total de frases respondidas: {total_phrases}
        • Total de aciertos: {total_aciertos}
        • Total de desaciertos: {total_desaciertos}
        • Porcentaje de aciertos: {porcentaje_aciertos:.1f}%
        • Promedio de frases por partida: {total_phrases/total_games:.1f}
        """
        
        stats_para = Paragraph(stats_text, normal_style)
        story.append(stats_para)
        story.append(Spacer(1, 30))
        
        # Pie de página
        footer = Paragraph(
            "Reporte generado automáticamente por el sistema Trivia de Películas. "
            "Para más información, consulte la aplicación web.",
            normal_style
        )
        story.append(footer)
        
        # Construir PDF
        doc.build(story)
        
        return filepath
    
    def get_report_url(self, report_path: str) -> str:
        """Convierte la ruta del archivo en URL para Flask"""
        if report_path and os.path.exists(report_path):
            filename = os.path.basename(report_path)
            return f'/static/reports/{filename}'
        return None
