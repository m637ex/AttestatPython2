# Задание №4
# Напишите для задачи 1 тесты pytest. Проверьте следующие варианты:
# возврат строки без изменений
# возврат строки с преобразованием регистра без потери символов
# возврат строки с удалением знаков пунктуации
# возврат строки с удалением букв других алфавитов
# возврат строки с учётом всех вышеперечисленных пунктов (кроме п. 1)

# pip install pytest
# pytest .\sem14_task4_pytest.py -v    из консоли
import pytest
from string import ascii_letters
import argparse
import logging

FORMAT = '{levelname:<8} - {asctime}. В модуле "{name}" ' \
'в строке {lineno:03d} функция "{funcName}()" ' \
'в {created} секунд записала сообщение: {msg}'
logging.basicConfig(
    filename='sem15_hw1.log', # имя файла логирования
    filemode='a',               # режим записи - 'w' или 'a'
    encoding='utf-8',           # кодировка
    format=FORMAT,              # формат строки для логирования
    style='{',                  # стиль для строки форматирования
    level=logging.INFO          # уровень логирования
    # errors                    # как обрабатывать ошибки, если возникают проблемы с кодировкой
)
# Уровни логирования:
# NOTSET, 0 # - без уровня, регистрируются все события
# DEBUG, 10 # - подробная информация, для дебагинга
# INFO, 20 # - подтверждение, что всё хорошо работает
# WARNING, 30 # - что-то не так, или будет не так ...
# ERROR, 40 # - программа не может что-то выполнить
# CRITICAL, 50 # - программа не может дальше работать
logger = logging.getLogger(__name__)

def clear_text(text: str) -> str:
    res = ''.join(char for char in text if char in ascii_letters + ' ').lower()
    logger.info(res)
    return res
    
def test_original(): # должно начинаться с "test_"
    assert clear_text('hello world') == 'Hello world', "Don't work!!!" # a == b, сообщение при False
def test_lower():
    assert clear_text('Hello World') == 'hello world', "Don't work!!!"
def test_punctuation():
    assert clear_text('Hello World!!!') == 'hello world', "Don't work!!!"
def test_lang():
    assert clear_text('HelloПривет WorldМир') == 'hello world', "Don't work!!!"
def test_all():
    assert clear_text('Hello(Привет), World(Мир)!!!') == 'hello world', "Don't work test_all!!!"

def parse(): # парсер командной строки
    parser = argparse.ArgumentParser(
        description='Чистим текст от всех символов и оставялем только английский язык в нижнем ригистре', 
        epilog='При отсутствии значений берем текущий день недели и месяц',
        prog='clear_text()')  # prog - функция которая будет применена к данным из командной строки
    parser.add_argument('-t', '--text', type=str, nargs='*', help='Введите текст: ')
    args = parser.parse_args()
    return clear_text(f'{args.text}')

if __name__ == '__main__':
    pytest.main(['-vv']) # ['-vv'] - увидеть результат
    # print(clear_text('Hello(Привет), World(Мир)!!!')) # -> hello world
    print(parse())