import logging
import functools
import time

# налаштування логування
# логуємо до файлу кожен раз створюючи новий
# форматуємо за принципом поточнйи дата час - повідомлення
logging.basicConfig(filename="", filemode="w", level=logging.INFO,
                    format='%(asctime)s:\n%(message)s', encoding='utf-8')



def logging_decorator(func):
    """ логер декоратор
    огортає функцію та логує повідомлення перед початком запуску
    відловлює виключення при виконанні
    при успішному виконанні логує час затрачений на виконання """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(
            f"* Було викликано функцію [{func.__name__}] з аргументами [{args}]\n* Що виконує дію : [{func.__doc__}]")
        start_time = time.time()
        try:
            func(*args, **kwargs)
        except Exception as e:
            logging.info(
                f"* При виконанні функції [{func.__name__}] було кинуто виключення [{e}]")
        else:
            end_time = time.time()
            elapsed_time = end_time-start_time 
            logging.info(f"* Функція успішно виконалась [{func.__name__}] час виконання [{elapsed_time}] секунд")
    return wrapper


class TaskManager:
    """ Клас менеджер завдань. 
        Має в собі список завдань. в даному випадку це функції без аргументів.
        Надає можлтивості додавання, виконання , та видалення завдань.
        Всі дії логуються.
    """
    def __init__(self) -> None:
        self._tasks = []

    @logging_decorator
    def add_task(self, task_func):
        """ Додаю завдання до списку завдань """
        self._tasks.append(task_func)

    @logging_decorator
    def del_first_task(self):
        """ Видаляю перше завдання з черги"""
        self._tasks.pop(0)

    @logging_decorator
    def del_last_task(self):
        """ Видаляю останнє завдання з черги  """
        self._tasks.pop()

    @logging_decorator
    def run_first_task(self):
        """ Запускаю перше завдання з черги """
        self._tasks.pop(0)()

    @logging_decorator
    def run_last_task(self):
        """ Запускаю останнє завдання з черги """
        self._tasks.pop()()

    def __str__(self):
        """ Рядкове представлення поточних завдань """
        if len(self._tasks) == 0:
            return 'Поточні завдання відсутні!'

        return 'Поточні завдання:\n' + \
               '\n'.join([f'{i+1}. '+x.__name__ for i,x in enumerate(self._tasks)])

# тут оголошені функції завдання
# кожна з них щось робить

def test_function1():
    print("Сплю 1.5 секунди...")
    time.sleep(1.5)


def test_function2():
    print("Сплю 2.5 секунди...")
    time.sleep(2.5)

def test_function3():
    print("Сплю 0.5 секунди...")
    time.sleep(0.5)
    print("ділю 1 на 0...")
    a = 1/0


if __name__ == "__main__":
    # створє об'єкт
    task_manager = TaskManager()

    # додає завдання
    task_manager.add_task(lambda: time.sleep(1))
    task_manager.add_task(test_function1)
    task_manager.add_task(test_function2)
    task_manager.add_task(test_function3)
    task_manager.add_task(lambda: time.sleep(1))
    
    # показує вміст
    print(task_manager)

    # видаляю перше і останнє
    task_manager.del_first_task()
    task_manager.del_last_task()

    # показує вміст
    print(task_manager)


    # запускає всі доступні в пордяку з кінця
    task_manager.run_last_task()
    task_manager.run_last_task()
    task_manager.run_last_task()
    task_manager.run_last_task()

    # показує вміст
    print(task_manager)

