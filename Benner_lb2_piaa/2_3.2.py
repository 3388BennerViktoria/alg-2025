import sys
import heapq
import math

def mst_approximation(cost_matrix, start_vertex):
    n = len(cost_matrix)
    graph = [[x if x != -1 else math.inf for x in row] for row in cost_matrix]

    # Построение MST алгоритмом Прима
    def prim_mst():
        mst = [[] for _ in range(n)]
        visited = [False] * n
        min_heap = [(0, start_vertex, -1)]  # (вес, текущая, родитель)
        
        while min_heap:
            weight, u, parent = heapq.heappop(min_heap)
            if visited[u]:
                continue
            visited[u] = True
            if parent != -1:
                mst[parent].append(u)
                mst[u].append(parent)
            for v in range(n):
                if graph[u][v] != math.inf and not visited[v]:
                    heapq.heappush(min_heap, (graph[u][v], v, u))
        return mst

    # Обход MST с выбором минимальных рёбер
    def dfs_traversal(mst):
        stack = [start_vertex]
        visited = [False] * n
        path = []
        
        while stack:
            u = stack.pop()
            if visited[u]:
                continue
            visited[u] = True
            path.append(u)
            # Сортируем соседей по весу рёбер
            neighbors = sorted(mst[u], key=lambda x: graph[u][x])
            for v in reversed(neighbors):
                if not visited[v]:
                    stack.append(v)
        return path

    mst = prim_mst()
    path = dfs_traversal(mst)
    path.append(start_vertex)  # Замыкаем цикл

    # Вычисление стоимости
    total_cost = 0
    for i in range(len(path)-1):
        u = path[i]
        v = path[i+1]
        total_cost += cost_matrix[u][v]

    return total_cost, path

def main():
    input_lines = [line.strip() for line in sys.stdin if line.strip()]
    start_vertex = int(input_lines[0])
    cost_matrix = []
    for line in input_lines[1:]:
        row = list(map(float, line.split()))
        cost_matrix.append(row)
    
    cost, path = mst_approximation(cost_matrix, start_vertex)
    
    # Форматируем вывод согласно требованиям
    print(f"{cost:.2f}")
    # Выводим путь с возвратом в стартовую вершину
    print(" ".join(map(str, path)))

if __name__ == "__main__":
    main()