from ..q_observable import QObservable


class ForkJoin:
    def __init__(self, *observables: QObservable):
        self._observables = observables
