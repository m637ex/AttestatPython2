# Задание №6
# На семинаре 13 был создан проект по работе с пользователями (имя, id, уровень).
# Напишите 3-7 тестов pytest для данного проекта. Используйте фикстуры.


from pathlib import Path
import json
import argparse
from random import randint
import logging

FORMAT = '{levelname:<8} - {asctime}. В модуле "{name}" ' \
'в строке {lineno:03d} функция "{funcName}()" ' \
'в {created} секунд записала сообщение: {msg}'
logging.basicConfig(
    filename='sem15_hw3.log', # имя файла логирования
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

class UserException(Exception):
    def __init__(self, text) -> None:
        self.text = text

    def __str__(self):
        logger.warning(self.text)
        return self.text
        

class UserLevelError(UserException):
    def __init__(self, text) -> None:
        self.text = text

    def __str__(self):
        logger.warning(self.text)
        return self.text

class UserAccessError(UserException):
    def __init__(self, text) -> None:
        self.text = text

    def __str__(self):
        logger.warning(self.text)
        return self.text

class User:
    def __init__(self, name, user_id, level):
        self.name = name
        self.user_id = user_id
        self.level = level
        
    def __str__(self):
        return f'{self.name = } {self.user_id = } {self.level = }'
    
    def __eq__(self, other) -> bool:    # магический метод проверки на равенство пользователей
        return self.name == other.name and self.user_id == other.user_id
        
    # def __lt__(self, other): # для оператора меньше <
    #     return self.level < other.level
    
    def __hash__(self):
        return hash((str(self.name), str(self.user_id)))
    
    
class Repo:
    def __init__(self):
        self.user = None
        self.users = set()       
            
            
    def read_file(self, user_file: Path) -> set[User]:
        with open(user_file, mode='r', encoding='utf-8') as f:
            data_json = json.load(f)  # загрузим данные из файла
        for dict_level, dict_value in data_json.items():
            for user_id, name in dict_value.items():
                self.users.add(User(name, int(user_id), int(dict_level)))
        return self.users


    def enter_user(self, name, user_id):
        current_user = User(name, user_id, level=0)
        if current_user not in self.users:
            raise UserAccessError('В доступе отказано')
        
        for user in self.users:
            if user == current_user:
                self.user = user
                logger.info(f'Пользователь {self.user} авторизовался в системе')
                return self.user
        
        
    def add_user(self, name, user_id, level):
        if level > self.user.level:
            raise UserLevelError('Уровень ниже положенного')
        new_user = User(name, user_id, level)
        self.users.add(new_user)
        logger.info(f'Пользователь {new_user} добавлен')
        return new_user

def parse(): # парсер командной строки
    parser = argparse.ArgumentParser(
        description='Добавляем данные нового пользователя с помощью существующей учётной записи', 
        epilog='При отсутствии значений нового пользователя добавляем пользователя anonim со случайным id и 1 уровнем допуска ',
        prog='add_user()')  # prog - функция которая будет применена к данным из командной строки
    parser.add_argument('-f', '--file', default='task2_users.json', help='Файл с данными: ')
    parser.add_argument('-nm', '--name_master', default='Андрей7', help='Имя авторизованного пользователя: ')
    parser.add_argument('-im', '--id_master', default='100071', help='ID авторизованного пользователя: ')
    parser.add_argument('-ns', '--name_slave', default='anonim', help='Имя нового пользователя: ')
    parser.add_argument('-is', '--id_slave', default=randint(100000, 999999), help='ID нового пользователя: ')
    parser.add_argument('-ls', '--level_slave', default=1, help='Уровень нового пользователя: ')
    args = parser.parse_args()    
    # repo = Repo()
    repo.read_file(Path(args.file))
    repo.enter_user(args.name_master, int(args.id_master))
    return repo.add_user(args.name_slave, int(args.id_slave), int(args.level_slave))
            

if __name__ == '__main__': 
    repo = Repo()
    print(parse())
    print(*repo.users, sep='\n')

# python .\sem15_hw3_users.py -nm Инокентий -im 100004 -ls 3    