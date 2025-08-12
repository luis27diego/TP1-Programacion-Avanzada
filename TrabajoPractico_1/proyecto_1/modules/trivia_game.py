import random
import json
from datetime import datetime
from typing import List, Tuple, Dict, Optional
import os

class TriviaGame:
    def __init__(self, data_file: str = "data/frases_de_peliculas.txt"):
        self.data_file = data_file
        self.phrases_data = []
        self.movies_list = []
        self.load_data()
        
    def load_data(self):
        """Carga los datos del archivo de frases de películas"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line and ';' in line:
                        phrase, movie = line.split(';', 1)
                        self.phrases_data.append({
                            'phrase': phrase.strip(),
                            'movie': movie.strip()
                        })
            
            # Extraer lista única de películas (sin duplicados, ordenada alfabéticamente)
            movies_set = set()
            for item in self.phrases_data:
                movies_set.add(item['movie'].lower())
            
            self.movies_list = sorted(list(movies_set))
            
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {self.data_file}")
            self.phrases_data = []
            self.movies_list = []
    
    def get_movies_list(self) -> List[str]:
        """Retorna la lista de películas disponibles"""
        return self.movies_list
    
    def get_random_phrase(self) -> Dict[str, str]:
        """Obtiene una frase aleatoria del juego"""
        if not self.phrases_data:
            return None
        return random.choice(self.phrases_data)
    
    def generate_question(self) -> Dict[str, any]:
        """Genera una pregunta con una frase y 3 opciones de películas"""
        if len(self.phrases_data) < 4:
            return None
            
        # Seleccionar frase aleatoria
        correct_answer = random.choice(self.phrases_data)
        correct_movie = correct_answer['movie'].lower()
        
        # Generar 3 opciones diferentes
        options = [correct_movie]
        available_movies = [m for m in self.movies_list if m != correct_movie]
        
        # Agregar 2 opciones incorrectas aleatorias
        if len(available_movies) >= 2:
            wrong_options = random.sample(available_movies, 2)
            options.extend(wrong_options)
        else:
            # Si no hay suficientes películas, duplicar algunas
            while len(options) < 3:
                random_movie = random.choice(self.movies_list)
                if random_movie not in options:
                    options.append(random_movie)
        
        # Mezclar las opciones
        random.shuffle(options)
        
        return {
            'phrase': correct_answer['phrase'],
            'correct_movie': correct_answer['movie'],
            'options': options,
            'correct_index': options.index(correct_movie)
        }
    
    def check_answer(self, question: Dict, selected_movie: str) -> bool:
        """Verifica si la respuesta del usuario es correcta"""
        return selected_movie.lower() == question['correct_movie'].lower()
    
    def get_movie_by_name(self, movie_name: str) -> Optional[str]:
        """Busca una película por nombre (ignorando mayúsculas/minúsculas)"""
        for movie in self.movies_list:
            if movie.lower() == movie_name.lower():
                return movie
        return None

class GameSession:
    def __init__(self, username: str, num_phrases: int):
        self.username = username
        self.num_phrases = num_phrases
        self.current_question = 0
        self.score = 0
        self.start_time = datetime.now()
        self.questions = []
        self.answers = []
        
    def add_question(self, question: Dict):
        """Agrega una pregunta a la sesión"""
        self.questions.append(question)
    
    def add_answer(self, is_correct: bool):
        """Registra una respuesta del usuario"""
        self.answers.append(is_correct)
        if is_correct:
            self.score += 1
        self.current_question += 1
    
    def is_finished(self) -> bool:
        """Verifica si la sesión ha terminado"""
        return self.current_question >= self.num_phrases
    
    def get_final_score(self) -> str:
        """Retorna el puntaje final en formato 'aciertos/N'"""
        return f"{self.score}/{self.num_phrases}"
    
    def get_start_time_formatted(self) -> str:
        """Retorna la fecha y hora de inicio formateada"""
        return self.start_time.strftime("%d/%m/%y %H:%M")

class GameHistory:
    def __init__(self, history_file: str = "data/game_history.json"):
        self.history_file = history_file
        self.history = []
        self.load_history()
    
    def load_history(self):
        """Carga el historial de juegos desde el archivo"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as file:
                    self.history = json.load(file)
            else:
                self.history = []
        except (json.JSONDecodeError, FileNotFoundError):
            self.history = []
    
    def save_history(self):
        """Guarda el historial de juegos en el archivo"""
        try:
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            with open(self.history_file, 'w', encoding='utf-8') as file:
                json.dump(self.history, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al guardar historial: {e}")
    
    def add_game(self, session: GameSession):
        """Agrega una nueva sesión al historial"""
        game_record = {
            'username': session.username,
            'score': session.get_final_score(),
            'start_time': session.get_start_time_formatted(),
            'num_phrases': session.num_phrases
        }
        self.history.append(game_record)
        self.save_history()
    
    def get_all_games(self) -> List[Dict]:
        """Retorna todo el historial de juegos"""
        return self.history
