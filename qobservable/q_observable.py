from qobservable.q_operator import QOperator

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from ._qt.aliased_imports import _QObject, _QThreadPool, _QRunnable
from qobservable.q_observer import QObserver
from qobservable.q_subscriber import QSubscriber
from qobservable.q_subscription import QSubscription


class QObservable(_QObject):
    def __init__(self, subscriber: QSubscriber, parent: _QObject = None):
        super().__init__(parent=parent)
        self._pool = _QThreadPool.globalInstance()

        self._subscriber = subscriber
        self._is_running = False

    def subscribe(self, observer: QObserver) -> QSubscription:

        if hasattr(observer, "next"):
            self._subscriber.sig_next.connect(observer.next)
        if hasattr(observer, "complete"):
            self._subscriber.sig_complete.connect(observer.complete)
        if hasattr(observer, "error"):
            self._subscriber.sig_error.connect(observer.error)

        subscription = QSubscription()

        if not self._is_running:
            self._exec()

        return subscription

    def pipe(self, *operators: QOperator) -> Self:
        return self

    def _exec(self) -> None:
        self._is_running = True
        self._pool.start(_SubscriberWrapper(self._subscriber))


class _SubscriberWrapper(_QRunnable):
    def __init__(self, subscriber: QSubscriber):
        super(_SubscriberWrapper, self).__init__()
        self._subscriber = subscriber

    def run(self):
        self._subscriber.run()
