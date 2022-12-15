import argparse
import re

from typing import Optional

from positions import list_of_strings_positions
from strings import list_of_strings, stop_words


class TextFormatter:
    def __init__(self, strings: list, positions: list, stop_words: Optional[list] = None):
        self.strings = strings
        self.positions = positions
        self.stop_words = stop_words if stop_words else []

    def get_as_list(self, username: str) -> list:
        """
        Метод возвращает правильно сформированный список слов итогового текста.
        Среди возвращаемых элементов не должно содержаться слов из списка стоп-слов.
        Элементы списка, содержащие шаблон {username}, должны быть заменены на значение переменной username.
        :param username: Имя пользователя
        :return: Список слов в правильном порядке
        """
        mapped = {}
        zipped = zip(self.strings, self.positions)
        for s, pos in zipped:
            if s in self.stop_words:
                continue
            if s == '{username}':
                s = username
            if isinstance(pos, int):
                mapped[pos] = s
            else:
                for subpos in pos:
                    mapped[subpos] = s
        as_list = [s for _, s in sorted(mapped.items(), key=lambda x: x[0])]
        return as_list


    def get_as_text(self, username: str) -> str:
        """
        Метод возвращает текст, сформированный из списка слов и позиций.
        В возвращаемом тексте не должно быть стоп-слов.
        Шаблон {username} должен быть заменён на значение переменной username.
        Каждое новое предложение должно начинаться с большой буквы.
        Между знаком препинания и впереди стоящим словом не должно быть пробелов.
        :param username: Имя пользователя
        :return: Текст, отформатированный согласно условиям задачи
        """
        as_list = self.get_as_list(username)
        as_text = ''
        for i, s in enumerate(as_list):
            if s in (',', '!', '?', '.') or i == 0:
                as_text += s
            else:
                as_text += f' {s}'

        p = re.compile(r'(?<=[\.\?!]\s)(\w+)')

        def cap(match):
            return(match.group().capitalize())

        return p.sub(cap, as_text)


formatter = TextFormatter(list_of_strings, list_of_strings_positions, stop_words)

arguments_parser = argparse.ArgumentParser(prog="python main.py", description="Консольный рассказчик.")
arguments_parser.add_argument('-u',
                              '--username',
                              action='store',
                              help='Имя пользователя в истории')

arguments = arguments_parser.parse_args()

if arguments.username:
    print(formatter.get_as_text(arguments.username))
