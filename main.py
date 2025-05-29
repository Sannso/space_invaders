import pygame
import sys
import random

# Inicializar PyGame
pygame.init()

# Tamaño de la pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invaders para niños")

# FPS
FPS = 60
clock = pygame.time.Clock()

# ------------------- Caracteristicas de Elementos -----------------------
# Cargar fondo
background = pygame.image.load("assets/background.png")
background = pygame.transform.scale(background, (ANCHO, ALTO))

# ------ Jugador
jugador_imagen = pygame.image.load("assets/player.png")
jugador_mid = jugador_imagen.get_width() // 2
jugador_x = ANCHO // 2 - jugador_mid
jugador_y = ALTO - jugador_imagen.get_height()

jugador_size = [jugador_imagen.get_width(), jugador_imagen.get_height()]
velocidad_jugador = 5

# ------- Proyectil
proyectil_img = pygame.image.load("assets/bullet.png")  # Asegúrate de tener esta imagen
proyectil_img = pygame.transform.scale(proyectil_img, (7, 10))
proyectil_mid = proyectil_img.get_width() // 2
proyectil_size = [proyectil_img.get_width(), proyectil_img.get_height()]

# Lista para guardar proyectiles activos
proyectiles = []

# Velocidad del proyectil
velocidad_proyectil = 5

# -------- Enemigo
enemigo_img = pygame.image.load("assets/enemy.png")
enemigo_img = pygame.transform.rotate(enemigo_img, 180)
enemigo = enemigo_img.get_width() // 2
enemigo_size = [enemigo_img.get_width(), enemigo_img.get_height()]

# Lista de enemigos
enemigos = []
velocidad_enemigo = 2

# Crear varios enemigos al inicio
for i in range(5):  # 5 enemigos
    enemigo_x = random.randint(0, ANCHO - 50)
    enemigo_y = random.randint(-150, -50)
    enemigos.append([enemigo_x, enemigo_y])

# --------- Boss ---------
boss_img = pygame.image.load("assets/boss.png")
boss_img = pygame.transform.scale(boss_img, (300, 300))
boss_mid = boss_img.get_width() // 2
boss_size = [boss_img.get_width(), boss_img.get_height()]

boss_x = ANCHO // 2 - boss_mid
boss_y = -boss_img.get_height()
velocidad_boss = 2
vida_boss = 20


# ------------- FUNCIONES --------------------
def pantalla_inicio():
    seleccion = 0  # 0 = Jugar, 1 = Instrucciones
    opciones = ["Jugar", "Instrucciones"]
    esperando = True

    while esperando:
        pantalla.fill((0, 0, 20))  # Fondo oscuro

        titulo_font = pygame.font.SysFont(None, 72)
        opcion_font = pygame.font.SysFont(None, 40)

        titulo = titulo_font.render("SPACE SHOOTER", True, (255, 255, 255))
        subtitulo = titulo_font.render("Prueba Kodland", True, (255, 255, 255))
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 100))
        pantalla.blit(subtitulo, (ANCHO//2 - subtitulo.get_width()//2, 150))

        for i, texto in enumerate(opciones):
            color = (255, 255, 0) if i == seleccion else (200, 200, 200)
            opcion = opcion_font.render(texto, True, color)
            pantalla.blit(opcion, (ANCHO//2 - opcion.get_width()//2, 300 + i * 50))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    if seleccion == 0:
                        esperando = False  # Jugar
                    elif seleccion == 1:
                        mostrar_instrucciones()


def mostrar_instrucciones():
    viendo = True
    while viendo:
        pantalla.fill((0, 0, 30))

        font_titulo = pygame.font.SysFont(None, 48)
        font_texto = pygame.font.SysFont(None, 30)

        titulo = font_titulo.render("Instrucciones", True, (255, 255, 255))
        linea1 = font_texto.render("Mueve tu nave con las flechas izquierda/derecha", True, (200, 200, 200))
        linea2 = font_texto.render("Presiona ESPACIO para disparar", True, (200, 200, 200))
        linea3 = font_texto.render("Evita que los enemigos te toquen o que el jefe llegue abajo", True, (200, 200, 200))
        linea4 = font_texto.render("Presiona ESC para volver", True, (200, 200, 0))

        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 100))
        pantalla.blit(linea1, (ANCHO//2 - linea1.get_width()//2, 180))
        pantalla.blit(linea2, (ANCHO//2 - linea2.get_width()//2, 220))
        pantalla.blit(linea3, (ANCHO//2 - linea3.get_width()//2, 260))
        pantalla.blit(linea4, (ANCHO//2 - linea4.get_width()//2, 320))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    viendo = False



# -------------- Bucle principal -----------------------
def main():
    global jugador_x            # Variables del jugador que cambian en el ciclo
    global proyectiles          # Variables de los proyectiles que cambian en el ciclo
    global boss_y, vida_boss    # Variables del jefe que cambian en el ciclo
    
    # Variables de la partida
    score = 0
    font = pygame.font.SysFont(None, 36)
    game_over = False
    win = False
    
    
    # Bucle menu
    pantalla_inicio()
    
    
    # Bucle juego
    corriendo = True
    while corriendo:
        pantalla.blit(background, (0, 0))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            
            # Presionar una tecla
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    # Crear un nuevo proyectil y guardarlo
                    proyectil_x = jugador_x + jugador_mid - proyectil_mid  # posición del centro de la nave
                    proyectil_y = jugador_y
                    proyectiles.append([proyectil_x, proyectil_y])

        # Movimiento
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jugador_x > 2:
            jugador_x -= velocidad_jugador
        if teclas[pygame.K_RIGHT] and jugador_x < ANCHO - jugador_imagen.get_width()+2:
            jugador_x += velocidad_jugador
  

        # ---------- jugador -----------------
        # Dibujar
        pantalla.blit(jugador_imagen, (jugador_x, jugador_y))

        
        #---------- proyectiles --------------
        # Mover proyectiles
        for proyectil in proyectiles:
            proyectil[1] -= velocidad_proyectil  # se mueve hacia arriba

        # Eliminar proyectiles que salen de la pantalla
        proyectil = [proyectil for proyectil in proyectiles if proyectil[1] > -30]

        # Dibujar proyectiles
        for proyectil in proyectiles:
            pantalla.blit(proyectil_img, (proyectil[0], proyectil[1]))
            
        # ----------- enemigos -------------------
        # Mover enemigos
        for enemigo in enemigos:
            enemigo[1] += velocidad_enemigo

            # Si el enemigo sale por abajo, reinicia arriba
            if enemigo[1] > ALTO:
                enemigo[0] = random.randint(0, ANCHO - 50)
                enemigo[1] = random.randint(-100, -40)

        # Dibujar enemigos
        for enemigo in enemigos:
            pantalla.blit(enemigo_img, (enemigo[0], enemigo[1]))
            
        # ------------ boss ------------------------
        if(len(enemigos) == 0):
            boss_y += velocidad_enemigo
            pantalla.blit(boss_img, (boss_x, boss_y))
            if(boss_y == ALTO - boss_y):
                game_over = True
            
            
        # --------------- Colisiones ----------------------
        # Rectángulo del jugador
        jugador_rect = pygame.Rect(jugador_x, jugador_y, jugador_size[0], jugador_size[1])

        # Verificar colisiones entre balas y enemigos
        for proyectil in proyectiles[:]:  # copiamos la lista para poder modificarla
            proyectil_rect = pygame.Rect(proyectil[0], proyectil[1], proyectil_size[0], proyectil_size[1])

            for enemigo in enemigos[:]:
                enemigo_rect = pygame.Rect(enemigo[0], enemigo[1], enemigo_size[0], enemigo_size[1])

                if proyectil_rect.colliderect(enemigo_rect):
                    proyectiles.remove(proyectil)
                    enemigos.remove(enemigo)

                    # Crear un nuevo enemigo
                    if(score < 8):
                        nuevo_enemigo_x = random.randint(0, ANCHO - 50)
                        nuevo_enemigo_y = random.randint(-100, -40)
                        enemigos.append([nuevo_enemigo_x, nuevo_enemigo_y])

                    score += 1  # sumar puntaje
                    break
                
            if(len(enemigos) == 0):
                boss_rect = pygame.Rect(boss_x, boss_y, boss_size[0], boss_size[1])
                if proyectil_rect.colliderect(boss_rect):
                    proyectiles.remove(proyectil)
                    
                    vida_boss -= 1
                    if(vida_boss == 0):
                        win = True

                    score += 20  # sumar puntaje
                    break
        
        
        # Verificar colisión con enemigos
        for enemigo in enemigos:
            enemigo_rect = pygame.Rect(enemigo[0], enemigo[1], enemigo_size[0], enemigo_size[1])
            
            if jugador_rect.colliderect(enemigo_rect):
                game_over = True
                break
        
        
        # ----------- GAME OVER ---------------
        if game_over:
            over_font = pygame.font.SysFont(None, 72)
            over_text = over_font.render("GAME OVER", True, (255, 0, 0))
            pantalla.blit(over_text, (ANCHO//2 - 180, ALTO//2 - 50))
            
            pygame.display.flip()
            pygame.time.delay(3000)  # Esperar 3 segundos
            corriendo = False
            
        # ----------- WIN ---------------
        if win:
            over_font = pygame.font.SysFont(None, 72)
            over_text = over_font.render("GANASTE!!!!", True, (255, 255, 0))
            pantalla.blit(over_text, (ANCHO//2 - 180, ALTO//2 - 50))
            
            pygame.display.flip()
            pygame.time.delay(5000)  # Esperar 3 segundos
            corriendo = False

        
        # ---------- Mostrar el puntaje --------------
        score_text = font.render(f"Puntos: {score}", True, (255, 255, 255))
        pantalla.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()