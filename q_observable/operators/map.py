from ._abstract_operator import AbstractOperator
from ..q_observable import QObservable
from .._typing import Callable


class Map(AbstractOperator):
    pass


def map(fn: Callable) -> Callable[[QObservable], QObservable]:
    def _wrapper(incoming: QObservable) -> QObservable:
        pass

    return _wrapper
