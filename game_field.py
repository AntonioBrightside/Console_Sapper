from random import randint
from cell import *


class GameField:
    """Для управления игровым полем"""

    ABC = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J',
           10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S',
           19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'}

    cells_around = (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)

    def __new__(cls, *args, **kwargs):
        if args[0] <= 26 and 0 < args[1] < args[0] ** 2:
            return super().__new__(cls)

    def __init__(self, n: int, m: int):
        self.field = [[Cell() for j in range(n)] for i in range(n)]
        self.n = n
        self.m = m
        self.init(n, m)
        self.values = list(self.ABC.values())
        self.keys = list(self.ABC.keys())
        self.cells = []
        self.__welcome()

        for i in self.field:
            for j in i:
                self.cells.append(j)  # создаём список со всеми ячейками

    def init(self, n: int, m: int):
        """инициализация поля с новой расстановкой M мин (случайным образом по игровому полю,
        разумеется каждая мина должна находиться в отдельной клетке)"""

        # Добавляем атрибут мин в случайные экземляры
        for i in range(m):
            self.__set_mines(self.field, n)

        # Обновляем атрибут around_mines
        for i in range(n):
            for j in range(n):
                for x, y in self.cells_around:
                    if not self.field[i][j].mine:
                        if 0 <= i + x < n and 0 <= j + y < n:
                            if self.field[i + x][j + y].mine:
                                self.field[i][j].around_mines += 1

    def show(self):
        """отображение поля в консоли в виде таблицы чисел открытых клеток
        (если клетка не открыта, то отображается символ #)"""
        print('~ ~ ' * self.n)
        print('    ', *self.values[0:self.n], end='\n')
        print('    ', '-' * (self.n * 2 - 1))
        for i, v in enumerate(self.field):
            if i + 1 >= 10:
                print(i + 1, '|', *v, '|', i + 1, end='\n')
            else:
                print(i + 1, ' |', *v, '| ', i + 1, end='\n')
        print('    ', '-' * (self.n * 2 - 1))
        print('    ', *self.values[0:self.n])

    @staticmethod
    def __welcome():
        """Приветственное сообщение с правилами и легендой"""
        print("""
Приветствую. 
Предлагаю поиграть в сапера в консоли. 
Правило: задаёте размер поля (до 26) и количество мин на этом поле.
Управление: 
 - формат написания ячейки:  'A1' ,или '1A' ,или 'a1' ,или '1a' - любое написание
 - '+' - поставить флажок на ячейку. К примеру, '+a1'
 - '-' - убрать флаг с ячейки. К примеру, '-a1'

 Начнём! 
         """)

    def __set_mines(self, lst: list, n: int):
        """Устанавливает атрибут "мина" в случайный экземпляр класса Cell. Попутно проверяет условие mine=True"""

        i, j = randint(0, n - 1), randint(0, n - 1)
        if getattr(lst[i][j], 'mine'):
            self.__set_mines(lst, n)
        else:
            return setattr(lst[i][j], 'mine', True)

    def set_flag(self, lst: list):
        """Ставит / Убирает в / из ячейки флаг"""
        try:
            if '+' in lst[-1]:  # если в последнем адересе есть '+'
                lst[-1] = lst[-1][:2]  # то удаляем '+' из списка
                for j, i in lst[-1:]:  # берем индексы
                    if not self.field[i][j].cell_open:
                        self.field[i][j].flag = True  # и ставим в ячейку индексов флаг
                        self.field[i][j].cell_open = True  # открываем яйку (увидим бомбочку)
            elif '-' in lst[0]:
                lst[0] = lst[0][:2]
                for j, i in lst:
                    if self.field[i][j].flag:
                        self.field[i][j].flag = False
                        self.field[i][j].cell_open = False
        except IndexError:
            pass

        self.show()

    def open_cell(self, lst: list):
        """Открывает ячейку, согласно выбору пользователя"""

        for j, i in lst[-1:]:  # ячейка для открытия
            if not self.field[i][j].cell_open:  # на случай, когда флаг стоит и User хочет снова открыть
                if self.field[i][j].mine:  # если в ней бомба, то конец игры
                    print('Увы, вы наступили на мину и вас теперь не найти...', 'Game Over, так сказать')
                    for a in self.field:
                        for b in a:
                            b.cell_open = True
                    self.show()
                    exit()

                elif not self.field[i][j].around_mines:  # если она пустая, то
                    self.field[i][j].cell_open = True  # переданную ячейку открываем
                    for x, y in self.cells_around:  # и для каждой соседней ячейки
                        if 0 <= i + x < self.n and 0 <= j + y < self.n:  # если соседняя ячейка находится в интервале
                            self.field[i + x][j + y].cell_open = True  # то открываем ячейку
                    self.__cell_around_checker()  # проверяем все ячейки на поле

                else:  # если в ней нет бомбы и она не пустая, то просто открываем её
                    self.field[i][j].cell_open = True

        self.show()

    def __cell_around_checker(self):
        """Перебирает все открытые ячейки и проверяет, что все соседние ячейки, которые пустые, открыты"""
        self.actions = None
        while self.actions != 0:  # Проверка, что все ячейки открыты, включая те, что открыли в рамках цикла ниже
            self.actions = 0
            for i, v in enumerate(self.field):  # для каждой ячейки
                for j, w in enumerate(v):
                    if not w.around_mines and w.cell_open:  # которая пустая и открытая
                        for x, y in self.cells_around:  # то для каждой соседней ячейки
                            if 0 <= i + x < self.n and 0 <= j + y < self.n and not self.field[i + x][j + y].cell_open:
                                self.field[i + x][j + y].cell_open = True  # то открываем ячейку
                                self.actions += 1

    def check_win(self):
        """Проверка на выигрыш"""
        flags = list(filter(lambda x: x.flag, self.cells))  # проставлен флаг
        rflags = list(filter(lambda x: x.flag and x.mine, self.cells))  # проставлен флаг верно
        closed = list(filter(lambda x: not x.cell_open, self.cells))  # ячейки закрыты

        if not len(closed) and len(flags) == self.m:  # если все ячейки открыты (флажок - открытая)
            self.winner()

        elif len(rflags) == self.m and len(flags) == self.m:  # все флажки стоят верно и флажков верное количество
            self.winner()

        elif (len(rflags) + len(closed)) == self.m:
            self.winner()

    def winner(self):
        """Сообщение о победе"""
        print('Что ж, Вы победили, поздравляю. В следующий раз я расставлю мины получше...')
        for i in self.cells:
            i.cell_open = True
        self.show()
        exit()
