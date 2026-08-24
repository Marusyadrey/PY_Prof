import pytest
from stack import Stack, is_balanced, check_brackets


class TestStack:
    def test_is_empty_new(self):
        s = Stack()
        assert s.is_empty() is True

    def test_push_and_size(self):
        s = Stack()
        s.push(1)
        s.push(2)
        assert s.size() == 2
        assert s.is_empty() is False

    def test_pop(self):
        s = Stack()
        s.push(10)
        s.push(20)
        assert s.pop() == 20
        assert s.pop() == 10
        assert s.is_empty() is True

    def test_peek(self):
        s = Stack()
        s.push("x")
        assert s.peek() == "x"
        assert s.size() == 1

    def test_pop_empty_raises(self):
        s = Stack()
        with pytest.raises(IndexError):
            s.pop()

    def test_peek_empty_raises(self):
        s = Stack()
        with pytest.raises(IndexError):
            s.peek()


class TestBrackets:
    @pytest.mark.parametrize(
        "s, expected",
        [
            ("(((([{}]))))", True),
            ("[([])((([[[]]])))]{()}", True),
            ("{{[()]}}", True),
            ("", True),
            ("()[]{}", True),
            ("}{}", False),
            ("{{[(])]}}", False),
            ("[[{())}]", False),
            ("([)]", False),
        ],
    )
    def test_is_balanced(self, s, expected):
        assert is_balanced(s) is expected
