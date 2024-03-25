# Задание №5
# На семинарах по ООП был создан класс прямоугольник хранящий длину и ширину, а также вычисляющую периметр,
# площадь и позволяющий складывать и вычитать прямоугольники беря за основу периметр.
# Напишите 3-7 тестов unittest для данного класса.

# Я не придумал какие данные тут можно парсить из командной строки поэтому только логирование в файл.

import unittest
import logging

FORMAT = '{levelname:<8} - {asctime}. В модуле "{name}" ' \
'в строке {lineno:03d} функция "{funcName}()" ' \
'в {created} секунд записала сообщение: {msg}'
logging.basicConfig(
    filename='sem15_hw2.log', # имя файла логирования
    filemode='a',               # режим записи - 'w' или 'a'
    encoding='utf-8',           # кодировка
    # format=FORMAT,              # формат строки для логирования
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

class TestCaseName(unittest.TestCase):   
    def setUp(self) -> None:
        logger.info(f'Запускаем тестирование')
        self.rect1 = Rectangle(5, 10)
        self.rect2 = Rectangle(3, 7)
        self.rect3 = Rectangle(2, 5)
        self.rect4 = Rectangle(10)   
    def test_craete(self): # Тест создания
        self.assertEqual(Rectangle(5, 10), self.rect1)
    def test_perimeter(self): # должно обязательно начинаться с "test_"
        self.assertEqual(self.rect1.perimeter(), 30)
        self.assertEqual(self.rect2.perimeter(), 20)
    def test_area(self):
        self.assertEqual(self.rect1.area(), 50)
        self.assertEqual(self.rect2.area(), 21)
    def test_less(self):
        self.assertLess(self.rect1, self.rect2)
    def test_equal(self):
        self.assertEqual(self.rect1, self.rect2)
    def test_less_equal(self):
        self.assertLessEqual(self.rect1, self.rect2)
    def test_greater(self):
        self.assertGreater(self.rect1, self.rect2)
    def test_greater_equal(self):
        self.assertGreaterEqual(self.rect1, self.rect2)
    def test_sum(self):
        rect3 = self.rect1 + self.rect2
        self.assertEqual(rect3.perimeter(), 50)
    def test_sub(self): # Вычитание
        rect3 = self.rect1 - self.rect2
        self.assertEqual(rect3.perimeter(), 10)
    def tearDown(self) -> None:
        logger.info(f'Завершаем тестирование')

class Rectangle:
    __slots__ = ('_width', '_height') # Задание №5
    
    def __init__(self, width: int|float, height: int|float|None=None):
        self._width = width
        if height:               # Если есть ширина
            self._height = height
        else:
            self._height = width    
        
    
    @property
    def width(self):    # Защищенные значения
        return self._width 
    
    
    @width.setter       # Контроль вводимых параметров
    def width(self, value):
        if value < 0:
            logger.warning(f'Длина прямоугольника должна быть положительной, а не {value}')
            raise ValueError('Длина прямоугольника должна быть положительной')
        self._width = value
        
    
    @property
    def height(self):   # Защищенные значения
        return self._height    
    
    
    @height.setter      # Контроль вводимых параметров
    def height(self, value):
        if value < 0:
            logger.warning(f'Ширина прямоугольника должна быть положительной, а не {value}')
            raise ValueError('Ширина прямоугольника должна быть положительной')
        self._height = value
    
    
    def perimeter(self):
        logger.info(f'Периметр прямоугольника со сторонами {self.width}x{self.height} = {(self.width + self.height) * 2}')
        return (self.width + self.height) * 2
    
    
    def area(self):
        logger.info(f'Площадь прямоугольника со сторонами {self.width}x{self.height} = {self.width * self.height}')
        return self.width * self.height
    
    
    def __add__(self, other):
        width = self.width + other.width
        height = self.height + other.height
        logger.info(f'Сумма прямоугольников = {Rectangle(width, height)}')
        return Rectangle(width, height)
    
    
    def __sub__(self, other):
        width = abs(self.width - other.width)
        height = abs(self.height - other.height)
        logger.info(f'Разница прямоугольников = {Rectangle(width, height)}')
        return Rectangle(width, height)


    def __eq__(self, other):
        logger.info(f'Сравнение "==" прямоугольников возвращает {self.area() == other.area()}')
        return self.area() == other.area()
    
    
    def __lt__(self, other):
        logger.info(f'Сравнение "< прямоугольников возвращает {self.area() == other.area()}')
        return self.area() < other.area()
    
    
    def __le__(self, other):
        logger.info(f'Сравнение "<=" прямоугольников возвращает {self.area() == other.area()}')
        return self.area() <= other.area()
   
    
    def __str__(self):
        return f'Прямоугольник со сторонами {self.width} и {self.height}'
    
    
    def __repr__(self) -> str:
        return f'Rectangle({self.width}, {self.height})'

if __name__ == '__main__':
    unittest.main(verbosity=2)
 


    