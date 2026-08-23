import os
import datetime
from functools import wraps

# ==========================================
# Задание 1: простой декоратор logger_simple (пишет в main.log)
# ==========================================
def logger_simple(old_function):
    @wraps(old_function)
    def new_function(*args, **kwargs):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        func_name = old_function.__name__

        args_repr = ", ".join(repr(arg) for arg in args)
        kwargs_repr = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
        all_args = f"{args_repr}, {kwargs_repr}".strip(", ")

        result = old_function(*args, **kwargs)

        log_line = f"[{timestamp}] {func_name}({all_args}) -> {result!r}\n"

        with open("main.log", "a", encoding="utf-8") as f:
            f.write(log_line)

        return result
    return new_function


# ==========================================
# Задание 2: параметризованный декоратор logger (пишет в указанный файл)
# ==========================================
def logger(path):
    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            func_name = old_function.__name__

            args_repr = ", ".join(repr(arg) for arg in args)
            kwargs_repr = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
            all_args = f"{args_repr}, {kwargs_repr}".strip(", ")

            result = old_function(*args, **kwargs)

            log_line = f"[{timestamp}] {func_name}({all_args}) -> {result!r}\n"

            with open(path, "a", encoding="utf-8") as f:
                f.write(log_line)

            return result
        return new_function
    return __logger


# ==========================================
# Тесты из задания (с исправленными именами декораторов)
# ==========================================
def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger_simple
    def hello_world():
        return 'Hello World'

    @logger_simple
    def summator(a, b=0):
        return a + b

    @logger_simple
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:
        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


# ==========================================
# Задание 3: применение логгера к функции из предыдущего ДЗ
# ==========================================
@logger("flat_generator.log")
def flat_generator(nested_list):
    for item in nested_list:
        if isinstance(item, (list, tuple)) and not isinstance(item, (str, bytes)):
            yield from flat_generator(item)
        else:
            yield item


def demo_usage():
    data = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    gen = flat_generator(data)
    result = list(gen)
    print("Результат flat_generator:", result)


if __name__ == '__main__':
    test_1()
    test_2()
    demo_usage()
    print("Все тесты пройдены, логи созданы.")
