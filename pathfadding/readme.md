# Campo de Futebol com Movimento de Jogador

Este é um projeto simples desenvolvido em Python com Pygame, onde um jogador pode se mover em um campo de futebol clicando na tela. O jogador utiliza o algoritmo A* para encontrar o caminho até o ponto clicado, desviando de obstáculos.

## Funcionalidades

- Movimento do jogador (Robô) para o ponto clicado na tela.
- Desvio de obstáculos utilizando o algoritmo A*.

## Requisitos

- Python 3.8.10
- Pygame 2.5.2

## Como Executar

1. Clone o repositório:

   ```bash
   git clone https://github.com/thxssio/TheStarAlgorithm.git


2. Instale as dependecias:

```
    pip install pygame
```

<h1 align="center"> Algoritimo A* </h1>


O algoritmo A* é um algoritmo de busca de caminho amplamente utilizado em jogos e simulações para encontrar o caminho mais curto entre dois pontos, levando em consideração um mapa ou grafo com obstáculos. Ele utiliza uma combinação de duas heurísticas:

* Custo real (g): O custo real é a distância percorrida do ponto inicial até o ponto atual ao longo do caminho atual.

* Custo estimado (h): O custo estimado é a estimativa do custo restante do ponto atual até o ponto de destino, calculada geralmente usando a distância euclidiana ou a distância de Manhattan.

Essas duas heurísticas são combinadas em uma função de avaliação f(n) = g(n) + h(n), onde n é o nó atual. O algoritmo A* seleciona o próximo nó a ser visitado com base na função de avaliação, dando prioridade aos nós com menor valor de f(n).

#Passos do algoritmo:

Inicialização: 

- Inicialize o nó inicial com g = 0 e adicione-o à lista aberta.

Loop principal:

Enquanto a lista aberta não estiver vazia:
 - Selecione o nó com o menor valor de f(n) da lista aberta como o nó atual.
 - Se o nó atual for o nó de destino, reconstrua o caminho até o nó inicial e retorne o caminho.

Para cada nó vizinho do nó atual:
 - Se o vizinho não estiver bloqueado e não estiver na lista fechada:
   - Calcule g e h para o vizinho.
   - Se o vizinho não estiver na lista aberta, adicione-o e defina o nó atual como seu pai.
   - Se o vizinho já estiver na lista aberta, verifique se o novo caminho é melhor e, se for, atualize o custo e o pai.
   - Se a lista aberta ficar vazia e o destino não for alcançado, não há caminho possível.

# Implementação no código:

No código do jogo, o algoritmo A* é implementado na função astar(inicio, objetivo, obstaculos). Ele recebe a posição inicial, a posição de destino e uma lista de obstáculos. O algoritmo calcula o caminho do jogador até o objetivo, evitando os obstáculos, e retorna uma lista de pontos que representam o caminho a seguir.



# Como Testar o exemplo 2:

Clique na tela para mover o jogador até o ponto clicado, desviando dos outros jogadores.
Detalhes de Implementação
Algoritmo A*
O algoritmo A* é utilizado para calcular o caminho mais curto do jogador até o ponto clicado na tela, levando em consideração a posição dos outros jogadores como obstáculos. Ele combina duas heurísticas: o custo real (distância percorrida até o ponto atual) e o custo estimado (distância até o ponto de destino).

Execute:

``` 
    python Example2.py
```
# Estrutura do Código

* O código foi organizado em classes para facilitar a compreensão e manutenção:

`CampoDeFutebol:` Responsável por controlar a lógica do jogo e desenhar os elementos na tela.

`Jogador:` Representa o jogador controlado pelo usuário, com métodos para movimentação e desenho.

`AStar:` Implementação do algoritmo A* para encontrar o caminho até o ponto clicado.



# Contribuição

Sinta-se à vontade para contribuir com melhorias no código, correção de bugs ou novas funcionalidades. Basta fazer um fork do repositório, realizar as modificações e enviar um pull request.

#Licença
Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE para obter mais informações.
