from options import *
from functions import *
import csv
import re
from typing import Dict, List, Tuple


_FName = GetFileName()
_OriginFName = f"{_FName}.{KRFILE_EXTENSION}"
_TargetFName = f"{_FName}.{COMPILED_EXTENSION}"

IFS = fopen_s(_OriginFName)
OFS = open(_TargetFName, "wt", encoding=ENCODE)
sfile = IFS.read()
IFS.close()


# Write meta info
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


# Handle macro/raw
while (info := DoRegex(
    r".*?(<define[\s\n]+(macro|raw)[\s\n]*=[\s\n]*['\"](.+?)['\"][\s\n]*>(.*?)</define[\s\n]*>)",
    sfile,
    re.match
    )):
    # info[0]: garbage
    # info[1]: all define text
    # info[2]: define type
    # info[3]: macro indentifier
    # info[4]: macro content
    sfile = sfile.replace(info[1], "", 1)
    if (info[2] == "macro"):
        sfile = sfile.replace(f"%{info[3]}%", info[4])
    elif (info[2] == "raw"):
        sfile = sfile.replace(info[3], info[4])

# Handle template
while (info := DoRegex(
    r".*?(<define[\s\n]+template[\s\n]*=[\s\n]*['\"](.+?)['\"][\s\n]*args[\s\n]*=[\s\n]*['\"](.+?)['\"][\s\n]*>(.*?)</define[\s\n]*>)",
    sfile,
    re.match
    )):
    # info[0]: garbage
    # info[1]: all define text
    # info[2]: template indentifier
    # info[3]: template args
    # info[4]: template content
    info:List[str]
    sfile = sfile.replace(info[1], "", 1)
    params = [RemoveLeftSpace(s) for s in info[3].split(",")]

    for callee in re.findall(rf"(%{info[2]}[\s\n]*\((.+?)\)%)", sfile):
        # callee[0]: all call text
        # callee[1]: args
        callee:List[str]
        args = [RemoveLeftSpace(s) for s in callee[1].split(",")]
        new = info[4]
        for i in range(len(args)):
            new = new.replace(params[i], args[i])
        sfile = sfile.replace(callee[0], new, 1)


# Remove by options
if REMOVE_ANNOTATION:
    for annotation in DoRegex(r"<!--.+?-->", sfile):
        sfile = sfile.replace(annotation, '', 1)

if REMOVE_NEWLINE:
    sfile = sfile.replace("\n", "")
else:
    if COMPRESS_NEWLINE:
        while(sfile.find("\n\n") != -1):
            sfile = sfile.replace("\n\n", "\n")
    if COMPRESS_BREAK:
        for brline in re.findall(f"(\n({BREAK_TAG_STYLE})+\n)", sfile):
            sfile = sfile.replace(brline[0], brline[0].lstrip("\n"))


OFS.write(sfile)
OFS.close()

input("Done")
