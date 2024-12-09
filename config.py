import pygame

pygame.init()

# Dimensiones de la pantalla
ANCHO, ALTURA = 700, 950
FPS = 60

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS_CLARO = (200, 200, 200)
GRIS_OSCURO = (150, 150, 150)
ROJO = (255, 0, 0)

# Fuente
fuente = pygame.font.Font(r"fuentes\Starjedi.ttf", 30)

# Cargamos sonidos de las explosiones y disparos
explosion_sonido = pygame.mixer.Sound(r"sonidos\sonido_explosion.mp3")
disparo_sonido = pygame.mixer.Sound(r"sonidos\disparo_sonido.mp3")


def cargar_y_redimensionar_imagenes(ruta_imagen_a_cargar: str, ancho: int, altura: int):
    """
    Carga y redimensiona una imagen pasada por parametro.

    Args:
        ruta_imagen_a_cargar (str): ruta de la imagen.
        ancho (int): anchoi de la imagen.
        altura (int): altura de la imagen.

    Returns:
        Retorna la imagen redimensionada
    """
    imagen = pygame.image.load(ruta_imagen_a_cargar).convert_alpha()
    imagen_redimensionada = pygame.transform.scale(imagen, (ancho, altura))
    return imagen_redimensionada

def crear_boton(pantalla, texto, x, y, ancho, alto, color_boton, color_boton_sombreado, color_texto, fuente):
    """
    Crea un botón interactivo y verifica si fue clickeado.

    Args:
        pantalla (pygame.Surface): Superficie donde se dibuja el botón.
        texto (str): Texto a mostrar en el botón.
        x (int): Coordenada X del botón.
        y (int): Coordenada Y del botón.
        ancho (int): Ancho del botón.
        alto (int): Alto del botón.
        color_boton (tuple): Color del botón en estado normal.
        color_boton_sombreado (tuple): Color del botón al pasar el mouse encima.
        color_texto (tuple): Color del texto del botón.
        fuente (pygame.font.Font): Fuente para el texto.

    Returns:
        bool: True si el botón fue clickeado, False en caso contrario.
    """
    # Obtener la posición del mouse
    mouse_pos = pygame.mouse.get_pos()
    mouse_clic = pygame.mouse.get_pressed()

    # Detectar si el mouse está sobre el botón
    rect_boton = pygame.Rect(x, y, ancho, alto)
    if rect_boton.collidepoint(mouse_pos):
        pygame.draw.rect(pantalla, color_boton_sombreado, rect_boton)  # Color hover
        if mouse_clic[0]:  # Botón izquierdo del mouse presionado
            return True
    else:
        pygame.draw.rect(pantalla, color_boton, rect_boton)  # Color normal

    # Dibujar texto
    texto_superficie = fuente.render(texto, True, color_texto)
    texto_rect = texto_superficie.get_rect(center=rect_boton.center)
    pantalla.blit(texto_superficie, texto_rect)

    return False