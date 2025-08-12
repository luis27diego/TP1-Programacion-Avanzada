from flask import Flask
from flask_session import Session

app = Flask("server")
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui_2024'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = 'data/sessions'
app.config['SESSION_FILE_THRESHOLD'] = 500

# Inicializar la extensión de sesiones
Session(app)