def compute_prefix_function(pattern, DEBUG=False):
    length = len(pattern)
    prefix = [0] * length
    if DEBUG:
        print(f"\nВычисляем префикс-функцию для образца: {pattern}")
        print(f"Начальный массив префиксов: {prefix}")
    
    for i in range(1, length):
        j = prefix[i-1]
        if DEBUG:
            print(f"\nОбрабатываем индекс {i}, символ '{pattern[i]}'")
            print(f"Начальное j = prefix[{i-1}] = {j}")
        
        while j > 0 and pattern[i] != pattern[j]:
            if DEBUG:
                print(f"Несовпадение: '{pattern[i]}' != '{pattern[j]}', сдвигаем j = prefix[{j-1}] = {prefix[j-1]}")
            j = prefix[j-1]
        
        if pattern[i] == pattern[j]:
            j += 1
            if DEBUG:
                print(f"Совпадение, увеличиваем j до {j}")
        else:
            if DEBUG:
                print(f"Нет совпадения, j остается {j}")
        
        prefix[i] = j
        if DEBUG:
            print(f"Обновленный массив префиксов: {prefix}")
    
    if DEBUG:
        print(f"\nИтоговый массив префиксов: {prefix}")
    return prefix


def find_cyclic_shift(A, B, DEBUG=False):
    if len(A) != len(B):
        if DEBUG:
            print("Длины строк разные, возвращаем -1")
        return -1
    
    n = len(A)
    if n == 0:
        if DEBUG:
            print("Обе строки пустые, возвращаем 0")
        return 0
    
    if DEBUG:
        print(f"\nИщем циклический сдвиг строки B='{B}' в A='{A}'")
        print(f"Создаем удвоенную строку B+B: '{B+B}'")
    
    doubled_B = B + B
    prefix = compute_prefix_function(A, DEBUG)
    
    j = 0
    if DEBUG:
        print("\nНачинаем поиск совпадений:")
    
    for i in range(len(doubled_B)):
        if DEBUG:
            print(f"\nПозиция {i}: символ текста '{doubled_B[i]}', текущее j={j}")
        
        while j > 0 and doubled_B[i] != A[j]:
            if DEBUG:
                print(f"Несовпадение: '{doubled_B[i]}' != '{A[j]}', сдвигаем j = prefix[{j-1}] = {prefix[j-1]}")
            j = prefix[j-1]
        
        if doubled_B[i] == A[j]:
            j += 1
            if DEBUG:
                print(f"Совпадение, увеличиваем j до {j}")
        else:
            if DEBUG:
                print(f"Нет совпадения, j остается {j}")
        
        if j == n:
            pos = (i - n + 1) % n
            if DEBUG:
                print(f"!!! Найдено полное совпадение на позиции {pos} !!!")
            return pos
    
    if DEBUG:
        print("\nСовпадений не найдено")
    return -1


A = input()
B = input()
result = find_cyclic_shift(B, A, DEBUG=True)
print(result)