from typing import Generic, TypeVar

T = TypeVar("T")


class MyQueue(Generic[T]):
    def __init__(self) -> None:
        self.bottom: list[T] = []
        self.top: list[T] = []

    def _fill(self) -> None:
        if not self.top:
            while self.bottom:
                self.top.append(self.bottom.pop())

    def push(self, item: T) -> None:
        self.bottom.append(item)

    def pop(self) -> T:
        self._fill()
        return self.top.pop()

    def peek(self) -> T:
        self._fill()
        return self.top[-1]

    def is_empty(self) -> bool:
        return not self.top and not self.bottom
