from options import __dict__ as options
from options import *
from typing import NoReturn, TextIO, Optional
import RegEx
import re
import sys

def printexit(text:str):
    if ("-ExitPause" in sys.argv):
        input(text)
    else:
        print(text)
    exit()

def WrapQuote(text:str) -> str:
    return f"\"{text}\""

def PrintErrorMessage(errortype:type, *args:str) -> NoReturn:
    if errortype is FileNotFoundError:
        if CLI_LANGUAGE == "kr":
            printexit(f"파일 {WrapQuote(args[0])}를 찾을 수 없습니다.")
        elif CLI_LANGUAGE == "en":
            printexit(f"File {WrapQuote(args[0])} is not found.")
        else:
            printexit(f"File {WrapQuote(args[0])} is not found.")

    elif errortype is UnicodeDecodeError:
        if CLI_LANGUAGE == "kr":
            printexit(f"""파일 {WrapQuote(args[0])}의 인코드가 {WrapQuote(args[1])}와는 다릅니다.\
 대상 파일의 인코드를 변경하거나, 소스 코드의 {WrapQuote("ENCODE")} 변수의 값을 변경해주세요.""")
        elif CLI_LANGUAGE == "en":
            printexit(f"""File {WrapQuote(args[0])} is not encoded by {WrapQuote(args[1])}.\
 Change encode of target file, of change source code's const variable {WrapQuote("ENCODE")}.""")
        else:
            printexit(f"""File {WrapQuote(args[0])} is not encoded by {WrapQuote(args[1])}.\
 Change encode of target file, of change source code's const variable {WrapQuote("ENCODE")}.""")

    printexit("Unknown Error")

def NotMakeFile() -> NoReturn:
    if CLI_LANGUAGE == "kr":
        printexit("현재 설정 상 `HtmlMacro.py`가 아무런 파일도 출력하지 않습니다.")
    elif CLI_LANGUAGE == "en":
        printexit("For now options set, `HtmlMacro.py` doesn't make any file.")
    else:
        printexit("For now options set, `HtmlMacro.py` doesn't make any file.")


def WrongPragma(what:str, text:str) -> None:
    if (what == "comment") or (what == "ytkey"):
        if CLI_LANGUAGE == "kr":
            print(f"\nytkey pragma에 동일한 속성 두 개가 존재합니다:\n{text}\n")
        elif CLI_LANGUAGE == "en":
            print(f"\nThe same two attributes exist in a ytkey pragma:\n{text}\n")
        else:
            print(f"\nThe same two attributes exist in a ytkey pragma:\n{text}\n")

    else:
        if CLI_LANGUAGE == "kr":
            print(f"\n알 수 없는 pragma입니다:\n{text}")
        elif CLI_LANGUAGE == "en":
            print(f"\nUnknown pragma:\n{text}\n")
        else:
            print(f"\nUnknown pragma:\n{text}\n")

def WrongMacro(text:str) -> None:
    if CLI_LANGUAGE == "kr":
        print(f"\n매크로 문법이 올바르지 않습니다:\n{text}\n")
    elif CLI_LANGUAGE == "en":
        print(f"\nWrong macro syntax:\n{text}\n")
    else:
        print(f"\nWrong macro syntax:\n{text}\n")

def GetFileName() -> str:
    if CLI_LANGUAGE == "kr":
        return input("파일 이름: ")
    elif CLI_LANGUAGE == "en":
        return input("File Name: ")
    else:
        return input("File Name: ")

def fopen_s(__Filename:str) -> TextIO:
    try:
        __File = open(__Filename, "rt", encoding=ENCODE)
    except FileNotFoundError:
        PrintErrorMessage(FileNotFoundError, __Filename)

    try:
        for _ in __File: ...
    except UnicodeDecodeError as E:
        __File.close()
        PrintErrorMessage(UnicodeDecodeError, __Filename, E.encoding)

    __File.seek(0) # return cursor to 0

    return __File


def HasItems(obj, *args:str):
    "obj: must have method `__contains__`"
    for name in args:
        if (name not in obj):
            return False
    return True

def GetItems(obj, *args:str):
    """
    Parameters:
        obj: must have method `__contains__` and `__getitem__`.
        args: keys
    Returns:
        `obj[key]` first founded by `__contains__`.\n
        None if not founded.
    """
    for key in args:
        if (key in obj):
            return obj[key]
    return None

def ParseValue(value:str):
    if (RegEx.Dec.match(value)):
        return int(value)
    elif (RegEx.Hex.match(value)):
        return int(value, base=16)
    elif (RegEx.Bin.match(value)):
        return int(value, base=2)
    elif (RegEx.Bool.match(value)):
        return True if value == "True" else False
    else:
        return value


def DoRegex(pattern:str, string:str, function = re.findall):
    return function(pattern, string, re.DOTALL)

def ParseAttr(string:str) -> dict[str, str]:
    return {
        m["NAME"]:m["VALUE"]
        for m in RegEx.Attr.finditer(string)
        }

def ParseDefine(string:str) -> dict[str, str]:
    m = RegEx.Define.match(string)
    di = ParseAttr(m["ATTR"])
    di.update(_content=m["CONTENT"])
    return di

def RemoveLeftSpace(string:str) -> str:
    return RegEx.LeftSpace.match(string)[1]


def FileDispatch(content:str, mytype:str) -> str:
    ret = content
    for m in RegEx.FileDispatch.finditer(content):
        if (m["FTYPE"] == mytype):
            return m["CONTENT"]
        else:
            ret = ""
    return ret


def WriteMacro(s:str, identifier:str, content:str, mytype:str):
    return s.replace(identifier, FileDispatch(content, mytype))

def WriteTemplate(s:str, identifier:str, params:list[str], content:str, mytype:str):
    content = FileDispatch(content, mytype)
    for callee in re.finditer(f"%{identifier}"r"[\s\n\t]*\((.+?)\)%", s):
        # callee[0]: all call text
        # callee[1]: args
        args = [RemoveLeftSpace(arg) for arg in callee[1].split(",")]
        for i in range(len(args)):
            content = content.replace(params[i], args[i])
        s = s.replace(callee[0], content, 1)
    return s

def WriteDefine(s:str, attrs:dict[str,str], content:str, mytype:str):
    if ("macro" in attrs):
        return WriteMacro(s, f"%{attrs["macro"]}%", content, mytype)
    elif ("raw" in attrs):
        return WriteMacro(s, attrs["raw"], content, mytype)
    elif (HasItems("template", "args")):
        params = [RemoveLeftSpace(s) for s in attrs["args"].split(",")]
        return WriteTemplate(s, attrs["template"], params, content, mytype)
    else:
        return s


class SafeFile:
    __slots__ = {"_FName", "_Buffer", "_Encoding", "_FileExit"}

    def __init__(self, fileName:str, encoding:Optional[str]=None):
        self._FName = fileName
        self._Buffer = ""
        self._Encoding = encoding
        self._FileExit = False

    def __del__(self):
        self.flush()

    def write(self, text:str):
        self._Buffer += text

    def flush(self):
        if (not self._Buffer): return
        f = open(self._FName, "at" if self._FileExit else "wt", encoding=self._Encoding)
        f.write(self._Buffer)
        f.flush()
        f.close()
        self._FileExit = True
        self._Buffer = ""


class MetaWrite:
    @staticmethod
    def Title(__File:TextIO, __key:str, __ko:str, __jp:str):
        __text:str
        if (__jp):
            __text = f"""{__key}: {__ko} ({__jp})<br>"""
        else:
            __text = f"""{__key}: {__ko}<br>"""
        __File.write(__text)

    @staticmethod
    def Artist(__File:TextIO, __key:str, __ko:str, __jp:str):
        MetaWrite.Title(__File, __key, __ko, __jp)

    @staticmethod
    def YoutubeLink(__File:TextIO, __Desc:str, __ko:str, __jp:str):
        __key = __ko or __jp or "재생키 작성"
        if (__Desc != ""):
            __Desc = f"<br>{__Desc}"
        __File.write(f"""<div>{__Desc}<br><p><div class="yt_thum_box"><div class="yt_movie">\
<embed src="https://www.youtube.com/v/{__key}?version=3" type="application/x-shockwave-flash" width="560" height="315" allowfullscreen="true"></div>\
<a class="yt_link" href="https://youtu.be/{__key}" target="_blank">https://youtu.be/{__key}</a></div></p></div>""")

__all__ = [
    "printexit", "PrintErrorMessage", "NotMakeFile", "WrongPragma", "WrongMacro", "GetFileName", "fopen_s",
    "HasItems", "GetItems", "ParseValue",
    "DoRegex", "ParseAttr", "ParseDefine", "RemoveLeftSpace",
    "FileDispatch",
    "WriteMacro", "WriteTemplate", "WriteDefine",
    "SafeFile", "MetaWrite",
]
