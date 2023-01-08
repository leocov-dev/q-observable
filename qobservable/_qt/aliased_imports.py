try:
    from PySide2.QtCore import (
        Signal as _Signal,
        Slot as _Slot,
        QObject as _QObject,
        QThreadPool as _QThreadPool,
        QRunnable as _QRunnable,
    )
except ImportError:
    pass

try:
    from PySide6.QtCore import Signal as _Signal, Slot as _Slot, QObject as _QObject
except ImportError:
    pass

try:
    from PyQt5.QtCore import Signal as _Signal, Slot as _Slot, QObject as _QObject
except ImportError:
    pass

try:
    from PyQt6.QtCore import Signal as _Signal, Slot as _Slot, QObject as _QObject
except ImportError:
    pass
