import matplotlib.pyplot as plt 

class AStar:
    def __init__(self, largura_campo, altura_campo, direcoes):
        self.largura_campo = largura_campo
        self.altura_campo = altura_campo
        self.direcoes = direcoes

    def calcular_caminho(self, inicio, objetivo, obstaculos):
        nodes = [(inicio, 0)]
        nodeInicial = {}
        custo_g = {inicio: 0}

        while nodes:
            atual, custo_atual = nodes.pop(0)

            if atual == objetivo:
                caminho = [atual]
                while atual != inicio:
                    atual = nodeInicial[atual]
                    caminho.append(atual)
                return caminho[::-1]

            for direcao in self.direcoes:
                proximo = (atual[0] + direcao[0], atual[1] + direcao[1])
                novo_custo_g = custo_g[atual] + (1 if direcao[0] == 0 or direcao[1] == 0 else 1.414)

                if proximo in obstaculos or proximo[0] < 0 or proximo[1] < 0 or proximo[0] >= self.largura_campo or proximo[1] >= self.altura_campo:
                    continue

                if proximo not in custo_g or novo_custo_g < custo_g[proximo]:
                    custo_g[proximo] = novo_custo_g
                    nodes.append((proximo, novo_custo_g))
                    nodeInicial[proximo] = atual

        return None


largura_campo = 200
altura_campo = 200

"""
    (0, 1): mover para cima (norte)
    (0, -1): mover para baixo (sul)
    (1, 0): mover para a direita (leste)
    (-1, 0): mover para a esquerda (oeste)
    (1, 1): mover para a diagonal superior direita (nordeste)
    (1, -1): mover para a diagonal inferior direita (sudeste)
    (-1, 1): mover para a diagonal superior esquerda (noroeste)
    (-1, -1): mover para a diagonal inferior esquerda (sudoeste)
"""

direcoes = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
astar = AStar(largura_campo, altura_campo, direcoes)
inicio = (0, 0)
objetivo = (90, 90) 
obstaculos = [(80, 40), (60, 60), (20, 50)]


caminho = astar.calcular_caminho(inicio, objetivo, obstaculos)
print(caminho)

x, y = zip(*caminho)

plt.figure()
plt.plot(x, y, 'o-')
obstaculos_x, obstaculos_y = zip(*obstaculos)
plt.plot(obstaculos_x, obstaculos_y, 'ro')
plt.show()

