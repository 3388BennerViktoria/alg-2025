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
n = int(input())
patterns = []
for i in range(n):
    patterns.append(input())
root = Node(None)

words_nods = {}
for pattern in patterns:
    node = root
    for letter in pattern:
        if node.next[letter] is not None:
            node = node.next[letter]
        else:
            node.next[letter] = Node(letter, parent=node)
            node = node.next[letter]
    node.is_word = True
    words_nods[node] = pattern

if DEBUG:
    print("Построенный бор:")
    for node, pattern in words_nods.items():
        print(f"Узел: {node.letter}, Слово: {pattern}")

node = root
ans = []
for i in range(len(text)):
    if DEBUG:
        print(f"\nОбработка символа {text[i]} на позиции {i}")
    node = node.get_path(text[i])
    if DEBUG:
        print(f"Текущий узел: {node.letter}, is_word: {node.is_word}")
    if node.is_word:
        ans.append((i + 2 - len(words_nods[node]), patterns.index(words_nods[node]) + 1))
        if DEBUG:
            print(f"Найдено слово: {words_nods[node]}, позиция: {i + 2 - len(words_nods[node])}")
    a = node.get_good_link()
    while a.letter is not None:
        ans.append((i + 2 - len(words_nods[a]), patterns.index(words_nods[a]) + 1))
        if DEBUG:
            print(f"Найдено слово через хорошую ссылку: {words_nods[a]}, позиция: {i + 2 - len(words_nods[a])}")
        a = a.get_good_link()

if DEBUG:
    print("\nРезультаты поиска:")
for x in sorted(ans):
    print(*x)