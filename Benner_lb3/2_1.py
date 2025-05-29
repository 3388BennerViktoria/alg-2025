def levenshtein_distance(s, t, debug=False):
    m = len(s)
    n = len(t)
    
    if debug:
        print(f"Строка S: '{s}' (длина {m})")
        print(f"Строка T: '{t}' (длина {n})")
        print("\nИнициализация массивов:")
    
    if m < n:
        if debug:
            print("Меняем строки местами для оптимизации памяти")
        return levenshtein_distance(t, s, debug)
    
    prev = list(range(n + 1))
    curr = [0] * (n + 1)
    
    if debug:
        print(f"prev: {prev}")
        print(f"curr: {curr}\n")
    
    for i in range(1, m + 1):
        curr[0] = i
        if debug:
            print(f"Обработка символа S[{i-1}] = '{s[i-1]}'")
            print(f"Установка curr[0] = {i} (удаление первых {i} символов)")
        
        for j in range(1, n + 1):
            if s[i-1] == t[j-1]:
                curr[j] = prev[j-1]
                if debug:
                    print(f"  Совпадение с T[{j-1}] = '{t[j-1]}'")
                    print(f"  curr[{j}] = prev[{j-1}] = {curr[j]}")
            else:
                replace_cost = prev[j-1] + 1
                insert_cost = curr[j-1] + 1
                delete_cost = prev[j] + 1
                curr[j] = min(replace_cost, insert_cost, delete_cost)
                if debug:
                    print(f"  Несовпадение с T[{j-1}] = '{t[j-1]}'")
                    print(f"  Варианты: замена={replace_cost}, вставка={insert_cost}, удаление={delete_cost}")
                    print(f"  Выбрано минимальное: curr[{j}] = {curr[j]}")
        
        if debug:
            print(f"\nПосле обработки символа '{s[i-1]}':")
            print(f"prev: {prev}")
            print(f"curr: {curr}\n")
        
        prev, curr = curr, prev
    
    if debug:
        print("\nФинальный массив prev:")
        print(prev)
        print(f"\nРасстояние Левенштейна: {prev[n]}")
    
    return prev[n]

s = input().strip()
t = input().strip()

DEBUG = True
distance = levenshtein_distance(s, t, DEBUG)
print(distance)