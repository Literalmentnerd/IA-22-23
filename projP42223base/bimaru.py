# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 30:
# 103262 Duarte Marques
# 102820 Bernardo Augusto
import numpy as np
import copy
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


class Board:
    """Representação interna de um tabuleiro de Bimaru."""
    def __init__(self, list_linhas, list_colunas, list_clues):
        self.list_linhas=list_linhas
        self.list_colunas=list_colunas
        self.celulas=[['-' for _ in range(10)] for _ in range(10)]
        self.lista_clues=list_clues
        self.boats=[[],[],[],[]]
        self.a_ser_colocado_em_linhas=list(list_linhas)
        self.a_ser_colocado_em_colunas=list(list_colunas)
        self.posicoes_livres_linhas=[10,10,10,10,10,10,10,10,10,10]
        self.posicoes_livres_col=[10,10,10,10,10,10,10,10,10,10]
        self.colunas_ajeitadas=[False, False, False, False, False, False, False, False, False, False]
        self.linhas_ajeitadas=[False, False, False, False, False, False, False, False, False, False]
        
        

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.celulas[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if row==0:
            return ('?', self.get_value(row+1, col))
        elif row==9:
            return (self.get_value(row-1, col), '?')
        else:
            return (self.get_value(row-1, col), self.get_value(row+1, col))
        pass

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        
        if col==0:
            return ('?', self.get_value(row, col+1))
        elif col==9:
            return (self.get_value(row, col-1),'?')
        else:
            return (self.get_value(row, col-1), self.get_value(row, col+1))        
        
        
    def ajeita_column(self, col:int):
        streak=0
        linha_inicial=-1
        pode_contar=0
        for i in range(10):
            if self.get_value(i, col).isalpha() and self.get_value(i, col)!='W':
                if linha_inicial==-1:
                    linha_inicial=i
                streak+=1
                if self.get_value(i,col) in ('m','a'):
                    self.celulas[i][col]='m'
                    if self.adjacent_vertical_values(i, col)[1] in ('m','a','b','B', 'M') and self.adjacent_vertical_values(i, col)[0] in ('.', '?', 'W'):
                        self.set_piece(i,col,'t')
                        pode_contar+=1
                    elif self.adjacent_vertical_values(i, col)[1] in ('?', '.', 'W') and self.adjacent_vertical_values(i, col)[0] in ('m','a','t','M','T'):
                        self.set_piece(i,col,'b')
                        pode_contar+=1
                elif self.get_value(i, col) in ('t','T', 'b','B'):
                    pode_contar+=1
            else:
                if streak>1 and streak<=4:
                    if not (streak, 'v', linha_inicial, col) in self.boats[streak-1] and pode_contar==2:
                        self.boats[streak-1].append((streak, 'v', linha_inicial, col))
                    #print("contei um barco de tamanho", streak, "na coluna ", col)
                elif streak==1:
                    if self.get_value(i-1, col) in ('m','a'):
                        if self.adjacent_horizontal_values(i-1, col)[0] in ('.', '?','W') and self.adjacent_horizontal_values(i-1, col)[1] in ('.', '?','W') and self.adjacent_vertical_values(i-1,col)[0] in ('?','.', 'W') and self.adjacent_vertical_values(i-1,col)[1] in ('?','.', 'W'):
                            self.celulas[i-1][col]='c'
                            if not (1,'c',linha_inicial,col) in self.boats[0]:
                                self.boats[0].append((1,'c',linha_inicial,col))
                pode_contar=0
                streak=0
                linha_inicial=-1
        if streak>1 and streak<=4:
            if not (streak, 'v', linha_inicial,col) in self.boats[streak-1] and pode_contar==2:
                self.boats[streak-1].append((streak, 'v', linha_inicial, col))
            #print("contei um barco de tamanho", streak, "na coluna ", col)
        elif streak==1:
            if self.get_value(9, col) in ('m','a'):
                if self.adjacent_horizontal_values(9, col)[0] in ('.', '?', 'W') and self.adjacent_horizontal_values(9, col)[1] in ('.', '?', 'W') and self.adjacent_vertical_values(9,col)[0] in ('?','.', 'W') and self.adjacent_vertical_values(9,col)[1] in ('?','.', 'W'):
                    self.celulas[9][col]='c'
                    if not (1, 'c', linha_inicial, col) in self.boats[0]:
                        self.boats[0].append((1,'c',linha_inicial, col))
        if self.posicoes_livres_col[col]==0:
            self.colunas_ajeitadas[col]=True 
    

    def ajeita_row(self, row:int):
        pode_contar=0
        streak=0
        coluna_inicial=-1
        for i in range(10):
            if self.get_value(row, i).isalpha() and self.get_value(row, i)!='W':
                if coluna_inicial==-1:
                    coluna_inicial=i
                streak+=1
                if self.get_value(row, i) in ('m', 'a'):
                    self.celulas[row][i]='m'
                    if self.adjacent_horizontal_values(row, i)[1] in ('m','a','r','M','R') and self.adjacent_horizontal_values(row, i)[0] in ('.', '?','W'):
                        self.set_piece(row,i,'l')
                        pode_contar+=1
                    elif self.adjacent_horizontal_values(row, i)[1] in ('?','.','W') and self.adjacent_horizontal_values(row, i)[0] in ('m','a','l','L','A','M'):
                        self.set_piece(row,i,'r')
                        pode_contar+=1
                elif self.get_value(row,i) in ('l','L', 'R','r'):
                    pode_contar+=1
            else:
                if streak>1 and streak<=4:
                    if not (streak, 'h', row, coluna_inicial) in self.boats[streak-1] and pode_contar==2:
                        self.boats[streak-1].append((streak, 'h', row, coluna_inicial))
                    #print("contei um barco de tamanho", streak, "na linha ", row)
                elif streak==1:
                    if self.get_value(row, i-1) in ('m','a'):
                        if self.adjacent_vertical_values(row, i-1)[0] in ('.', '?', 'W') and self.adjacent_vertical_values(row, i-1)[1] in ('.', '?', 'W') and self.adjacent_horizontal_values(row, i-1)[0] in ('?','.', 'W') and self.adjacent_horizontal_values(row,i-1)[1] in ('?','.', 'W'):
                            self.celulas[row][i-1]='c'
                            if not (1, 'c', row, coluna_inicial) in self.boats[0]:
                                self.boats[0].append((1, 'c', row, coluna_inicial))
                pode_contar=0
                streak=0
                coluna_inicial=-1
        if streak>1 and streak<=4:
            if not (streak, 'h', row, coluna_inicial) in self.boats[streak-1] and pode_contar==2:
                self.boats[streak-1].append((streak, 'h', row, coluna_inicial))
            #print("contei um barco de tamanho", streak, "na linha ", row)
        elif streak==1:
            if self.get_value(row, 9) in ('m','a'):
                if self.adjacent_vertical_values(row, 9)[0] in ('.', '?', 'W') and self.adjacent_vertical_values(row, 9)[1] in ('.','?', 'W')and self.adjacent_horizontal_values(row, 9)[0] in ('?','.', 'W') and self.adjacent_horizontal_values(row,9)[1] in ('?','.', 'W'):
                    self.celulas[row][9]='c'
                    if not (1, 'c', row, coluna_inicial) in self.boats[0]:
                        self.boats[0].append((1, 'c', row, coluna_inicial))
        if self.posicoes_livres_linhas[row]==0:
            self.linhas_ajeitadas[row]=True

    
    def clear_row(self, row:int):
        for i in range(10):
            if self.get_value(row, i)=='-':
                self.set_piece(row, i, '.')

            
    def clear_column(self, column:int):
        for i in range(10):
            if self.get_value(i, column)=='-':
                self.set_piece(i, column, '.')


    def print_board(self):
        for i in range(10):
            for j in range(10):
                print(self.get_value(i, j), end='')
            print("")
                
    
    def Meio_vertical(self, row:int, col:int):
        return (self.adjacent_horizontal_values(row, col)[0] in ('.','W') or self.adjacent_horizontal_values(row, col)[1] in ('.','W') or not self.adjacent_vertical_values(row, col)[0] in ('.','W','-') or not self.adjacent_vertical_values(row, col)[1] in ('.','W','-') or (self.a_ser_colocado_em_linhas[row]<2 and self.a_ser_colocado_em_colunas[col]>2))
    

    def Meio_horizontal(self, row:int, col:int):
        return (not self.adjacent_horizontal_values(row, col)[0] in ('.','W','-') or not self.adjacent_horizontal_values(row, col)[1] in ('.','W', '-') or self.adjacent_vertical_values(row, col)[0] in ('.','W') or self.adjacent_vertical_values(row, col)[1] in ('.','W') or (self.a_ser_colocado_em_linhas[row]>2 and self.a_ser_colocado_em_colunas[col]<2)) 
    

    def set_piece(self, row:int, column:int ,piece:str):
        if self.celulas[row][column]=='-':
            self.celulas[row][column]=piece
            self.posicoes_livres_linhas[row]-=1
            self.posicoes_livres_col[column]-=1
            if piece.isalpha() and piece!='W':
                self.a_ser_colocado_em_linhas[row]-=1
                self.a_ser_colocado_em_colunas[column]-=1
            if piece=='c' or piece=='C':
                self.boats[0].append((1, 'c', row, column))
            if self.a_ser_colocado_em_colunas[column]==0 and self.posicoes_livres_col[column] >0:
                self.clear_column(column)
            if self.a_ser_colocado_em_linhas[row]==0 and self.posicoes_livres_linhas[row]>0:
                self.clear_row(row)
            if self.a_ser_colocado_em_colunas[column]==self.posicoes_livres_col[column] and self.posicoes_livres_col[column]>0:
                self.completa_coluna(column)
            if self.a_ser_colocado_em_linhas[row]==self.posicoes_livres_linhas[row] and self.posicoes_livres_linhas[row]>0:
                self.completa_row(row)
        else:
            if self.get_value(row,column).isalpha() and piece=='.':
                return
            elif self.get_value(row,column).lower()!=piece: 
                self.celulas[row][column]=piece
                if piece=='c' or piece=='C':
                    self.boats[0].append((1,'c',row, column))

    def clear_adj_pos(self, row:int, col:int, piece):
        if piece=='M' or piece=='m':
            if row==9:
                self.set_piece(row-1, col, '.')
                self.set_piece(row-1, col-1, '.')
                self.set_piece(row-1, col+1, '.')
            elif row==0:
                self.set_piece(row+1, col, '.')
                self.set_piece(row+1, col-1, '.')
                self.set_piece(row+1, col+1, '.')
            else:
                if col==0:
                    self.set_piece(row+1, col+1, '.')
                    self.set_piece(row, col+1, '.')
                    self.set_piece(row-1, col+1, '.')
                elif col==9:
                    self.set_piece(row+1, col-1, '.')
                    self.set_piece(row, col-1, '.')
                    self.set_piece(row-1, col-1, '.')
                else:
                    self.set_piece(row+1, col-1, '.')
                    self.set_piece(row+1, col+1, '.')
                    self.set_piece(row-1, col-1, '.')
                    self.set_piece(row-1, col+1, '.')
                    if self.Meio_horizontal(row, col) and not self.Meio_vertical(row, col):
                        self.set_piece(row+1, col, '.')
                        self.set_piece(row-1, col, '.')
                    elif not self.Meio_horizontal(row, col) and self.Meio_vertical(row, col):
                        self.set_piece(row, col-1, '.')
                        self.set_piece(row, col+1, '.')
        elif piece=='a':
            if row==9:
                if col==0:
                    self.set_piece(row-1, col+1,'.')
                elif col==9:
                    self.set_piece(row-1, col-1,'.')
                else:
                    self.set_piece(row-1, col+1,'.')
                    self.set_piece(row-1, col-1,'.')
            elif row==0:
                if col==0:
                    self.set_piece(row+1, col+1,'.')
                elif col==9:
                    self.set_piece(row+1, col-1, '.')
                else:
                    self.set_piece(row+1, col+1,'.')
                    self.set_piece(row+1, col+1,'.')
            else:
                if col==0:
                    self.set_piece(row-1, col+1,'.')
                    self.set_piece(row+1, col+1,'.')
                elif col==9:
                    self.set_piece(row-1, col-1,'.')
                    self.set_piece(row+1, col-1,'.')
                else:
                    self.set_piece(row-1, col+1,'.')
                    self.set_piece(row+1, col+1,'.')
                    self.set_piece(row-1, col-1,'.')
                    self.set_piece(row+1, col-1,'.')
            
        elif piece=='T' or piece=='t':
            if row==0:
                if col==0:
                    self.set_piece(row, col+1, '.')
                    self.set_piece(row+1, col+1, '.')
                elif col==9:
                    self.set_piece(row, col-1, '.')
                    self.set_piece(row+1, col-1, '.')
                else:
                    self.set_piece(row, col+1, '.')
                    self.set_piece(row+1, col+1, '.')
                    self.set_piece(row, col-1, '.')
                    self.set_piece(row+1, col-1, '.')
            else:
                self.set_piece(row-1, col, '.')
                if col==0:
                    self.set_piece(row-1, col+1, '.')
                    self.set_piece(row, col+1, '.')
                    self.set_piece(row+1, col+1, '.')
                elif col==9:
                    self.set_piece(row-1, col-1, '.')
                    self.set_piece(row, col-1, '.')
                    self.set_piece(row+1, col-1, '.')
                else:
                    self.set_piece(row-1, col+1, '.')
                    self.set_piece(row-1, col-1, '.')
                    self.set_piece(row, col+1, '.')
                    self.set_piece(row+1, col+1, '.')
                    self.set_piece(row, col-1, '.')
                    self.set_piece(row+1, col-1, '.')
        elif piece=='B' or piece=='b':
            if row==9:
                if col==0:
                    self.set_piece(row, col+1, '.')
                    self.set_piece(row-1, col+1, '.')
                elif col==9:
                    self.set_piece(row, col-1, '.')
                    self.set_piece(row-1, col-1, '.')
                else:
                    self.set_piece(row, col+1, '.')
                    self.set_piece(row-1, col+1, '.')
                    self.set_piece(row, col-1, '.')
                    self.set_piece(row-1, col-1, '.')
            else:
                self.set_piece(row+1, col, '.')
                if col==0:
                    self.set_piece(row-1, col+1, '.')
                    self.set_piece(row, col+1, '.')
                    self.set_piece(row+1, col+1, '.')
                elif col==9:
                    self.set_piece(row-1, col-1, '.')
                    self.set_piece(row, col-1, '.')
                    self.set_piece(row+1, col-1, '.')
                else:
                    self.set_piece(row-1, col+1, '.')
                    self.set_piece(row-1, col-1, '.')
                    self.set_piece(row, col+1, '.')
                    self.set_piece(row+1, col+1, '.')
                    self.set_piece(row, col-1, '.')
                    self.set_piece(row+1, col-1, '.')
        elif piece=='C' or piece=='c':
            if row==0:
                self.set_piece(row+1, col, '.')
                if col==0:
                    self.set_piece(row+1, col+1, '.')
                    self.set_piece(row, col+1, '.')
                elif col==9:
                    self.set_piece(row+1, col-1, '.')
                    self.set_piece(row, col-1, '.')
                else:
                    self.set_piece(row+1, col+1, '.')
                    self.set_piece(row, col+1, '.')
                    self.set_piece(row+1, col-1, '.')
                    self.set_piece(row, col-1, '.')
            elif row==9:
                self.set_piece(row-1, col, '.')
                if col==0:
                    self.set_piece(row-1, col+1, '.')
                    self.set_piece(row, col+1, '.')
                elif col==9:
                    self.set_piece(row-1, col-1, '.')
                    self.set_piece(row, col-1, '.')
                else:
                    self.set_piece(row-1, col+1, '.')
                    self.set_piece(row, col+1, '.')
                    self.set_piece(row-1, col-1, '.')
                    self.set_piece(row, col-1, '.')
            else:
                self.set_piece(row-1, col, '.')
                self.set_piece(row+1, col, '.')
                if col==0:
                    self.set_piece(row-1, col+1, '.')
                    self.set_piece(row, col+1, '.')
                    self.set_piece(row+1, col+1, '.')
                elif col==9:
                    self.set_piece(row-1, col-1, '.')
                    self.set_piece(row, col-1, '.')
                    self.set_piece(row+1, col-1, '.')
                else:
                    self.set_piece(row-1, col+1, '.')
                    self.set_piece(row, col+1, '.')
                    self.set_piece(row+1, col+1, '.')
                    self.set_piece(row-1, col-1, '.')
                    self.set_piece(row, col-1, '.')
                    self.set_piece(row+1, col-1, '.')
        elif piece=='L' or piece=='l':
            if row ==0:
                self.set_piece(row+1, col, '.')
                self.set_piece(row+1, col+1, '.')
                if col>=1 and col<=8:
                    self.set_piece(row+1, col-1, '.')
                    self.set_piece(row, col-1, '.')
            elif row==9:
                self.set_piece(row-1, col, '.')
                self.set_piece(row-1, col+1, '.')
                if col>=1 and col<=8:
                    self.set_piece(row-1, col-1, '.')
                    self.set_piece(row, col-1, '.')
            else:
                self.set_piece(row+1, col, '.')
                self.set_piece(row+1, col+1, '.')
                self.set_piece(row-1, col, '.')
                self.set_piece(row-1, col+1, '.')
                if col>=1 and col<=8:
                    self.set_piece(row, col-1, '.')
                    self.set_piece(row+1, col-1, '.')
                    self.set_piece(row-1, col-1, '.')
        elif piece=='R' or piece=='r':
            if row==0:
                self.set_piece(row+1, col, '.')
                self.set_piece(row+1, col-1, '.')
                if col>=1 and col<=8:
                    self.set_piece(row+1, col+1, '.')
                    self.set_piece(row, col+1, '.')
            elif row==9:
                self.set_piece(row-1, col, '.')
                self.set_piece(row-1, col-1, '.')
                if col>=1 and col<=8:
                    self.set_piece(row, col+1, '.')
                    self.set_piece(row-1, col+1, '.')
            else:
                self.set_piece(row+1, col, '.')
                self.set_piece(row+1, col-1, '.')
                self.set_piece(row-1, col, '.')
                self.set_piece(row-1, col-1, '.')
                if col>=1 and col<=8:
                    self.set_piece(row, col+1, '.')
                    self.set_piece(row+1, col+1, '.')
                    self.set_piece(row-1, col+1, '.')


    def completa_coluna(self, col:int):
        for i in range(10):
            if self.celulas[i][col]=='-' and self.posicoes_livres_col[col]>0:
                self.set_piece(i,col,'a')
                self.clear_adj_pos(i, col, 'a')


    def completa_row(self, row:int):
        for i in range(10):
            if self.celulas[row][i]=='-' and self.posicoes_livres_linhas[row]>0:
                self.set_piece(row,i,'a')
                self.clear_adj_pos(row,i,'a')
    

    def place_boat(self, tamanho:int, sentido:str, row:int, col:int):
        if tamanho==1:
            self.set_piece(row, col, 'c')
            return
        if sentido=='v':
            for i in range(tamanho):
                if i==0:
                    self.set_piece(row, col, 't')
                    self.clear_adj_pos(row, col, 't')
                elif i==tamanho-1:
                    self.set_piece(row+i, col, 'b')
                    self.clear_adj_pos(row+i, col, 'b')
                else:
                    self.set_piece(row+i, col, 'm')
                    self.clear_adj_pos(row+i, col, 'm')
        elif sentido=='h':
            for i in range(tamanho):
                if i==0:
                    self.set_piece(row, col, 'l')
                    self.clear_adj_pos(row, col, 'l')
                elif i==tamanho-1:
                    self.set_piece(row, col+i, 'r')
                    self.clear_adj_pos(row, col+i, 'r')
                else:
                    self.set_piece(row, col+i, 'm')
                    self.clear_adj_pos(row, col+i, 'm')
        self.boats[tamanho-1].append((tamanho, sentido, row, col))

   
    def ajeita_board(self):
        for i in range(10):
            if self.linhas_ajeitadas[i]==False:
                self.ajeita_row(i)
            if self.colunas_ajeitadas[i]==False:
                self.ajeita_column(i)     


    def find_pos_boat(self, size:int):
        #procurar horizontalmente
        hipoteses=[]
        for row in range(10):
            aux=self.list_linhas[row]
            if aux>=size:
                for col in range(10-(size-1)):
                    flag=True
                    aux_a_colocar=self.a_ser_colocado_em_linhas[row]
                    if aux<size:
                        break
                    for i in range(size): 
                        if i==0:
                            if self.get_value(row,col) in ('.','W') or not self.adjacent_horizontal_values(row,col)[0] in ('-','.','?','W'):
                                flag=False
                                break
                            if self.get_value(row,col).isalpha() and self.get_value(row,col)!='W':
                                aux-=1
                                
                        if i==(size-1):
                            if self.get_value(row,col+i) in ('.','W') or not self.adjacent_horizontal_values(row,col+i)[1] in ('-','.','?','W'):
                                flag=False 
                                break
                        if self.get_value(row,col+i) in ('.','W'):
                            flag=False
                            break    
                         
                        if self.get_value(row,col+i)=='-':
                            aux_a_colocar-=1
                    if aux_a_colocar>=0 and flag:
                        if size==1:
                            if not (size, 'c', row,col) in self.boats[size-1]:
                                hipoteses.append((size,'c',row,col))
                        else:
                            if not (size,'h', row,col) in self.boats[size-1]:
                                hipoteses.append((size,'h',row,col))
                                         
        
        #procura vertical
        for col in range(10):
            aux=self.list_colunas[col]
            if aux>=size:
                for row in range(10-(size-1)):
                    flag=True
                    aux_a_colocar=self.a_ser_colocado_em_colunas[col]
                    if aux<size:
                        break
                    for i in range(size):
                        if i==0:
                            if self.get_value(row,col) in ('.','W') or not self.adjacent_vertical_values(row,col)[0] in ('-','.','?'):
                                flag=False
                                break
                            if self.get_value(row,col).isalpha() and self.get_value(row,col)!='W':
                                aux-=1
                        if i==(size-1):
                            if self.get_value(row+i,col) in ('.','W') or not self.adjacent_vertical_values(row+i,col)[1] in ('-','.','W','?'):
                                flag=False
                                break
                        if self.get_value(row+i,col) in ('.','W'):
                            flag=False
                            break
                        if self.get_value(row+i,col)=='-':
                            aux_a_colocar-=1
                    if aux_a_colocar>=0 and flag:
                        if size==1:
                            if not (size ,'c', row, col) in self.boats[size-1]:
                                hipoteses.append((size,'c',row,col))
                        else:
                            if not (size ,'v', row, col) in self.boats[size-1]:
                                hipoteses.append((size, 'v',row, col))
        return hipoteses

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """
        from sys import stdin
        str_linhas=stdin.readline().split()
        row_numbers=[]
        for word in str_linhas:
            if word.isdigit():
                row_numbers.append(int(word))
        str_colunas=stdin.readline().split()
        column_numbers=[]
        for word in str_colunas:
            if word.isdigit():
                column_numbers.append(int(word))
        n_clues=stdin.readline()
        n_clues=int(n_clues)
        clues=[]
        i=0
        while (i<n_clues):
            clue_input=stdin.readline().split()
            clue_x=int(clue_input[1])
            clue_y=int(clue_input[2])
            clue_piece=clue_input[3]
            clue=(clue_x, clue_y, clue_piece)
            clues.append(clue)
            i+=1
        tabuleiro=Board(row_numbers, column_numbers, clues)
        return tabuleiro

    


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.board=board
        self.initial=0

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        actions=[]
        if len(state.board.boats[3])<1:
            actions=state.board.find_pos_boat(4)
        elif len(state.board.boats[2])<2:
            actions= state.board.find_pos_boat(3)
        elif len(state.board.boats[1])<3:
            actions=state.board.find_pos_boat(2)
        elif len(state.board.boats[0])<4:
            actions=state.board.find_pos_boat(1)
        return actions
        
    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        new_state=BimaruState(state.board)
        new_state.board=copy.deepcopy(state.board)
        new_state.board.celulas=copy.deepcopy(state.board.celulas)
        new_state.board.a_ser_colocado_em_linhas=copy.deepcopy(state.board.a_ser_colocado_em_linhas)
        new_state.board.a_ser_colocado_em_colunas=copy.deepcopy(state.board.a_ser_colocado_em_colunas)
        new_state.board.posicoes_livres_linhas=copy.deepcopy(state.board.posicoes_livres_linhas)
        new_state.board.posicoes_livres_col=copy.deepcopy(state.board.posicoes_livres_col)
        new_state.board.boats=copy.deepcopy(state.board.boats)
        new_state.board.linhas_ajeitadas=copy.deepcopy(state.board.linhas_ajeitadas)
        new_state.board.colunas_ajeitadas=copy.deepcopy(state.board.colunas_ajeitadas)
        new_state.board.list_linhas=copy.deepcopy(state.board.list_linhas)
        new_state.board.list_colunas=copy.deepcopy(state.board.list_colunas)
        new_state.board.lista_clues=copy.deepcopy(state.board.lista_clues)
        new_state.board.place_boat(action[0], action[1], action[2], action[3])
        new_state.board.ajeita_board()
        return new_state

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        completo=np.full(10,0) #[0,0,0,0,0,0,0,0,0,0]
        if len(state.board.boats[0])==4 and len(state.board.boats[1])==3 and len(state.board.boats[2])==2 and len(state.board.boats[3])==1 and np.all(state.board.posicoes_livres_col == completo) and np.all(state.board.posicoes_livres_linhas == completo) and np.all(state.board.a_ser_colocado_em_colunas == completo) and np.all(state.board.a_ser_colocado_em_linhas == completo): #state.board.posicoes_livres_col==completo and state.board.posicoes_livres_linhas==completo and state.board.a_ser_colocado_em_colunas==completo and state.board.a_ser_colocado_em_linhas==completo:
            return True
        else:
            return False
        

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        falta_colocar=0
        for i in range(10):
            falta_colocar+=node.state.board.a_ser_colocado_em_linhas[i]
            falta_colocar+=node.state.board.a_ser_colocado_em_colunas[i]
        return falta_colocar
    
    def zero_in_board(self):
        for i in range(10):
            if self.board.list_linhas[i]==0:
                for j in range(10):
                    if self.board.get_value(i,j)=='-':
                        self.board.posicoes_livres_linhas[i]-=1
                        self.board.posicoes_livres_col[j]-=1
                    self.board.celulas[i][j]='.'
            if self.board.list_colunas[i]==0:
                for j in range(10):
                    if self.board.get_value(j,i)=='-':
                        self.board.posicoes_livres_col[i]-=1
                        self.board.posicoes_livres_linhas[j]-=1
                    self.board.celulas[j][i]='.'


    def set_clues(self, lista_clues):
        for clue in lista_clues:
            self.board.set_piece(clue[0], clue[1], clue[2])
            self.board.clear_adj_pos(clue[0], clue[1], clue[2])    
    
    
    def analisa_clues(self):
        for i in range(len(self.board.lista_clues)):
            if self.board.lista_clues[i][2]=='T':
                if self.board.lista_clues[i][0]==8:
                    if self.board.adjacent_vertical_values(self.board.lista_clues[i][0], self.board.lista_clues[i][1])[1]=='-':
                        self.board.set_piece(9, self.board.lista_clues[i][1], 'b')
                        self.board.clear_adj_pos(9, self.board.lista_clues[i][1], 'b')
                        self.board.boats[1].append((2, 'v', self.board.lista_clues[i][0], self.board.lista_clues[i][1]))
                else:
                    if self.board.adjacent_vertical_values(self.board.lista_clues[i][0], self.board.lista_clues[i][1])[1]=='-':
                        self.board.set_piece(self.board.lista_clues[i][0]+1, self.board.lista_clues[i][1], 'm')
                        self.board.clear_adj_pos(self.board.lista_clues[i][0]+1, self.board.lista_clues[i][1], 'm')
            elif self.board.lista_clues[i][2]=='B':
                if self.board.lista_clues[i][0]==1:
                    if self.board.adjacent_vertical_values(self.board.lista_clues[i][0], self.board.lista_clues[i][1])[0]=='-':
                        self.board.set_piece(0, self.board.lista_clues[i][1], 't')
                        self.board.clear_adj_pos(0, self.board.lista_clues[i][1], 't')
                        self.board.boats[1].append((2, 'v', self.board.lista_clues[i][0]-1, self.board.lista_clues[i][1]))
                else:
                    if self.board.adjacent_vertical_values(self.board.lista_clues[i][0], self.board.lista_clues[i][1])[0]=='-':
                        self.board.set_piece(self.board.lista_clues[i][0]-1, self.board.lista_clues[i][1], 'm')
                        self.board.clear_adj_pos(self.board.lista_clues[i][0]-1, self.board.lista_clues[i][1], 'm')
            elif self.board.lista_clues[i][2]=='L':
                if self.board.lista_clues[i][1]==8:
                    if self.board.adjacent_horizontal_values(self.board.lista_clues[i][0], self.board.lista_clues[i][1])[1]=='-':
                        self.board.set_piece(self.board.lista_clues[i][0], 9, 'r')
                        self.board.clear_adj_pos(self.board.lista_clues[i][0], 9, 'r')
                        self.board.boats[1].append((2, 'h', self.board.lista_clues[i][0], self.board.lista_clues[i][1]))
                else:
                    if self.board.adjacent_horizontal_values(self.board.lista_clues[i][0], self.board.lista_clues[i][1])[1]=='-':
                        self.board.set_piece(self.board.lista_clues[i][0], self.board.lista_clues[i][1]+1, 'm')
                        self.board.clear_adj_pos(self.board.lista_clues[i][0], self.board.lista_clues[i][1]+1, 'm')
            elif self.board.lista_clues[i][2]=='R':
                if self.board.lista_clues[i][1]==1:
                    if self.board.adjacent_horizontal_values(self.board.lista_clues[i][0], self.board.lista_clues[i][1])[0]=='-':
                        self.board.set_piece(self.board.lista_clues[i][0], 0, 'l')
                        self.board.clear_adj_pos(self.board.lista_clues[i][0], 0, 'l')
                        self.board.boats[1].append((2, 'h', self.board.lista_clues[i][0]-1, self.board.lista_clues[i][1]))
                else:
                    if self.board.adjacent_horizontal_values(self.board.lista_clues[i][0], self.board.lista_clues[i][1])[0]=='-':
                        self.board.set_piece(self.board.lista_clues[i][0], self.board.lista_clues[i][1]-1, 'm')
                        self.board.clear_adj_pos(self.board.lista_clues[i][0], self.board.lista_clues[i][1]-1, 'm')
            elif self.board.lista_clues[i][2]=='M':
                if self.board.lista_clues[i][0]==0 or self.board.lista_clues[i][0]==9:
                    if self.board.lista_clues[i][1]==1:
                        self.board.set_piece(self.board.lista_clues[i][0], 0, 'l')
                        self.board.clear_adj_pos(self.board.lista_clues[i][0], 0, 'l')
                        self.board.set_piece(self.board.lista_clues[i][0], 2, 'm')
                        self.board.clear_adj_pos(self.board.lista_clues[i][0], 2, 'm')
                    elif self.board.lista_clues[i][1]==8:
                        self.board.set_piece(self.board.lista_clues[i][0], 9, 'r')
                        self.board.clear_adj_pos(self.board.lista_clues[i][0], 9, 'r')
                        self.board.set_piece(self.board.lista_clues[i][0], 7, 'm')
                        self.board.clear_adj_pos(self.board.lista_clues[i][0], 7, 'm')
                    else:
                        self.board.set_piece(self.board.lista_clues[i][0], self.board.lista_clues[i][1]+1,'m')
                        self.board.clear_adj_pos(self.board.lista_clues[i][0], self.board.lista_clues[i][1]+1,'m')
                        self.board.set_piece(self.board.lista_clues[i][0], self.board.lista_clues[i][1]-1,'m')
                        self.board.clear_adj_pos(self.board.lista_clues[i][0], self.board.lista_clues[i][1]+1,'m')
                elif self.board.lista_clues[i][1]==0 or self.board.lista_clues[i][1]==9:
                    if self.board.lista_clues[i][0]==1:
                        self.board.set_piece(0, self.board.lista_clues[i][1], 't')
                        self.board.clear_adj_pos(0, self.board.lista_clues[i][1], 't')
                        self.board.set_piece(2, self.board.lista_clues[i][1], 'm')
                        self.board.clear_adj_pos(2, self.board.lista_clues[i][1], 'm')
                    elif self.board.lista_clues[i][0]==8:
                        self.board.set_piece(9, self.board.lista_clues[i][1], 'b')
                        self.board.clear_adj_pos(9, self.board.lista_clues[i][1], 'b')
                        self.board.set_piece(7, self.board.lista_clues[i][1], 'm')
                        self.board.clear_adj_pos(7, self.board.lista_clues[i][1], 'm')
                    else:
                        self.board.set_piece(self.board.lista_clues[i][0]+1, self.board.lista_clues[i][1],'m')
                        self.board.clear_adj_pos(self.board.lista_clues[i][0]+1, self.board.lista_clues[i][1],'m')
                        self.board.set_piece(self.board.lista_clues[i][0]-1, self.board.lista_clues[i][1],'m')
                        self.board.clear_adj_pos(self.board.lista_clues[i][0]-1, self.board.lista_clues[i][1],'m')
                else:
                    if self.board.Meio_horizontal(self.board.lista_clues[i][0],self.board.lista_clues[i][1])==False and self.board.Meio_vertical(self.board.lista_clues[i][0],self.board.lista_clues[i][1])==True:
                        if self.board.lista_clues[i][0]==1:
                            self.board.set_piece(0,self.board.lista_clues[i][1],'t')
                            if self.board.get_value(3,self.board.lista_clues[i][1])=='.':
                                self.board.set_piece(2,self.board.lista_clues[i][1],'b')
                                self.board.clear_adj_pos(2,self.board.lista_clues[i][1],'b')
                            else:
                                self.board.set_piece(2,self.board.lista_clues[i][1],'m')
                                self.board.clear_adj_pos(2,self.board.lista_clues[i][1],'m')
                        elif self.board.lista_clues[i][0]==8:
                            self.board.set_piece(9,self.board.lista_clues[i][1],'b')
                            if self.board.get_value(6,self.board.lista_clues[i][1])=='.':
                                self.board.set_piece(7,self.board.lista_clues[i][1],'t')
                                self.board.clear_adj_pos(7,self.board.lista_clues[i][1],'t')
                            else:
                                self.board.set_piece(7,self.board.lista_clues[i][1],'m')
                                self.board.clear_adj_pos(7,self.board.lista_clues[i][1],'m')
                        else:
                            if self.board.get_value(self.board.lista_clues[i][0]-2,self.board.lista_clues[i][1])=='.':
                                self.board.set_piece(self.board.lista_clues[i][0]-1,self.board.lista_clues[i][1],'t')
                                self.board.clear_adj_pos(self.board.lista_clues[i][0]-1,self.board.lista_clues[i][1],'t')
                            else:
                                self.board.set_piece(self.board.lista_clues[i][0]-1,self.board.lista_clues[i][1],'m')
                                self.board.clear_adj_pos(self.board.lista_clues[i][0]-1,self.board.lista_clues[i][1],'m')
                            if self.board.get_value(self.board.lista_clues[i][0]+2,self.board.lista_clues[i][1])=='.':
                                self.board.set_piece(self.board.lista_clues[i][0]+1,self.board.lista_clues[i][1],'b')
                                self.board.clear_adj_pos(self.board.lista_clues[i][0]+1,self.board.lista_clues[i][1],'b')
                            else:
                                self.board.set_piece(self.board.lista_clues[i][0]+1,self.board.lista_clues[i][1],'m')
                                self.board.clear_adj_pos(self.board.lista_clues[i][0]+1,self.board.lista_clues[i][1],'m')
                    elif self.board.Meio_vertical(self.board.lista_clues[i][0],self.board.lista_clues[i][1])==False and self.board.Meio_horizontal(self.board.lista_clues[i][0],self.board.lista_clues[i][1])==True:
                        if self.board.lista_clues[i][1]==1:
                            self.board.set_piece(self.board.lista_clues[i][0],0,'l')
                            self.board.set_piece(self.board.lista_clues[i][0],2,'m')
                            self.board.clear_adj_pos(self.board.lista_clues[i][0],2,'m')
                        elif self.board.lista_clues[i][1]==8:
                            self.board.set_piece(self.board.lista_clues[i][0],9,'r')
                            self.board.set_piece(self.board.lista_clues[i][0],7,'m')
                            self.board.clear_adj_pos(self.board.lista_clues[i][1],7,'m')
                        else:
                            if self.board.get_value(self.board.lista_clues[i][0],self.board.lista_clues[i][1]-2)=='.':
                                self.board.set_piece(self.board.lista_clues[i][0],self.board.lista_clues[i][1]-1,'l')
                                self.board.clear_adj_pos(self.board.lista_clues[i][0],self.board.lista_clues[i][1]-1,'l')
                            else:
                                self.board.set_piece(self.board.lista_clues[i][0],self.board.lista_clues[i][1]-1,'m')
                                self.board.clear_adj_pos(self.board.lista_clues[i][0],self.board.lista_clues[i][1]-1,'m')
                            if self.board.get_value(self.board.lista_clues[i][0],self.board.lista_clues[i][1]+2)=='.':
                                self.board.set_piece(self.board.lista_clues[i][0],self.board.lista_clues[i][1]+1,'r')
                                self.board.clear_adj_pos(self.board.lista_clues[i][0],self.board.lista_clues[i][1]+1,'r')
                            else:
                                self.board.set_piece(self.board.lista_clues[i][0],self.board.lista_clues[i][1]+1,'m')
                                self.board.clear_adj_pos(self.board.lista_clues[i][0],self.board.lista_clues[i][1]+1,'m')
    

if __name__ == "__main__":
    board=Board.parse_instance()
    bimaru1=Bimaru(board)
    bimaru1.zero_in_board()
    bimaru1.set_clues(board.lista_clues)
    bimaru1.analisa_clues()
    board.ajeita_board()
    bimaru1.initial=BimaruState(board)
    if bimaru1.goal_test(bimaru1.initial):
        bimaru1.initial.board.print_board()
        exit(0)
    goal_node=astar_search(bimaru1)
    if goal_node==None:
        print("¯\_(ツ)_/¯")
    else:
        goal_node.state.board.print_board()
    exit(0)
    
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
