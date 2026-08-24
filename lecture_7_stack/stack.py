class Stack:
    def __init__(self):
        self._items = []

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def size(self) -> int:
        return len(self._items)


def is_balanced(s: str) -> bool:
    stack = Stack()
    pairs = {')': '(', ']': '[', '}': '{'}
    opening = set(pairs.values())

    for ch in s:
        if ch in opening:
            stack.push(ch)
        elif ch in pairs:
            if stack.is_empty():
                return False
            top = stack.pop()
            if top != pairs[ch]:
                return False

    return stack.is_empty()


def check_brackets(s: str):
    if is_balanced(s):
        print("Сбалансированно")
    else:
        print("Несбалансированно")
