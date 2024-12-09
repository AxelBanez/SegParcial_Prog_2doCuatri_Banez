

lista_explosiones = []

def actualizar_explosiones():
    """Actualiza las explosiones y las elimina cuando terminan."""

    for explosion in lista_explosiones[:]:
        explosion["frame"] += 1
        if explosion["frame"] >= 7:
            lista_explosiones.remove(explosion)

