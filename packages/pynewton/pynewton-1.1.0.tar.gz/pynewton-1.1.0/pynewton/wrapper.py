"""An asnycio-based wrapper for `https://newton.now.sh`"""
import sys
import httpx
from urllib.parse import quote

ENDPOINTS = [
    "simplify",
    "factor",
    "derive",
    "integrate",
    "zeroes",
    "tangent",
    "area",
    "cos",
    "sin",
    "tan",
    "arccos",
    "arcsin",
    "arctan",
    "abs",
    "log",
]


class Result:
    def __init__(self, **kwargs):
        self.operation = kwargs.get("operation", None)
        self.expression = kwargs.get("expression", None)
        self.result = kwargs.get("result", None)
        self.raw = kwargs

    def __str__(self):
        return str(self.result)

    __repr__ = __str__


async def _make_request(operation, expression):
    """Internal function to request a page by using a given string"""

    encoded_expression = quote(expression, safe="")
    url = f"https://newton.now.sh/api/v2/{operation}/{encoded_expression}"

    async with httpx.AsyncClient(http2=True) as session:
        req = await session.get(url)
        res = req.json()
        await session.aclose()
        return Result(**res)


def wrap_coro(coro):
    async def func():
        return await coro

    return func()


def expose_endpoints(module, *args):
    """
    Expose modules globally
    """

    # Credit goes to https://github.com/benpryke/PyNewtonMath
    # for giving me the idea of wrapping them dynamically.
    for op in args:
        # Wrap function
        def wrap(operator):
            return lambda exp: wrap_coro(_make_request(operator, exp))

        setattr(sys.modules[__name__], op, wrap(op))
        setattr(module, op, getattr(sys.modules[__name__], op))
