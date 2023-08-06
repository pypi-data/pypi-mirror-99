from typing import Generic, TypeVar

from . import __version__

VInt = TypeVar("VInt", bound=int)


class ValueInt(Generic[VInt]):
    pass


def get_headers():
    return {
        "Connection": "keep-alive",
        "User-Agent": f"pypi.org/project/covid19-id/{__version__}",
    }
