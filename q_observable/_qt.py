import warnings

from .exceptions import QObservableQtImportWarning

__imports_done = False

# PySide2 ----------------------------------------------------------------------
try:
    from shiboken2.shiboken2 import isValid as is_valid
    from PySide2.QtCore import (
        Signal,
        Slot,
        QObject,
        QThreadPool,
        QRunnable,
    )

    __imports_done = True
except ImportError:
    pass

# PySide6 ----------------------------------------------------------------------
try:
    if not __imports_done:
        from shiboken6 import isValid as is_valid
        from PySide6.QtCore import (
            Signal,
            Slot,
            QObject,
            QThreadPool,
            QRunnable,
        )

        __imports_done = True
except ImportError:
    pass

# PyQt5 ------------------------------------------------------------------------
try:
    if not __imports_done:
        from PyQt5.sip import isdeleted
        from PyQt5.QtCore import (
            Signal,
            Slot,
            QObject,
            QThreadPool,
            QRunnable,
        )

        def is_valid(obj) -> bool:
            return not isdeleted(obj)

        __imports_done = True
except ImportError:
    pass

# PyQt6 ------------------------------------------------------------------------
try:
    if not __imports_done:
        from PyQt6.sip import isdeleted
        from PyQt6.QtCore import (
            Signal,
            Slot,
            QObject,
            QThreadPool,
            QRunnable,
        )

        def is_valid(obj) -> bool:
            return not isdeleted(obj)

        __imports_done = True
except ImportError:
    pass

if not __imports_done:
    warnings.warn(
        "Failed to import any Qt library [PySide2, PySide6, PyQt5, PyQt6]",
        QObservableQtImportWarning,
    )
