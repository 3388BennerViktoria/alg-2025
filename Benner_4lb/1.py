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
                print(f"Символ '{pattern[i]}' не совпадает с '{pattern[j]}', устанавливаем j = prefix[{j-1}] = {prefix[j-1]}")
            j = prefix[j-1]
        
        if pattern[i] == pattern[j]:
            j += 1
            if DEBUG:
                print(f"Найдено совпадение, увеличиваем j до {j}")
        else:
            if DEBUG:
                print(f"Совпадений нет, оставляем j = {j}")
        
        prefix[i] = j
        if DEBUG:
            print(f"Обновленный массив префиксов: {prefix}")
    
    if DEBUG:
        print(f"\nИтоговый массив префиксов: {prefix}")
    return prefix

def kmp_search(pattern, text, DEBUG=False):
    n = len(pattern)
    m = len(text)
    if DEBUG:
        print(f"\nНачинаем поиск KMP")
        print(f"Длина образца: {n}, Длина текста: {m}")
        print(f"Образец: {pattern}")
        print(f"Текст: {text}")
    
    if n == 0:
        if DEBUG:
            print("Пустой образец совпадает везде")
        return [0]
    
    prefix = compute_prefix_function(pattern, DEBUG)
    j = 0
    occurrences = []
    
    if DEBUG:
        print("\nНачинаем сканирование текста:")
    
    for i in range(m):
        if DEBUG:
            print(f"\nТекущая позиция в тексте: {i}, символ '{text[i]}'")
            print(f"Текущее состояние: j = {j}")
        
        while j > 0 and text[i] != pattern[j]:
            if DEBUG:
                print(f"Несовпадение: '{text[i]}' != '{pattern[j]}'")
                print(f"Сдвигаем j = prefix[{j-1}] = {prefix[j-1]}")
            j = prefix[j-1]
        
        if text[i] == pattern[j]:
            j += 1
            if DEBUG:
                print(f"Совпадение символов, увеличиваем j до {j}")
        else:
            if DEBUG:
                print(f"Символы не совпали, j остается {j}")
        
        if j == n:
            pos = i - n + 1
            occurrences.append(pos)
            if DEBUG:
                print(f"!!! Найдено полное совпадение на позиции {pos} !!!")
            j = prefix[j-1]
            if DEBUG:
                print(f"Сдвигаем j = prefix[{n-1}] = {j} для поиска следующих вхождений")
    
    if DEBUG:
        if occurrences:
            print(f"\nНайдены вхождения на позициях: {occurrences}")
        else:
            print("\nВхождения не найдены")
    
    return occurrences if occurrences else [-1]

DEBUG_MODE = True
P = input()
T = input()

result = kmp_search(P, T, DEBUG_MODE)
print(','.join(map(str, result)))