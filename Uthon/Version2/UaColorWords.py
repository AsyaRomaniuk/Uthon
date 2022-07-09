from TranslateUaToPy import is_keyword, uakeywords

keywords: tuple = ('спробувати виконати', 'нелокальний', 'імпортувати', 'якщо інакше', 'для змінної', 'продовжити',
                   'глобальний', 'асинхронна', 'сформувати', 'пропустити', 'остаточно', 'виключити', 'повернути',
                   'перервати', 'повертати', 'з модуля', 'видалити', 'заявити', 'функція', 'лямбда',
                   'чекати', 'інакше', 'клас', 'поки', 'якщо', 'або', 'не', 'як', 'є?',
                   'з', 'і', 'в')
builtins: tuple = ('відсортований зворотньо', 'цілочисельно поділити', 'встановити атрибут', 'вивести в консоль',
                   'комплексне число', 'видалити атрибут', 'отримати атрибут', 'глобальні змінні', 'ввести з консолі',
                   "перегляд пам_яті", 'шістнадцятковий', 'локальні змінні', 'статичний метод', 'масив з байтів',
                   'є екземпляром?', 'очистити вивід', 'викликається?', 'стала множина', 'ідентифікатор',
                   'число символу', 'відсортований', 'всі істинні?', 'точка зупину', 'перерахувати', 'має атрибут?',
                   'є підкласом?', 'перетворювач', 'імпортування', 'є істинний?', 'метод класу', 'компілювати',
                   'фільтрувати', 'форматувати', 'максимальне', 'властивість', 'ціле число', 'мінімальне',
                   'вісімковий', 'до степеня', 'двійковий', 'обчислити', 'ітерувати', 'наступний', 'рядкувати',
                   'округлити', 'логічний', 'виконати', 'допомога', 'відкрити', 'діапазон', 'стиснути', 'атрибути',
                   'словник', 'каталог', 'довжина', 'множина', 'вивести', 'модуль', 'аскдіо', 'символ', 'список',
                   "об_єкт", 'кортеж', 'змінні', 'ввести', 'байти', 'число', 'текст', 'супер', 'вийти', 'зріз',
                   'сума', 'хеш', 'тип')

constants: tuple = ('Еліпсис', 'Істина', 'Хиба', 'Ніщо')
magic_methods: tuple = ('', '')

uakeywords = sorted(uakeywords, key=len, reverse=True)


def IndexKeywords(str_line: str) -> list:
    str_line = str_line + " "
    inds: list = []
    for word in keywords:
        if word in str_line:
            for i in range(str_line.count(word)):
                if is_keyword(str_line, word):
                    ind: int = str_line.find(word)
                    str_line = str_line.replace(word, " " * len(word), 1)
                    inds.extend((ind, ind + len(word)))
    return inds


def IndexBuiltins(str_line: str) -> list:
    str_line = str_line + " "
    inds: list = []
    for word in builtins:
        if word in str_line:
            for i in range(str_line.count(word)):
                if is_keyword(str_line, word):
                    ind: int = str_line.find(word)
                    str_line = str_line.replace(word, " " * len(word), 1)
                    inds.extend((ind, ind + len(word)))
    return inds


def IndexConstants(str_line: str) -> list:
    str_line = str_line + " "
    inds: list = []
    for word in constants:
        if word in str_line:
            for i in range(str_line.count(word)):
                if is_keyword(str_line, word):
                    ind: int = str_line.find(word)
                    str_line = str_line.replace(word, " " * len(word), 1)
                    inds.extend((ind, ind + len(word)))
    return inds


if __name__ == "__main__":
    print(tuple(sorted(builtins, key=len, reverse=True)))
    print(tuple(sorted(constants, key=len, reverse=True)))
    print(IndexKeywords("з модуля tkinter імпортувати ttk як t"))
