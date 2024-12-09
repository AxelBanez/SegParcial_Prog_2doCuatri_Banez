import pygame
import random
import json

from balas import *
from config import *
from enemys import *
from explosiones import *

# Inicializamos pygame
pygame.init()

# Configuramos pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTURA))
fondo = cargar_y_redimensionar_imagenes(r"imagenes\fondo_pantalla.jpg", ANCHO, ALTURA)

pygame.display.set_caption("Alpha Mission")
clock = pygame.time.Clock()

# Cargar el icono
icono = pygame.image.load(r"imagenes\naves\nave.png")  # Reemplaza con la ruta de tu imagen
pygame.display.set_icon(icono)

# * ---------- Cargamos imagen de jugador y sus variables ---------- *

ancho_player, altura_player = 70, 70
player_img = cargar_y_redimensionar_imagenes(r"imagenes\naves\nave.png", ancho_player, altura_player)
player_pos = [(ANCHO - ancho_player) // 2, ALTURA - 2 * altura_player]
player_speed = 7

# * ------------ Cargamos imagenes de las explosiones y sus tamaños ------------- *

img_explosion = [cargar_y_redimensionar_imagenes(f"imagenes\\explosiones\\explosion{i}.png", 70, 70)
                for i in range(1, 8)]
img_explosion_comandante = [cargar_y_redimensionar_imagenes(f"imagenes\\explosiones\\explosion{i}.png", 100, 100)
                for i in range(1, 8)]
img_explosion_jefe = [cargar_y_redimensionar_imagenes(f"imagenes\\explosiones\\explosion{i}.png", 150, 150)
                for i in range(1, 8)]

# * -------------------- Cargamos imagenes de las naves enemigas -------------------------- *

ancho_enemy, altura_enemy = dict_enemies["normal"]["ancho"], dict_enemies["normal"]["altura"]
img_enemy = cargar_y_redimensionar_imagenes(r"imagenes\naves\nave_enemiga.png", ancho_enemy, altura_enemy)

ancho_comandante, altura_comandante = dict_enemies["comandante"]["ancho"], dict_enemies["comandante"]["altura"]
img_comandante = cargar_y_redimensionar_imagenes(r"imagenes\naves\nave_comandante.png", ancho_comandante, altura_comandante)

ancho_jefe, altura_jefe = dict_enemies["jefe"]["ancho"], dict_enemies["jefe"]["altura"]
img_jefe = cargar_y_redimensionar_imagenes(r"imagenes\naves\nave_jefe.png", ancho_jefe, altura_jefe)

# *--------------------------------------- FUNCIONES -------------------------------------------------*

def manejar_colisiones():
    """Maneja las colisiones entre balas y enemigos."""

    global lista_explosiones, puntaje

    balas_a_eliminar = []

    for bala in lista_balas[:]:
        bala_rect = pygame.Rect(bala[0], bala[1], ancho_bala, altura_bala)

        for enemy in lista_enemies[:]:
            # Obtener los datos del enemigo (sin explosión, solo los datos básicos)
            enemigo_data = dict_enemies[enemy["tipo"]]

            # Crear el rectángulo del enemigo usando el ancho y la altura del diccionario
            enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemigo_data["ancho"], enemigo_data["altura"])

            # Colisión
            if bala_rect.colliderect(enemy_rect):  # Verifica la colisión
                enemy["salud"] -= 1
                balas_a_eliminar.append(bala)

                if enemy["salud"] <= 0:
                    # Dependiendo del tipo de enemigo, elige las imágenes de explosión correspondientes
                    if enemy["tipo"] == "jefe":
                        explosion_img = img_explosion_jefe
                    elif enemy["tipo"] == "comandante":
                        explosion_img = img_explosion_comandante
                    else:  # Enemigo normal
                        explosion_img = img_explosion

                    lista_explosiones.append({
                        "x": enemy["x"], 
                        "y": enemy["y"],
                        "tipo": enemy["tipo"], 
                        "frame": 0,  # Inicio de la animación
                        "explosion_img": explosion_img  # Añadir las imágenes de explosión
                    })

                    explosion_sonido.play()

                    lista_enemies.remove(enemy)

                    puntaje = sumar_puntos(enemy, puntaje)

    # Eliminar balas que colisionaron
    for bala in balas_a_eliminar:
        if bala in lista_balas:
            lista_balas.remove(bala)

def mover_enemigos():
    """Actualiza la posición de los enemigos en pantalla."""
    global vidas

    for enemy in lista_enemies:
        # Accedemos a los datos del enemigo usando el tipo
        datos_enemy = dict_enemies[enemy["tipo"]]
        enemy["y"] += datos_enemy["velocidad"]
        if enemy["y"] > ALTURA:
            lista_enemies.remove(enemy)
            vidas -= 1

def dibujar_explosiones():
    """Dibuja las explosiones en pantalla."""
    for explosion in lista_explosiones:
        if explosion["tipo"] == "jefe":
            img = img_explosion_jefe[explosion["frame"]]

        elif explosion["tipo"] == "comandante":
            img = img_explosion_comandante[explosion["frame"]]

        else:
            img = img_explosion[explosion["frame"]]

        pantalla.blit(img, (explosion["x"], explosion["y"]))

def menu_pausa():
    """Muestra el menu de pausa y permite interactuar con el mouse."""

    pausa = True
    fondo_y = 0

    while pausa:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Fondo del menu de pausa y movimiento de fondo
        fondo_y += 1
        if fondo_y >= ALTURA:
            fondo_y = 0
            
        pantalla.blit(fondo, (0, fondo_y))
        pantalla.blit(fondo, (0, fondo_y - ALTURA))

        # Titulo
        texto_pausa = fuente.render("Juego en Pausa", True, BLANCO)
        pantalla.blit(texto_pausa, (ANCHO // 2 - texto_pausa.get_width() // 2, ALTURA // 4))

        # Botones

        if crear_boton(pantalla, "Reanudar", ANCHO // 2 - 100, ALTURA // 2 - 60, 200, 50, GRIS_CLARO, GRIS_OSCURO, NEGRO, fuente):
            pausa = False
        if crear_boton(pantalla, "Salir", ANCHO // 2 - 100, ALTURA // 2 + 20, 200, 50, GRIS_CLARO, GRIS_OSCURO, NEGRO, fuente):
            guardar_nombre_y_puntaje_en_json(nombre, puntaje)
            pygame.quit()
            exit()
        
        pygame.display.flip()
        clock.tick(FPS)

def pantalla_bienvenida():
    """Muestra la pantalla de inicio hasta que el jugador seleccione una opcion."""
    fondo_y = 0  # Para el movimiento del fondo

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        # Movimiento del fondo
        fondo_y += 1
        if fondo_y >= ALTURA:
            fondo_y = 0

        pantalla.blit(fondo, (0, fondo_y))
        pantalla.blit(fondo, (0, fondo_y - ALTURA))

        # Titulo
        titulo_juego = fuente.render("Alpha Mission", True, BLANCO)
        pantalla.blit(titulo_juego, (ANCHO // 2 - titulo_juego.get_width() // 2, ALTURA // 4))

        if crear_boton(pantalla, "Jugar", ANCHO // 2 - 100, ALTURA // 2 - 60, 200, 50, GRIS_CLARO, GRIS_OSCURO, NEGRO, fuente):
            nombre = ingresar_nombre()

            return nombre
            
        # if crear_boton(pantalla, "Ranking", ANCHO // 2 - 100, ALTURA // 2 + 20, 200, 50, GRIS_CLARO, GRIS_OSCURO, NEGRO, fuente):
        #     # pausa = False
        #     pass
        if crear_boton(pantalla, "Salir", ANCHO // 2 - 100, ALTURA // 2 + 100, 200, 50, GRIS_CLARO, GRIS_OSCURO, NEGRO, fuente):
            pygame.quit()
            exit()

        pygame.display.flip()
        clock.tick(FPS)

def fin_de_juego(pantalla, puntos, nombre_jugador):
    """Muestra una pantalla de fin de juego con el nombre y puntaje del jugador conseguidos en la partida.

    Args:
        pantalla (pygame.Surface): Superficie donde se mostrara el fin del juego.
        puntos: puntaje del jugador.
        nombre_jugador: nombre del jugador.

    Returns:
        Me retorna un string que diga Inico o Salir
    """
    end_game = True
    fondo_y = 0  # Para el movimiento del fondo

    while end_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
        # Movimiento del fondo
        fondo_y += 1
        if fondo_y >= ALTURA:
            fondo_y = 0

        pantalla.blit(fondo, (0, fondo_y))
        pantalla.blit(fondo, (0, fondo_y - ALTURA))

        texto_fin = fuente.render("fin de juego", True, (BLANCO))
        texto_puntos = fuente.render(f"puntos: {puntos}", True, (BLANCO))
        texto_nombre = fuente.render(f"jugador: {nombre_jugador}", True, (BLANCO))

        # Centramos los textos en la pantalla
        pantalla.blit(texto_fin, ((pantalla.get_width() - texto_fin.get_width()) // 2, 150))
        pantalla.blit(texto_puntos, ((pantalla.get_width() - texto_puntos.get_width()) // 2, 250))
        pantalla.blit(texto_nombre, ((pantalla.get_width() - texto_nombre.get_width()) // 2, 300))
        
        if crear_boton(pantalla, "volver a jugar", ANCHO // 2 - 300 // 2, ALTURA // 2 + 20, 300, 50, GRIS_CLARO, GRIS_OSCURO, NEGRO, fuente):
            return "reiniciar"

        if crear_boton(pantalla, "salir", ANCHO // 2 - 100, ALTURA // 2 + 100, 200, 50, GRIS_CLARO, GRIS_OSCURO, NEGRO, fuente):
            pygame.quit()
            exit()
            return "salir"

        pygame.display.flip()  # Actualizamos la pantalla
        clock.tick(FPS)


def guardar_nombre_y_puntaje_en_json(nombre, puntaje):
    """Guarda el nombre del jugador en un archivo JSON."""
    archivo = "players.json"
    try:
        # Cargar datos existentes
        with open(archivo, "r") as file:
            datos = json.load(file)
    except FileNotFoundError:
        datos = []  # Si el archivo no existe, comenzamos con una lista vacía

    # Añadir el nuevo jugador
    datos.append({"nombre": nombre, "puntaje": puntaje})

    # Guardar de nuevo en el archivo
    with open(archivo, "w") as file:
        json.dump(datos, file, indent=4)

def ingresar_nombre():
    """Pantalla para que el jugador ingrese su nombre."""
    nombre = ""  # Inicialmente vacío
    texto_activo = True  # Estado del cuadro de texto
    fondo_y = 0
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # exit()

            if event.type == pygame.KEYDOWN:
                if texto_activo:

                    if event.key == pygame.K_RETURN:  # Presionar Enter para confirmar
                        guardar_nombre_y_puntaje_en_json(nombre, 0)
                        return nombre
                    
                    elif event.key == pygame.K_BACKSPACE:  # Borrar el último carácter
                        nombre = nombre[:-1]
                    else:
                        # Agregar solo caracteres alfabéticos y limitar a 15 caracteres
                        if len(nombre) < 10 and event.unicode.isalpha():
                            nombre += event.unicode

        # Movimiento del fondo
        fondo_y += 1
        if fondo_y >= ALTURA:
            fondo_y = 0

        pantalla.blit(fondo, (0, fondo_y))
        pantalla.blit(fondo, (0, fondo_y - ALTURA))

        # Texto de entrada
        texto_instruccion = fuente.render("ingrese su nick", True, BLANCO)
        pantalla.blit(texto_instruccion, (ANCHO // 2 - texto_instruccion.get_width() // 2, ALTURA // 3))

        # Mostrar el nombre ingresado
        cuadro_texto = pygame.Rect(ANCHO // 2 - 150, ALTURA // 2 - 25, 300, 50)
        pygame.draw.rect(pantalla, GRIS_CLARO, cuadro_texto)
        pygame.draw.rect(pantalla, BLANCO, cuadro_texto, 2)  # Borde del cuadro
        texto_nombre = fuente.render(nombre, True, NEGRO)
        pantalla.blit(texto_nombre, (cuadro_texto.x + 10, cuadro_texto.y + 10))

        pygame.display.flip()
        clock.tick(FPS)

def mostrar_info(puntaje, tiempo, vidas):
    minutos = tiempo // 3600  # dado que los fps son 60 que FPS = 60
    segundos = (tiempo // 60) % 60
    texto_puntaje = fuente.render(f"puntos: {puntaje}", True, BLANCO)
    texto_tiempo = fuente.render(f"tiempo: {minutos}:{segundos:02}", True, BLANCO)
    
    texto_vidas = fuente.render(f"vidas: {vidas}", True, BLANCO)

    pantalla.blit(texto_puntaje, (10, 10))
    pantalla.blit(texto_tiempo, (ANCHO - texto_tiempo.get_width() - 10, 10))
    pantalla.blit(texto_vidas, (10, 40))

def sumar_puntos(enemy, puntaje):
    """
    Suma puntos al destruir enemigos.
    """
    if enemy["tipo"] == "normal":
        puntaje += 10
    elif enemy["tipo"] == "comandante":
        puntaje += 20
    elif enemy["tipo"] == "jefe":
        puntaje += 30
    
    return puntaje

def dibujar_enemigos():
    for enemy in lista_enemies:
        if enemy["tipo"] == "jefe":
            pantalla.blit(img_jefe, (enemy["x"], enemy["y"]))
        elif enemy["tipo"] == "comandante":
            pantalla.blit(img_comandante, (enemy["x"], enemy["y"]))
        else:
            pantalla.blit(img_enemy, (enemy["x"], enemy["y"]))


# --------------------------------------------------------------------------------------------

nombre = pantalla_bienvenida()

# Variables para puntaje, tiempo y vidas
puntaje = 0
tiempo = 0
vidas = 3  

# Bucle principal
run = True
fondo_y = 0


while run:
    tiempo += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu_pausa()  # Llamar al menú de pausa
    
    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < ANCHO - ancho_player:
        player_pos[0] += player_speed
    if keys[pygame.K_SPACE] and tiempo_disparo == 0:
        lista_balas.append([player_pos[0] + (ancho_player - ancho_bala) // 2, player_pos[1]])
        tiempo_disparo = 10

        pygame.mixer.Channel(0).play(disparo_sonido) # 

    # Enfriamiento de disparo
    if tiempo_disparo > 0:
        tiempo_disparo -= 1

    # Movimiento de balas
    for bala in lista_balas[:]:
        bala[1] -= velocidad_bala
        if bala[1] < 0:  # Fuera de la pantalla
            lista_balas.remove(bala)

    # Crear enemigos si no hay
    if not lista_enemies:
        for _ in range(5):
            crear_enemigo()
    elif random.random() < 0.02:  # Probabilidad de que aparezcan enemigos
        crear_enemigo()

    # Actualizaciones
    mover_enemigos()
    manejar_colisiones()
    actualizar_explosiones()
    
    # Sumamos puntos al destruir enemigos
    for enemy in lista_enemies[:]:
        if enemy["salud"] <= 0:
            puntaje = sumar_puntos(enemy, puntaje)

    if vidas <= 0:
        guardar_nombre_y_puntaje_en_json(nombre, puntaje)
        resultado = fin_de_juego(pantalla, puntaje, nombre)

        if resultado == "reiniciar":
            puntaje = 0
            tiempo = 0
            vidas = 3
            lista_enemies.clear()
            lista_balas.clear()

        elif resultado == "salir":
            run = False # finalizamos el juego


    # Dibujar en pantalla
    fondo_y += 2   # Movimiento de fondo
    if fondo_y >= ALTURA:
        fondo_y = 0

    pantalla.blit(fondo, (0, fondo_y))
    pantalla.blit(fondo, (0, fondo_y - ALTURA))
    pantalla.blit(player_img, player_pos)

    dibujar_balas()
    dibujar_enemigos()

    mostrar_info(puntaje, tiempo, vidas)

    dibujar_explosiones()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()