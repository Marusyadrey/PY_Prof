import types
from collections.abc import Iterable

# ==========================================
# Задание 1: FlatIterator для списка списков (ровно 2 уровня)
# ==========================================
class FlatIterator:
    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.outer_index = 0
        self.inner_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        # Пропускаем пустые внутренние списки
        while self.outer_index < len(self.list_of_list):
            current_inner_list = self.list_of_list[self.outer_index]
            if self.inner_index < len(current_inner_list):
                item = current_inner_list[self.inner_index]
                self.inner_index += 1
                return item
            else:
                # Переходим к следующему внутреннему списку
                self.outer_index += 1
                self.inner_index = 0

        raise StopIteration


def test_1():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


# ==========================================
# Задание 2: flat_generator для списка списков (ровно 2 уровня)
# ==========================================
def flat_generator(list_of_lists):
    for inner_list in list_of_lists:
        for item in inner_list:
            yield item


def test_2():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)


# ==========================================
# Задание 3*: FlatIterator с любой вложенностью
# ==========================================
class FlatIterator:
    def __init__(self, nested_list):
        # Используем стек: каждый элемент — это пара (список, индекс)
        self.stack = [(nested_list, 0)]

    def __iter__(self):
        return self

    def __next__(self):
        while self.stack:
            current_list, index = self.stack[-1]

            # Если дошли до конца текущего списка — поднимаемся выше
            if index >= len(current_list):
                self.stack.pop()
                continue

            item = current_list[index]
            self.stack[-1] = (current_list, index + 1)  # увеличиваем индекс

            if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
                # Если это итерируемый объект (но не строка/байты), спускаемся внутрь
                self.stack.append((item, 0))
            else:
                return item

        raise StopIteration


def test_3():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    expected = ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']

    for flat_iterator_item, check_item in zip(FlatIterator(list_of_lists_2), expected):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_2)) == expected


# ==========================================
# Задание 4*: flat_generator с любой вложенностью
# ==========================================
def flat_generator(nested_list):
    for item in nested_list:
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            # Рекурсивно «расплющиваем» вложенные структуры
            yield from flat_generator(item)
        else:
            yield item


def test_4():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    expected = ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']

    for flat_iterator_item, check_item in zip(flat_generator(list_of_lists_2), expected):
        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_2)) == expected
    assert isinstance(flat_generator(list_of_lists_2), types.GeneratorType)


if __name__ == '__main__':
    # Запускаем все тесты по очереди
    test_1()
    print("test_1 OK")

    test_2()
    print("test_2 OK")

    test_3()
    print("test_3 OK")

    test_4()
    print("test_4 OK")
