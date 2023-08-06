from typing import Generic, TypeVar


VInt = TypeVar("VInt", bound=int)


class ValueInt(Generic[VInt]):
    pass
