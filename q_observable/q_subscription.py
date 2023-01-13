from ._qt import QObject, Signal
from ._typing import Callable

__all__ = ["QSubscription"]


class QSubscription(QObject):
    _sig_unsubscribe = Signal()

    def __init__(self, on_unsubscribe: Callable[[], None]):
        super(QSubscription, self).__init__()
        self._is_active = True
        self._sig_unsubscribe.connect(on_unsubscribe)

    def unsubscribe(self) -> None:
        if not self._is_active:
            return

        self._sig_unsubscribe.emit()
        self._is_active = False
