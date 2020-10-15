import pygame, sys
from pygame.locals import *
import math, random

# CONSTANTES
# Constantes para o tamanho da tela
LARGURA_TELA = 640
ALTURA_TELA = 480
# Será utilizado para a velocidade do jogo
FPS = 200
# cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)


def carregaImagens():
    global coelho
    global grama
    global castelo
    global flecha
    global inimigoImg
    global vidaBarra
    global vidaResto
    global ganhou
    global gameover
    coelho = pygame.image.load("resources/images/dude.png")
    grama = pygame.image.load("resources/images/grass.png")
    castelo = pygame.image.load("resources/images/castle.png")
    flecha = pygame.image.load("resources/images/bullet.png")
    inimigoImg = pygame.image.load("resources/images/badguy.png")
    vidaBarra = pygame.image.load("resources/images/healthbar.png")
    vidaResto = pygame.image.load("resources/images/health.png")
    gameover = pygame.image.load("resources/images/gameover.png")
    ganhou = pygame.image.load("resources/images/youwin.png")


def configuracaoSom():
    global hitSom
    global inimigoSom
    global tiroSom
    hitSom = pygame.mixer.Sound("resources/audio/explode.wav")
    inimigoSom = pygame.mixer.Sound("resources/audio/enemy.wav")
    tiroSom = pygame.mixer.Sound("resources/audio/shoot.wav")
    hitSom.set_volume(0.05)
    inimigoSom.set_volume(0.05)
    tiroSom.set_volume(0.05)
    pygame.mixer.music.load('resources/audio/moonlight.wav')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.25)


def desenharArena():
    carregaImagens()
    for x in range(LARGURA_TELA // grama.get_width() + 1):
        for y in range(ALTURA_TELA // grama.get_height() + 1):
            DISPLAYSURF.blit(grama, (x * 100, y * 100))

    for y in range(30, 350, 105):
        DISPLAYSURF.blit(castelo, (0, y))

    # atualizar tempo restante
    font = pygame.font.Font(None, 24)
    texto = font.render(str((90000 - pygame.time.get_ticks()) // 60000) + ":" + str(
        (90000 - pygame.time.get_ticks()) // 1000 % 60).zfill(2), True, (0, 0, 0))
    textoRect = texto.get_rect()
    textoRect.topright = [635, 5]
    DISPLAYSURF.blit(texto, textoRect)

    # atualizar barra de vida
    DISPLAYSURF.blit(vidaBarra, (5, 5))
    for valor in range(vida):
        DISPLAYSURF.blit(vidaResto, (valor + 8, 8))


def desenhaCoelho(coelhoPos):
    DISPLAYSURF.blit(coelho, (coelhoPos[0], coelhoPos[1]))


def moveCoelho(teclas, coelhoPos):
    if teclas[0] and coelhoPos[1] > 0:
        coelhoPos[1] -= 5
    elif teclas[2] and coelhoPos[1] < 420:
        coelhoPos[1] += 5
    if teclas[1] and coelhoPos[0] > 0:
        coelhoPos[0] -= 5
    elif teclas[3] and coelhoPos[0] < 570:
        coelhoPos[0] += 5
    return coelhoPos


def giraCoelho(mousePos, coelhoPos):
    global coelho
    X, Y = (mousePos[1] - (coelhoPos[1]), mousePos[0] - (coelhoPos[0]))
    anguloRadianos = math.atan2(X, Y)
    angulo = math.degrees(anguloRadianos)
    coelho = pygame.transform.rotozoom(coelho, -angulo, 1)


def criaInimigos():
    if random.randint(1, 100) <= 5 or len(inimigos) == 0:
        inimigos.append([640, random.randint(50, 430)])


def moveInimigos():
    for inimigo in inimigos:
        inimigo[0] -= 7
        verificaColisao(inimigo)


def desenhaInimigos():
    for inimigo in inimigos:
        DISPLAYSURF.blit(inimigoImg, inimigo)


def desenhaFlecha(flechas):
    global flecha
    for bala in flechas:
        index = 0
        velx = math.cos(bala[0]) * 10
        vely = math.sin(bala[0]) * 10
        bala[1] += velx
        bala[2] += vely
        if bala[1] <= 64 or bala[1] > 640 or bala[2] <= 64 or bala[2] > 480:
            flechas.pop(index)
        index += 1
        for projectil in flechas:
            flecha_temp = pygame.transform.rotate(flecha, 360 - projectil[0] * 57.29)
            DISPLAYSURF.blit(flecha_temp, (projectil[1], projectil[2]))


def verificaColisao(inimigo):
    global vida
    global acuracia
    inimigoRect = pygame.Rect(inimigoImg.get_rect())
    inimigoRect.top = inimigo[1]
    inimigoRect.left = inimigo[0]

    # verifica com as flechas
    for bala in flechas:

        balarect = pygame.Rect(flecha.get_rect())
        balarect.left = bala[1]
        balarect.top = bala[2]
        if inimigoRect.colliderect(balarect):
            acuracia[0] += 1
            inimigos.remove(inimigo)
            flechas.remove(bala)
            inimigoSom.play()
            break

    # colisão com o castelo
    if inimigoRect.left < 64:
        vida -= random.randint(5, 20)
        inimigos.remove(inimigo)
        hitSom.play()


def desenhaFim(acuraciaFinal, imagem):
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    texto = font.render("Acurácia: " + str(acuraciaFinal) + "%", True, (0, 255, 0))
    textoRect = texto.get_rect()
    textoRect.centerx = DISPLAYSURF.get_rect().centerx
    textoRect.centery = DISPLAYSURF.get_rect().centery + 24
    DISPLAYSURF.blit(imagem, (0, 0))
    DISPLAYSURF.blit(texto, textoRect)


def verificaFim():
    if acuracia[1] != 0:
        acuraciaFinal = acuracia[0] * 1.0 / acuracia[1] * 100
    else:
        acuraciaFinal = 0
    if pygame.time.get_ticks() >= 90000:
        desenhaFim(acuraciaFinal, ganhou)
    if vida <= 0:
        desenhaFim(acuraciaFinal, gameover)


# Função principal
def main():
    pygame.init()
    global DISPLAYSURF
    mousePos = [100, 100]

    global acuracia
    acuracia = [0, 0]
    global flechas
    flechas = []

    # inimigos

    global inimigos
    inimigos = [[640, 100]]

    # Vida da mamae coelho
    global vida
    vida = 196

    # indices 0,1,2 e3 sao respectivamente as teclas ‘w’, ‘s’, ‘a’ e ‘d’
    teclas = [False, False, False, False]
    coelhoPos = [100, 100]

    DISPLAYSURF = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption('Mamãe Coelho')
    terminou = False

    configuracaoSom()

    while not terminou:  # Loop principal do jogo
        for event in pygame.event.get():
            if event.type == QUIT:
                terminou = True

        # Enquanto estiver pressionado, o coelho vai se mexer
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                teclas[0] = True
            elif event.key == K_a:
                teclas[1] = True
            elif event.key == K_s:
                teclas[2] = True
            elif event.key == K_d:
                teclas[3] = True

        # No momento que parou de pressionar a tecla
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                teclas[0] = False
            elif event.key == pygame.K_a:
                teclas[1] = False
            elif event.key == pygame.K_s:
                teclas[2] = False
            elif event.key == pygame.K_d:
                teclas[3] = False

        if event.type == pygame.MOUSEMOTION:
            mousePos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            tiroSom.play()
            clickPos = pygame.mouse.get_pos()
            acuracia[1] += 1
            flechas.append(
                [math.atan2(clickPos[1] - (coelhoPos[1] + 32), clickPos[0] - (coelhoPos[0] + 32)), coelhoPos[0] + 32,
                 coelhoPos[1] + 32])

        desenharArena()
        coelhoPos = moveCoelho(teclas, coelhoPos)
        giraCoelho(mousePos, coelhoPos)
        desenhaCoelho(coelhoPos)
        desenhaFlecha(flechas)
        criaInimigos()
        moveInimigos()
        desenhaInimigos()
        verificaFim()
        pygame.display.update()

    # Finaliza a janela do jogo
    pygame.display.quit()
    # Finaliza o pygame
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
