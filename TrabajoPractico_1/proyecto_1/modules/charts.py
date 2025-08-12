import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np
from datetime import datetime
import os
from typing import List, Dict, Tuple
import io
import base64

# Configurar estilo de las gráficas
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class GameCharts:
    def __init__(self, charts_dir: str = "static/charts"):
        self.charts_dir = charts_dir
        os.makedirs(charts_dir, exist_ok=True)
        
    def _parse_score(self, score_str: str) -> Tuple[int, int]:
        """Convierte un string de puntuación '3/5' en tupla (aciertos, total)"""
        try:
            aciertos, total = map(int, score_str.split('/'))
            return aciertos, total
        except:
            return 0, 0
    
    def _prepare_data_for_line_chart(self, games: List[Dict]) -> Tuple[List, List, List]:
        """Prepara los datos para la gráfica de líneas"""
        dates = []
        aciertos = []
        desaciertos = []
        
        for game in games:
            try:
                # Parsear fecha
                date_obj = datetime.strptime(game['start_time'], '%d/%m/%y %H:%M')
                dates.append(date_obj)
                
                # Parsear puntuación
                aciertos_count, total = self._parse_score(game['score'])
                desaciertos_count = total - aciertos_count
                
                aciertos.append(aciertos_count)
                desaciertos.append(desaciertos_count)
                
            except Exception as e:
                print(f"Error procesando juego: {e}")
                continue
        
        return dates, aciertos, desaciertos
    
    def _prepare_data_for_pie_chart(self, games: List[Dict]) -> Tuple[int, int]:
        """Prepara los datos para la gráfica circular"""
        total_aciertos = 0
        total_desaciertos = 0
        
        for game in games:
            aciertos_count, total = self._parse_score(game['score'])
            total_aciertos += aciertos_count
            total_desaciertos += (total - aciertos_count)
        
        return total_aciertos, total_desaciertos
    
    def generate_line_chart(self, games: List[Dict]) -> str:
        """Genera gráfica de líneas de aciertos y desaciertos por fecha"""
        if not games:
            return None
            
        dates, aciertos, desaciertos = self._prepare_data_for_line_chart(games)
        
        if not dates:
            return None
        
        # Crear figura
        plt.figure(figsize=(12, 8))
        
        # Gráfica de líneas
        plt.plot(dates, aciertos, 'o-', linewidth=2, markersize=6, 
                label='Aciertos', color='#2E8B57', alpha=0.8)
        plt.plot(dates, desaciertos, 's-', linewidth=2, markersize=6, 
                label='Desaciertos', color='#DC143C', alpha=0.8)
        
        # Configurar eje X (fechas)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.xticks(rotation=45)
        
        # Configurar ejes y título
        plt.ylabel('Cantidad', fontsize=12, fontweight='bold')
        plt.xlabel('Fecha de Juego', fontsize=12, fontweight='bold')
        plt.title('Evolución de Aciertos y Desaciertos por Fecha', 
                 fontsize=14, fontweight='bold', pad=20)
        
        # Configurar leyenda
        plt.legend(fontsize=11, loc='upper right')
        plt.grid(True, alpha=0.3)
        
        # Ajustar layout
        plt.tight_layout()
        
        # Guardar gráfica
        chart_path = os.path.join(self.charts_dir, 'line_chart.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close()
        
        return chart_path
    
    def generate_pie_chart(self, games: List[Dict]) -> str:
        """Genera gráfica circular de aciertos y desaciertos acumulados"""
        if not games:
            return None
            
        total_aciertos, total_desaciertos = self._prepare_data_for_pie_chart(games)
        
        if total_aciertos == 0 and total_desaciertos == 0:
            return None
        
        # Crear figura
        plt.figure(figsize=(10, 8))
        
        # Datos para la gráfica
        sizes = [total_aciertos, total_desaciertos]
        labels = [f'Aciertos\n({total_aciertos})', f'Desaciertos\n({total_desaciertos})']
        colors = ['#2E8B57', '#DC143C']
        explode = (0.05, 0.05)  # Separar ligeramente las secciones
        
        # Gráfica circular
        wedges, texts, autotexts = plt.pie(sizes, explode=explode, labels=labels, 
                                          colors=colors, autopct='%1.1f%%',
                                          startangle=90, shadow=True)
        
        # Configurar texto
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        for text in texts:
            text.set_fontsize(12)
            text.set_fontweight('bold')
        
        # Título
        plt.title('Distribución Total de Aciertos y Desaciertos', 
                 fontsize=14, fontweight='bold', pad=20)
        
        # Ajustar layout
        plt.tight_layout()
        
        # Guardar gráfica
        chart_path = os.path.join(self.charts_dir, 'pie_chart.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close()
        
        return chart_path
    
    def generate_charts(self, games: List[Dict]) -> Dict[str, str]:
        """Genera ambas gráficas y retorna las rutas"""
        line_chart_path = self.generate_line_chart(games)
        pie_chart_path = self.generate_pie_chart(games)
        
        return {
            'line_chart': line_chart_path,
            'pie_chart': pie_chart_path
        }
    
    def get_chart_url(self, chart_path: str) -> str:
        """Convierte la ruta del archivo en URL para Flask"""
        if chart_path and os.path.exists(chart_path):
            filename = os.path.basename(chart_path)
            return f'/static/charts/{filename}'
        return None
