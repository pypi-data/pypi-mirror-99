from abc import ABC, abstractmethod
from decimal import Decimal
from collections import deque
from typing import Generic, Optional, TypeVar, Callable
from highwire.events import Event


Tick = Event[Optional[int]]

T = TypeVar("T")
X = TypeVar("X", float, Decimal)


class Sampler(Generic[T], ABC):
    @abstractmethod
    def sample(self, tick: Optional[Tick] = None) -> None:
        pass

    @abstractmethod
    def get(self) -> Optional[T]:
        pass

    def __call__(self, tick: Optional[Tick] = None) -> Optional[T]:
        self.sample(tick)
        return self.get()


class MovingAverage(Sampler[X]):
    def __init__(self, n: int, fn: Callable[[], Optional[X]]):
        self._n = n
        self._buffer: deque = deque(maxlen=n)
        self._fn: Callable[[], Optional[X]] = fn

    def sample(self, tick: Optional[Tick] = None) -> None:
        val = self._fn()
        if val is not None:
            self._buffer.append(val)

    def get(self) -> Optional[X]:
        if len(self._buffer) == self._n:
            return sum(self._buffer) / self._n  # type: ignore
        return None
