import logging

from .interfaces import QSubscriberInterface
from .q_observable import QObservable
from .q_subscription import QSubscription
from .q_observable_thread_pool import (
    wait_for_running_observables,
    set_observable_thread_pool,
    get_observable_thread_pool,
)

__version__ = "0.1.0"

__all__ = [
    "QSubscription",
    "QObservable",
    "QSubscriberInterface",
    "get_observable_thread_pool",
    "set_observable_thread_pool",
    "wait_for_running_observables",
]

# TODO: ...
# log = logging.basicConfig(level=logging.DEBUG)
