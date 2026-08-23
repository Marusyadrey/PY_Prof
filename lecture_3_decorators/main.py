import os
import datetime
from functools import wraps

# ==========================================
# Задание 1: простой декоратор logger (пишет в main.log)
# ==========================================
def logger(old_function):
    @wraps(old_function)
    def new_function(*args, **kwargs):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        func_name = old_function.__name__

        # Формируем строку аргументов (чтобы было читаемо в логе)
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
# Задание 2: параметризованный декоратор logger(path)
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
# Тесты из задания (без изменений)
# ==========================================
def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
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
# Возьмём flat_generator из ДЗ «Iterators. Generators. Yield»
# и обернём его в параметризованный логгер, чтобы видеть вызовы.

@logger("flat_generator.log")
def flat_generator(nested_list):
    for item in nested_list:
        # Важно: не логировать каждый yield отдельно — логгер срабатывает на вызов функции
        if isinstance(item, (list, tuple)) and not isinstance(item, (str, bytes)):
            yield from flat_generator(item)
        else:
            yield item


def demo_usage():
    """Демонстрация: прогоняем flat_generator и смотрим лог."""
    data = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    # flat_generator — это генератор, поэтому логгер запишет вызов, но не каждый yield
    gen = flat_generator(data)
    result = list(gen)
    print("Результат flat_generator:", result)


if __name__ == '__main__':
    # Сначала прогоняем тесты (они должны пройти без ошибок)
    test_1()
    test_2()

    # Затем демонстрация применения к предыдущему ДЗ
    demo_usage()

    print("Все тесты пройдены, логи созданы.")
