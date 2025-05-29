def get_edit_sequence(replace_cost, insert_cost, delete_cost, A, B, debug=False):
    len_A = len(A)
    len_B = len(B)
    dp = [[0] * (len_B + 1) for _ in range(len_A + 1)]

    for j in range(len_B + 1):
        dp[0][j] = j * insert_cost
        if debug:
            print(f"Инициализация: вставка {j} символов -> стоимость {dp[0][j]}, операции: {ops[0][j]}")

    for i in range(1, len_A + 1):
        dp[i][0] = dp[i - 1][0] + delete_cost
        for j in range(1, len_B + 1):
            if A[i-1] == B[j-1]:
                nothing = dp[i-1][j-1]
            else:
                nothing = float("+inf")
            replace = dp[i-1][j-1] + replace_cost
            insert = dp[i][j-1] + insert_cost
            delete = dp[i-1][j] + delete_cost
            cost = min(nothing, replace, insert, delete)
            if nothing == cost:
                dp[i][j] = dp[i-1][j-1]
            elif insert == cost:
                dp[i][j] = insert
                if debug:
                    print(f"Вставка: B[{j-1}]='{B[j-1]}' стоимость {insert}")
            elif replace == cost:
                dp[i][j] = replace
                if debug:
                    print(f"Замена: A[{i-1}]='{A[i-1]}'->B[{j-1}]='{B[j-1]}' стоимость {replace}")
            else:
                dp[i][j] = delete
                if debug:
                    print(f"Удаление: A[{i-1}]='{A[i-1]}' стоимость {delete}")

            if debug:
                print(f"dp[{i}][{j}] = {dp[i][j]}")

    operations = []
    i, j = len_A, len_B
    while i > 0 or j > 0:
        if i > 0 and j > 0 and A[i - 1] == B[j - 1]:
            operations.append("M")
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + delete_cost:
            operations.append("D")
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + insert_cost:
            operations.append("I")
            j -= 1
        else:
            operations.append("R")
            i -= 1
            j -= 1
    return "".join(reversed(operations))

replace_cost, insert_cost, delete_cost = map(int, input().split())
A = input().strip()
B = input().strip()

DEBUG = False
operations = get_edit_sequence(replace_cost, insert_cost, delete_cost, A, B, DEBUG)

print(operations)
print(A)
print(B)