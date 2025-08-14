import matplotlib
matplotlib.use('Agg')  # Backend no interactivo para servidores web
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as patches
from matplotlib.patches import Circle, FancyBboxPatch
import seaborn as sns
import numpy as np
from datetime import datetime
import os
from typing import List, Dict, Tuple
import io
import base64

# Configurar estilo moderno con efectos visuales avanzados
plt.style.use('default')
sns.set_style("white")

# Configurar fuentes modernas y elegantes
plt.rcParams['font.family'] = ['SF Pro Display', 'Roboto', 'Helvetica Neue', 'Arial', 'DejaVu Sans']
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 11
plt.rcParams['ytick.labelsize'] = 11
plt.rcParams['legend.fontsize'] = 12

class GameCharts:
    def __init__(self, charts_dir: str = "static/charts"):
        self.charts_dir = charts_dir
        os.makedirs(charts_dir, exist_ok=True)
        
        # Paleta de colores moderna con gradientes y efectos glassmorphism
        self.colors = {
            # Colores principales con gradientes
            'aciertos_primary': '#10B981',      # Verde esmeralda
            'aciertos_secondary': '#34D399',    # Verde claro
            'desaciertos_primary': '#F59E0B',   # Ámbar
            'desaciertos_secondary': '#FBBF24', # Ámbar claro
            'accent': '#8B5CF6',                # Violeta
            'accent_light': '#A78BFA',          # Violeta claro
            
            # Backgrounds y superficies
            'background': '#0F172A',            # Azul oscuro profundo
            'surface': '#1E293B',               # Azul gris oscuro
            'card': '#334155',                  # Azul gris medio
            
            # Texto y elementos
            'text_primary': '#F8FAFC',          # Blanco hueso
            'text_secondary': '#CBD5E1',        # Gris claro
            'text_muted': '#64748B',            # Gris medio
            
            # Elementos de UI
            'border': '#475569',                # Gris azulado
            'grid': '#374151',                  # Gris oscuro
            'shadow': '#000000',                # Negro para sombras
        }
        
        # Configurar tema oscuro moderno
        plt.rcParams['figure.facecolor'] = self.colors['background']
        plt.rcParams['axes.facecolor'] = self.colors['surface']
        plt.rcParams['text.color'] = self.colors['text_primary']
        plt.rcParams['axes.labelcolor'] = self.colors['text_primary']
        plt.rcParams['xtick.color'] = self.colors['text_secondary']
        plt.rcParams['ytick.color'] = self.colors['text_secondary']
        
    def _parse_score(self, score_str: str) -> Tuple[int, int]:
        """Convierte un string de puntuación '3/5' en tupla (aciertos, total)"""
        try:
            aciertos, total = map(int, score_str.split('/'))
            return aciertos, total
        except:
            return 0, 0
    
    def _prepare_data_for_charts(self, games: List[Dict]) -> Tuple[List, List, List, List, List, List]:
        """Prepara los datos para las gráficas con mejor estructura"""
        dates = []
        aciertos = []
        desaciertos = []
        totales = []
        porcentajes = []
        usernames = []
        
        for game in games:
            try:
                # Parsear fecha
                date_obj = datetime.strptime(game['start_time'], '%d/%m/%y %H:%M')
                dates.append(date_obj)
                
                # Obtener nombre de usuario
                username = game.get('username', 'Usuario')
                usernames.append(username)
                
                # Parsear puntuación
                aciertos_count, total = self._parse_score(game['score'])
                desaciertos_count = total - aciertos_count
                
                aciertos.append(aciertos_count)
                desaciertos.append(desaciertos_count)
                totales.append(total)
                
                # Calcular porcentaje de aciertos
                porcentaje = (aciertos_count / total * 100) if total > 0 else 0
                porcentajes.append(porcentaje)
                
            except Exception as e:
                print(f"Error procesando juego: {e}")
                continue
        
        return dates, aciertos, desaciertos, totales, porcentajes, usernames
    
    def _create_gradient_bars(self, ax, x_pos, values, color_start, color_end, width=0.35, alpha=0.9):
        """Crea barras con efecto gradiente"""
        bars = []
        for i, (x, height) in enumerate(zip(x_pos, values)):
            if height > 0:
                # Crear gradiente vertical
                gradient = np.linspace(0, 1, 256).reshape(256, -1)
                gradient = np.hstack((gradient, gradient))
                
                # Crear la barra base
                bar = ax.bar(x, height, width, alpha=alpha, 
                           color=color_start, edgecolor='white', 
                           linewidth=2, capstyle='round')
                bars.extend(bar)
                
                # Agregar efecto de sombra
                shadow = ax.bar(x + 0.01, height, width, alpha=0.3,
                              color='black', zorder=0)
        
        return bars
    
    def _add_glow_effect(self, ax, artist, glow_color, glow_radius=3):
        """Agrega efecto de resplandor a elementos gráficos"""
        for i in range(glow_radius):
            alpha = 0.1 * (glow_radius - i) / glow_radius
            # Implementar efecto de resplandor usando múltiples capas
            pass
    
    def generate_performance_dashboard(self, games: List[Dict]) -> str:
        """Genera un dashboard completo con múltiples visualizaciones"""
        if not games:
            return None
            
        dates, aciertos, desaciertos, totales, porcentajes, usernames = self._prepare_data_for_charts(games)
        
        if not dates:
            return None
        
        # Crear figura principal con diseño de dashboard
        fig = plt.figure(figsize=(20, 14), facecolor=self.colors['background'])
        
        # Configurar grid complejo para dashboard
        gs = fig.add_gridspec(4, 4, height_ratios=[0.5, 2, 1.5, 1], 
                             width_ratios=[1, 1, 1, 1], hspace=0.4, wspace=0.3)
        
        # === HEADER CON TÍTULO Y ESTADÍSTICAS ===
        ax_header = fig.add_subplot(gs[0, :])
        ax_header.set_facecolor(self.colors['background'])
        ax_header.axis('off')
        
        # Título principal con estilo moderno
        fig.suptitle('🎮 DASHBOARD DE RENDIMIENTO - GAME ANALYTICS', 
                    fontsize=24, fontweight='bold', color=self.colors['text_primary'],
                    y=0.95, fontfamily='SF Pro Display')
        
        # Estadísticas rápidas en el header
        total_games = len(games)
        total_questions = sum(totales)
        avg_score = np.mean(porcentajes) if porcentajes else 0
        
        header_text = f"📊 {total_games} Partidas  |  🎯 {total_questions} Preguntas  |  📈 {avg_score:.1f}% Promedio"
        ax_header.text(0.5, 0.3, header_text, transform=ax_header.transAxes, 
                      fontsize=16, ha='center', color=self.colors['text_secondary'],
                      fontweight='500')
        
        # === GRÁFICA PRINCIPAL: BARRAS AGRUPADAS CON GRADIENTES ===
        ax_main = fig.add_subplot(gs[1, :3])
        ax_main.set_facecolor(self.colors['surface'])
        
        x_pos = np.arange(len(dates))
        width = 0.35
        
        # Barras con efecto gradiente y sombras
        bars_aciertos = ax_main.bar(x_pos - width/2, aciertos, width, 
                                   color=self.colors['aciertos_primary'],
                                   alpha=0.9, label='✅ Aciertos',
                                   edgecolor='white', linewidth=2)
        
        bars_desaciertos = ax_main.bar(x_pos + width/2, desaciertos, width,
                                      color=self.colors['desaciertos_primary'],
                                      alpha=0.9, label='❌ Desaciertos',
                                      edgecolor='white', linewidth=2)
        
        # Agregar valores con estilo moderno
        for i, (bar_a, bar_d, acierto, desacierto) in enumerate(zip(bars_aciertos, bars_desaciertos, aciertos, desaciertos)):
            if acierto > 0:
                ax_main.text(bar_a.get_x() + bar_a.get_width()/2, acierto + 0.1,
                           str(acierto), ha='center', va='bottom', fontweight='bold',
                           color=self.colors['aciertos_primary'], fontsize=12)
            if desacierto > 0:
                ax_main.text(bar_d.get_x() + bar_d.get_width()/2, desacierto + 0.1,
                           str(desacierto), ha='center', va='bottom', fontweight='bold',
                           color=self.colors['desaciertos_primary'], fontsize=12)
        
        # Configurar ejes y estilo
        ax_main.set_xlabel('👥 Jugadores', fontsize=14, fontweight='600', color=self.colors['text_primary'])
        ax_main.set_ylabel('📊 Respuestas', fontsize=14, fontweight='600', color=self.colors['text_primary'])
        ax_main.set_title('Rendimiento Individual por Jugador', fontsize=18, fontweight='bold', 
                         color=self.colors['text_primary'], pad=20)
        
        # Etiquetas del eje X con formato mejorado
        ax_main.set_xticks(x_pos)
        labels = [f"{username}\n{date.strftime('%d/%m %H:%M')}" for username, date in zip(usernames, dates)]
        ax_main.set_xticklabels(labels, fontsize=11, color=self.colors['text_secondary'])
        
        # Grid sutil y elegante
        ax_main.grid(True, alpha=0.2, color=self.colors['grid'], axis='y', linestyle='-', linewidth=1)
        ax_main.set_axisbelow(True)
        
        # Eliminar spines superiores y derecho
        ax_main.spines['top'].set_visible(False)
        ax_main.spines['right'].set_visible(False)
        ax_main.spines['left'].set_color(self.colors['border'])
        ax_main.spines['bottom'].set_color(self.colors['border'])
        
        # Leyenda moderna
        legend = ax_main.legend(loc='upper left', frameon=True, fancybox=True, 
                               shadow=False, fontsize=12, framealpha=0.9)
        legend.get_frame().set_facecolor(self.colors['surface'])
        legend.get_frame().set_edgecolor(self.colors['border'])
        
        # === MEDIDOR CIRCULAR DE RENDIMIENTO PROMEDIO ===
        ax_gauge = fig.add_subplot(gs[1, 3])
        ax_gauge.set_facecolor(self.colors['surface'])
        
        # Crear medidor circular
        theta = np.linspace(0, np.pi, 100)
        radius = 1
        
        # Fondo del medidor
        ax_gauge.plot(radius * np.cos(theta), radius * np.sin(theta), 
                     linewidth=15, color=self.colors['grid'], alpha=0.3)
        
        # Arco de rendimiento
        progress = avg_score / 100
        theta_progress = np.linspace(0, np.pi * progress, int(100 * progress))
        
        if avg_score >= 80:
            gauge_color = self.colors['aciertos_primary']
        elif avg_score >= 60:
            gauge_color = self.colors['desaciertos_primary']
        else:
            gauge_color = '#EF4444'  # Rojo para bajo rendimiento
            
        ax_gauge.plot(radius * np.cos(theta_progress), radius * np.sin(theta_progress),
                     linewidth=15, color=gauge_color, alpha=0.9)
        
        # Texto del porcentaje
        ax_gauge.text(0, -0.3, f'{avg_score:.1f}%', ha='center', va='center',
                     fontsize=24, fontweight='bold', color=gauge_color)
        ax_gauge.text(0, -0.5, 'PROMEDIO', ha='center', va='center',
                     fontsize=12, color=self.colors['text_secondary'])
        
        ax_gauge.set_xlim(-1.3, 1.3)
        ax_gauge.set_ylim(-0.7, 1.3)
        ax_gauge.set_aspect('equal')
        ax_gauge.axis('off')
        ax_gauge.set_title('🎯 Rendimiento Global', fontsize=14, fontweight='bold',
                          color=self.colors['text_primary'], pad=20)
        
        # === GRÁFICA DE TENDENCIAS (LÍNEA DE TIEMPO) ===
        ax_trend = fig.add_subplot(gs[2, :2])
        ax_trend.set_facecolor(self.colors['surface'])
        
        # Línea de tendencia con gradiente
        line = ax_trend.plot(range(len(porcentajes)), porcentajes, 
                            linewidth=4, color=self.colors['accent'], 
                            marker='o', markersize=8, markerfacecolor=self.colors['accent_light'],
                            markeredgecolor='white', markeredgewidth=2,
                            label='📈 Tendencia de Aciertos')
        
        # Área bajo la curva
        ax_trend.fill_between(range(len(porcentajes)), porcentajes, alpha=0.2, 
                             color=self.colors['accent'])
        
        # Línea de referencia del 50%
        ax_trend.axhline(y=50, color=self.colors['text_muted'], linestyle='--', 
                        alpha=0.6, linewidth=2, label='50% Referencia')
        
        ax_trend.set_xlabel('🕒 Secuencia de Juegos', fontsize=12, color=self.colors['text_primary'])
        ax_trend.set_ylabel('📊 % Aciertos', fontsize=12, color=self.colors['text_primary'])
        ax_trend.set_title('Evolución del Rendimiento', fontsize=16, fontweight='bold',
                          color=self.colors['text_primary'])
        
        ax_trend.grid(True, alpha=0.2, color=self.colors['grid'])
        ax_trend.set_ylim(0, 100)
        
        # Eliminar spines
        ax_trend.spines['top'].set_visible(False)
        ax_trend.spines['right'].set_visible(False)
        ax_trend.spines['left'].set_color(self.colors['border'])
        ax_trend.spines['bottom'].set_color(self.colors['border'])
        
        # === DISTRIBUCIÓN DE SCORES (HISTOGRAMA) ===
        ax_hist = fig.add_subplot(gs[2, 2:])
        ax_hist.set_facecolor(self.colors['surface'])
        
        # Histograma con bins personalizados
        bins = [0, 20, 40, 60, 80, 100]
        hist, bin_edges = np.histogram(porcentajes, bins=bins)
        colors_hist = ['#EF4444', '#F59E0B', '#EAB308', '#22C55E', '#10B981']
        
        bars_hist = ax_hist.bar(range(len(hist)), hist, color=colors_hist, 
                               alpha=0.8, edgecolor='white', linewidth=2)
        
        # Etiquetas de los bins
        labels_hist = ['0-20%', '20-40%', '40-60%', '60-80%', '80-100%']
        ax_hist.set_xticks(range(len(hist)))
        ax_hist.set_xticklabels(labels_hist, rotation=45)
        
        ax_hist.set_ylabel('🎮 Cantidad de Juegos', fontsize=12, color=self.colors['text_primary'])
        ax_hist.set_title('Distribución de Rendimiento', fontsize=16, fontweight='bold',
                         color=self.colors['text_primary'])
        
        # Agregar valores en las barras
        for bar, count in zip(bars_hist, hist):
            if count > 0:
                ax_hist.text(bar.get_x() + bar.get_width()/2, count + 0.05,
                           str(int(count)), ha='center', va='bottom', 
                           fontweight='bold', color=self.colors['text_primary'])
        
        ax_hist.spines['top'].set_visible(False)
        ax_hist.spines['right'].set_visible(False)
        ax_hist.spines['left'].set_color(self.colors['border'])
        ax_hist.spines['bottom'].set_color(self.colors['border'])
        
        # === PANEL DE ESTADÍSTICAS DETALLADAS ===
        ax_stats = fig.add_subplot(gs[3, :])
        ax_stats.set_facecolor(self.colors['surface'])
        ax_stats.axis('off')
        
        # Crear tarjetas de estadísticas
        total_aciertos = sum(aciertos)
        total_desaciertos = sum(desaciertos)
        mejor_jugador = usernames[np.argmax(porcentajes)] if porcentajes else "N/A"
        mejor_score = max(porcentajes) if porcentajes else 0
        
        stats_cards = [
            {"title": "🏆 Mejor Jugador", "value": f"{mejor_jugador}", "subtitle": f"{mejor_score:.1f}%"},
            {"title": "✅ Total Aciertos", "value": f"{total_aciertos}", "subtitle": f"{len(games)} partidas"},
            {"title": "❌ Total Errores", "value": f"{total_desaciertos}", "subtitle": "respuestas"},
            {"title": "📊 Promedio General", "value": f"{avg_score:.1f}%", "subtitle": "rendimiento"},
        ]
        
        card_width = 0.22
        card_positions = [0.05, 0.28, 0.51, 0.74]
        
        for i, (card, pos) in enumerate(zip(stats_cards, card_positions)):
            # Crear tarjeta con bordes redondeados
            card_rect = FancyBboxPatch((pos, 0.2), card_width, 0.6,
                                      boxstyle="round,pad=0.02",
                                      facecolor=self.colors['card'],
                                      edgecolor=self.colors['border'],
                                      linewidth=2, alpha=0.9)
            ax_stats.add_patch(card_rect)
            
            # Texto de la tarjeta
            ax_stats.text(pos + card_width/2, 0.7, card['title'], 
                         transform=ax_stats.transAxes, ha='center', va='center',
                         fontsize=12, fontweight='600', color=self.colors['text_secondary'])
            
            ax_stats.text(pos + card_width/2, 0.5, card['value'],
                         transform=ax_stats.transAxes, ha='center', va='center',
                         fontsize=18, fontweight='bold', color=self.colors['text_primary'])
            
            ax_stats.text(pos + card_width/2, 0.3, card['subtitle'],
                         transform=ax_stats.transAxes, ha='center', va='center',
                         fontsize=10, color=self.colors['text_muted'])
        
        # Guardar con máxima calidad
        chart_path = os.path.join(self.charts_dir, 'modern_dashboard.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight', 
                   facecolor=self.colors['background'], edgecolor='none',
                   transparent=False, metadata={'Software': 'Modern Game Analytics'})
        plt.close()
        
        return chart_path
    
    def generate_circular_performance_chart(self, games: List[Dict]) -> str:
        """Genera una gráfica circular moderna con diseño glassmorphism"""
        if not games:
            return None
            
        dates, aciertos, desaciertos, totales, porcentajes, usernames = self._prepare_data_for_charts(games)
        
        if not dates:
            return None
        
        # Crear figura circular con diseño moderno
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 16), 
                                                     facecolor=self.colors['background'])
        
        # === DONUT CHART PRINCIPAL ===
        ax1.set_facecolor(self.colors['surface'])
        
        total_aciertos = sum(aciertos)
        total_desaciertos = sum(desaciertos)
        
        # Datos para el donut chart
        sizes = [total_aciertos, total_desaciertos]
        labels = ['Aciertos', 'Desaciertos']
        colors = [self.colors['aciertos_primary'], self.colors['desaciertos_primary']]
        
        # Crear donut chart con efectos modernos
        wedges, texts, autotexts = ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                                          colors=colors, startangle=90, 
                                          wedgeprops={'width': 0.5, 'edgecolor': 'white', 'linewidth': 3},
                                          textprops={'fontsize': 14, 'fontweight': 'bold'})
        
        # Agregar círculo central con estadística
        centre_circle = Circle((0,0), 0.50, fc=self.colors['surface'], 
                              edgecolor=self.colors['border'], linewidth=3)
        ax1.add_artist(centre_circle)
        
        # Texto central
        total_questions = total_aciertos + total_desaciertos
        accuracy = (total_aciertos / total_questions * 100) if total_questions > 0 else 0
        
        ax1.text(0, 0.1, f'{accuracy:.1f}%', ha='center', va='center',
                fontsize=28, fontweight='bold', color=self.colors['text_primary'])
        ax1.text(0, -0.1, 'PRECISIÓN', ha='center', va='center',
                fontsize=12, color=self.colors['text_secondary'])
        
        ax1.set_title('🎯 Distribución Global de Respuestas', fontsize=16, 
                     fontweight='bold', color=self.colors['text_primary'], pad=20)
        
        # === RADAR CHART DE JUGADORES ===
        ax2.set_facecolor(self.colors['surface'])
        
        if len(usernames) <= 6:  # Solo mostrar radar si hay pocos jugadores
            # Configurar radar
            angles = np.linspace(0, 2 * np.pi, len(usernames), endpoint=False).tolist()
            angles += angles[:1]  # Completar el círculo
            
            # Normalizar porcentajes para el radar
            values = porcentajes + [porcentajes[0]]  # Completar el círculo
            
            ax2 = plt.subplot(2, 2, 2, projection='polar', facecolor=self.colors['surface'])
            ax2.plot(angles, values, 'o-', linewidth=3, color=self.colors['accent'], 
                    markersize=8, markerfacecolor=self.colors['accent_light'],
                    markeredgecolor='white', markeredgewidth=2)
            ax2.fill(angles, values, alpha=0.25, color=self.colors['accent'])
            
            ax2.set_xticks(angles[:-1])
            ax2.set_xticklabels(usernames, fontsize=11, color=self.colors['text_primary'])
            ax2.set_ylim(0, 100)
            ax2.set_yticks([20, 40, 60, 80, 100])
            ax2.set_yticklabels(['20%', '40%', '60%', '80%', '100%'], 
                               fontsize=9, color=self.colors['text_secondary'])
            ax2.grid(True, alpha=0.3, color=self.colors['grid'])
            ax2.set_title('🕸️ Comparativa de Rendimiento', fontsize=16, 
                         fontweight='bold', color=self.colors['text_primary'], pad=30)
        else:
            ax2.text(0.5, 0.5, '📊\n\nDemasiados jugadores\npara mostrar radar\n\n(máx. 6 jugadores)', 
                    transform=ax2.transAxes, ha='center', va='center',
                    fontsize=14, color=self.colors['text_secondary'])
            ax2.axis('off')
        
        # === GRÁFICA DE BARRAS RADIALES ===
        ax3.set_facecolor(self.colors['surface'])
        ax3 = plt.subplot(2, 2, 3, projection='polar')
        
        # Crear barras radiales
        theta = np.linspace(0.0, 2 * np.pi, len(porcentajes), endpoint=False)
        radii = [p/100 for p in porcentajes]  # Normalizar a 0-1
        width = 2 * np.pi / len(porcentajes) * 0.8
        
        bars = ax3.bar(theta, radii, width=width, bottom=0.0, alpha=0.8)
        
        # Colorear barras según rendimiento
        for bar, porcentaje in zip(bars, porcentajes):
            if porcentaje >= 80:
                bar.set_facecolor(self.colors['aciertos_primary'])
            elif porcentaje >= 60:
                bar.set_facecolor(self.colors['desaciertos_primary'])
            else:
                bar.set_facecolor('#EF4444')
            bar.set_edgecolor('white')
            bar.set_linewidth(2)
        
        ax3.set_ylim(0, 1)
        ax3.set_title('🎪 Rendimiento Circular', fontsize=16, 
                     fontweight='bold', color=self.colors['text_primary'], pad=30)
        ax3.set_rticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax3.set_rmax(1)
        ax3.grid(True, alpha=0.3)
        
        # === MÉTRICAS AVANZADAS ===
        ax4.set_facecolor(self.colors['surface'])
        ax4.axis('off')
        
        # Calcular métricas avanzadas
        consistency = 100 - np.std(porcentajes) if len(porcentajes) > 1 else 100
        trend = "↗️ Mejorando" if len(porcentajes) > 1 and porcentajes[-1] > porcentajes[0] else "↘️ Descendente" if len(porcentajes) > 1 else "➖ Estable"
        
        metrics_text = f"""
        📈 MÉTRICAS AVANZADAS
        
        🎯 Precisión Promedio: {np.mean(porcentajes):.1f}%
        📊 Mejor Puntuación: {max(porcentajes):.1f}%
        📉 Peor Puntuación: {min(porcentajes):.1f}%
        🔄 Consistencia: {consistency:.1f}%
        📈 Tendencia: {trend}
        
        🏅 RANKINGS:
        """
        
        # Crear ranking de jugadores
        rankings = sorted(zip(usernames, porcentajes), key=lambda x: x[1], reverse=True)
        for i, (name, score) in enumerate(rankings[:5]):  # Top 5
            medal = ["🥇", "🥈", "🥉", "🏅", "🎖️"][i] if i < 5 else "🏅"
            metrics_text += f"\n        {medal} {name}: {score:.1f}%"
        
        ax4.text(0.1, 0.9, metrics_text, transform=ax4.transAxes, fontsize=12,
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle="round,pad=0.5", facecolor=self.colors['card'], 
                         edgecolor=self.colors['border'], alpha=0.9),
                color=self.colors['text_primary'])
        
        plt.suptitle('🎮 ANÁLISIS CIRCULAR DE RENDIMIENTO - GAME INSIGHTS', 
                    fontsize=20, fontweight='bold', color=self.colors['text_primary'],
                    y=0.95)
        
        plt.tight_layout()
        
        # Guardar con máxima calidad
        chart_path = os.path.join(self.charts_dir, 'circular_performance.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight', 
                   facecolor=self.colors['background'], edgecolor='none',
                   transparent=False)
        plt.close()
        
        return chart_path
    
    def generate_interactive_timeline(self, games: List[Dict]) -> str:
        """Genera una línea de tiempo interactiva con eventos y milestones"""
        if not games:
            return None
            
        dates, aciertos, desaciertos, totales, porcentajes, usernames = self._prepare_data_for_charts(games)
        
        if not dates:
            return None
        
        # Crear figura de línea de tiempo
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(18, 14), 
                                           gridspec_kw={'height_ratios': [2, 1, 1]},
                                           facecolor=self.colors['background'])
        
        # === LÍNEA DE TIEMPO PRINCIPAL ===
        ax1.set_facecolor(self.colors['surface'])
        
        # Crear línea temporal con gradiente
        x_timeline = range(len(dates))
        
        # Línea principal con marcadores especiales
        line_main = ax1.plot(x_timeline, porcentajes, linewidth=4, 
                            color=self.colors['accent'], alpha=0.8, 
                            marker='o', markersize=10, markerfacecolor=self.colors['accent_light'],
                            markeredgecolor='white', markeredgewidth=3,
                            label='📈 Evolución del Rendimiento')
        
        # Área bajo la curva con gradiente
        ax1.fill_between(x_timeline, porcentajes, alpha=0.2, color=self.colors['accent'])
        
        # Marcar eventos especiales (mejores y peores puntuaciones)
        if porcentajes:
            best_idx = np.argmax(porcentajes)
            worst_idx = np.argmin(porcentajes)
            
            # Mejor puntuación
            ax1.scatter(best_idx, porcentajes[best_idx], s=200, 
                       color=self.colors['aciertos_primary'], marker='*',
                       edgecolor='white', linewidth=3, zorder=5,
                       label='🏆 Mejor Puntuación')
            
            # Peor puntuación (solo si hay variación)
            if porcentajes[best_idx] != porcentajes[worst_idx]:
                ax1.scatter(worst_idx, porcentajes[worst_idx], s=200,
                           color=self.colors['desaciertos_primary'], marker='v',
                           edgecolor='white', linewidth=3, zorder=5,
                           label='⚠️ Menor Puntuación')
        
        # Líneas de referencia con etiquetas
        ax1.axhline(y=90, color=self.colors['aciertos_primary'], linestyle='--', 
                   alpha=0.6, linewidth=2, label='🎯 Excelente (90%)')
        ax1.axhline(y=70, color=self.colors['desaciertos_primary'], linestyle='--', 
                   alpha=0.6, linewidth=2, label='👍 Bueno (70%)')
        ax1.axhline(y=50, color='#EF4444', linestyle='--', 
                   alpha=0.6, linewidth=2, label='⚡ Regular (50%)')
        
        # Configurar ejes
        ax1.set_xlabel('🕒 Secuencia Temporal de Juegos', fontsize=14, fontweight='600')
        ax1.set_ylabel('📊 Porcentaje de Aciertos (%)', fontsize=14, fontweight='600')
        ax1.set_title('📈 EVOLUCIÓN TEMPORAL DEL RENDIMIENTO', fontsize=18, 
                     fontweight='bold', pad=20)
        
        # Etiquetas personalizadas en el eje X
        ax1.set_xticks(x_timeline)
        timeline_labels = [f"{username}\n{date.strftime('%d/%m\n%H:%M')}" 
                          for username, date in zip(usernames, dates)]
        ax1.set_xticklabels(timeline_labels, fontsize=10)
        
        ax1.set_ylim(0, 100)
        ax1.grid(True, alpha=0.2, color=self.colors['grid'])
        ax1.legend(loc='upper left', frameon=True, fancybox=True, 
                  framealpha=0.9, fontsize=11)
        
        # Eliminar spines superiores
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['left'].set_color(self.colors['border'])
        ax1.spines['bottom'].set_color(self.colors['border'])
        
        # === HEATMAP DE ACTIVIDAD POR HORA ===
        ax2.set_facecolor(self.colors['surface'])
        
        # Extraer horas de las fechas
        hours = [date.hour for date in dates]
        hour_performance = {}
        
        for hour, perf in zip(hours, porcentajes):
            if hour not in hour_performance:
                hour_performance[hour] = []
            hour_performance[hour].append(perf)
        
        # Calcular promedio por hora
        hour_avg = {hour: np.mean(perfs) for hour, perfs in hour_performance.items()}
        
        # Crear heatmap por horas
        all_hours = list(range(24))
        hour_values = [hour_avg.get(hour, 0) for hour in all_hours]
        
        # Crear barras coloreadas por rendimiento
        bars_hours = ax2.bar(all_hours, [1]*24, color='lightgray', alpha=0.3, width=0.8)
        
        for i, (hour, value) in enumerate(zip(all_hours, hour_values)):
            if value > 0:
                if value >= 80:
                    color = self.colors['aciertos_primary']
                elif value >= 60:
                    color = self.colors['desaciertos_primary'] 
                else:
                    color = '#EF4444'
                    
                bars_hours[i].set_color(color)
                bars_hours[i].set_alpha(0.8)
                
                # Agregar texto con el valor
                ax2.text(hour, 0.5, f'{value:.0f}%', ha='center', va='center',
                        fontsize=9, fontweight='bold', color='white')
        
        ax2.set_xlabel('🕐 Hora del Día', fontsize=12, fontweight='600')
        ax2.set_ylabel('Actividad', fontsize=12, fontweight='600')
        ax2.set_title('🌡️ Mapa de Calor - Rendimiento por Hora', fontsize=14, fontweight='bold')
        ax2.set_xlim(-0.5, 23.5)
        ax2.set_ylim(0, 1)
        ax2.set_xticks(range(0, 24, 2))
        ax2.set_xticklabels([f'{h:02d}:00' for h in range(0, 24, 2)], rotation=45)
        
        # Eliminar yticks ya que solo es visual
        ax2.set_yticks([])
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['left'].set_visible(False)
        ax2.spines['bottom'].set_color(self.colors['border'])
        
        # === PANEL DE ESTADÍSTICAS DE PROGRESO ===
        ax3.set_facecolor(self.colors['surface'])
        ax3.axis('off')
        
        # Calcular estadísticas de progreso
        if len(porcentajes) > 1:
            first_half = porcentajes[:len(porcentajes)//2]
            second_half = porcentajes[len(porcentajes)//2:]
            
            progress = np.mean(second_half) - np.mean(first_half)
            progress_text = f"{'📈 +' if progress > 0 else '📉 '}{progress:.1f}%"
            progress_desc = "Mejorando" if progress > 0 else "Descendiendo" if progress < 0 else "Estable"
        else:
            progress_text = "➖ 0.0%"
            progress_desc = "Datos insuficientes"
        
        # Crear panel de estadísticas como tarjetas
        stats_data = [
            {"icon": "🎮", "label": "Total Partidas", "value": str(len(games)), "color": self.colors['text_primary']},
            {"icon": "📊", "label": "Promedio Global", "value": f"{np.mean(porcentajes):.1f}%", "color": self.colors['accent']},
            {"icon": "🚀", "label": "Progreso", "value": progress_text, "color": self.colors['aciertos_primary'] if progress > 0 else self.colors['desaciertos_primary']},
            {"icon": "🎯", "label": "Consistencia", "value": f"{100 - np.std(porcentajes):.1f}%", "color": self.colors['text_primary']},
            {"icon": "⭐", "label": "Mejor Jugador", "value": usernames[np.argmax(porcentajes)] if porcentajes else "N/A", "color": self.colors['aciertos_primary']},
        ]
        
        # Dibujar tarjetas de estadísticas
        card_width = 0.18
        start_x = 0.05
        
        for i, stat in enumerate(stats_data):
            x_pos = start_x + i * (card_width + 0.02)
            
            # Fondo de la tarjeta
            card_bg = FancyBboxPatch((x_pos, 0.2), card_width, 0.6,
                                   boxstyle="round,pad=0.02",
                                   facecolor=self.colors['card'],
                                   edgecolor=stat['color'],
                                   linewidth=2, alpha=0.9)
            ax3.add_patch(card_bg)
            
            # Contenido de la tarjeta
            ax3.text(x_pos + card_width/2, 0.7, stat['icon'], 
                    transform=ax3.transAxes, ha='center', va='center',
                    fontsize=20)
            
            ax3.text(x_pos + card_width/2, 0.5, stat['value'],
                    transform=ax3.transAxes, ha='center', va='center',
                    fontsize=14, fontweight='bold', color=stat['color'])
            
            ax3.text(x_pos + card_width/2, 0.3, stat['label'],
                    transform=ax3.transAxes, ha='center', va='center',
                    fontsize=9, color=self.colors['text_secondary'])
        
        plt.tight_layout()
        
        # Guardar gráfica
        chart_path = os.path.join(self.charts_dir, 'interactive_timeline.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight', 
                   facecolor=self.colors['background'], edgecolor='none',
                   transparent=False)
        plt.close()
        
        return chart_path
    
    def generate_charts(self, games: List[Dict]) -> Dict[str, str]:
        """Genera las gráficas básicas compatibles con el servidor actual"""
        # Generar los gráficos modernos pero con nombres compatibles
        dashboard_path = self.generate_performance_dashboard(games)
        circular_path = self.generate_circular_performance_chart(games)
        
        return {
            'line_chart': dashboard_path,  # El dashboard moderno como 'line_chart'
            'pie_chart': circular_path     # El análisis circular como 'pie_chart'
        }
    
    def generate_all_charts(self, games: List[Dict]) -> Dict[str, str]:
        """Genera todas las gráficas mejoradas y retorna las rutas"""
        dashboard_path = self.generate_performance_dashboard(games)
        circular_path = self.generate_circular_performance_chart(games)
        timeline_path = self.generate_interactive_timeline(games)
        
        return {
            'dashboard': dashboard_path,
            'circular': circular_path,
            'timeline': timeline_path
        }
    
    def get_chart_url(self, chart_path: str) -> str:
        """Convierte la ruta del archivo en URL para Flask"""
        if chart_path and os.path.exists(chart_path):
            filename = os.path.basename(chart_path)
            return f'/static/charts/{filename}'
        return None

# Ejemplo de uso y prueba
if __name__ == "__main__":
    # Datos de ejemplo basados en el formato proporcionado
    sample_games = [
        {"username": "LUISITO", "score": "1/5", "start_time": "11/08/25 14:56", "num_phrases": 5},
        {"username": "MARIA", "score": "4/5", "start_time": "11/08/25 15:30", "num_phrases": 5},
        {"username": "CARLOS", "score": "3/5", "start_time": "11/08/25 16:15", "num_phrases": 5},
        {"username": "ANA", "score": "5/5", "start_time": "11/08/25 17:00", "num_phrases": 5},
        {"username": "PEDRO", "score": "2/5", "start_time": "11/08/25 18:30", "num_phrases": 5},
        {"username": "SOFIA", "score": "4/5", "start_time": "11/08/25 19:15", "num_phrases": 5},
    ]
    
    # Crear instancia de la clase
    chart_generator = GameCharts()
    
    # Generar todas las gráficas
    chart_paths = chart_generator.generate_all_charts(sample_games)
    
    print("✅ Gráficas generadas exitosamente:")
    for chart_type, path in chart_paths.items():
        if path:
            print(f"   📊 {chart_type.capitalize()}: {path}")
        else:
            print(f"   ❌ {chart_type.capitalize()}: Error al generar")
    
    print("\n🎨 Características de los nuevos gráficos:")
    print("   • Tema oscuro moderno con efectos glassmorphism")
    print("   • Paleta de colores vibrante y accesible")
    print("   • Dashboard completo con múltiples visualizaciones")
    print("   • Gráficas circulares con radar y métricas avanzadas")
    print("   • Línea de tiempo interactiva con heatmap por horas")
    print("   • Tarjetas de estadísticas con diseño moderno")
    print("   • Gradientes, sombras y efectos visuales avanzados")
    print("   • Rankings y comparativas entre jugadores")
    print("   • Métricas de consistencia y progreso temporal")