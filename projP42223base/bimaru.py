# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 30:
# 103262 Duarte Marques
# 102820 Bernardo Augusto
import numpy
import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)



class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id
    
    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""
    def __init__(self, list_linhas, list_colunas):
        self.list_linhas=list_linhas
        self.list_colunas=list_colunas
        self.celulas= [['-' for _ in range(10)] for _ in range(10)]
        
        

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.celulas[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if row==0:
            return ('X', self.get_value(row+1, col))
        elif row==9:
            return (self.get_value(row-1, col), 'X')
        else:
            return (self.get_value(row-1, col), self.get_value(row+1, col))
        pass

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        
        if col==0:
            return ('X', self.get_value(row, col+1))
        elif col==9:
            return (self.get_value(row, col-1),'X')
        else:
            return (self.get_value(row, col-1), self.get_value(row, col+1))
    
    'def clear_adj_pos(self, row, col, piece):'
            
        
    def clear_row(self, row:int):
        for i in range(10):
            if not self.get_value(row, i).isalpha():
                self.celulas[row][i]='.'
            
    def clear_column(self, column:int):
        for i in range(10):
            if not self.get_value(i, col).isalpha():
                self.celulas[i][column]='.'

    def set_piece(self, row:int, column:int ,piece):
        self.celulas[row][column]=piece
    
        
    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """
        # TODO
        pass

    # TODO: outros metodos da classe


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.board=Board

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass
    

    def set_clues(self, lista_clues):
        for clue in lista_clues:
            self.board.set_piece(clue[0], clue[1], clue[2])
        

if __name__ == "__main__":
    # TODO:
    
    str_linhas=input()
    row_numbers=[int(num) for num in str_linhas.split(' ')]
    str_colunas=input()
    column_numbers=[int(num) for num in str_colunas.split(' ')]
    n_clues=(int(input))
    clues=[]
    while (n_clues>0):
        clue_input=input()
        clue_parts=clue_input.split()
        clue_x=clue_parts[1]
        clue_y=clue_parts[2]
        clue_piece=clue_parts[3]
        clue=(clue_x, clue_y, clue_piece)
        clues.append(clue)
        n_clues=n_clues-1
    tabuleiro=Board(row_numbers, column_numbers)
    
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
