# -*- coding: utf-8 -*-
""" Algoritmo genérico de busca de caminho A-Star """

from abc import ABC, abstractmethod
from typing import Callable, Dict, Iterable, Union, TypeVar, Generic
from math import inf as infinito
import sortedcontainers  # type: ignore

# introduzir tipo genérico
T = TypeVar("T")


################################################################################
class NoDeBusca(Generic[T]):
    """Representação de um nó de busca"""

    __slots__ = ("data", "gscore", "fscore", "fechado", "veio_de", "na_lista_aberta")

    def __init__(
        self, data: T, gscore: float = infinito, fscore: float = infinito
    ) -> None:
        self.data = data
        self.gscore = gscore
        self.fscore = fscore
        self.fechado = False
        self.na_lista_aberta = False
        self.veio_de: Union[None, NoDeBusca[T]] = None

    def __lt__(self, b: "NoDeBusca[T]") -> bool:
        """A ordem natural é baseada no valor fscore e é usada pelas operações do heapq"""
        return self.fscore < b.fscore


################################################################################
class DicionarioDeNoDeBusca(Dict[T, NoDeBusca[T]]):
    """Um dicionário que retorna um novo NoDeBusca quando uma chave está ausente"""

    def __missing__(self, k) -> NoDeBusca[T]:
        v = NoDeBusca(k)
        self.__setitem__(k, v)
        return v


################################################################################
STipoNo = TypeVar("STipoNo", bound=NoDeBusca)


class ListaAberta(Generic[STipoNo]):
    def __init__(self) -> None:
        self.lista_ordenada = sortedcontainers.SortedList(key=lambda x: x.fscore)

    def push(self, item: STipoNo) -> None:
        item.na_lista_aberta = True
        self.lista_ordenada.add(item)

    def pop(self) -> STipoNo:
        item = self.lista_ordenada.pop(0)
        item.na_lista_aberta = False
        return item

    def remover(self, item: STipoNo) -> None:
        self.lista_ordenada.remove(item)
        item.na_lista_aberta = False

    def __len__(self) -> int:
        return len(self.lista_ordenada)


################################################################################*


class AStar(ABC, Generic[T]):
    __slots__ = ()

    @abstractmethod
    def estimativa_de_custo_heuristico(self, atual: T, objetivo: T) -> float:
        """
        Calcula a distância estimada (aproximada) entre um nó e o objetivo.
        O segundo parâmetro é sempre o objetivo.
        Este método deve ser implementado em uma subclasse.
        """
        raise NotImplementedError

    @abstractmethod
    def distancia_entre(self, n1: T, n2: T) -> float:
        """
        Dá a distância real entre dois nós adjacentes n1 e n2 (ou seja, n2
        pertence à lista de vizinhos de n1).
        É garantido que n2 pertence à lista retornada pela chamada para neighbors(n1).
        Este método deve ser implementado em uma subclasse.
        """

    @abstractmethod
    def vizinhos(self, nó: T) -> Iterable[T]:
        """
        Para um determinado nó, retorna (ou gera) a lista de seus vizinhos.
        Este método deve ser implementado em uma subclasse.
        """
        raise NotImplementedError

    def objetivo_alcançado(self, atual: T, objetivo: T) -> bool:
        """
        Retorna verdadeiro quando podemos considerar que 'atual' é o objetivo.
        A implementação padrão simplesmente compara `atual == objetivo`, mas este
        método pode ser sobrescrito em uma subclasse para fornecer verificações mais refinadas.
        """
        return atual == objetivo

    def reconstruir_caminho(self, último: NoDeBusca, caminho_invertido=False) -> Iterable[T]:
        def _gen():
            atual = último
            while atual:
                yield atual.data
                atual = atual.veio_de

        if caminho_invertido:
            return _gen()
        else:
            return reversed(list(_gen()))

    def astar(
        self, inicial: T, objetivo: T, caminho_invertido: bool = False
    ) -> Union[Iterable[T], None]:
        if self.objetivo_alcançado(inicial, objetivo):
            return [inicial]

        lista_aberta: ListaAberta[NoDeBusca[T]] = ListaAberta()
        nós_de_busca: DicionarioDeNoDeBusca[T] = DicionarioDeNoDeBusca()
        nó_inicial = nós_de_busca[inicial] = NoDeBusca(
            inicial, gscore=0.0, fscore=self.estimativa_de_custo_heuristico(inicial, objetivo)
        )
        lista_aberta.push(nó_inicial)

        while lista_aberta:
            atual = lista_aberta.pop()

            if self.objetivo_alcançado(atual.data, objetivo):
                return self.reconstruir_caminho(atual, caminho_invertido)

            atual.fechado = True

            for vizinho in map(lambda n: nós_de_busca[n], self.vizinhos(atual.data)):
                if vizinho.fechado:
                    continue

                gscore_tentativo = atual.gscore + self.distancia_entre(
                    atual.data, vizinho.data
                )

                if gscore_tentativo >= vizinho.gscore:
                    continue

                vizinho_na_lista_aberta = vizinho.na_lista_aberta

                if vizinho_na_lista_aberta:
                    # temos que remover o item do heap, pois seu score mudou
                    lista_aberta.remover(vizinho)

                # atualiza o nó
                vizinho.veio_de = atual
                vizinho.gscore = gscore_tentativo
                vizinho.fscore = gscore_tentativo + self.estimativa_de_custo_heuristico(
                    vizinho.data, objetivo
                )

                lista_aberta.push(vizinho)

        return None


################################################################################
U = TypeVar("U")


def encontrar_caminho(
    inicial: U,
    objetivo: U,
    função_vizinhos: Callable[[U], Iterable[U]],
    caminho_invertido=False,
    função_estimativa_de_custo_heuristico: Callable[[U, U], float] = lambda a, b: infinito,
    função_distancia_entre: Callable[[U, U], float] = lambda a, b: 1.0,
    função_objetivo_alcançado: Callable[[U, U], bool] = lambda a, b: a == b,
) -> Union[Iterable[U], None]:
    """Uma versão não baseada em classes do algoritmo de busca de caminho"""

    class EncontrarCaminho(AStar):
        def estimativa_de_custo_heuristico(self, atual: U, objetivo: U) -> float:
            return função_estimativa_de_custo_heuristico(atual, objetivo)  # type: ignore

        def distancia_entre(self, n1: U, n2: U) -> float:
            return função_distancia_entre(n1, n2)

        def vizinhos(self, nó) -> Iterable[U]:
            return função_vizinhos(nó)  # type: ignore

        def objetivo_alcançado(self, atual: U, objetivo: U) -> bool:
            return função_objetivo_alcançado(atual, objetivo)

    return EncontrarCaminho().astar(inicial, objetivo, caminho_invertido)


__all__ = ["AStar", "encontrar_caminho"]
