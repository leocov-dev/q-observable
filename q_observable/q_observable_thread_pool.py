import functools
import warnings

from ._typing import Optional

from ._qt import QObject, QThreadPool, QRunnable

__all__ = [
    "wait_for_running_observables",
    "get_observable_thread_pool",
    "set_observable_thread_pool",
]

from .exceptions import QObservableShutdownWarning, QObservableWarning
from .interfaces import QSubscriberRunnableInterface


class QObservableThreadPool(QObject):
    def __init__(
        self,
        thread_pool: Optional[QThreadPool] = None,
        parent: Optional[QObject] = None,
    ):
        super(QObservableThreadPool, self).__init__(parent=parent)

        print("NEW")
        self._running_count = 0

        if thread_pool:
            self._pool = thread_pool
            self._pool.setParent(self)
            if not parent:
                raise Exception(
                    "QObservablePool with custom QThreadPool MUST define a parent QObject"
                )
        else:
            self._pool = QThreadPool.globalInstance()

    @property
    def running_count(self) -> int:
        return self._running_count

    def wait_for_done(self) -> None:
        self._pool.waitForDone()

    def start(self, runnable: QSubscriberRunnableInterface) -> None:
        self._running_count += 1
        runnable.connect_signals(complete_slot=functools.partial(self._decrement_count))
        # TODO: should priority setting be allowed?
        self._pool.start(runnable)

    def _decrement_count(self) -> None:
        self._running_count -= 1


__observable_thread_pool: Optional[QObservableThreadPool] = None


def get_observable_thread_pool() -> QObservableThreadPool:
    global __observable_thread_pool

    if not __observable_thread_pool:
        __observable_thread_pool = QObservableThreadPool()

    return __observable_thread_pool


def set_observable_thread_pool(custom_pool: QThreadPool) -> None:
    global __observable_thread_pool

    if __observable_thread_pool:
        warnings.warn(
            "Can't reassign global observable thread pool. Set it earlier in your application lifecycle",
            QObservableWarning,
        )
        return

    __observable_thread_pool = QObservableThreadPool(custom_pool)


def wait_for_running_observables(*args, **kwargs) -> None:
    global __observable_thread_pool

    if not __observable_thread_pool:
        return

    if __observable_thread_pool.running_count > 0:
        warnings.warn(
            f"Waiting for {__observable_thread_pool.running_count} running observables to complete.",
            QObservableShutdownWarning,
        )
        __observable_thread_pool.wait_for_done()
        warnings.warn(
            "Running observables are complete.",
            QObservableShutdownWarning,
        )
