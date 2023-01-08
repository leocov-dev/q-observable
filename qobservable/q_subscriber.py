import abc

from ._qt.aliased_imports import _QObject, _Signal


class QSubscriber(_QObject):
    sig_next = _Signal(object)
    sig_complete = _Signal()
    sig_error = _Signal(object)

    def next(self, val) -> None:
        self.sig_next.emit(val)

    def complete(self) -> None:
        self.sig_complete.emit()

    def error(self, error: Exception) -> None:
        self.sig_error.emit(error)

    @abc.abstractmethod
    def run(self) -> None:
        raise NotImplementedError
