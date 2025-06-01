import sys
import math
from copy import deepcopy

def little_algorithm(N, cost_matrix):
    if N == 1:
        return [0], 0.0
    
    # Проверка связности графа
    def is_connected():
        visited = [False] * N
        stack = [0]
        visited[0] = True
        count = 1
        
        while stack:
            u = stack.pop()
            for v in range(N):
                if not visited[v] and cost_matrix[u][v] != -1:
                    visited[v] = True
                    stack.append(v)
                    count += 1
        return count == N
    
    if not is_connected():
        return [], math.inf

    best_path = []
    min_cost = math.inf

    # Нормализация матрицы
    norm_matrix = [[x if x != -1 else math.inf for x in row] for row in cost_matrix]

    def reduce_matrix(matrix):
        reduction = 0
        
        # Редукция строк
        row_mins = [min(row) for row in matrix]
        for i in range(N):
            if row_mins[i] != math.inf:
                reduction += row_mins[i]
                for j in range(N):
                    if matrix[i][j] != math.inf:
                        matrix[i][j] -= row_mins[i]
        
        # Редукция столбцов
        col_mins = [min(matrix[i][j] for i in range(N)) for j in range(N)]
        for j in range(N):
            if col_mins[j] != math.inf:
                reduction += col_mins[j]
                for i in range(N):
                    if matrix[i][j] != math.inf:
                        matrix[i][j] -= col_mins[j]
        
        return reduction

    def branch_and_bound(path, cost, matrix, visited):
        nonlocal best_path, min_cost
        
        if len(path) == N:
            return_cost = matrix[path[-1]][0]
            if return_cost != math.inf:
                total = cost + return_cost
                if total < min_cost:
                    min_cost = total
                    best_path = path.copy()
            return
        
        current = path[-1]
        neighbors = sorted(
            [v for v in range(N) if not visited[v] and matrix[current][v] != math.inf],
            key=lambda v: matrix[current][v]
        )
        
        for next_city in neighbors:
            new_matrix = deepcopy(matrix)
            # Запрещаем переходы
            new_matrix[current] = [math.inf] * N
            for i in range(N):
                new_matrix[i][next_city] = math.inf
            new_matrix[next_city][current] = math.inf
            
            reduction = reduce_matrix(new_matrix)
            new_cost = cost + matrix[current][next_city] + reduction
            
            if new_cost < min_cost:
                visited[next_city] = True
                branch_and_bound(path + [next_city], new_cost - reduction, new_matrix, visited)
                visited[next_city] = False

    initial_cost = reduce_matrix(deepcopy(norm_matrix))
    visited = [False] * N
    visited[0] = True
    branch_and_bound([0], initial_cost, norm_matrix, visited)
    
    if not best_path:
        return [], math.inf
    
    # Вычисляем фактическую стоимость
    total = 0
    for i in range(N-1):
        total += cost_matrix[best_path[i]][best_path[i+1]]
    total += cost_matrix[best_path[-1]][0]
    
    return best_path, total

def main():
    input_lines = [line.strip() for line in sys.stdin if line.strip()]
    if not input_lines:
        print("0")
        print("0.0")
        return
    
    N = int(input_lines[0])
    if N == 0:
        print("0")
        print("0.0")
        return
    
    cost_matrix = []
    for line in input_lines[1:N+1]:
        row = list(map(float, line.split()))
        cost_matrix.append(row)
    
    path, cost = little_algorithm(N, cost_matrix)
    
    if not path:
        print("No solution")
    else:
        print(' '.join(map(str, path)))
        print(f"{cost:.1f}")

if __name__ == "__main__":
    main()