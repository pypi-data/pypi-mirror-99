
from typing import Any, Dict

from .base import Evaluated
from .functions import function, Function


@function('AND')
class AndFunction(Function):
    MIN_ARGS = 2

    async def eval(self, context: Dict[str, Any]) -> Evaluated:
        r = True
        for e in await self.eval_args(context):
            r = r and bool(e)

        return int(r)


@function('OR')
class OrFunction(Function):
    MIN_ARGS = 2

    async def eval(self, context: Dict[str, Any]) -> Evaluated:
        r = False
        for e in await self.eval_args(context):
            r = r or bool(e)

        return int(r)


@function('NOT')
class NotFunction(Function):
    MIN_ARGS = MAX_ARGS = 1

    async def eval(self, context: Dict[str, Any]) -> Evaluated:
        return int(not bool((await self.eval_args(context))[0]))


@function('XOR')
class XOrFunction(Function):
    MIN_ARGS = MAX_ARGS = 2

    async def eval(self, context: Dict[str, Any]) -> Evaluated:
        eval_args = await self.eval_args(context)

        e1 = bool(eval_args[0])
        e2 = bool(eval_args[1])

        return int(e1 and not e2 or e2 and not e1)
