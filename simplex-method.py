import numpy as np
import math

def to_tableau(c, A, b):
    xb = [eq + [x] for eq, x in zip(A, b)]
    z = c + [0]

    return xb + [z]


def can_be_improved(tableau):
    z = tableau[-1]
    return any(x > 0 for x in z[:-1])


def get_pivot_position(tableau):
    z = tableau[-1]
    column = next(i for i, x in enumerate(z[:-1]) if x > 0)
    
    restrictions = []
    for eq in tableau[:-1]:
        el = eq[column]
        restrictions.append(math.inf if el <= 0 else eq[-1] / el)

    row = restrictions.index(min(restrictions))
    return row, column


def pivot_step(tableau, pivot_position):
    new_tableau = [[] for eq in tableau]
    
    i, j = pivot_position
    pivot_value = tableau[i][j]
    new_tableau[i] = np.array(tableau[i]) / pivot_value
    
    for eq_i, eq in enumerate(tableau):
        if eq_i != i:
            multiplier = np.array(new_tableau[i]) * tableau[eq_i][j]
            new_tableau[eq_i] = np.array(tableau[eq_i]) - multiplier
   
    return new_tableau


def is_basic(column):
    return sum(column) == 1 and len([c for c in column if c == 0]) == len(column) - 1


def get_solution(tableau):
    columns = np.array(tableau).T
    solutions = []
    for column in columns:
        solution = 0
        if is_basic(column):
            one_index = column.tolist().index(1)
            solution = columns[-1][one_index]
        solutions.append(solution)
        
    return solutions


def simplex(c, A, b):
    tableau = to_tableau(c, A, b)

    while can_be_improved(tableau):
        pivot_position = get_pivot_position(tableau)
        tableau = pivot_step(tableau, pivot_position)

    print("aboba")

    return get_solution(tableau)



"""test data"""
"""
7x1 + 2x2 + 5x3 + x4 ≤ 1,
2x1 + 2x2 + 3x3 + 4x4 ≤ 1,
5x1 + 3x2 + 4x3 + 4x4 ≤ 1,
3x1 + 2x2 + x3 + 6x4 ≤ 1,
x1 ≥ 0, . . . , x2 ≥ 0
 

7x1 + 2x2 + 5x3 + x4  + x5 = 1,
2x1 + 2x2 + 3x3 + 4x4 + x6 = 1,
5x1 + 3x2 + 4x3 + 4x4 + x7 = 1,
3x1 + 2x2 +  x3 + 6x4 + x8 = 1,


 max L=x1+x2

"""

c = [1, 1, 0, 0, 0, 0, 0, 0]
A = [
    [7, 2, 5, 1, 1, 0, 0, 0],
    [2, 2, 3, 4, 0, 1, 0, 0],
    [5, 3, 4, 4, 0, 0, 1, 0],
    [3, 2, 1, 6, 0, 0, 0, 1]
]
b = [1,1,1,1]

z=to_tableau(c, A, b)
print(z)
print('\n')

print('solution: ', simplex(c, A, b))
