from typing import Tuple, List, Iterable, Union, TypeVar, Generic
from src.Astar import AStar
import math

T = TypeVar("T")

class CampoFutebolAStar(AStar, Generic[T]):
    def __init__(self, campo: List[str]):
        """Inicializa o solucionador A* para um campo de futebol representado por uma lista de strings."""
        self.linhas = campo
        self.largura = len(self.linhas[0])
        self.altura = len(self.linhas)

    def estimativa_de_custo_heuristico(self, n1: T, n2: T) -> float:
        """Calcula a estimativa de custo heurístico entre dois nós no campo de futebol."""
        (x1, y1) = n1
        (x2, y2) = n2
        return math.hypot(x2 - x1, y2 - y1)

    def distancia_entre(self, n1: T, n2: T) -> float:
        """Calcula a distância entre dois nós no campo de futebol (sempre retorna 1)."""
        return 1.0

    def vizinhos(self, nó: T) -> Iterable[T]:
        """Retorna os vizinhos alcançáveis a partir de um nó no campo de futebol."""
        x, y = nó
        return [(nx, ny) for nx, ny in [(x-1, y-1), (x, y-1), (x+1, y-1),
                                         (x-1, y),             (x+1, y),
                                         (x-1, y+1), (x, y+1), (x+1, y+1)]
                if 0 <= nx < self.largura and 0 <= ny < self.altura and self.linhas[ny][nx] == ' ']

    def desviar_jogadores(self, jogador: Tuple[int, int], jogadores: List[Tuple[int, int]]) -> Iterable[Tuple[int, int]]:
        """Calcula os movimentos válidos para desviar dos outros jogadores no campo de futebol."""
        x, y = jogador
        vizinhos_validos = [(nx, ny) for nx, ny in [(x-1, y-1), (x, y-1), (x+1, y-1),
                                                    (x-1, y),             (x+1, y),
                                                    (x-1, y+1), (x, y+1), (x+1, y+1)]
                            if 0 <= nx < self.largura and 0 <= ny < self.altura and (nx, ny) not in jogadores]
        return vizinhos_validos

def resolver_campo_futebol(campo: List[str], jogador: Tuple[int, int], objetivo: Tuple[int, int]) -> str:
    """Resolve o campo de futebol, desviando dos outros jogadores para alcançar o objetivo."""
    solucionador = CampoFutebolAStar(campo)
    caminho_encontrado = list(solucionador.astar(jogador, objetivo, caminho_invertido=True))
    caminho = campo.copy()
    for x, y in caminho_encontrado:
        caminho[y] = caminho[y][:x] + '*' + caminho[y][x+1:]
    return '\n'.join(caminho)

if __name__ == '__main__':
    campo_futebol = [
        "##############################",
        "#                            #",
        "#                            #",
        "#        #    ##    #        #",
        "#        #    ##    #        #",
        "#                            #",
        "#                            #",
        "#                            #",
        "# ########################## #",
        "#                            #",
        "#  ##      #####             #",
        "#                            #",
        "#                            #",
        "#     ##   ##        ##      #",
        "#                            #",
        "#                            #",
        "#                            #",
        "#                            #",
        "#                            #",
        "##############################"
    ]
                       
    jogador = (1, 1)
    objetivo = (5 ,5)

    resultado = resolver_campo_futebol(campo_futebol, jogador, objetivo)
    print(resultado)
