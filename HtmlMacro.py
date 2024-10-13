from options import __dict__ as options
from options import *
from functions import *
import csv
import re
from math import ceil
from typing import Dict, List, Tuple
import RegEx
import Subtitles
import FileString


_FName = GetFileName()
_OriginFName = f"{_FName}.{KRFILE_EXTENSION}"
_TargetHTMLName = f"{_FName}.{COMPILED_EXTENSION}"

IFS = fopen_s(_OriginFName)
sfile = IFS.read()
IFS.close()


_YTInfoList:List[Tuple[str, str, str]] = []
_DefaultTag:Dict[str,str] = {}

while (pragma := RegEx.Pragma.search(sfile)):
    sfile = sfile.replace(pragma[0], "")
    attrs = ParseAttr(pragma["ATTR"])

    if (HasItems(attrs, "ytkey", "comment")):
        _YTInfoList.append((attrs["comment"], attrs["ytkey"], ""))

    elif (HasItems(attrs, "option", "value")):
        options[attrs["option"]] = ParseValue(attrs["value"])

    elif (HasItems(attrs, "tag", "value")):
        _DefaultTag[attrs["tag"]] = attrs["value"]

    else:
        WrongPragma("", pragma[0])


fstring = FileString.CreateFileString(sfile, options["MAKE_HTML"], options["MAKE_SUBTITLES"])
fstring.process_macro()

if options["MAKE_HTML"]:
    OFS = SafeFile(fileName=_TargetHTMLName, encoding=ENCODE)
    OFS.write("<div>")

# Write meta info
if options["MAKE_HTML"] and options["USE_META"]:
    _CsvFName = f"{_FName}.{METAFILE_EXTENSION}"
    CSV = fopen_s(_CsvFName)

    Reader = csv.DictReader(CSV)
    _Dict:Dict[str, Tuple[str, str]] = {}

    for row in Reader:
        _Dict.setdefault(row["Index"], (row["Kr"], row["Jp"]))

    BreakLine = lambda: OFS.write("<br>")

    OFS.write("<div>")

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
        _YTInfoList.insert(0, ("", *_Dict[META_ORDER[2]]))

    for _YtInfo in _YTInfoList:
        MetaWrite.YoutubeLink(OFS, *_YtInfo)

    OFS.write("</div>")
    for _ in range(3): BreakLine()

    CSV.close()


if (options["MAKE_SUBTITLES"]):
    if (options["SUBTITLES_EXTENSION"] == "srt"):
        SubFile = Subtitles.Srt_KoreanOnly if options["SUBTITLES_ONLY_KOREAN"] else Subtitles.Srt_AllLyrics
    elif (options["SUBTITLES_EXTENSION"] == "ass"):
        SubFile = Subtitles.Ass_KoreanOnly if options["SUBTITLES_ONLY_KOREAN"] else Subtitles.Ass_AllLyrics
    SubFile = SubFile(_FName + "." + options["SUBTITLES_EXTENSION"])

    Time = Subtitles.MHTMLTime(options["FPS"])
    pos = 0
    string:str = fstring.SubtitlesContent
    while (m := RegEx.SubtitlesLoop.search(string, pos)):
        pos = m.pos
        if (m["TIME"] is not None):
            m2 = RegEx.TimeBlock.match(m["TIME"])
            attrs = ParseAttr(m2["ATTR"])
            if (t := GetItems(attrs, "abs", "absolute")):
                Time << t
            if (t := GetItems(attrs, "rel", "relative")):
                Time += t

            string = string.replace(m2[0], "", 1)

        elif (m["LYRICS"] is not None):
            _tags = _DefaultTag.copy()
            _dur = Subtitles.SubTime()
            _dupcnt:int = 1
            _sepcnt:int = 1

            m2 = RegEx.Lyrics.match(m["LYRICS"])
            attrs = ParseAttr(m2["ATTR"])
            for key, val in attrs.items():
                if (key in ("dur", "duration")):
                    _dur = Time.strtotime(val)
                elif (key == "begin"):
                    Time << val
                elif (key == "rel"):
                    Time += val
                elif (key == "end"):
                    _dur = Time.strtotime(val) - Time.nowt
                elif (key in ("dup", "duplicate")):
                    _dupcnt = ParseValue(val)
                elif (key in ("sep", "separate")):
                    _sepcnt = ParseValue(val)
                else:
                    _tags[key] = val

            _dur_per_sep = _dur / _sepcnt
            _now_begin = Time.nowt
            _now_end = Time.nowt + _dur_per_sep
            for i in range(_sepcnt):
                for _ in range(_dupcnt):
                    SubFile.write(_now_begin, _now_end, m2["CONTENT"], **_tags)
                _now_begin = _now_end
                _now_end += _dur_per_sep

            if (options["LYRICS_TAG_TAKES_TIME"]):
                Time += _dur

            string = string.replace(m2[0], m2["CONTENT"], 1)


if (options["MAKE_HTML"]):
    sfile:str = RegEx.HtmlSubtitlesRemove.sub("", fstring.HTMLContent)

    # Remove by options
    if REMOVE_ANNOTATION:
        for annotation in DoRegex(r"<!--.*?-->", sfile):
            sfile = sfile.replace(annotation, '', 1)

    if REMOVE_NEWLINE:
        sfile = sfile.translate({ord("\n"):None})
    else:
        if COMPRESS_NEWLINE:
            sfile = RegEx.NewLine.sub("\n", sfile)
        if COMPRESS_BREAK:
            while (m := RegEx.BreakTag.search(sfile)):
                sfile = sfile.replace(m[0], f"{m[1]}\n")

    OFS.write(sfile)
    OFS.write("</div>")
    del OFS


printexit("Done")
