import pygame
from random import randrange

rosa = (139, 95, 101)
preto = (0, 0, 0)
vermelho = (255, 0, 0)

try:
    pygame.init()
except:
    print("ERRO")

largura = 640
altura = 320
tamanho = 10

relogio = pygame.time.Clock()
fundo = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Snake by Mah Bührer")
fonte = pygame.font.SysFont(None, 18)


def texto(msg, cor):
    texto_um = fonte.render(msg, True, cor)
    fundo.blit(texto_um, [largura / 10.00, altura / 2.00])


def cobra(CobraXY):
    for XY in CobraXY:
        pygame.draw.rect(fundo, preto, [XY[0], XY[1], tamanho, tamanho])


def maca(pos_x, pos_y):
    pygame.draw.rect(fundo, vermelho, [pos_x, pos_y, tamanho, tamanho])


def jogo():
    sair = True
    fim_de_jogo = False
    pos_x = randrange(0, largura - tamanho, 10)
    pos_y = randrange(0, altura - tamanho, 10)
    maca_x = randrange(0, largura - tamanho, 10)
    maca_y = randrange(0, altura - tamanho, 10)
    velocidade_x = 0
    velocidade_y = 0
    CobraXY = []
    CobraComp = 1
    while sair:
        while fim_de_jogo:
            fundo.fill(rosa)
            texto("GAME OVER!!! Para sair, aperte a tecla C ou S. Volte sempre!!!", preto)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sair = False
                    fim_de_jogo = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        sair = True
                        fim_de_jogo = False
                        pos_x = randrange(0, largura - tamanho, 10)
                        pos_y = randrange(0, altura - tamanho, 10)
                        maca_x = randrange(0, largura - tamanho, 10)
                        maca_y = randrange(0, altura - tamanho, 10)
                        velocidade_x = 0
                        velocidade_y = 0
                        CobraXY = []
                        CobraComp = 1
                        if event.key == pygame.K_s:
                            sair = False
                            fim_de_jogo = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and velocidade_x != tamanho:
                    velocidade_x = - tamanho
                    velocidade_y = 0
                if event.key == pygame.K_RIGHT and velocidade_x != - tamanho:
                    velocidade_x = tamanho
                    velocidade_y = 0
                if event.key == pygame.K_UP and velocidade_y != tamanho:
                    velocidade_x = 0
                    velocidade_y = - tamanho
                if event.key == pygame.K_DOWN and velocidade_x != - tamanho:
                    velocidade_x = 0
                    velocidade_y = tamanho
                if event.key == pygame.K_SPACE:
                    CobraComp += 1
        if sair:
            fundo.fill(rosa)
            pos_x += velocidade_x
            pos_y += velocidade_y

# if pos_x > largura:
# pos_x = 0
# if pos_x < 0:
# pos_x = largura - tamanho
# if pos_y > altura:
# pos_y = 0
# if pos_y < 0:
# pos_y = altura - tamanho
            if pos_x > largura:
                fim_de_jogo = True
            if pos_x < 0:
                fim_de_jogo = True
            if pos_y > altura:
                fim_de_jogo = True
            if pos_y < 0:
                fim_de_jogo = True

            if pos_x == maca_x and pos_y == maca_y:
                maca_x = randrange(0, largura - tamanho, 10)
                maca_y = randrange(0, altura - tamanho, 10)
                CobraComp += 1

            CobraInicio = [pos_x, pos_y]
            CobraXY.append(CobraInicio)
            if len(CobraXY) > CobraComp:
                del CobraXY[0]
            if any(Bloco == CobraInicio for Bloco in CobraXY[:-1]):
                fim_de_jogo = True

            cobra(CobraXY)

            maca(maca_x, maca_y)
            relogio.tick(5)
            pygame.display.update()


jogo()
pygame.quit()
