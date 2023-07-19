class Cell:
    """Для представления клетки игрового поля"""

    def __init__(self, mine=False, around_mines=0):
        self.mine = mine  # есть ли мина в клетке (булево)
        self.around_mines = around_mines  # число мин вокруг клетки
        self.cell_open = False  # открыта клетка или закрыта (булево)
        self.flag = False  # поставлен флаг или нет  # ДОБАВИЛ!!!

    def __repr__(self):
        if self.cell_open:
            if self.flag:
                return 'F'
            elif self.around_mines == 0 and not self.mine:
                return ' '
            elif self.mine:
                return '*'  # u"\U0001F4A3"
            else:
                return str(self.around_mines)
        else:
            return '#'
