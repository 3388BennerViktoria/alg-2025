ALPHABET = "ACGTN"

DEBUG = True


class Node:
    def __init__(self, letter, parent=None, is_word=False):
        self.letter = letter
        self.next = dict().fromkeys(ALPHABET)
        self.parent = parent
        self.is_word = is_word
        self.suff_link = None
        self.good_link = None
        self.paths = dict().fromkeys(ALPHABET)

    def get_suff_link(self):
        if DEBUG:
            print(f"Вызов get_suff_link для узла с буквой: {self.letter}")
        if self.suff_link is not None:
            if DEBUG:
                print(f"Суффиксная ссылка уже установлена: {self.suff_link.letter}")
            return self.suff_link
        if self.letter is None:
            self.suff_link = self
            if DEBUG:
                print(f"Узел корневой, суффиксная ссылка на себя: {self.suff_link.letter}")
            return self.suff_link
        if self.parent.letter is None:
            self.suff_link = self.parent
            if DEBUG:
                print(f"Родитель корневой, суффиксная ссылка на корень: {self.suff_link.letter}")
            return self.suff_link
        self.suff_link = self.parent.get_suff_link().get_path(self.letter)
        if DEBUG:
            print(f"Суффиксная ссылка установлена: {self.suff_link.letter}")
        return self.suff_link

    def get_path(self, letter):
        if DEBUG:
            print(f"Вызов get_path для узла с буквой: {self.letter}, ищем путь для буквы: {letter}")
        if self.paths[letter] is not None:
            if DEBUG:
                print(f"Путь уже установлен: {self.paths[letter].letter}")
            return self.paths[letter]
        if self.next[letter] is not None:
            self.paths[letter] = self.next[letter]
            if DEBUG:
                print(f"Путь найден через next: {self.paths[letter].letter}")
            return self.paths[letter]
        if self.letter is not None:
            self.paths[letter] = self.get_suff_link().get_path(letter)
            if DEBUG:
                print(f"Путь найден через суффиксную ссылку: {self.paths[letter].letter}")
            return self.paths[letter]
        self.paths[letter] = self
        if DEBUG:
            print(f"Путь установлен на себя: {self.paths[letter].letter}")
        return self.paths[letter]

    def get_good_link(self):
        if DEBUG:
            print(f"Вызов get_good_link для узла с буквой: {self.letter}")
        if self.good_link is not None:
            if DEBUG:
                print(f"Хорошая ссылка уже установлена: {self.good_link.letter}")
            return self.good_link
        if self.letter is None or self.get_suff_link().is_word:
            self.good_link = self.get_suff_link()
            if DEBUG:
                print(f"Хорошая ссылка установлена на суффиксную ссылку: {self.good_link.letter}")
            return self.good_link
        self.good_link = self.get_suff_link().get_good_link()
        if DEBUG:
            print(f"Хорошая ссылка установлена через рекурсию: {self.good_link.letter}")
        return self.good_link


text = input()
pattern = input()
joker = input()
antijoker = input()
root = Node(None)
patterns = []
l = []
tmp = ""
for i in range(len(pattern)):
    if pattern[i] == joker:
        if tmp:
            patterns.append(tmp)
            l.append(i - len(tmp) + 1)
            tmp = ""
        continue
    tmp += pattern[i]

if tmp:
    patterns.append(tmp)
    l.append(len(pattern) - len(tmp) + 1)

if DEBUG:
    print(f"Шаблоны: {patterns}")
    print(f"Смещения: {l}")

c = [0] * (len(text) + 1)

words_nods = {}
for pattern_ in patterns:
    node = root
    for letter in pattern_:
        if node.next[letter] is not None:
            node = node.next[letter]
        else:
            node.next[letter] = Node(letter, parent=node)
            node = node.next[letter]
    node.is_word = True
    words_nods[node] = pattern_

if DEBUG:
    print("Построенный бор:")
    for node, pattern_ in words_nods.items():
        print(f"Узел: {node.letter}, Слово: {pattern_}")

node = root
ans = []
for i in range(len(text)):
    if DEBUG:
        print(f"\nОбработка символа {text[i]} на позиции {i}")
    node = node.get_path(text[i])
    if DEBUG:
        print(f"Текущий узел: {node.letter}, is_word: {node.is_word}")
    if node.is_word:
        for j in range(len(patterns)):
            k = i + 2 - len(words_nods[node]) - l[j] + 1
            if words_nods[node] == patterns[j] and k > 0:
                c[k] += 1
                if DEBUG:
                    print(f"Найдено слово: {words_nods[node]}, позиция: {k}")

    a = node.get_good_link()
    while a.letter is not None:
        for j in range(len(patterns)):
            k = i + 2 - len(words_nods[a]) - l[j] + 1
            if words_nods[a] == patterns[j] and k > 0:
                c[k] += 1
                if DEBUG:
                    print(f"Найдено слово через хорошую ссылку: {words_nods[a]}, позиция: {k}")
        a = a.get_good_link()

if DEBUG:
    print("\nРезультаты подсчета:")
    print(c)

bad_symbols = [i for i in range(len(text)) if text[i] == antijoker]
bad_indexes = [i for i in bad_symbols if i + 1 not in l]

if DEBUG:
    print(f"Плохие символы: {bad_symbols}")
    print(f"Плохие индексы: {bad_indexes}")

for i in range(1, len(c)):
    if c[i] == len(patterns) and i + len(pattern) - 1 <= len(text):
        for j in range(i - 1, i - 1 + len(pattern)):
            if j in bad_indexes:
                if DEBUG:
                    print(f"Позиция {i} пропущена из-за плохого символа на индексе {j}")
                break
        else:
            print(i)