# TODO
# Сделать генератор текста на основе статистики
# Подсчитаем, какие буквы наиболее часто встречаются
# Точнее подсчитаем, как часто идет буква Х за буквой У в каком-либо тексте
# После этого начнем с произвольной буквы и будем в зависимости от
# частоты появления будем выбирать каждую следующу

import zipfile
# Библиотека для вывода словарей
from pprint import pprint
from random import randint

class Chatterer:
    analise_count = 10

    def __init__(self, file_name):
        self.file_name = file_name
        self.stat = {}

    def unzip(self):
        """Распаковка zip-архива, если файл заархивирован"""
        zfile = zipfile.ZipFile(self.file_name, 'r')
        for filename in zfile.namelist():
            zfile.extract(filename)
        self.file_name = filename

    def collect(self):
        """Сбор статистики по символам через словарь"""
        if self.file_name.endswith(".zip"):
            self.unzip()

        sequence = ' ' * self.analise_count
        with open(self.file_name, mode='r') as file:
            for line in file:
                line = line[:-1]
                # print(line)
                for char in line:
                    if sequence in self.stat:
                        if char in self.stat[sequence]:
                            self.stat[sequence][char] += 1
                        else:
                            self.stat[sequence][char] = 1
                    else:
                        self.stat[sequence] = {char: 1}
                    sequence = sequence[1:] + char

    def prepare(self):
        """Подготовка словаря"""
        self.totals = {}
        self.stat_for_generate = {}
        for sequence, char_stat in self.stat.items():
            self.totals[sequence] = 0
            self.stat_for_generate[sequence] = []
            for char, count in char_stat.items():
                self.totals[sequence] += count
                self.stat_for_generate[sequence].append([count, char])
                self.stat_for_generate[sequence].sort(reverse=True)  # reverse - сортировка по убыванию

    def chat(self, N, out_file_name=None):
        """Генерация текста"""
        if out_file_name is not None:
            file = open(out_file_name, 'w', encoding='utf8')
        else:
            file = None
        # Генерация
        printed = 0
        sequence = ' ' * self.analise_count
        spaces_printed = 0
        while printed < N:
            char_stat = self.stat_for_generate[sequence]
            total = self.totals[sequence]
            dice = randint(1, total)
            pos = 0
            for count, char in char_stat:
                pos += count
                if dice <= pos:
                    break
            if file:
                file.write(char)
            else:
                print(char, end='')
            if char == " ":
                spaces_printed += 1
                if spaces_printed >= 10:
                    if file:
                        file.write("\n")
                    else:
                        print()
                    spaces_printed = 0
            printed += 1
            sequence = sequence[1:] + char
        if file:
            file.close()


chatterer = Chatterer(file_name='Voina_i_mir.txt.zip')
chatterer.collect()
chatterer.prepare()
chatterer.chat(10000, 'output_file.txt')






