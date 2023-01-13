# warnings


class QObservableWarning(Warning):
    """Base warning for QObservable library"""


class QObservableQtImportWarning(QObservableWarning):
    """There was a problem importing a Qt library"""


class QObservableObjectWarning(QObservableWarning):
    """The C++ Qt object no longer exists"""


class QObservableShutdownWarning(QObservableWarning):
    """The application is shutting down but there are still running observables"""
