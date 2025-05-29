def extended_levenshtein(s, t, replace_cost=1, insert_cost=1, delete_cost=1, double_replace_cost=1, debug=False):
    m = len(s)
    n = len(t)
    
    if debug:
        print(f"Строка S: '{s}' (длина {m})")
        print(f"Строка T: '{t}' (длина {n})")
        print("\nПараметры операций:")
        print(f"  Замена: {replace_cost}")
        print(f"  Вставка: {insert_cost}")
        print(f"  Удаление: {delete_cost}")
        print(f"  Двойная замена: {double_replace_cost}")
        print("\nИнициализация матрицы:")
    
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i * delete_cost
    for j in range(n + 1):
        dp[0][j] = j * insert_cost
    
    if debug:
        print("Начальная матрица:")
        for row in dp:
            print(row)
        print()
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1]
                if debug:
                    print(f"Совпадение: S[{i-1}]='{s[i-1]}' и T[{j-1}]='{t[j-1]}'")
            else:
                replace = dp[i-1][j-1] + replace_cost
                insert = dp[i][j-1] + insert_cost
                delete = dp[i-1][j] + delete_cost
                
                double_replace = float('inf')
                if i > 1 and j > 0:
                    double_replace = dp[i-2][j-1] + double_replace_cost
                
                dp[i][j] = min(replace, insert, delete, double_replace)
                
                if debug:
                    print(f"Несовпадение: S[{i-1}]='{s[i-1]}' и T[{j-1}]='{t[j-1]}'")
                    print(f"  Варианты:")
                    print(f"  - Замена: {replace} (стоимость {replace_cost})")
                    print(f"  - Вставка: {insert} (стоимость {insert_cost})")
                    print(f"  - Удаление: {delete} (стоимость {delete_cost})")
                    if i > 1:
                        print(f"  - Двойная замена: {double_replace} (стоимость {double_replace_cost})")
                    print(f"  Выбрано: {dp[i][j]}")
        
        if debug and i < m:
            print(f"\nПосле строки {i}:")
            for row in dp:
                print(row)
            print()
    
    if debug:
        print("\nФинальная матрица:")
        for row in dp:
            print(row)
        print(f"\nМинимальная стоимость преобразования: {dp[m][n]}")
    
    return dp[m][n]

s = input().strip()
t = input().strip()

REPLACE_COST = 1
INSERT_COST = 1
DELETE_COST = 1
DOUBLE_REPLACE_COST = 1

DEBUG = True
distance = extended_levenshtein(
    s, t, 
    replace_cost=REPLACE_COST,
    insert_cost=INSERT_COST,
    delete_cost=DELETE_COST,
    double_replace_cost=DOUBLE_REPLACE_COST,
    debug=DEBUG
)
print(distance)
