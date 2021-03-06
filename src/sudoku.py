from cnf_utils import cnf_variables, litteral

import copy
import random
from itertools import product

import numpy as np
"""
implementation pour representer un sudoku en une
formule propositionnelle


"""
variables_sudoku = {}


def sudoku():
    """
    Un sudoku de niveau simple
    """
    return [
        [0, 0, 9, 0, 0, 0, 0, 7, 1],
        [2, 0, 0, 6, 9, 8, 5, 0, 0],
        [6, 5, 0, 3, 1, 0, 0, 0, 2],

        [5, 6, 3, 8, 0, 1, 4, 0, 9],
        [0, 9, 0, 0, 0, 0, 0, 0, 8],
        [1, 0, 8, 9, 0, 2, 3, 6, 5],

        [7, 0, 5, 0, 8, 3, 2, 9, 0],
        [8, 3, 0, 0, 2, 0, 0, 5, 0],
        [9, 0, 0, 4, 6, 0, 0, 3, 7]
    ]


def s_16():

    return [
        [0, 6, 8, 12, 0, 0, 13, 0, 1, 7, 0, 2, 0, 0, 4, 10],
        [7, 14, 0, 10, 0, 5, 8, 1, 12, 0, 0, 13, 0, 9, 3, 16],
        [1, 0, 5, 0, 0, 0, 11, 0, 0, 0, 14, 0, 13, 0, 12, 0],
        [13, 15, 0, 0, 12, 0, 0, 6, 3, 0, 4, 0, 7, 11, 0, 0],
        [0, 0, 0, 11, 0, 0, 0, 15, 0, 0, 0, 7, 0, 0, 14, 12],
        [0, 4, 0, 0, 0, 0, 14, 12, 13, 3, 9, 0, 8, 1, 0, 0],
        [12, 8, 14, 0, 0, 2, 0, 0, 10, 0, 1, 0, 0, 0, 0, 9],
        [0, 2, 0, 9, 1, 8, 0, 0, 11, 16, 12, 0, 15, 0, 10, 13],
        [5, 12, 0, 15, 0, 1, 7, 4, 0, 0, 16, 3, 10, 0, 13, 0],
        [2, 0, 0, 0, 0, 3, 0, 9, 0, 0, 13, 0, 0, 12, 8, 5],
        [0, 0, 4, 8, 0, 11, 15, 10, 5, 12, 0, 0, 0, 0, 9, 0],
        [3, 16, 0, 0, 13, 0, 0, 0, 8, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 15, 6, 0, 7, 0, 11, 14, 0, 0, 8, 0, 0, 5, 1],
        [0, 10, 0, 14, 0, 13, 0, 0, 0, 11, 0, 0, 0, 6, 0, 7],
        [11, 5, 1, 0, 9, 0, 0, 3, 6, 10, 7, 0, 12, 0, 15, 8],
        [16, 7, 0, 0, 14, 0, 10, 8, 0, 1, 0, 0, 11, 13, 2, 0]

    ]


def reset_var():
    global variables_sudoku
    variables_sudoku = {}


def var(row, column, value, n):
    """
    var doit obligatoirement etre comprit dans l'intervalle:
    [1; +infini]
    """
    global variables_sudoku

    var = (row * n + column) + (n**2 * (value - 1)) + 1
    variables_sudoku[var] = (row, column, value)

    return var


def unvar(var):
    global variables_sudoku
    return variables_sudoku[var]


def printer(s, n):
    """
    Affichage pour sudoku
    """
    space = len(str(n**2))
    
    for i in range(n**2):
        if i != 0 and i % n == 0:
            print('-' * (((n+2)*space)*n + n))

        to_print = ''
        for j in range(n**2):
            if j != 0 and j % n == 0:
                to_print += "|"
                
            v = "." if s[i][j] == 0 else str(s[i][j])
                
            if len(v) == space:
                p = v
            else:
                p = v + " " * (space - len(v))

            to_print += " " + p

        print(to_print)


def translate(s, dict_s):
    """
    Transforme le sudoku de depart s en sudoku resolu a
    l'aide des assignations valide donnees dans dict_s
    """

    for key, val in dict_s.items():
        if val is True:
            row, col, val = unvar(key)
            s[row][col] = val

    return s


def print_vars(interp, line):
    print("----------------------------------------")
    print(f"------------------{line}-------------------")
    for key, val in interp.items():
        print(unvar(key), val)


def display(s_start, dict_s, n):
    """
    Affichage du sudoku de depart, puis de sa version complete.
    """

    s_end = translate(copy.deepcopy(s_start), dict_s)

    print("## Original\n")

    printer(s_start, n)
    print()

    print("## Solved\n")

    printer(s_end, n)
    print()


def formulate_sudoku(sudoku, n):
    """
    args:
        n: la taille d'un carre du sudoku, n^2 = le nombre de chiffre contenu, n*n*n= le nombre total de chiffre
        sudoku : list(list()) avec sudoku[i][j] = {x un nombre | 1 =< x =< n*n, '-' la case vide}

    return:
        list: une list de clause en 'forme normale conjonctive' ou CNF

    Pour construire le sudoku, 

    Contraintes:
        1) chaque case doit contenir au moins un nombre
        2) chaque ligne de taille n*n doit contenir qu'une seul fois un meme nombre
        3) chaque colonne de taille n*n doit contenir qu'une seul fois un meme nombre
        4) chaque carre de taille n*n doit contenir qu'une seul fois un meme nombre

    """
    reset_var()

    # Conjonctions de disjonctions
    clauses = []

    clause = []
    squared = n * n

    # Initialiser avec les nombres deja presents dans le sudoku
    for row in range(squared):
        for column in range(squared):
            if sudoku[row][column] != 0:
                clauses.append([
                    var(row, column, int(sudoku[row][column]), squared)
                ])

    # 1)
    for row in range(squared):
        for column in range(squared):
            clause = []
            for value in range(1, squared + 1):
                clause.append(var(row, column, value, squared))
            clauses.append(clause)

    # 2)
    """
                Pour chaque ligne on veut qu'il n'y ait pas deux fois le meme nombre
                donc on fait pour chaque valeur:
                i = row
                j = column
                v = value
    
                (xi,j,v nand xi,j+1,v) and (xi,j,v nand xi,j+2,v) and ... and (xi,j,v nand xi,j+(squared-i),v)
                De cette maniere on empeche deux case d'une meme ligne d'avoir le meme nombre

                x nand y <=> (not x or not y)
    """
    for row in range(squared):
        for column in range(squared):
            for value in range(1, squared + 1):
                for pair in range(column + 1, squared):
                    clauses.append([
                        litteral(var(row, column, value, squared), false=True),
                        litteral(var(row, pair, value, squared), false=True)
                    ])

    # 3)
    # Meme proceder pour les colonnes que pour les lignes
    for column in range(squared):
        for row in range(squared):
            for value in range(1, squared + 1):
                for pair in range(row + 1, squared):
                    clauses.append([
                        litteral(var(row, column, value, squared), false=True),
                        litteral(var(pair, column, value, squared), false=True)
                    ])

    # 4)
    # On fait en gros la meme chose mais en plus complique:
    """ 
    r = row
    c = column

        r   0     1     2 

    c     0 1 2 3 4 5 6 7 8 = r+i
       0 [-,-,-,-,-,-,-,-,-]
    0  1 [-,-,-,-,-,-,-,-,-]
       2 [-,-,-,-,-,-,-,-,-]
       3 [-,-,-,-,-,-,-,-,-]
    1  4 [-,-,-,-,-,-,-,-,-]
       5 [-,-,-,-,-,-,-,-,-]
       6 [-,-,-,-,-,-,-,-,-]
    2  7 [-,-,-,-,-,-,-,-,-]
       8 [-,-,-,-,-,-,-,-,-]
       = c+j
    """

    for row in range(0, squared, n):
        for col in range(0, squared, n):

            for value in range(1, squared+1):

                for row_case in range(row, row + n):
                    for col_case in range(col, col + n):

                        for col_case_pair in range(col_case+1, col + n):
                            clauses.append([
                                litteral(
                                    var(row_case, col_case, value, squared), false=True),
                                litteral(
                                    var(row_case, col_case_pair, value, squared), false=True)
                            ])

                        for row_case_pair in range(row_case+1, row+n):
                            for col_case_pair in range(col, col+n):

                                clauses.append([
                                    litteral(
                                        var(row_case, col_case, value, squared), false=True),
                                    litteral(
                                        var(row_case_pair, col_case_pair, value, squared), false=True)
                                ])

    # for y_case in range(0, squared, n):
    #     for x_case in range(0, squared, n):

    #         # i,j in [0, n-1]
    #         for i in range(n):
    #             for j in range(n):

    #                 for value in range(1, squared + 1):

    #                     for i_pair in range(i, n):
    #                         for j_pair in range(j, n):

    #                             # Pour ne pas avoir (not x or not x)
    #                             if j_pair == j: continue

    #                             clauses.append([
    #                                 litteral(
    #                                     var(y_case + i, x_case + j, value, squared), false=True),
    #                                 litteral(
    #                                     var(y_case + i_pair, x_case + j_pair, value, squared), false=True)
    #                             ])

    return clauses


def row_constraint(sudoku_array, n):
    for row in range(0, n * n):
        for col in range(0, n * n):
            for col_pair in range(col + 1, n * n):
                if (sudoku_array[row][col] != 0 and sudoku_array[row][col_pair] != 0 and
                        sudoku_array[row][col] == sudoku_array[row][col_pair]):
                    return False
    return True


def col_constraint(sudoku_array, n):
    for col in range(0, n * n):
        for row in range(0, n * n):
            for row_pair in range(row + 1, n * n):
                if (sudoku_array[row][col] != 0 and sudoku_array[row_pair][col] != 0 and
                        sudoku_array[row][col] == sudoku_array[row_pair][col]):
                    return False
    return True


def square_constraint(sudoku_array, n):
    squared = n**2
    for row in range(0, squared, n):
        for col in range(0, squared, n):

            for value in range(1, squared+1):

                for row_case in range(row, row + n):
                    for col_case in range(col, col + n):

                        for col_case_pair in range(col_case+1, col + n):
                            if (sudoku_array[row_case][col_case] != 0 and sudoku_array[row_case][col_case_pair] != 0 and
                                    sudoku_array[row_case][col_case] == sudoku_array[row_case][col_case_pair]):
                                return False

                        for row_case_pair in range(row_case+1, row+n):
                            for col_case_pair in range(col, col+n):

                                if (sudoku_array[row_case][col_case] != 0 and sudoku_array[row_case_pair][col_case_pair] != 0 and
                                        sudoku_array[row_case][col_case] == sudoku_array[row_case_pair][col_case_pair]):
                                    return False

    return True


def possible(n):
    # [(x, y, value), ... ]
    return list(product(list(range(0, n * n)), list(range(0, n * n)), list(range(1, n * n + 1))))


def possible_set(n):
    # [(x, y, value), ... ]
    return set(product(list(range(0, n * n)), list(range(0, n * n)), list(range(1, n * n + 1))))



def generate_glouton_with_verification(n):
    
    sudoku_array = np.zeros((n * n, n * n), dtype="int")
    possibility = possible_set(n)

    nb_to_generate = (4 * n * n)

    while nb_to_generate != 0:
        choice = random.choice(list(possibility))
        sudoku_array[choice[0]][choice[1]] = choice[2]

        if row_constraint(sudoku_array, n) and col_constraint(sudoku_array, n) and square_constraint(sudoku_array, n):
            possibility.intersection(choice)
            nb_to_generate -= 1

        else:
            sudoku_array[choice[0]][choice[1]] = 0

    return sudoku_array


def generate(n, difficulty):
    """
    n: the size of the side of one square of the sudoku
    difficulty: number of filled case in each square(approximately)
    """

    squared = pow(n, 2)

    values = set(range(1, squared + 1))
    row = []
    column = []
    s = []

    # init du random generator
    random.seed()

    # a l'indice i se trouve la case i avec un set
    # avec un set representant les nombres present dans la case i
    square = []

    # contrainte pour les colonnes et lignes
    for i in range(squared):
        row.append(set())
        column.append(set())

    # contraintes pour les carres
    for i in range(squared):
        square.append(set())

    # init du sudoku avec des zeros
    for y in range(squared):
        l = []
        for x in range(squared):
            l.append(0)
        s.append(l)

    for diff in range(difficulty):
        for y in range(n):
            for x in range(n):

                # on genere un number non-present dans le square selectionne
                number = random.choice(
                    list(values - set(square[y * n + x])))

                # les rows ou n'est pas present number
                r_possible = set()
                for r in range(y * n, y * n + n):
                    if number not in row[r]:
                        r_possible.add(r)

                # les columns ou n'est pas present number
                c_possible = set()
                for c in range(x * n, x * n + n):
                    if number not in column[c]:
                        c_possible.add(c)

                possible_case = []

                # on test les cases possibles (celles vide)
                for r in r_possible:
                    for c in c_possible:
                        if s[r][c] == 0:
                            possible_case.append((r, c))

                if not possible_case:
                    continue

                r, c = random.choice(possible_case)

                s[r][c] = number
                column[c].add(number)
                row[r].add(number)
                square[y * n + x].add(number)

    return s
