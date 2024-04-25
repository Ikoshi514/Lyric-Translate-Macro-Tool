from options import *
from functions import *
from functions import MetaWrite
import csv
from typing import Dict, Tuple
from types import LambdaType


_FName = GetFileName()
_OriginFName = f"{_FName}.{KRFILE_EXTENSION}"
_TargetFName = f"{_FName}.{COMPILED_EXTENSION}"

IFS = fopen_s(_OriginFName)
OFS = open(_TargetFName, "wt", encoding=ENCODE)

if USE_META:
    _CsvFName = f"{_FName}.{METAFILE_EXTENSION}"
    CSV = fopen_s(_CsvFName)

    Reader = csv.DictReader(CSV)
    _Dict:Dict[str, Tuple[str, str]] = {}

    for row in Reader:
        _Dict.setdefault(row["Index"], (row["Kr"], row["Jp"]))

    BreakLine = lambda: OFS.write("<br>")

    for k in META_ORDER[0]:
        if _Dict.get(k) == None:
            continue
        MetaWrite.Title(OFS, k, *_Dict[k])
    BreakLine()
    for k in META_ORDER[1]:
        if _Dict.get(k) == None:
            continue
        MetaWrite.Artist(OFS, k, *_Dict[k])
    if _Dict.get(META_ORDER[2]) != None:
        MetaWrite.YoutubeLink(OFS, *_Dict[META_ORDER[2]])

    for _ in range(3): BreakLine()

    CSV.close()


Defines:Dict[str, str] = dict()
_Macro:str
_ChangeTo:str
_MacroCreating = False

def __Clear():
    global _Macro, _ChangeTo, _MacroCreating, Defines
    _ChangeTo = _ChangeTo.replace("\n", "")
    _ChangeTo = _ChangeTo.rsplit("</define>")[0]
    for macro in Defines.items():
        _ChangeTo = _ChangeTo.replace(*macro)
    Defines.setdefault(_Macro, _ChangeTo)
    _Macro = ""
    _ChangeTo = ""
    _MacroCreating = False

for text in IFS:
    try:
        if (_MacroCreating):
            _ChangeTo += text
            if ("</define>" in _ChangeTo):
                __Clear()
            continue

        # <define macro="foo">bar</macro>
        if ("<define " in text):
            __macropos:int
            __namming:LambdaType
            __stringpair:str
            if ("macro=" in text):
                __macropos = text.find("macro=") + 7
                __stringpair = text[__macropos - 1]
                __namming = lambda s: f"%{s}%"
            elif ("raw=" in text):
                __macropos = text.find("raw=") + 5
                __stringpair = text[__macropos - 1]
                __namming = lambda s: s
            else:
                raise
            __macroend = text.find(__stringpair, __macropos)
            _Macro = __namming(text[__macropos:__macroend])
            _ChangeTopos = text.find(">", __macroend) + 1
            _ChangeTo = text[_ChangeTopos:]
            if ("</define>" in _ChangeTo):
                __Clear()
                continue
            else:
                _MacroCreating = True
                continue

        for macro in Defines.items():
            text = text.replace(*macro)
        OFS.write(text)
    except:
        WrongMacro(text)

IFS.close()
OFS.close()

input("Done")
