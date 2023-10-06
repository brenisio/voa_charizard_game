import pygame, sys, random

### Trabalho final de Introdução à Informática para Automação ###
##----------- Aluno: Breno Juliano de Mello Sayão -------------##


def desenhar_piso():
    tela.blit(piso_surface, (piso_x_pos, 950))                      ## Definição do posicionamento do chão na tela
    tela.blit(piso_surface, (piso_x_pos + 576, 950))                ## Abrange toda imagem do piso na tela


def desenhar_background():
    tela.blit(background_surface, (background_x_pos, 0))            ## Definição do posicionamento do plano de fundo na tela
    tela.blit(background_surface, (background_x_pos + 1920, 0))     ## Abrange toda imagem na tela

def criar_lava():
    random_lava_pos = random.choice(altura_lava)                                ## Escolherá um número aleatório na lista "altura_lava"
    lava_baixo = lava_surface.get_rect(midtop=(700, random_lava_pos))            ## Criará o obstáculo entre o meio e o teto
    lava_cima = lava_surface.get_rect(midbottom=(700, random_lava_pos - 300))    ## Criará o obstáculo entre o meio e o chão
    return lava_baixo, lava_cima

def mover_lavas(lavas):
    for lava in lavas:                                                          ## Função que cria uma nova lista com novos retângulos
        lava.centerx -= 5                                                       ##Definir o centro do obstáculo
    return lavas

def desenhar_lavas(lavas):
    for lava in lavas:                                                          ## Criação de obstáculos (Imagem da lava) na tela
        if lava.bottom >= 900:
            tela.blit(lava_surface, lava)
        else:
            inverter_pipe = pygame.transform.flip(lava_surface, False, True)    ## Comando para inverter a rotação do obstáculo lava
            tela.blit(inverter_pipe, lava)

def checar_contato(lavas):
    for lava in lavas:                                                          ## Def para checar se a contato com os obstáculos
        if charizard_rect.colliderect(lava):
            return False

        if charizard_rect.top <= -100 or charizard_rect.bottom >= 950:          ## Definindo limite de movimentação entre o teto e o solo
            return False

    return True

def rotaciona_charizard(charizard):
    novo_charizard = pygame.transform.rotozoom(charizard, -movimento_charizard * 3, 1)      ## Def para criar um movimento de queda do personagem
    return novo_charizard

def baterasas_charizard():
    novo_charizard = charizard_frames[charizard_index]                                      ## Cria movimento entre os itens da lista
    novo_chrizard_rect = novo_charizard.get_rect(center=(100, charizard_rect.centery))      ## Retângulo para definir limites do personagem
    return novo_charizard, novo_chrizard_rect

def pontuaçao_tela(pontuacao_jogo):
    if pontuacao_jogo == 'main_game':                                                       ## Def para apresentar pontuação na tela
        pontuaçao_surface = fonte_jogo.render(str(int(pontuaçao)), True, (255, 255, 255))   ## Fonte da letra, além da cor RGB
        pontuaçao_rect = pontuaçao_surface.get_rect(center=(288, 100))                      ## Posição da pontuação na tela
        tela.blit(pontuaçao_surface, pontuaçao_rect)
    if pontuacao_jogo == 'game_over':
        pontuaçao_surface = fonte_jogo.render(f'Pontuação: {int(pontuaçao)}', True, (255, 255, 255))
        pontuaçao_rect = pontuaçao_surface.get_rect(center=(288, 100))
        tela.blit(pontuaçao_surface, pontuaçao_rect)

        pontuaçao_max_surface = fonte_jogo.render(f'Pontuação máxima: {int(pontuaçao_max)}', True, (255, 255, 255)) ## Pontuação máxima, com a mesma fonte e cor da anterior
        pontuaçao_max_rect = pontuaçao_max_surface.get_rect(center=(288, 850))                                      ## Posição da pontuação máxima na tela
        tela.blit(pontuaçao_max_surface, pontuaçao_max_rect)

def atualizar_pontuacao(pontuacao, pontuacao_max):
    pontuaçao_max = 0                                                           ## Definição da pontuação máxima
    if pontuaçao > pontuaçao_max:                                               ## Se a pontuação for maior que a pontuação máxima
        pontuaçao_max = pontuaçao                                               ## A pontuação máxima recebe a pontuação
    return pontuaçao_max

pygame.init()                                                                   ## Inicia o pygame

tela = pygame.display.set_mode((576, 1024))                                     ## Janela aberta para rodar o jogo, tamanho 576x1024
clock = pygame.time.Clock()                                                     ## Criar a váriavel "clock" para conseguirmos rodar o FPS
fonte_jogo = pygame.font.Font('C:\Windows\Fonts\calibri.ttf', 40)

# Variáveis do jogo
gravidade = 0.25                                                                ## Variável de gravidade
movimento_charizard = 0                                                         ## Movimento do personagem
jogo_rodando = True                                                             ## Confirmação se o jogo está jogando
pontuaçao = 0                                                                   ## Pontuação começa zerada (0)
pontuaçao_max = 0                                                               ## Pontuação máxima começa zerada (0)

background_surface = pygame.image.load('Imagens/Plano_de_fundo.jpg').convert()  ## Imagem que será o plano de fundo da tela do jogo

piso_surface = pygame.image.load('Imagens/piso.png').convert()                  ## Imagem que será o piso do jogo
piso_x_pos = 0
background_x_pos = 0

charizard_voobaixo = pygame.image.load('Imagens/Charizard-desce.png').convert_alpha()       ## Criação do bater de asas do personagem (Voo baixo)
charizard_voomedio = pygame.image.load('Imagens/Charizard-meio2.png').convert_alpha()       ## Voo médio
charizard_vooalto = pygame.image.load('Imagens/Charizard-sobe.png').convert_alpha()         ## Voo alto
charizard_frames = [charizard_voobaixo, charizard_voomedio, charizard_vooalto]              ## Lista com os 3 tipos de voo
charizard_index = 0                                                                         ## Index que começa na posição 0 da lista (Voo baixo)
charizard_surface = charizard_frames[charizard_index]
charizard_rect = charizard_surface.get_rect(center=(100, 512))                              ## Posição que o personagem fica na tela

ASASCHARIZARD = pygame.USEREVENT + 1                                             ## Evento para o personagem "bater asas"
pygame.time.set_timer(ASASCHARIZARD, 200)

lava_surface = pygame.image.load('Imagens/Lava-baixo1.png')                     ## Imagem que será os obstáculos do jogo
lava_list = []                                                                  ## Criação de lista para guardar os retângulos que serão os obstáculos
CRIARLAVA = pygame.USEREVENT
pygame.time.set_timer(CRIARLAVA, 1200)                                          ## Será criado um obstáculo a cada 1200 milisegundos
altura_lava = [400, 600, 800]

game_over_surface = pygame.image.load('Imagens/Fim.png').convert_alpha()        ## Imagem que aparece quando o jogador bate no obstáculo
game_over_rect = game_over_surface.get_rect(center=(288, 512))                  ## Posição que imagem aparece

while True:
    for event in pygame.event.get():                                        ## Loop que mantém a janela aberta
        if event.type == pygame.QUIT:
            pygame.quit()                                                   ## Comando para que possa ser fechado o jogo
            sys.exit()                                                      ## FPS(Frames per second) = Quantas imagens são desenhadas por segundo, eles influenciam a velocidade e fluidez do jogo
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and jogo_rodando:                ## Se a tecla espaço for apertada ->
                movimento_charizard = 0
                movimento_charizard -= 9                                   ## -> o personagem executa o movimento "-= 9"
            if event.key == pygame.K_SPACE and jogo_rodando == False:
                jogo_rodando = True                                         ## O jogo inicia novamente quando apertado "Espaço"
                lava_list.clear()                                           ## As variáveis são limpas e zeradas para recomeçar o jogo
                charizard_rect.center = (100, 512)
                movimento_charizard = 0
                pontuaçao = 0

        if event.type == CRIARLAVA:
            lava_list.extend(criar_lava())                      ## Lista, que cria retângulos constantemente

        if event.type == ASASCHARIZARD:                         ## Criar um tipo de evento que consiga transitar entre os elementos ->
            if charizard_index < 2:                             ## -> 0 1 e 2 da lista, formando um movimento
                charizard_index += 1
            else:
                charizard_index = 0

            charizard_surface, charizard_rect = baterasas_charizard()

    # Plano de fundo
    background_x_pos -= 1                                   ## Posição da tela de fundo(background) criará movimento
    desenhar_background()                                   ## Chamada a def de desenhar o background
    if background_x_pos <= -1920:                           ## Torna infinito o movimento da imagem, toda vez que a tela de fundo for menor ou igual a -1920 (comprimento da imagem) ->
        background_x_pos = 0                                ## -> a imagem retorna a 0

    if jogo_rodando:
        # Personagem ('Charizard')
        movimento_charizard += gravidade                                    ## Movimento do "Charizard" varia de acordo com a gravidade
        rotacionar_charizard = rotaciona_charizard(charizard_surface)       ## Cria um movimento de rotacionar o personagem
        charizard_rect.centery += movimento_charizard                       ## Criar a queda do "Charizard" usando o centro y do rect(retangulo) que contorna o "Charizard"
        tela.blit(rotacionar_charizard, charizard_rect)                     ## Mostra na tela o "Charizard"
        jogo_rodando = checar_contato(lava_list)

        # Lavas
        lava_list = mover_lavas(lava_list)                                  ## Criação de obstáculos usando "lista"
        desenhar_lavas(lava_list)
        pontuaçao += 0.01                                                   ## Pontuação cresce no decorrer do jogo
        pontuaçao_tela('main_game')
    else:
        tela.blit(game_over_surface,game_over_rect)                         ## Caso bata em algum obstáculo, a tela apresenta a imagem de "game over"
        pontuaçao_max = atualizar_pontuacao(pontuaçao,pontuaçao_max)
        pontuaçao_tela('game_over')



    # Piso (chão)
    piso_x_pos -= 1                                     ## Variável piso recebe número inteiro, para dar movimento ao chão
    desenhar_piso()
    if piso_x_pos <= -576:                              ## Torna infinito o movimento da imagem, toda vez que o piso for menor ou igual a -576, ele volta a imagem do começo
        piso_x_pos = 0
    pygame.display.update()
    clock.tick(120)                                     ## Definição de 120 frames por segundo

pygame.quit()  ## Fechar o pygame