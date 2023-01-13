from ._abstract_operator import AbstractOperator
from ..q_observable import QObservable


class ForkJoin(AbstractOperator):
    def __init__(self, *observables: QObservable):
        self._observables = observables
