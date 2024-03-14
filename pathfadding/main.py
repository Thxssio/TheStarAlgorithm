from src.Astar import AStar
import sys
import math
import unittest

def criar_labirinto(largura=30, altura=30):
    """retorna um labirinto ASCII como uma string"""
    from random import shuffle, randrange
    vis = [[0] * largura + [1] for _ in range(altura)] + [[1] * (largura + 1)]
    ver = [["|  "] * largura + ['|'] for _ in range(altura)] + [[]]
    hor = [["+--"] * largura + ['+'] for _ in range(altura + 1)]

    def andar(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                hor[max(y, yy)][x] = "+  "
            if yy == y:
                ver[y][max(x, xx)] = "   "
            andar(xx, yy)

    andar(randrange(largura), randrange(altura))
    resultado = ''
    for (a, b) in zip(hor, ver):
        resultado = resultado + (''.join(a + ['\n'] + b)) + '\n'
    return resultado.strip()


def desenhar_labirinto(labirinto, conjunto1=[], conjunto2=[], c='#', c2='*'):
    """retorna um labirinto ASCII, desenhando eventualmente um (ou 2) conjuntos de posições.
        útil para desenhar a solução encontrada pelo algoritmo A*.
    """
    conjunto1 = list(conjunto1)
    conjunto2 = list(conjunto2)
    linhas = labirinto.strip().split('\n')
    largura = len(linhas[0])
    altura = len(linhas)
    resultado = ''
    for j in range(altura):
        for i in range(largura):
            if (i, j) in conjunto1:
                resultado = resultado + c
            elif (i, j) in conjunto2:
                resultado = resultado + c2
            else:
                resultado = resultado + linhas[j][i]
        resultado = resultado + '\n'
    return resultado


class SolucionadorLabirinto(AStar):

    """uso de exemplo do algoritmo A*. Neste exemplo, trabalhamos com um labirinto feito de caracteres ASCII,
    e um 'nó' é apenas uma tupla (x,y) que representa uma posição alcançável"""

    def __init__(self, labirinto):
        self.linhas = labirinto.strip().split('\n')
        self.largura = len(self.linhas[0])
        self.altura = len(self.linhas)

    def estimativa_de_custo_heuristico(self, n1, n2):
        """calcula a distância 'direta' entre duas tuplas (x,y)"""
        (x1, y1) = n1
        (x2, y2) = n2
        return math.hypot(x2 - x1, y2 - y1)

    def distancia_entre(self, n1, n2):
        """este método sempre retorna 1, pois dois 'vizinhos' estão sempre adjacentes"""
        return 1

    def vizinhos(self, nó):
        """para uma coordenada dada no labirinto, retorna até 4 nós adjacentes (norte, leste, sul, oeste)
            que podem ser alcançados (=qualquer coordenada adjacente que não seja uma parede)
        """
        x, y = nó
        return[(nx, ny) for nx, ny in[(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]if 0 <= nx < self.largura and 0 <= ny < self.altura and self.linhas[ny][nx] == ' ']

def resolver_labirinto():
    # gerar um labirinto ASCII
    tamanho = 20
    labirinto = criar_labirinto(tamanho, tamanho)

    largura = len(labirinto.split('\n')[0])
    altura = len(labirinto.split('\n'))

    inicio = (1, 1)  
    objetivo = (largura - 2, altura - 2) 

    caminhoEncontrado = list(SolucionadorLabirinto(labirinto).astar(inicio, objetivo))

    return desenhar_labirinto(labirinto, list(caminhoEncontrado))

class TestesLabirinto(unittest.TestCase):
    def test_resolver_labirinto(self):
        resolver_labirinto()

if __name__ == '__main__':
    print(resolver_labirinto())
