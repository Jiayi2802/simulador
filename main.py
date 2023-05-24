import pygame
import sys
import time
import asyncio
import random
import math
import tkinter as tk


pygame.init()
reloj = pygame.time.Clock()
tiempo_anterior = int(pygame.time.get_ticks()/1000)
prev_x_pos = 0
prev_y_pos = 0
pygame.mixer.music.load('D:\ETSIAE\python y javas\python\simulador\imagenes y sonidos\sonidofondo.mp3')
sonido_motor = pygame.mixer.Sound("D:\ETSIAE\python y javas\python\simulador\imagenes y sonidos\sonido_motor.mp3")
sonido_explosion = pygame.mixer.Sound("D:\ETSIAE\python y javas\python\simulador\imagenes y sonidos\sonido_explosion.mp3")
sonido_victoria = pygame.mixer.Sound("D:\ETSIAE\python y javas\python\simulador\imagenes y sonidos\sonido_victoria.mp3")
pygame.mixer.music.play(-1)
WIDTH = 800
HEIGHT = 600
VISIBLE_WIDTH = 1000
VISIBLE_HEIGHT = 600
font = pygame.font.Font(None, 20) #fuente de tamaño 30, none = archivo de fuente

camera_surface = pygame.Surface((VISIBLE_WIDTH, VISIBLE_HEIGHT))

screen = pygame.display.set_mode((WIDTH, 750))
pygame.display.set_caption('Simulador de vuelo') #título del programa
alfa = 0 #angulo de ataque del avion
#--------------------portada-------------------
portada_visible = True
portada_image = pygame.image.load("D:/ETSIAE/python y javas/python/simulador/imagenes y sonidos/portada.png").convert_alpha() # cargar la portada
new_size_portada = (800, 750) #cambiar el tamaño de la foto descargado
class portada():
    def __init__(self):
        self.image = pygame.transform.scale(portada_image, (new_size_portada))
        self.rect = self.image.get_rect()    #coordenada y tamaño del fondo
        self.rect.center = (WIDTH // 2, HEIGHT // 2)


instruccion_visible = False
instruccion_image = pygame.image.load("D:/ETSIAE/python y javas/python/simulador/imagenes y sonidos/instruccion.png").convert_alpha() # cargar la portada
new_size_instruccion = (800, 750) #cambiar el tamaño de la foto descargado
class instruccion():
    def __init__(self):
        self.image = pygame.transform.scale(instruccion_image, (new_size_instruccion))
        self.rect = self.image.get_rect()    #coordenada y tamaño del fondo
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

#-------------- Configuración del menú desplegable------------
menu_visible = False
menu_items = ['Llegar al ','aeropueto más', 'próximo: 3000Km']
color_menu = (200, 200, 200)
color_texto = (0, 0, 0)

# Definir la función que se ejecuta cuando se hace clic en "Opción 1"
def opcion_1():
    print("Seleccionaste la opción 1")

# Definir la función que se ejecuta cuando se hace clic en "Opción 2"
def opcion_2():
    print("Seleccionaste la opción 2")

#----------------Datos de nuestro aeronave----------------

original_image = pygame.image.load("D:/ETSIAE/python y javas/python/simulador/imagenes y sonidos/avion.png").convert_alpha() # cargar la imagen del avion y establecer la transparencia
new_size = (100, 100) #cambiar el tamaño de la foto descargado
class Avion(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(original_image, new_size)
        self.rect = self.image.get_rect()    #coordenada y tamaño del avion
        self.rect.center = (100, 549)
        self.traccion = 0.1
        self.aceleracion = 0
        self.sustentacion = 0
        self.velocidad_x = 0
        self.alfa = 0
        self.masa = 300
        self.K = 1
        self.Cd0 = 0.12

        # .....gravedad......
        self.gravity = 3
        self.dy = 0  # velocidad vertical


        #--------Densidad de la atmósfera--------
        self.densidad=1.225

        #--------superficie alar-----
        self.Sw = 1
        #--------coeficiente de sustentación------
        self.Cl = 1
        self.Cd = self.aceleracion * self.Sw


    # -----------------Movimiento del avión-------------
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.alfa += 0.1
        if keys[pygame.K_s]:
            self.alfa -= 0.1
        if keys[pygame.K_UP]:
            if self.aceleracion <= 20:
             self.aceleracion += self.traccion
            else:
               self.aceleracion = 20
        if keys[pygame.K_DOWN]:
            self.aceleracion -= self.traccion

    
        #----------sustentación al movimiento------
        self.densidad=1.2*(1+(avion.rect.y+500)/12500)  #Densidad del aire según ISA
        
        if self.alfa < 16:
         self.Cl = 0.1+ 2*3.14*self.alfa/100  #Coeficiente de sustentación de una placa plana 2D
         self.Cd = self.Cd0+(self.K*self.Cl**2)/1000
        else:
            self.Cl = 2*3.14*self.alfa/100 - 2*3.14*(self.alfa/100) #entrada en perdida debida al exceso angulo de ataque
            self.Cd = self.Cd0*self.alfa/100 +(self.K*self.Cl**2)/1000
     
    
        
        self.peso = self.gravity*self.masa
        self.aceleracion_x = self.aceleracion*math.cos(math.radians(self.alfa))/1000
        self.aceleracion_y = self.aceleracion*math.sin(math.radians(self.alfa))
        
        if self.velocidad_x < self.aceleracion:
         self.velocidad_x = self.velocidad_x + 0.5*self.aceleracion_x
        else:
         self.velocidad_x = self.velocidad_x -0.005*abs(self.velocidad_x-self.aceleracion_x)

        self.sustentacion = -0.5*self.aceleracion_y**2*self.densidad*self.Sw*self.Cl
        self.resistencia = 0.5*self.aceleracion_x**2*self.densidad*self.Sw*self.Cd

        if self.resistencia < self.velocidad_x:
         self.resistencia = 0.5*self.aceleracion_x**2*self.densidad*self.Sw*self.Cd
        else:
            self.resistencia = 0
        #-------- Equilibrio de fuerzas
        self.rect.y +=self.sustentacion + self.gravity
        self.rect.x += self.velocidad_x - self.resistencia


        # -------Mantener la cámara enfocado al avion
        

#---------FONDO de la pantalla----------
background_image = pygame.image.load("D:/ETSIAE/python y javas/python/simulador/imagenes y sonidos/fondo3.jpg").convert() # cargar la imagen del avion y establecer la transparencia
new_size_FONDO = (WIDTH, HEIGHT) #cambiar el tamaño de la foto descargado
class fondo():
    def __init__(self):
        self.image = pygame.transform.scale(background_image, (new_size_FONDO))
        self.rect = self.image.get_rect()    #coordenada y tamaño del fondo
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

indicador_image = pygame.image.load("D:/ETSIAE/python y javas/python/simulador/imagenes y sonidos/indicador.png").convert_alpha() # cargar la imagen del avion y establecer la transparencia
new_size_indicador = (WIDTH, HEIGHT//4) #cambiar el tamaño de la foto descargado
class indicador():
    def __init__(self):
        self.image = pygame.transform.scale(indicador_image, (new_size_indicador))
        self.rect = self.image.get_rect()    #coordenada y tamaño del fondo
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
                            
suelo_image = pygame.image.load("D:/ETSIAE/python y javas/python/simulador/imagenes y sonidos/suelo.png").convert() # cargar la imagen del avion y establecer la transparencia
new_size_suelo = (WIDTH, HEIGHT/8) #cambiar el tamaño de la foto descargado
class suelo():
    def __init__(self):
        self.image = pygame.transform.scale(suelo_image, (new_size_suelo))
        self.rect = self.image.get_rect()    #coordenada y tamaño del suelo
        self.rect.center = (WIDTH // 2, HEIGHT-20)


bosque_image = pygame.image.load("D:/ETSIAE/python y javas/python/simulador/imagenes y sonidos/bosque.png").convert_alpha() # cargar la imagen del avion y establecer la transparencia
new_size_bosque = (WIDTH/2, HEIGHT/2) #cambiar el tamaño de la foto descargado
class bosque():
    def __init__(self):
        self.image = pygame.transform.scale(bosque_image, (new_size_bosque))
        self.rect = self.image.get_rect()    #coordenada y tamaño del suelo
        self.rect.center = (WIDTH //2 , HEIGHT//2)



mando_image = pygame.image.load("D:/ETSIAE/python y javas/python/simulador/imagenes y sonidos/mando.png").convert_alpha() # cargar la imagen del avion y establecer la transparencia
new_size_mando = (40, 30) #cambiar el tamaño de la foto descargado
class mando():
    def __init__(self):
        self.image = pygame.transform.scale(mando_image, (new_size_mando))
        self.rect = self.image.get_rect()    #coordenada y tamaño del suelo
        self.rect.center = (WIDTH // 2, HEIGHT-20)

hangar_image = pygame.image.load("D:/ETSIAE/python y javas/python/simulador/imagenes y sonidos/hangar.png").convert_alpha() # cargar la imagen del avion y establecer la transparencia
new_size_hangar = (300, 300) #cambiar el tamaño de la foto descargado
class hangar():
    def __init__(self):
        self.image = pygame.transform.scale(hangar_image, (new_size_hangar))
        self.rect = self.image.get_rect()    #coordenada y tamaño del suelo
        self.rect.center = (WIDTH // 2, HEIGHT-20)

explosion_image = pygame.image.load("D:/ETSIAE/python y javas/python/simulador/imagenes y sonidos/explosion.png").convert_alpha() # cargar la imagen del avion y establecer la transparencia
new_size_explosion = (500, 300) #cambiar el tamaño de la foto descargado
class explosion():
    def __init__(self):
        self.image = pygame.transform.scale(explosion_image, (new_size_explosion))
        self.rect = self.image.get_rect()    #coordenada y tamaño del suelo
        self.rect.center = (100, 550)

#----------Menu desplegable----------------

def dibujar_menu():
    menu_superficie = pygame.Surface((160, 80))
    menu_superficie.fill(color_menu)
    for i, item in enumerate(menu_items):
        texto = pygame.font.SysFont(None, 24).render(item, True, color_texto)
        menu_superficie.blit(texto, (10, i*25 + 5))   
    screen.blit(menu_superficie, (10, 40))

#-------------------------Game over------------------------------

def mostrar_game_over():
    font = pygame.font.Font(None, 50)  # Fuente y tamaño del texto
    texto = font.render("Game Over", True, (255, 0, 0))  # Color del texto: rojo
    texto_rect = texto.get_rect(center=(WIDTH/2, HEIGHT/2))  # Posición del texto
    screen.blit(texto, texto_rect)
    pygame.display.flip()  # Actualizar la pantalla
    sonido_explosion.play() 
    avion.rect.x = 100
    avion.rect.y = 549
    avion.traccion = 0.1
    avion.aceleracion = 0
    avion.sustentacion = 0
    avion.velocidad_x = 0
    avion.alfa = 0


#---------------------------victoria------------------------------------------

def mostrar_victoria():
    font = pygame.font.Font(None, 50)  # Fuente y tamaño del texto
    texto = font.render("Misión Exitosa", True, (255, 0, 0))  # Color del texto: rojo
    texto_rect = texto.get_rect(center=(WIDTH/2, HEIGHT/2))  # Posición del texto
    screen.blit(texto, texto_rect)
    pygame.display.flip()  # Actualizar la pantalla


#-------------Entrada en pérdida-------------

#-----------Cuadro de datos----------
avion = Avion()
fondo = fondo()
suelo = suelo()
bosque = bosque()
indicador = indicador()
menu = dibujar_menu()
portada = portada()
instruccion = instruccion()
mando = mando()
hangar = hangar()
explosion = explosion()
#----------Bucle para actualizar el estado del avión---------------- 

simulador = True
while simulador:
    tiempo_actual = int(pygame.time.get_ticks()/1000) #contador de segundos

    for event in pygame.event.get():

        # if event.type == pygame.KEYDOWN:
        #      menu.draw()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                sonido_motor.play() 

            if event.key ==pygame.K_SPACE:
               instruccion_visible = False


        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1 and portada_visible:
                portada_visible = False
                instruccion_visible = True

    
            if event.button == 1 and not menu_visible:
                menu_visible = True
            elif event.button == 1 and menu_visible:
                menu_visible = False
            
   
    #-----------pantalla principal-------------
    #fondo de pantalla
    screen.fill((39, 67, 98))
    camera_x = -avion.rect.x 
    camera_y = -avion.rect.y 
    
    n = int(avion.rect.x/WIDTH)+1
    m = int(-avion.rect.y/HEIGHT)+1

    screen.blit(fondo.image, (camera_x + WIDTH*n, camera_y + HEIGHT)) # fondo derecha abajo
    screen.blit(fondo.image, (camera_x + WIDTH*(n-1), camera_y + HEIGHT)) # fondo derecha abajo

    screen.blit(fondo.image, (camera_x + WIDTH*n, camera_y-HEIGHT*m ))  #fondo derecha arriba
    screen.blit(fondo.image, (camera_x + WIDTH*n, camera_y-HEIGHT*(m-1) ))  #fondo derecha arriba
    screen.blit(fondo.image, (camera_x + WIDTH*(n-1), camera_y-HEIGHT*m ))  #fondo derecha arriba
    screen.blit(fondo.image, (camera_x + WIDTH*(n-1), camera_y-HEIGHT*(m-1) ))  #fondo derecha arriba
    

    screen.blit(bosque.image, (camera_x + WIDTH*n,820-avion.rect.y)) #representacion del bosque
    screen.blit(bosque.image, (camera_x + WIDTH*(n+0.5),820-avion.rect.y)) #representacion del bosque
    screen.blit(bosque.image, (camera_x + WIDTH*(n-1),820-avion.rect.y)) #representacion del bosque
    screen.blit(bosque.image, (camera_x + WIDTH*(n-0.5),820-avion.rect.y)) #representacion del bosque
    if avion.rect.x < 3000:
     screen.blit(suelo.image, (camera_x + WIDTH*n,1050-avion.rect.y)) #representacion del suelo
     screen.blit(suelo.image, (camera_x + WIDTH*(n-1),1050-avion.rect.y)) #representacion del suelo

    if avion.rect.x > 30000 and avion.rect.x< 33000:
     screen.blit(suelo.image, (camera_x + WIDTH*n,1050-avion.rect.y)) #representacion del suelo
     screen.blit(suelo.image, (camera_x + WIDTH*(n-1),1050-avion.rect.y)) #representacion del suelo



    pygame.draw.rect(screen, (178, 218, 255), (410, 600, 120, 120)) #indicador de actitud
    screen.blit(hangar.image, (camera_x,camera_y+820)) #representacion del hangar
    screen.blit(hangar.image, (4800,camera_y+820)) #representacion del hangar
    horizonte = 660 + avion.alfa #indicador de actitud
    pygame.draw.rect(screen, (61, 59, 24), (410, horizonte, 120, 60)) #indicador de actitud
    screen.blit(indicador.image, (0,600)) #representacion del suelo

   


    if avion.alfa <= 0 :
        screen.blit(mando.image, (632.5, 615)) #mando para flaps del avion
    elif avion.alfa >= 18:
       screen.blit(mando.image, (632.5, 705)) #mando para flaps del avion
    else:
       flaps = 615 + avion.alfa*5
       screen.blit(mando.image, (632.5, flaps)) #mando para flaps del avion



    if avion.aceleracion <= 0 :
     screen.blit(mando.image, (732, 613)) #Empuje del avion
    elif avion.aceleracion >= 20:
       screen.blit(mando.image, (732, 710)) #Empuje del avion
    else:  
     empuje = 613 + avion.aceleracion*5
     screen.blit(mando.image, (732, empuje)) #Empuje del avion

    

    
    #----------------velocidad del avion------------------------------------------


    
    elapsed_time = tiempo_actual - tiempo_anterior

    # Calcular la velocidad
    vel_x = (avion.rect.x - prev_x_pos) / (elapsed_time+0.02)
    vel_y = (avion.rect.y - prev_y_pos) / (elapsed_time+0.02)

    # Limitar la velocidad máxima
    velocidad = (vel_x ** 2 + vel_y ** 2) ** 0.5

    # Guardar la posición y tiempo actuales como previos para la siguiente iteración
    prev_x_pos = avion.rect.x
    prev_y_pos = avion.rect.y
    tiempo_anterior = tiempo_actual

   #------------------------game over--------------------------------




    # -----------------------------------Dibujar el menú desplegable------------------
    texto_boton = pygame.font.SysFont(None, 24).render('Misión actual:', True, color_texto)
    rect_boton = texto_boton.get_rect()
    rect_boton.topleft = (10, 10)
    screen.blit(texto_boton, rect_boton)
    # Dibujar menú si está visible
    if menu_visible:
        dibujar_menu()

   


    #------------------------avion------------------------------
    

    
    imagen_avion = pygame.transform.rotate(avion.image, avion.alfa)

    dif = avion.rect.y-100
    if avion.rect.y < 100:
        v=1
    else:
        v=0

    if avion.rect.x < WIDTH/2:
     screen.blit(imagen_avion, avion.rect) #representación del avión inicial

    if avion.rect.x > WIDTH/2:
        screen.blit(imagen_avion, (WIDTH/2,avion.rect.y-dif*v)) # Movimiento de la cámara para evitar que el avion salga de la pantalla

    if avion.rect.y > 500:
        avion.rect.y = 500 # Movimiento de la cámara = avión inmóvil


    if avion.rect.y == 500 and vel_y >150:
     screen.blit(explosion.image, (WIDTH/2,HEIGHT/2))
     mostrar_game_over()
     pygame.time.wait(3000)  # Esperar 2 segundos (ajusta el tiempo según tus necesidades)  # Detener el juego
     screen.blit(explosion.image, (WIDTH/2-150,HEIGHT/2+200))
     mostrar_game_over()
     pygame.time.wait(3000)  # Esperar 2 segundos (ajusta el tiempo según tus necesidades)  # Detener el juego


    if avion.rect.y == 500 and avion.rect.x < 30000 and avion.rect.x > 3000 :
     screen.blit(explosion.image, (WIDTH/2,HEIGHT/2))
     mostrar_game_over()
     pygame.time.wait(3000)  # Esperar 2 segundos (ajusta el tiempo según tus necesidades)  # Detener el juego
     screen.blit(explosion.image, (WIDTH/2-150,HEIGHT/2+200))
     mostrar_game_over()
     pygame.time.wait(3000)  # Esperar 2 segundos (ajusta el tiempo según tus necesidades)  # Detener el juego


    if avion.rect.y == 500 and avion.rect.x > 33000 :
     screen.blit(explosion.image, (WIDTH/2,HEIGHT/2))
     mostrar_game_over()
     pygame.time.wait(3000)  # Esperar 2 segundos (ajusta el tiempo según tus necesidades)  # Detener el juego
     screen.blit(explosion.image, (WIDTH/2-150,HEIGHT/2+200))
     mostrar_game_over()
     pygame.time.wait(3000)  # Esperar 2 segundos (ajusta el tiempo según tus necesidades)  # Detener el juego


    if 24860-avion.velocidad_x*100 <=0:
       avion.sustentacion = 0
       avion.aceleracion = 0

    

    if avion.rect.x/10 > 500 and avion.velocidad_x < 1 :
      sonido_victoria.play() 
      mostrar_victoria()
      pygame.time.wait(8000)  # Esperar 2 segundos (ajusta el tiempo según tus necesidades)  # Detener el juego
      simulador = False
  

    
    altura = font.render(f"ALT    {-avion.rect.y+500}", True, (255, 0, 0))  #cuadro de coordenada del avión
    alcance = font.render(f"R     {avion.rect.x/10}", True, (255, 0, 0))  #cuadro de coordenada del avión
    tiempo = font.render(f"Tiempo de misión: {tiempo_actual}", True, (0, 0, 255))  #cuadro de tiempo del avión
    velocidad = font.render(f"SPD    {int(velocidad)}", True, (255, 0, 0))  #cuadro de velocidad del avión
    combustible = font.render(f"FUEL {int(24860-avion.velocidad_x*100)}", True, (255, 0, 0))  #cuadro de velocidad del avión
    densidad = font.render(f"RHO: {int(avion.densidad*100)/100}", True, (255, 0, 0))  #cuadro de velocidad del avión
    alfa = font.render(f"º   {int(avion.alfa*100)/100}", True, (255, 0, 0))  #cuadro de velocidad del avión

    #panel de datos
    screen.blit(tiempo, (600, 10)) #representación de tiempo
    screen.blit(altura, (115, 610)) #representación de la coordenada
    screen.blit(alcance, (210, 610)) #representación de la coordenada
    screen.blit(velocidad, (295, 610)) #representación de la coordenada
    screen.blit(combustible, (110, 680)) #representación de tiempo
    screen.blit(densidad, (210, 680)) #representación de tiempo
    screen.blit(alfa, (300, 680)) #representación de tiempo
    if portada_visible:
     screen.blit(portada.image,(0,0))
    
    if instruccion_visible:
     screen.blit(instruccion.image,(0,0))

    avion.update()
    pygame.display.flip() #actualiza la ventana
    reloj.tick(60)  # limita a 60fps

    









    