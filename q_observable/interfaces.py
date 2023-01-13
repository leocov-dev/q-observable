from ._typing import TypeVar, Protocol, Callable, Optional

__all__ = ["QSubscriberInterface", "QOperatorInterface"]

T = TypeVar("T")


class QSubscriberInterface(Protocol[T]):
    def next(self, val: T) -> None:
        ...

    def complete(self) -> None:
        ...

    def error(self, error: Exception) -> None:
        ...


SubscriberTeardownFn = Callable[[], None]
SubscriberFn = Callable[[QSubscriberInterface[T]], Optional[SubscriberTeardownFn]]

NextSlotFn = Callable[[T], None]
CompleteSlotFn = Callable[[], None]
ErrorSlotFn = Callable[[Exception], None]


class QOperatorInterface(Protocol):
    ...


class QSubscriberRunnableInterface(Protocol):
    def run(self) -> None:
        ...

    def connect_signals(
        self,
        *,
        next_slot: Optional[NextSlotFn[T]] = None,
        complete_slot: Optional[CompleteSlotFn] = None,
        error_slot: Optional[ErrorSlotFn] = None,
    ) -> None:
        ...

    def disconnect_signals(
        self,
        *,
        next_slot: Optional[NextSlotFn[T]] = None,
        complete_slot: Optional[CompleteSlotFn] = None,
        error_slot: Optional[ErrorSlotFn] = None,
    ) -> None:
        ...
