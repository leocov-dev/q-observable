# noinspection PyUnresolvedReferences
from typing import (
    Optional,
    Generic,
    TypeVar,
    Any,
    Callable,
    List,
)

try:
    from typing import Self, Protocol
except ImportError:
    from typing_extensions import Self, Protocol
