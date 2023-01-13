import functools
import warnings

from ._qt import is_valid, QObject, QRunnable, Signal
from ._typing import Optional, Generic, TypeVar, Any, Self
from .exceptions import QObservableObjectWarning, QObservableWarning
from .interfaces import (
    SubscriberFn,
    NextSlotFn,
    CompleteSlotFn,
    ErrorSlotFn,
    QOperatorInterface,
)
from .q_observable_thread_pool import get_observable_thread_pool
from .q_subscription import QSubscription

__all__ = ["QObservable"]

T = TypeVar("T")


class QObservable(Generic[T], QObject):
    def __init__(self, fn: SubscriberFn[T]):
        super(QObservable, self).__init__()
        self._pool = get_observable_thread_pool()

        self._subscriber_function = fn
        self._subscriber_wrapper = _RunnableSubscriberWrapper(fn)
        self._is_running = False

    def subscribe(
        self,
        next_fn: Optional[NextSlotFn[T]] = None,
        complete_fn: Optional[CompleteSlotFn] = None,
        error_fn: Optional[ErrorSlotFn] = None,
    ) -> QSubscription:
        subscription = QSubscription(
            functools.partial(
                self._subscriber_wrapper.disconnect_signals,
                next_slot=next_fn,
                complete_slot=complete_fn,
                error_slot=error_fn,
            )
        )

        def _complete() -> None:
            if callable(complete_fn):
                complete_fn()
            subscription.unsubscribe()

        self._subscriber_wrapper.connect_signals(
            next_slot=next_fn, complete_slot=_complete, error_slot=error_fn
        )

        if not self._is_running:
            self._is_running = True
            self._pool.start(self._subscriber_wrapper)

        return subscription

    def pipe(self, *operators: QOperatorInterface) -> Self:
        # TODO: handle stacking connections
        return self


class _Subscriber(QObject):
    sig_next = Signal(object)
    sig_complete = Signal()
    sig_error = Signal(object)

    def __init__(self):
        super(_Subscriber, self).__init__()
        self._is_complete = False

    def next(self, val: Any) -> None:
        if not is_valid(self):
            warnings.warn(
                "Can't call Subscriber.next(). The Qt Object is already deleted",
                QObservableObjectWarning,
            )
            return
        self.sig_next.emit(val)

    def complete(self) -> None:
        if not is_valid(self):
            warnings.warn(
                "Can't call Subscriber.complete(). The Qt Object is already deleted",
                QObservableObjectWarning,
            )
            return

        if self._is_complete:
            warnings.warn(
                "Skipping Subscriber.complete(). The QObservable is already complete",
                QObservableWarning,
            )
            return

        self._is_complete = True
        self.sig_complete.emit()

    def error(self, error: Exception) -> None:
        if not is_valid(self):
            warnings.warn(
                "Can't call Subscriber.error(). The Qt Object is already deleted",
                QObservableObjectWarning,
            )
            return

        self.sig_error.emit(error)


class _RunnableSubscriberWrapper(Generic[T], QRunnable):
    def __init__(self, fn: SubscriberFn[T]):
        super(_RunnableSubscriberWrapper, self).__init__()
        self.setAutoDelete(True)

        self._sub_sig = _Subscriber()
        self._fn = fn

    def connect_signals(
        self,
        *,
        next_slot: Optional[NextSlotFn[T]] = None,
        complete_slot: Optional[CompleteSlotFn] = None,
        error_slot: Optional[ErrorSlotFn] = None,
    ) -> None:
        if callable(next_slot):
            self._sub_sig.sig_next.connect(next_slot)
        if callable(complete_slot):
            self._sub_sig.sig_complete.connect(complete_slot)
        if callable(error_slot):
            self._sub_sig.sig_error.connect(error_slot)

    def disconnect_signals(
        self,
        *,
        next_slot: Optional[NextSlotFn[T]] = None,
        complete_slot: Optional[CompleteSlotFn] = None,
        error_slot: Optional[ErrorSlotFn] = None,
    ) -> None:
        if callable(next_slot):
            self._sub_sig.sig_next.disconnect(next_slot)
        if callable(complete_slot):
            self._sub_sig.sig_complete.disconnect(complete_slot)
        if callable(error_slot):
            self._sub_sig.sig_error.disconnect(error_slot)

    def run(self):

        teardown_fn = self._fn(self._sub_sig)
        if callable(teardown_fn):
            teardown_fn()

        self._sub_sig.complete()
