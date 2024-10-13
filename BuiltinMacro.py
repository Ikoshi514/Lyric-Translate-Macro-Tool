from functions import WriteMacro, WriteTemplate
from typing import Iterable
import abc

class IMacro(metaclass=abc.ABCMeta):
    __slots__ = tuple()

    @abc.abstractmethod
    def __call__(self, s:str, mytype:str) -> str: ...


class Macro(IMacro):
    __slots__ = ("_Identifier", "_Content",)

    def __init__(self, identifier:str, content:str=""):
        self._Identifier = identifier
        self._Content = content

    def __call__(self, s:str, mytype:str) -> str:
        return WriteMacro(s, self._Identifier, self._Content, mytype)


class Template(IMacro):
    __slots__ = ("_Identifier", "_Params", "_Content",)

    def __init__(self, identifier:str, params:Iterable[str]=[], content:str=""):
        self._Identifier = identifier
        self._Params = params
        self._Content = content

    def __call__(self, s:str, mytype:str) -> str:
        return WriteTemplate(s, self._Identifier, self._Params, self._Content, mytype)


DoubleSpace = Macro(
    "  ",
    "<html>&nbsp;&nbsp;</html><subtitles>  </subtitles>"
)


# %ColorBegin(_R, _G, _B)%
ColorBegin = Template(
    "ColorBegin",
    ("_R", "_G", "_B"),
    """<html><span style="color: #_R_G_B"></html><subtitles>{\\1c(_B_G_R)}</subtitles>"""
    )

# %ColorEnd%
ColorEnd = Macro(
    "%ColorEnd%",
    "<html></span></html><subtitles>{\\1c(ffffff)}</subtitles>"
    )


BuiltinMacros:list[IMacro] = [
    DoubleSpace,
    ColorBegin, ColorEnd
]
