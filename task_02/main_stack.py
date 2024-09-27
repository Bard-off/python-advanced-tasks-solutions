from collections.abc import Iterable, Iterator
from typing import Generic, TypeVar


T = TypeVar("T")


class Stack(Generic[T], Iterator):
    def __init__(self, initial: Iterable[T] = ()) -> None:
        self._items: list[T] = list(initial)
        self._iter_idx: int = 0

    def push(self, item: T) -> None:
        self._items.append(item)

    def is_empty(self) -> bool:
        return not self._items

    def check_is_empty(self) -> None:
        if self.is_empty():
            raise IndexError("Stack is empty")

    def pop(self) -> T:
        self.check_is_empty()
        return self._items.pop()

    def peek(self) -> T:
        self.check_is_empty()
        return self._items[-1]

    def __iter__(self) -> "Stack[T]":
        # too easy:
        # return reversed(self.items)
        self._iter_idx = len(self._items) - 1
        return self

    def __next__(self) -> T:
        if self._iter_idx < 0:
            raise StopIteration
        self._iter_idx -= 1
        return self._items[self._iter_idx + 1]


class IntStack(Stack[int]):
    pass


def main() -> None:
    numbers_stack = IntStack([1, 2, 3])
    numbers_stack.push(4)
    numbers_stack.push(5)
    print("to list:", list(numbers_stack))
    print("one by one:")
    for idx, number in enumerate(numbers_stack):
        print(idx, number)
    print("pop:", numbers_stack.pop())
    print("add 7")
    numbers_stack.push(7)
    print("Top:", numbers_stack.peek())
    for idx, number in enumerate(numbers_stack):
        print(idx, number)


if __name__ == "__main__":
    main()
