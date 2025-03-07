class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x} {self.y}"


class Square:
    def __init__(self, x, y, side):
        self.p = Point(x, y)
        self.side = side

    def __str__(self):
        return f"{self.p} {self.side}"

    def str_with_delta(self, delta):
        return str(Square(self.p.x + delta, self.p.y + delta, self.side))


class SquareCombination:
    def __init__(self, N):
        self.area = 0
        self.matrix = [0]*N
        self.squares = []
        self.next = Point(0, 0)

    def append(self, square, mask):
        self.area += square.side**2
        self.squares.append(square)
        self.next = Point(square.p.x + 1, square.p.y)
        for y in range(square.p.y, square.p.y + square.side):
            self.matrix[y] |= mask

    def add_square(self, square, mask):
        matrix = self.matrix.copy()
        for y in range(square.p.y, square.p.y + square.side):
            matrix[y] |= mask
        comb = SquareCombination(1)
        comb.squares = self.squares.copy()
        comb.squares.append(square)
        comb.area = self.area + square.side**2
        comb.next = Point(square.p.x + 1, square.p.y)
        comb.matrix = matrix
        return comb

    def __len__(self):
        return len(self.squares)


class Solution:
    def __init__(self, N=2, debug=False):
        self.assessment_funcs = [
            lambda N: N + 4,
            lambda N: N // 2 + 7,
            lambda N: N // 3 + 9,
            lambda N: N // 4 + 10,
            lambda N: N // 5 + 11
        ]
        self.debug = debug
        self.N = N
        self.area = N**2
        self.assesment, self.top_side, self.low_side = self._get_assesment()
        self.n = self.top_side
        self.mask_max = (1 << self.top_side) - 1
        self.iter_count = 0
        self.comb_count = 0

    def _get_assesment(self):
        if self.N % 2 == 0:
            return 4, self.N // 2, self.N // 2

        for d in range(3, int(self.N**0.5) + 1, 2):
            if self.N % d == 0:
                d_max = self.N // d
                top_side = d_max*(d // 2 + 1)
                low_side = self.N - top_side
                solution_len = 2*top_side // low_side + 2 + (top_side % low_side != 0)*(2*low_side // (top_side - low_side))
                return solution_len, top_side, low_side

        top_side = self.N // 2 + 1
        low_side = self.N - top_side

        assessment = min(f(self.N) for f in self.assessment_funcs) - (2 if self.N < 35 else 3)
        return max(assessment, 6), top_side, low_side

    def _get_square_row(self, x, side):
        return (self.mask_max >> (self.n - side)) << (self.n - x - side)

    def _check_place(self, row, x, side):
        square_row = self._get_square_row(x, side)
        return (row | square_row) == (row ^ square_row)

    def _get_child_combinations(self, comb):
        stack = []
        for y in range(comb.next.y, self.n):
            for x in range(comb.next.x if comb.next.y == y else 0, self.n):
                if self.debug:
                    print(f"Проверка точки {x} {y}\n")
                for max_side in range(self.n - max(x, y), 0, -1):
                    if self.debug:
                        self.iter_count += 1
                    if self._check_place(comb.matrix[y], x, max_side):
                        if self.debug:
                            print(f"Точка {x} {y} подошла. Длина стороны от 1 до {max_side}. Добавление в стек всех возможных комбинаций\n")
                        for side in range(1, max_side + 1):
                            stack.append(comb.add_square(Square(x, y, side), self._get_square_row(x, side)))
                            if self.debug:
                                self.iter_count += 1
                        return stack
                print(f"Точка {x} {y} не подошла.\n")
        return stack

    def print_solution(self, comb):
        print(len(comb))
        for square in comb.squares[:3]:
            print(square.str_with_delta(1))
        for square in comb.squares[3:]:
            print(square.str_with_delta(self.low_side + 1))

    def solve(self, N):
        if self.debug:
            print("Вычисление оптимальных начальных параметров\n")
        self.__init__(N, self.debug)
        start_square_side = self.top_side - self.low_side
        start_square_row = self._get_square_row(0, start_square_side)
        start_squares = [Square(0, 0, self.top_side), Square(0, self.top_side, self.low_side), Square(self.top_side, 0, self.low_side)]
        start_combination = SquareCombination(self.N)
        for square in start_squares:
            start_combination.append(square, 0)
        for y in range(0, start_square_side):
            start_combination.matrix[y] |= start_square_row
        start_combination.next.x = start_square_side
        start_combination.next.y = 0
        if self.debug:
            print(f"Начальные параметры: длина {self.assesment} оптимальная сторона {self.top_side}\n")
        while True:
            stack = [start_combination]
            while stack:
                combination = stack.pop()
                if self.debug:
                    self.comb_count += 1
                    print(f"Проверка комбинации номер {self.comb_count} длина {len(combination)}\n")
                if combination.area == self.area:
                    if self.debug:
                        print(f"Найдено решение: длина {len(combination)} количество проверенных комбинаций {self.comb_count} количество итераций {self.iter_count}\n")
                        self.iter_count = 0
                        self.comb_count = 0
                    self.print_solution(combination)
                    return

                if len(combination) == self.assesment:
                    if self.debug:
                        print(f"Комбинация номер {self.comb_count} превысила максимальную длину. Прекращение поиска в ее потомках\n")
                    continue

                stack.extend(self._get_child_combinations(combination))
            if self.debug:
                print(f"Решение длины {self.assesment} не найдено. Увеличение длины на 1\n")
            self.assesment += 1


if __name__ == "__main__":
    Solution(debug=True).solve(int(input()))
