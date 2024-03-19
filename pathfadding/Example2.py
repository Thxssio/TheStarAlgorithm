import pygame
from pygame.locals import *

class JogoCampoFutebol:
    def __init__(self):
        # Definir as cores
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

        # Inicializar o Pygame
        pygame.init()

        # Definir o tamanho da tela e outras configurações
        self.largura_tela, self.altura_tela = 800, 600
        self.tela = pygame.display.set_mode((self.largura_tela, self.altura_tela))
        pygame.display.set_caption('Campo de Futebol')

        # Carregar a imagem do campo de futebol com o tamanho correto
        self.escala = 40
        self.largura_campo, self.altura_campo = 20 * self.escala, 15 * self.escala
        self.campo_imagem = pygame.transform.scale(pygame.image.load('campo_de_futebol.png'), (self.largura_campo, self.altura_campo))

        # Carregar a imagem do jogador com o tamanho correto
        self.jogador_imagem = pygame.transform.scale(pygame.image.load('jogador.png'), (self.escala, self.escala))
        self.posicao_jogador = [self.largura_tela // 2, self.altura_tela // 2]

        # Definir a posição inicial e o destino do jogador
        self.posicao_objetivo = [0, 0]
        self.jogadores = [(10, 10), (15, 10), (5, 5)]  # Exemplo de posição de outros jogadores

    def desenhar_campo(self):
        self.tela.fill(self.WHITE)  # Preencher a tela com a cor branca
        self.tela.blit(self.campo_imagem, (0, 0))  # Desenhar a imagem do campo de futebol na tela
        for jogador in self.jogadores:
            self.tela.blit(self.jogador_imagem, (jogador[0] * self.escala, jogador[1] * self.escala))  # Desenhar outros jogadores
        self.tela.blit(self.jogador_imagem, self.posicao_jogador)  # Desenhar o jogador na tela

    def astar(self, inicio, objetivo, obstaculos):
        borda = [(inicio, 0)]
        pais = {}
        custo_g = {inicio: 0}

        while borda:
            atual, custo_atual = borda.pop(0)

            if atual == objetivo:
                caminho = [atual]
                while atual != inicio:
                    atual = pais[atual]
                    caminho.append(atual)
                return caminho[::-1]

            for vizinho in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
                proximo = (atual[0] + vizinho[0], atual[1] + vizinho[1])
                novo_custo_g = custo_g[atual] + (1 if vizinho[0] == 0 or vizinho[1] == 0 else 1.414)

                if proximo in obstaculos or proximo[0] < 0 or proximo[1] < 0 or proximo[0] >= self.largura_campo // self.escala or proximo[1] >= self.altura_campo // self.escala:
                    continue

                if proximo not in custo_g or novo_custo_g < custo_g[proximo]:
                    custo_g[proximo] = novo_custo_g
                    borda.append((proximo, novo_custo_g))
                    pais[proximo] = atual

        return None

    def executar(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == MOUSEBUTTONDOWN:
                    self.posicao_objetivo[0], self.posicao_objetivo[1] = pygame.mouse.get_pos()
                    self.posicao_objetivo[0] -= self.jogador_imagem.get_width() // 2
                    self.posicao_objetivo[1] -= self.jogador_imagem.get_height() // 2
                    self.posicao_objetivo[0] = max(0, min(self.posicao_objetivo[0], self.largura_tela - self.jogador_imagem.get_width()))
                    self.posicao_objetivo[1] = max(0, min(self.posicao_objetivo[1], self.altura_tela - self.jogador_imagem.get_height()))
                    obstaculos = [(jogador[0], jogador[1]) for jogador in self.jogadores]
                    caminho = self.astar((self.posicao_jogador[0] // self.escala, self.posicao_jogador[1] // self.escala), 
                                         (self.posicao_objetivo[0] // self.escala, self.posicao_objetivo[1] // self.escala), 
                                         obstaculos)
                    if caminho:
                        for ponto in caminho:
                            self.posicao_jogador[0] = ponto[0] * self.escala
                            self.posicao_jogador[1] = ponto[1] * self.escala
                            self.desenhar_campo()
                            pygame.display.update()
                            clock.tick(5)

            self.desenhar_campo()  # Chamar a função para desenhar o campo de futebol
            pygame.display.update()  # Atualizar a tela
            clock.tick(60)  # Limitar a taxa de quadros para 60 FPS

if __name__ == '__main__':
    jogo = JogoCampoFutebol()
    jogo.executar()




"""



"""