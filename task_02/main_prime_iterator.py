from collections.abc import Iterator


class PrimeIterator(Iterator):
    def __init__(self, start: int = 2, end: int | None = None) -> None:
        self.current = start
        self.end = end

    @classmethod
    def is_prime(cls, num: int) -> bool:
        if num < 2:
            return False
        for val in range(2, int(num**0.5) + 1):
            if num % val == 0:
                return False
        return True

    # Iterator cls!
    # def __iter__(self):
    #     return self

    def __next__(self) -> int:
        while self.current != self.end:
            if self.is_prime(self.current):
                prime_number = self.current
                self.current += 1
                return prime_number
            self.current += 1
        raise StopIteration


def main() -> None:
    for idx, prime in zip(range(1, 17), PrimeIterator()):
        print(f"prime {idx:2d}: {prime}")

    print()

    for idx, prime in enumerate(PrimeIterator(end=100), start=1):
        print(f"prime {idx:2d}: {prime}")

    print()
    print("Primes:")

    for prime in PrimeIterator(start=20, end=100):
        print(prime)

    print("List of primes:", list(PrimeIterator(start=5, end=70)))


if __name__ == "__main__":
    main()
