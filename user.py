class User:
    """Для взаимодействия пользователя с доской"""

    __CBA = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9,
             'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18,
             'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25}

    def __init__(self, cell: str, n: int):
        self.steps = []  # сохраняет все действия пользователя (индексы клеток)
        self.n = n  # размеры поля
        self.__cell = cell  # адрес ячейки от пользователя (необработанная)
        self.__add_cell_checker(self.__cell)  # добавление обработанной ячейки в действия
        self.duplicate = []  # дубликаты для работы со снятием флажка

    def show_cell(self, cell: str):
        """Пользователь указывает адрес ячейки, которую хочет открыть"""
        self.__cell = cell
        self.__add_cell_checker(self.__cell)

    def set_flag(func):
        """Декоратор, который проверяет вводимую ячейку на желание установки флага"""

        def wrapper(*cell):
            if '+' in cell[1]:
                cell = (cell[0], cell[1].replace('+', ''))
                func(*cell)
                cell[0].steps[-1].append('+')
            elif '-' in cell[1]:
                try:
                    cell = (cell[0], cell[1].replace('-', ''))
                    func(*cell)
                    cell[0].steps.remove(cell[0].duplicate[0])
                    cell[0].duplicate[0].append('-')
                except IndexError:
                    pass
            else:
                func(*cell)

        return wrapper

    @set_flag
    def __add_cell_checker(self, cell):
        """Проверяет вводимый адрес от пользователя на корректность, переводит в формат [индекс столбца, индекс строки].
        Добавляет действия в список"""
        self.__cell = cell
        self.duplicate = []  # обновялем дипликаты, чтобы оставалось всего одно значение
        try:
            if len(self.__cell) in [2, 3]:  # если символов в строке 2 или 3
                if self.__cell[0] in self.__CBA.keys():  # если первый символ буква
                    result = [self.__CBA.get(self.__cell[0]), int(''.join(self.__cell[1:])) - 1]  # задаём индекс
                    if result[0] + 1 <= self.n and result[1] <= self.n:  # если оба индекса в интервале
                        if result not in self.steps:  # если индексы не в списке действий
                            self.steps.append(result)  # сохраняем в список действий
                        else:
                            self.duplicate.append(result)
                    else:
                        print('Адрес ячейки находится за рамками поля. Введите новый адрес')
                else:
                    result = [self.__CBA.get(self.__cell[-1]), int(''.join(self.__cell[:-1])) - 1]  # задаём индекс
                    if result[0] + 1 <= self.n and result[1] <= self.n:
                        if result not in self.steps:
                            self.steps.append(result)
                        else:
                            pass
                    else:
                        print('Адрес ячейки находится за рамками поля. Введите новый адрес')

        except TypeError:
            print('Адрес ячейки находится за рамками поля. Введите новый адрес')
