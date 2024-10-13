import abc
from collections.abc import Iterable
from typing import Optional, Union, NoReturn, overload
from typing_extensions import deprecated
from datetime import time
from functions import ParseValue
import RegEx


class SubTime:
    __slots__ = ("_Minute", "_Second", "_Millisecond")

    def __init__(self, minute:int=0, second:int=0, millisecond:int=0) -> None:
        if (millisecond >= 1000 or millisecond < 0):
            second += millisecond // 1000
            millisecond %= 1000

        if (second >= 60 or second < 0):
            minute += second // 60
            second %= 60

        self._Minute = minute
        self._Second = second
        self._Millisecond = millisecond

    @property
    def minute(self):
        return self._Minute

    @property
    def second(self):
        return self._Second

    @property
    def millisecond(self):
        return self._Millisecond

    def __add__(self, other:"SubTime"):
        return SubTime(self._Minute + other._Minute, self._Second + other._Second, self._Millisecond + other._Millisecond)

    def __iadd__(self, other:"SubTime"):
        return self + other

    def __sub__(self, other:"SubTime"):
        return SubTime(self._Minute - other._Minute, self._Second - other._Second, self._Millisecond - other._Millisecond)

    def __isub__(self, other:"SubTime"):
        return self - other

    @overload
    def __mul__(self, other:int) -> "SubTime": ...
    @overload
    def __mul__(self, other:"SubTime") -> "SubTime": ...

    def __mul__(self, other:"Union[int,SubTime]"):
        if (type(other) is SubTime):
            val = other.to_millisecond()
        elif (type(other) is int):
            val = other
        else:
            raise TypeError(f"Wrong type `{type(other)}`")
        return SubTime(millisecond=int(self.to_millisecond() * val))

    @overload
    def __truediv__(self, other:int) -> "SubTime": ...
    @overload
    def __truediv__(self, other:"SubTime") -> "SubTime": ...

    def __truediv__(self, other:"Union[int,SubTime]"):
        if (type(other) is SubTime):
            val = other.to_millisecond()
        elif (type(other) is int):
            val = other
        else:
            raise TypeError(f"Wrong type `{type(other)}`")
        return SubTime(millisecond=int(self.to_millisecond() / val))

    @overload
    def __itruediv__(self, other:int) -> "SubTime": ...
    @overload
    def __itruediv__(self, other:"SubTime") -> "SubTime": ...

    def __itruediv__(self, other:"Union[int,SubTime]"):
        return self / other

    def to_second(self):
        return self._Minute * 60 + self._Second

    def to_millisecond(self):
        return self.to_second() * 1000 + self._Millisecond

    def to_srt(self):
        return "00:{:02}:{:02}.{:03}".format(self._Minute, self._Second, self._Millisecond)

    def to_ass(self):
        return "0:{:02}:{:02}.{:03}".format(self._Minute, self._Second, self._Millisecond)[:-1]


def _str_milli_to_int_milli(s:str) -> int:
    return int(s) * (10 ** (3 - len(s)))

class MHTMLTime:
    __slots__ = {"_FrameRate", "_TimePerFrame", "_NowTime"}

    def __init__(self, frameRate:int, nowTime:SubTime=SubTime()):
        self._FrameRate = frameRate
        self._TimePerFrame = 1/frameRate
        self._NowTime = nowTime

    def copy(self):
        return MHTMLTime(self._FrameRate, self._NowTime)

    def strtotime(self, s:str) -> Union[SubTime,NoReturn]:
        if (type(s) is str):
            if (len(s) == 0):
                return 0
            elif (s[-1] == "f"):
                SubTime(millisecond=ParseValue(s[:-1]) * self._TimePerFrame)
            else:
                t = None
                if (s[-1] == "t"):
                    t = RegEx.Time.match(s[:-1])
                else:
                    t = RegEx.Time.match(s)
                if (t is None):
                    raise ValueError(f"Can't parse `{s}`.")
                _min = t["MIN"]
                _sec = t["SEC"]
                _milli = t["MILLI"]
                return SubTime(
                    minute=0 if _min is None else int(_min),
                    second=int(_sec),
                    millisecond=0 if _milli is None else _str_milli_to_int_milli(_milli)
                )
        else:
            raise TypeError(f"Wrong type `{type(s)}`.")

    @overload
    def __add__(self, rel:str) -> "MHTMLTime": ...
    @overload
    def __add__(self, rel:SubTime) -> "MHTMLTime": ...

    def __add__(self, rel:Union[SubTime,str]):
        return MHTMLTime(self._FrameRate, self._NowTime + (rel if type(rel) is SubTime else self.strtotime(rel)))

    @overload
    def __iadd__(self, rel:str) -> "MHTMLTime": ...
    @overload
    def __iadd__(self, rel:SubTime) -> "MHTMLTime": ...

    def __iadd__(self, rel:Union[SubTime,str]):
        if (type(rel) is SubTime):
            self._NowTime += rel
        else:
            self._NowTime += self.strtotime(rel)
        return self

    @overload
    def __lshift__(self, t:SubTime) -> None: ...
    @overload
    def __lshift__(self, t:str) -> None: ...

    def __lshift__(self, t:Union[SubTime,str]):
        self._NowTime = t if (type(t) is SubTime) else self.strtotime(t)

    @property
    def nowt(self):
        return self._NowTime


class ISubtitlesFile(metaclass=abc.ABCMeta):
    __slots__ = set()

    @abc.abstractmethod
    def __init__(self, fname:Optional[str]=...): ...

    @abc.abstractmethod
    def open(self, fname:str) -> bool: ...

    @abc.abstractmethod
    def close(self,): ...

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    @abc.abstractmethod
    def writable(self) -> bool: ...

    def __bool__(self):
        return self.writable()

    @abc.abstractmethod
    def write(self, begin:SubTime, end:SubTime, string:str, **kwargs:str): ...


class SubtitlesFile(ISubtitlesFile):
    __slots__ = {"_File"}

    def __init__(self, fname:Optional[str]=...):
        if (type(fname) is str):
            self.open(fname)

    def open(self, fname:str):
        self._File = open(fname, "wt", encoding="UTF-8")
        return bool(self)

    def close(self):
        self._File.close()

    def writable(self) -> bool:
        return hasattr(self, "_File") and self._File.writable()



class SrtFile(SubtitlesFile):
    __slots__ = {"_Count"}

    def open(self, fname:str):
        self._Count = 1
        return super().open(fname)

    def write(self, begin:SubTime, end:SubTime, string:str, **kwargs):
        self._File.write(f"{self._Count}\n{begin.to_srt()} --> {end.to_srt()}\n{string}\n\n")
        self._Count += 1


class AssFile(SubtitlesFile):
    __slots__ = set()

    def open(self, fname:str):
        ret = super().open(fname)
        if (ret):
            self._File.write("""[Script Info]
; Script generated by Aegisub 9706-cibuilds-20caaabc0
; http://www.aegisub.org/
Title: Default Aegisub file
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1920
PlayResY: 1080

[Aegisub Project Garbage]

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold\
, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,5,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""")

    def write(self, begin: SubTime, end: SubTime, string: str, **kwargs:str):
        if (len(kwargs)):
            attrs = "{"
            for name, value in kwargs.items():
                attrs += f"\\{name}({value})"
            attrs += "}"
            string = attrs + string
        self._File.write(f"Dialogue: 0,{begin.to_ass()},{end.to_ass()},Default,,0,0,0,,{string}\n")


def CreateAllLyricsClass(base:type, join):
    class _AllLyricsClass(base):
        __slots__ = set()

        def write(self, begin:SubTime, end:SubTime, string:str, **kwargs):
            if (m := RegEx.Lyric_JPK.match(string)):
                string = self._Join((m["JP"], m["PN"], m["KR"]))
            elif (m := RegEx.Lyric_EK.match(string)):
                string = self._Join((m["JP"], m["EN"]))
            super().write(begin, end, string, **kwargs)

    _AllLyricsClass._Join = join
    return _AllLyricsClass


def CreateKoreanOnlyClass(base:type):
    class _KoreanOnlyClass(base):
        __slots__ = set()

        def write(self, begin:SubTime, end:SubTime, string:str, **kwargs):
            m = RegEx.Lyric_JPK.match(string)
            if (not m):
                m = RegEx.Lyric_EK.match(string)
            super().write(begin, end, m["KR"] if m is not None else string, **kwargs)

    return _KoreanOnlyClass

Srt_AllLyrics = CreateAllLyricsClass(SrtFile, lambda x: "\n".join(x))
Ass_AllLyrics = CreateAllLyricsClass(AssFile, lambda x: "\\N".join(x))

Srt_KoreanOnly = CreateKoreanOnlyClass(SrtFile)
Ass_KoreanOnly = CreateKoreanOnlyClass(AssFile)
