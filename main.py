from game_field import *
from user import *


def start():
    field = None
    while field is None:
        try:
            n = int(input('Укажите размеры поля. Число должно быть в интервале (2, 26). Введите одно целое число: '))
            m = int(input('Укажите количество мин на поле. Введите одно целое число: '))
            field = GameField(n, m)
            field.show()
        except ValueError:
            print('Необходимо ввести целое число')
        except RecursionError:
            print('Число должно быть больше 1')
        except AttributeError:
            print('Размеры поля либо за указанным интервалом (2, 26), либо количество мин '
                  'превышает количество генерируемых ячеек. Задайте новые числа с учетом этих комментариев')

    return field, n


if __name__ == '__main__':
    field, n = start()

    while True:
        adress = input('\nУкажите адрес ячейки: ')
        user = User(adress.upper(), n)

        if '+' in adress:
            user.show_cell(adress.upper())
            field.set_flag(user.steps)
        elif '-' in adress:
            user.show_cell(adress.upper())
            field.set_flag(user.duplicate)
        else:
            user.show_cell(adress.upper())
            field.open_cell(user.steps)

        field.check_win()