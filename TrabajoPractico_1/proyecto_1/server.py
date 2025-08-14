from flask import render_template, request, redirect, url_for, session, flash, jsonify, send_file
from modules.config import app
from modules.trivia_game import TriviaGame, GameSession, GameHistory
from modules.validators import validate_num_phrases, validate_username, sanitize_input
from modules.charts import GameCharts
from modules.pdf_generator import GameReportPDF
import os

# Inicializar el juego, historial, gráficas y PDFs
trivia_game = TriviaGame()
game_history = GameHistory()
game_charts = GameCharts()
pdf_generator = GameReportPDF()

@app.route('/')
def index():
    """Página principal con explicación del juego y formulario de inicio"""
    return render_template('inicio.html')

@app.route('/listar_peliculas')
def listar_peliculas():
    """Muestra la lista de todas las películas disponibles"""
    movies = trivia_game.get_movies_list()
    return render_template('listar_peliculas.html', movies=movies)

@app.route('/iniciar_juego', methods=['POST'])
def iniciar_juego():
    """Inicia una nueva partida del juego"""
    username = sanitize_input(request.form.get('username', ''))
    num_phrases = request.form.get('num_phrases', '')
    
    # Validar entrada
    is_valid_username, username_error = validate_username(username)
    is_valid_phrases, phrases_error, num_phrases_int = validate_num_phrases(num_phrases)
    
    if not is_valid_username:
        flash(username_error, 'error')
        return redirect(url_for('index'))
    
    if not is_valid_phrases:
        flash(phrases_error, 'error')
        return redirect(url_for('index'))
    
    # Crear nueva sesión de juego
    game_session = GameSession(username, num_phrases_int)
    session['game_session'] = {
        'username': username,
        'num_phrases': num_phrases_int,
        'current_question': 0,
        'score': 0,
        'start_time': game_session.start_time.isoformat()
    }
    
    # Generar primera pregunta
    question = trivia_game.generate_question()
    if question:
        session['current_question'] = question
        return redirect(url_for('jugar_pregunta'))
    else:
        flash('Error al generar la pregunta. Intente nuevamente.', 'error')
        return redirect(url_for('index'))

@app.route('/jugar_pregunta')
def jugar_pregunta():
    """Muestra la pregunta actual del juego"""
    if 'game_session' not in session:
        return redirect(url_for('index'))
    
    if 'current_question' not in session:
        return redirect(url_for('index'))
    
    question = session['current_question']
    game_session = session['game_session']
    
    return render_template('pregunta.html', 
                         question=question, 
                         game_session=game_session)

@app.route('/responder', methods=['POST'])
def responder():
    """Procesa la respuesta del usuario"""
    if 'game_session' not in session:
        return redirect(url_for('index'))
    
    selected_movie = request.form.get('selected_movie', '')
    current_question = session.get('current_question', {})
    
    if not selected_movie or not current_question:
        return redirect(url_for('index'))
    
    # Verificar respuesta
    is_correct = trivia_game.check_answer(current_question, selected_movie)
    
    # Actualizar sesión
    session['game_session']['current_question'] += 1
    if is_correct:
        session['game_session']['score'] += 1
    
    # Verificar si el juego ha terminado
    if session['game_session']['current_question'] >= session['game_session']['num_phrases']:
        # Juego terminado, guardar en historial
        game_session = GameSession(
            session['game_session']['username'],
            session['game_session']['num_phrases']
        )
        game_session.score = session['game_session']['score']
        game_session.current_question = session['game_session']['current_question']
        game_history.add_game(game_session)
        
        # Limpiar sesión
        session.pop('game_session', None)
        session.pop('current_question', None)
        
        return render_template('resultado_final.html', 
                             username=game_session.username,
                             score=game_session.get_final_score(),
                             is_correct=is_correct,
                             correct_movie=current_question['correct_movie'])
    
    # Generar siguiente pregunta
    next_question = trivia_game.generate_question()
    if next_question:
        session['current_question'] = next_question
        return render_template('pregunta.html', 
                             question=next_question, 
                             game_session=session['game_session'])
    else:
        flash('Error al generar la siguiente pregunta.', 'error')
        return redirect(url_for('index'))

@app.route('/resultados_historicos')
def resultados_historicos():
    """Muestra el historial de todos los juegos con gráficas"""
    games = game_history.get_all_games()
    
    # Generar gráficas si hay datos
    charts_paths = {}
    line_chart_url = None
    pie_chart_url = None
    pdf_report_url = None
    
    if games:
        charts_paths = game_charts.generate_charts(games)
        
        if charts_paths.get('line_chart'):
            line_chart_url = game_charts.get_chart_url(charts_paths['line_chart'])
        
        if charts_paths.get('pie_chart'):
            pie_chart_url = game_charts.get_chart_url(charts_paths['pie_chart'])
        
        # Verificar si ya existe un reporte PDF
        reports_dir = "static/reports"
        if os.path.exists(reports_dir):
            pdf_files = [f for f in os.listdir(reports_dir) if f.endswith('.pdf')]
            if pdf_files:
                # Tomar el más reciente
                latest_pdf = max(pdf_files, key=lambda x: os.path.getctime(os.path.join(reports_dir, x)))
                pdf_report_url = f'/static/reports/{latest_pdf}'
    
    return render_template('resultados_historicos.html', 
                         games=games,
                         line_chart_url=line_chart_url,
                         pie_chart_url=pie_chart_url,
                         pdf_report_url=pdf_report_url)

@app.route('/actualizar_graficas')
def actualizar_graficas():
    """Actualiza las gráficas con los datos más recientes"""
    games = game_history.get_all_games()
    
    if games:
        # Generar nuevas gráficas
        charts_paths = game_charts.generate_charts(games)
        flash('Gráficas actualizadas correctamente.', 'info')
    else:
        flash('No hay datos para generar gráficas.', 'error')
    
    return redirect(url_for('resultados_historicos'))

@app.route('/generar_reporte_pdf')
def generar_reporte_pdf():
    """Genera y descarga un reporte PDF completo"""
    games = game_history.get_all_games()
    
    if not games:
        flash('No hay datos para generar el reporte.', 'error')
        return redirect(url_for('resultados_historicos'))
    
    try:
        # Generar gráficas primero
        charts_paths = game_charts.generate_charts(games)
        import logging
        app.logger.info(charts_paths)
        
        # Generar reporte PDF
        pdf_path = pdf_generator.generate_report(games, charts_paths)
        
        if pdf_path and os.path.exists(pdf_path):
            # Enviar archivo para descarga
            return send_file(pdf_path, as_attachment=True, 
                           download_name=os.path.basename(pdf_path),
                           cache_timeout=0)
        else:
            flash('Error al generar el reporte PDF.', 'error')
            return redirect(url_for('resultados_historicos'))
            
    except Exception as e:
        flash(f'Error al generar el reporte: {str(e)}', 'error')
        return redirect(url_for('resultados_historicos'))

@app.route('/reiniciar')
def reiniciar():
    """Reinicia el juego y vuelve a la página principal"""
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    # Crear directorios necesarios
    os.makedirs('data/sessions', exist_ok=True)
    os.makedirs('static/charts', exist_ok=True)
    os.makedirs('static/reports', exist_ok=True)
    app.run(host="0.0.0.0", debug=True)