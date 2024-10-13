import re
import abc
from typing import Optional, Union, NoReturn
from functions import NotMakeFile, WriteTemplate, WriteDefine, ParseAttr, FileDispatch
from BuiltinMacro import BuiltinMacros
import RegEx


class IFileString(metaclass=abc.ABCMeta):
    __slots__ = tuple()

    @abc.abstractmethod
    def __init__(self, string:str) -> None: ...

    @abc.abstractmethod
    def process_macro(self) -> None: ...

    @abc.abstractmethod
    def remove(self, string:str) -> None: ...

    @abc.abstractmethod
    def writemacro(self, identifier:str, content:str) -> None: ...

    @abc.abstractmethod
    def writetemplate(self, identifier:str, params:list[str], content:str) -> None: ...

    @property
    def HTMLContent(self) -> Optional[str]:
        return None

    @HTMLContent.setter
    def HTMLContent(self, s:str): ...

    @property
    def SubtitlesContent(self) -> Optional[str]:
        return None

    @SubtitlesContent.setter
    def SubtitlesContent(self, s:str): ...


class OneFile_Only(IFileString):
    __slots__ = ("_Str",)

    def __init__(self, string: str) -> None:
        self._Str = string

    def remove(self, string: str) -> None:
        self._Str = self._Str.replace(string, "", 1)

    def writemacro(self, identifier: str, content: str) -> None:
        self._Str = self._Str.replace(identifier, content)

    def writetemplate(self, identifier: str, params: list[str], content: str) -> None:
        self._Str = WriteTemplate(self._Str, identifier, params, content)


def _Macro_Process(s:str, mytype:str):
    pos = 0
    while (m := RegEx.Define.search(s, pos)):
        pos = m.pos
        s = s.replace(m[0], "", 1)
        attrs = ParseAttr(m["ATTR"])
        s = WriteDefine(s, attrs, m["CONTENT"], mytype)
    for m in BuiltinMacros:
        s = m(s, mytype)
    return s


class HTML_Only(OneFile_Only):
    __slots__ = tuple()

    def process_macro(self) -> None:
        self._Str = _Macro_Process(self._Str, "html")

    @IFileString.HTMLContent.getter
    def HTMLContent(self):
        return self._Str

    @HTMLContent.setter
    def HTMLContent(self, s:str):
        self._Str = s


class SubtitlesOnly(OneFile_Only):
    __slots__ = tuple()

    def process_macro(self) -> None:
        self._Str = _Macro_Process(self._Str, "subtitles")

    @IFileString.SubtitlesContent.getter
    def SubtitlesContent(self):
        return self._Str

    @SubtitlesContent.setter
    def SubtitlesContent(self, s:str):
        self._Str = s


class BothFile(IFileString):
    __slots__ = ("_SHTML", "_SSubtitles")

    def __init__(self, string: str) -> None:
        self._SHTML = self._SSubtitles = string

    def process_macro(self) -> None:
        self._SHTML = _Macro_Process(self._SHTML, "html")
        self._SSubtitles = _Macro_Process(self._SSubtitles, "subtitles")

    def remove(self, string: str) -> None:
        self._SHTML = self._SHTML.replace(string, "", 1)
        self._SSubtitles = self._SSubtitles.replace(string, "", 1)

    def writemacro(self, identifier: str, content: str) -> None:
        if (li := RegEx.FileDispatch.findall(content)):
            for m in li:
                m:re.Match
                if (m["FTYPE"] == "html"):
                    self._SHTML = self._SHTML.replace(identifier, m["CONTENT"])
                elif (m["FTYPE"] == "subtitles"):
                    self._SSubtitles = self._SSubtitles.replace(identifier, m["CONTENT"])
        else:
            self._SHTML = self._SHTML.replace(identifier, content)
            self._SSubtitles = self._SSubtitles.replace(identifier, content)

    def writetemplate(self, identifier: str, params: list[str], content: str) -> None:
        self._SHTML = WriteTemplate(self._SHTML, identifier, params, content, "html")
        self._SSubtitles = WriteTemplate(self._SSubtitles, identifier, params, content, "subtitles")

    @IFileString.HTMLContent.getter
    def HTMLContent(self):
        return self._SHTML

    @HTMLContent.setter
    def HTMLContent(self, s:str):
        self._SHTML = s

    @IFileString.SubtitlesContent.getter
    def SubtitlesContent(self):
        return self._SSubtitles

    @SubtitlesContent.setter
    def SubtitlesContent(self, s:str):
        self._SSubtitles = s



def CreateFileString(string:str, use_html:bool, use_subtitles:bool) -> Union[IFileString, NoReturn]:
    if (use_html and (not use_subtitles)):
        return HTML_Only(string)
    elif ((not use_html) and use_subtitles):
        return SubtitlesOnly(string)
    elif (use_html and use_subtitles):
        return BothFile(string)
    else:
        NotMakeFile()
