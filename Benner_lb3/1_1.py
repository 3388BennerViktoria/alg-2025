def min_edit_cost(replace_cost, insert_cost, delete_cost, A, B, debug=False):
    m = len(A)
    n = len(B)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i * delete_cost
        if debug:
            print(f"dp[{i}][0] = {dp[i][0]} (удалить {i} символов из A)")
    
    for j in range(n + 1):
        dp[0][j] = j * insert_cost
        if debug:
            print(f"dp[0][{j}] = {dp[0][j]} (вставить {j} символов в B)")
    
    if debug:
        print("\nНачальная таблица:")
        for row in dp:
            print(row)
        print()
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if A[i - 1] == B[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
                if debug:
                    print(f"Совпадение: A[{i-1}]='{A[i-1]}' == B[{j-1}]='{B[j-1]}'")
                    print(f"dp[{i}][{j}] = dp[{i-1}][{j-1}] = {dp[i][j]}")
            else:
                replace_op = dp[i - 1][j - 1] + replace_cost
                insert_op = dp[i][j - 1] + insert_cost
                delete_op = dp[i - 1][j] + delete_cost
                dp[i][j] = min(replace_op, insert_op, delete_op)
                if debug:
                    print(f"Несовпадение: A[{i-1}]='{A[i-1]}' != B[{j-1}]='{B[j-1]}'")
                    print(f"  Замена: {replace_op} (dp[{i-1}][{j-1}] + {replace_cost})")
                    print(f"  Вставка: {insert_op} (dp[{i}][{j-1}] + {insert_cost})")
                    print(f"  Удаление: {delete_op} (dp[{i-1}][{j}] + {delete_cost})")
                    print(f"  dp[{i}][{j}] = min({replace_op}, {insert_op}, {delete_op}) = {dp[i][j]}")
        
        if debug and i < m:
            print(f"\nПосле обработки строки {i}:")
            for row in dp:
                print(row)
            print()
    
    if debug:
        print("\nИтоговая таблица:")
        for row in dp:
            print(row)
        print(f"\nМинимальная стоимость преобразования: {dp[m][n]}")
    
    return dp[m][n]

replace_cost, insert_cost, delete_cost = map(int, input().split())
A = input().strip()
B = input().strip()

DEBUG = True
result = min_edit_cost(replace_cost, insert_cost, delete_cost, A, B, DEBUG)
print(result)