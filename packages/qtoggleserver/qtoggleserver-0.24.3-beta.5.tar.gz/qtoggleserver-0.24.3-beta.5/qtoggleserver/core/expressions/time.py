
import time

from typing import Any, Dict

from .base import Evaluated
from .functions import function, Function


@function('TIME')
class TimeFunction(Function):
    MIN_ARGS = MAX_ARGS = 0
    DEPS = ['second']

    async def eval(self, context: Dict[str, Any]) -> Evaluated:
        return int(time.time())


@function('TIMEMS')
class TimeMSFunction(Function):
    MIN_ARGS = MAX_ARGS = 0
    DEPS = ['millisecond']

    async def eval(self, context: Dict[str, Any]) -> Evaluated:
        return int(time.time() * 1000)
