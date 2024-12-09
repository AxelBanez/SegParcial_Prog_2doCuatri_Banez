import random

from config import ANCHO


lista_enemies = []

# Diccionario con datos de los enemigos
dict_enemies = {
    "normal": {
        "ancho": 70,
        "altura": 70,
        "salud": 1,
        "velocidad": 3
    },
    "comandante": {
        "ancho": 100,
        "altura": 100,
        "salud": 5,
        "velocidad": 2.5
    },
    "jefe": {
        "ancho": 150,
        "altura": 150,
        "salud": 10,
        "velocidad": 2
    }
}

def crear_enemigo():
    """Crea un enemigo de forma aleatoria (normal, comandante o jefe) y lo añade a la lista de enemigos."""
    probabilidad = random.random()

    if probabilidad < 0.05:  # 5% de probabilidad para el jefe
        tipo = "jefe"
    elif probabilidad < 0.2:  # 15% de probabilidad para el comandante
        tipo = "comandante"
    else:  # 80% de probabilidad para el enemigo normal
        tipo = "normal"

    # Datos del enemigo según el tipo
    datos_enemy = dict_enemies[tipo]
    x = random.randint(0, ANCHO - datos_enemy["ancho"])

    lista_enemies.append({
        "tipo": tipo,
        "x": x,
        "y": - datos_enemy["altura"],  # Aparece fuera de la pantalla
        "salud": datos_enemy["salud"]
    })
