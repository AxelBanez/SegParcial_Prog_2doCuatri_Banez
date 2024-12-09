import pygame
from config import ANCHO, ALTURA, ROJO

pygame.init

pantalla = pygame.display.set_mode((ANCHO, ALTURA))


lista_balas = []

# * ----- Variables de las Balas ----- *
ancho_bala, altura_bala = 5, 10
velocidad_bala = 5
tiempo_disparo = 0

def dibujar_balas():
    for bala in lista_balas:
        pygame.draw.rect(pantalla, ROJO, (bala[0], bala[1], ancho_bala, altura_bala))