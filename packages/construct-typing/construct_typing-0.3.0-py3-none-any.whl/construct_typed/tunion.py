import dataclasses
import textwrap
import typing as t

import construct as cs

from .generic_wrapper import *

DataclassType = t.TypeVar("DataclassType")


def ufield(
    subcon: Construct[ParsedType, t.Any],
    doc: t.Optional[str] = None,
    parsed: t.Optional[t.Callable[[t.Any, "cs.Context"], None]] = None,
) -> ParsedType:
    """
    Create a dataclass field for a "TUnion" from a subcon.
    """
    # Rename subcon, if doc or parsed are available
    if (doc is not None) or (parsed is not None):
        if doc is not None:
            doc = textwrap.dedent(doc)
        subcon = cs.Renamed(subcon, newdocs=doc, newparsed=parsed)

    if subcon.flagbuildnone is True:
        # some subcons have a predefined default value. all other have "None"
        default: t.Any = None
        if isinstance(subcon, (cs.Const, cs.Default)):
            if callable(subcon.value):
                raise ValueError("lamda as default is not supported")
            default = subcon.value

        # if subcon builds from "None", set default to "None"
        field = dataclasses.field(
            default=default,
            init=False,
            metadata={"subcon": cs.Renamed(subcon, newdocs=doc)},
        )
    else:
        field = dataclasses.field(metadata={"subcon": subcon})

    return field  # type: ignore

TUnionField = ufield  # also support legacy name

class TUnion(Adapter[t.Any, t.Any, DataclassType, DataclassType]):
    pass  # TODO
