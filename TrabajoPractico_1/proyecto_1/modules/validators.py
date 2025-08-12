def validate_num_phrases(num_phrases: str) -> tuple[bool, str, int]:
    """
    Valida el número de frases ingresado por el usuario
    
    Args:
        num_phrases: String con el número de frases
        
    Returns:
        tuple: (es_valido, mensaje_error, numero_frases)
    """
    try:
        num = int(num_phrases)
        if num < 3:
            return False, "El número de frases debe ser mayor o igual a 3", 0
        if num > 100:
            return False, "El número de frases no puede ser mayor a 100", 0
        return True, "", num
    except ValueError:
        return False, "Debe ingresar un número válido", 0

def validate_username(username: str) -> tuple[bool, str]:
    """
    Valida el nombre de usuario ingresado
    
    Args:
        username: String con el nombre de usuario
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if not username or not username.strip():
        return False, "Debe ingresar un nombre de usuario"
    
    if len(username.strip()) < 2:
        return False, "El nombre de usuario debe tener al menos 2 caracteres"
    
    if len(username.strip()) > 50:
        return False, "El nombre de usuario no puede tener más de 50 caracteres"
    
    return True, ""

def sanitize_input(text: str) -> str:
    """
    Sanitiza el texto de entrada para prevenir XSS básico
    
    Args:
        text: Texto a sanitizar
        
    Returns:
        str: Texto sanitizado
    """
    if not text:
        return ""
    
    # Reemplazar caracteres potencialmente peligrosos
    dangerous_chars = {
        '<': '&lt;',
        '>': '&gt;',
        '&': '&amp;',
        '"': '&quot;',
        "'": '&#x27;'
    }
    
    sanitized = text
    for char, replacement in dangerous_chars.items():
        sanitized = sanitized.replace(char, replacement)
    
    return sanitized.strip()
