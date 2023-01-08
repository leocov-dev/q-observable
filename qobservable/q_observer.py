from typing import TypeVar

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol

OV = TypeVar("OV")


class QObserver(Protocol[OV]):
    def next(self, value: OV) -> None:
        ...

    def complete(self) -> None:
        ...

    def error(self, error: Exception) -> None:
        ...
