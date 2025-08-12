# 🎬 Trivia de Películas

Una aplicación web interactiva desarrollada en Flask que permite a los usuarios jugar un juego de trivia basado en frases famosas de películas.

## 🎯 Descripción

Este proyecto implementa un juego de trivia donde los usuarios deben adivinar a qué película pertenece una frase específica. La aplicación cumple con todos los requerimientos especificados en la guía del trabajo práctico:

- **Interfaz web usando Flask** ✅
- **Uso de funciones implementadas en archivos dentro de la carpeta "modules"** ✅
- **Aplicación completa del Trivia de películas** ✅
- **Gráficas de resultados organizadas** ✅
- **Descarga de reportes en PDF** ✅

## 🚀 Funcionalidades

### Página Principal
- Explicación clara de la dinámica del juego
- Formulario para ingresar nombre de usuario y número de frases
- Validación de entrada (mínimo 3 frases)
- Botones para acceder a todas las funcionalidades

### Juego de Trivia
- Generación aleatoria de preguntas con frases de películas
- 3 opciones de respuesta diferentes para cada pregunta
- Seguimiento de puntuación en tiempo real
- Felicitación por respuestas correctas
- Información de la respuesta correcta en caso de error

### Lista de Películas
- Visualización de todas las películas disponibles
- Lista indexada y ordenada alfabéticamente
- Eliminación automática de duplicados
- Manejo de mayúsculas/minúsculas

### Resultados Históricos con Gráficas
- Registro de todas las partidas jugadas
- Formato de puntuación "aciertos/N"
- Fecha y hora de inicio de cada partida
- **Gráfica de líneas**: Evolución de aciertos y desaciertos por fecha
- **Gráfica circular**: Distribución total de aciertos vs desaciertos
- Estadísticas generales del juego

### 📊 Análisis Gráfico Avanzado
- **Gráfica de Líneas**: Muestra la evolución temporal de aciertos y desaciertos a lo largo del tiempo
- **Gráfica Circular**: Visualiza la distribución porcentual total de aciertos vs desaciertos
- **Actualización automática**: Las gráficas se generan automáticamente con cada nueva partida
- **Diseño responsivo**: Gráficas adaptables a diferentes dispositivos

### 📄 Reportes PDF Descargables
- **Reporte completo**: Incluye ambas gráficas y estadísticas detalladas
- **Formato profesional**: Diseño atractivo con colores y estilos
- **Estadísticas detalladas**: Análisis completo de rendimiento
- **Descarga directa**: Botón para descargar inmediatamente
- **Generación automática**: Se crea al solicitar el reporte

## 🏗️ Arquitectura del Proyecto

```
proyecto_1/
├── apps/
├── data/
│   ├── frases_de_peliculas.txt    # Archivo de datos del juego
│   └── game_history.json         # Historial de partidas (se crea automáticamente)
├── deps/
├── docs/
├── modules/
│   ├── config.py                  # Configuración de Flask y sesiones
│   ├── trivia_game.py            # Lógica principal del juego
│   ├── validators.py             # Validaciones de entrada
│   ├── charts.py                 # Generación de gráficas
│   └── pdf_generator.py          # Generación de reportes PDF
├── static/
│   ├── style.css                 # Estilos CSS de la aplicación
│   ├── charts/                   # Gráficas generadas
│   └── reports/                  # Reportes PDF generados
├── templates/
│   ├── inicio.html               # Página principal
│   ├── listar_peliculas.html    # Lista de películas
│   ├── pregunta.html             # Preguntas del juego
│   ├── resultado_final.html      # Resultado final
│   └── resultados_historicos.html # Historial con gráficas
├── tests/
├── server.py                     # Aplicación principal Flask
├── requirements.txt              # Dependencias del proyecto
└── README.md
```

## 📋 Módulos Implementados

### `modules/trivia_game.py`
- **Clase TriviaGame**: Maneja la carga de datos y generación de preguntas
- **Clase GameSession**: Gestiona las sesiones de juego individuales
- **Clase GameHistory**: Administra el historial de todas las partidas

### `modules/validators.py`
- Validación del número de frases (mínimo 3)
- Validación del nombre de usuario
- Sanitización de entrada para prevenir XSS

### `modules/config.py`
- Configuración de Flask con manejo de sesiones
- Configuración de seguridad y directorios

### `modules/charts.py` 🆕
- **Clase GameCharts**: Genera gráficas profesionales de los resultados
- **Gráfica de líneas**: Evolución temporal de aciertos/desaciertos
- **Gráfica circular**: Distribución total acumulada
- **Configuración automática**: Estilos y colores profesionales

### `modules/pdf_generator.py` 🆕
- **Clase GameReportPDF**: Crea reportes PDF completos
- **Formato profesional**: Estilos y diseño atractivo
- **Inclusión de gráficas**: Integra las gráficas generadas
- **Estadísticas detalladas**: Análisis completo de rendimiento

## 🛠️ Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd proyecto_1
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**
   ```bash
   python server.py
   ```

4. **Abrir en el navegador**
   ```
   http://localhost:5000
   ```

## 🎮 Cómo Jugar

1. **Iniciar Juego**
   - Ingresa tu nombre de usuario
   - Selecciona el número de frases (mínimo 3)
   - Haz clic en "Iniciar Trivia"

2. **Responder Preguntas**
   - Lee la frase mostrada
   - Selecciona una de las 3 opciones de películas
   - Haz clic en "Responder"

3. **Ver Resultados y Gráficas**
   - Al final del juego verás tu puntuación final
   - Puedes ver el historial con gráficas interactivas
   - Descarga reportes PDF completos
   - Opción de reiniciar y jugar nuevamente

## 📊 Funcionalidades de Gráficas

### Gráfica de Líneas (Evolución Temporal)
- **Eje X**: Fechas de los juegos
- **Eje Y**: Cantidad de aciertos/desaciertos
- **Dos líneas**: Aciertos (verde) y Desaciertos (rojo)
- **Marcadores**: Puntos visibles para cada partida
- **Leyenda**: Identificación clara de cada métrica

### Gráfica Circular (Distribución Total)
- **Secciones**: Aciertos vs Desaciertos
- **Porcentajes**: Visualización clara de la proporción
- **Colores**: Verde para aciertos, rojo para desaciertos
- **Valores**: Cantidades absolutas en las etiquetas
- **Efectos**: Sombra y separación para mejor visualización

### Características Técnicas
- **Alta resolución**: 300 DPI para calidad profesional
- **Formato PNG**: Compatible con todos los navegadores
- **Responsive**: Se adapta al tamaño de pantalla
- **Actualización automática**: Se regenera con nuevos datos

## 📄 Sistema de Reportes PDF

### Contenido del Reporte
- **Portada**: Título y fecha de generación
- **Resumen ejecutivo**: Estadísticas principales
- **Gráficas integradas**: Ambas gráficas en alta calidad
- **Tabla de resultados**: Últimos 10 juegos
- **Estadísticas detalladas**: Análisis completo
- **Pie de página**: Información del sistema

### Características del PDF
- **Formato A4**: Estándar internacional
- **Estilos profesionales**: Colores y tipografías atractivas
- **Navegación**: Estructura clara y organizada
- **Descarga directa**: Botón de descarga inmediata
- **Nombre único**: Timestamp para evitar conflictos

## 🔧 Funcionalidades Técnicas

- **Manejo de Sesiones**: Cada usuario tiene su propia sesión de juego
- **Persistencia de Datos**: Los resultados se guardan en archivo JSON
- **Validación de Entrada**: Verificación de datos de usuario
- **Interfaz Responsiva**: Diseño adaptable a diferentes dispositivos
- **Manejo de Errores**: Validaciones y mensajes informativos
- **Generación de Gráficas**: Matplotlib y Seaborn para visualizaciones
- **Generación de PDFs**: ReportLab para reportes profesionales
- **Código Modular**: Estructura clara y mantenible

## 📱 Características de la Interfaz

- **Diseño Moderno**: Gradientes y efectos visuales atractivos
- **Responsive**: Adaptable a dispositivos móviles y de escritorio
- **Navegación Intuitiva**: Botones claros y navegación sencilla
- **Feedback Visual**: Mensajes de éxito, error y progreso
- **Accesibilidad**: Contraste adecuado y estructura semántica
- **Gráficas Interactivas**: Visualización clara de datos
- **Botones de Acción**: Descarga y actualización de gráficas

## 🧪 Estructura de Datos

### Archivo de Frases (`data/frases_de_peliculas.txt`)
```
Frase de la película;Nombre de la Película
```

### Historial de Juegos (`data/game_history.json`)
```json
[
  {
    "username": "Nombre del Usuario",
    "score": "3/5",
    "start_time": "15/12/24 14:30",
    "num_phrases": 5
  }
]
```

### Gráficas Generadas (`static/charts/`)
- `line_chart.png` - Gráfica de evolución temporal
- `pie_chart.png` - Gráfica de distribución total

### Reportes PDF (`static/reports/`)
- `reporte_trivia_YYYYMMDD_HHMMSS.pdf` - Reportes con timestamp

## 🚀 Ejecución

```bash
# Desde la raíz del proyecto
python server.py

# La aplicación estará disponible en:
# http://localhost:5000
```

## 📊 Funcionalidades Cumplidas

- ✅ Aplicación con interfaz web usando Flask
- ✅ Uso de funciones en módulos de la carpeta "modules"
- ✅ Explicación del juego en la página principal
- ✅ Formulario para nombre de usuario y número de frases
- ✅ Validación de número de frases (≥ 3)
- ✅ Botón para iniciar el juego
- ✅ Botón para listar películas
- ✅ Botón para ver resultados históricos
- ✅ Lista de películas indexada y ordenada alfabéticamente
- ✅ Eliminación de duplicados en nombres de películas
- ✅ Manejo de mayúsculas/minúsculas
- ✅ Generación de preguntas con 3 opciones diferentes
- ✅ Verificación de respuestas correctas/incorrectas
- ✅ Felicitación por aciertos
- ✅ Información de respuesta correcta en errores
- ✅ Puntuación final en formato "aciertos/N"
- ✅ Historial con nombre de usuario, puntuación y fecha/hora
- ✅ Formato de fecha "dd/mm/aa hh:mm"
- ✅ **Gráfica de líneas de aciertos y desaciertos por fecha** 🆕
- ✅ **Gráfica circular de aciertos y desaciertos acumulados** 🆕
- ✅ **Descarga de reportes en formato PDF** 🆕
- ✅ **Análisis gráfico organizado en dos gráficas** 🆕
- ✅ **Opción de descarga de gráficas en PDF** 🆕

## 👨‍💻 Autor

Desarrollado para el Trabajo Práctico N°1 de Programación Avanzada.

## 📄 Licencia

Este proyecto es parte de un trabajo académico.
