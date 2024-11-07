import re

def SelfClosingTag(tag:str, hasattr:bool = True):
    if (hasattr):
        return re.compile(r"<"f"{tag}"r"[\s\n\t]+(?P<ATTR>.+?['\"])[\s\n\t]*/>", re.S)
    else:
        return re.compile(r"<"f"{tag}"r"[\s\n\t]*/>")

def NormalTag(tag:str, hasattr:bool = True):
    if (hasattr):
        return re.compile(r"<"f"{tag}"r"[\s\n\t]+(?P<ATTR>.+?)>(?P<CONTENT>.*?)</"f"{tag}"r"[\s\n\t]*>", re.S)
    else:
        return re.compile(r"<"f"{tag}"r"[\s\n\t]*>(?P<CONTENT>.*?)</"f"{tag}"r"[\s\n\t]*>", re.S)


Attr = re.compile(r"[\s\n\t]*(?P<NAME>.*?)[\s\n\t]*=[\s\n\t]*(?P<QUOTE>['\"])(?P<VALUE>.*?)(?P=QUOTE)", re.S)
LeftSpace = re.compile(r"[\s\n\t]*(.*)", re.S)
Define = re.compile(r"<define[\s\n\t]+(?P<ATTR>.+?['\"])[\s\n\t]*>(?P<CONTENT>.*?)</define[\s\n\t]*>", re.S)
Pragma = SelfClosingTag(r"pragma")
TimeBlock = SelfClosingTag(r"timeblock")
Lyrics = NormalTag(r"lyrics")

NewLine = re.compile(r"(?:\n[\s\t]*){2,}")
BreakTag = re.compile(r"[\s\n\t]+((?:</?[\s\n\t]*br[\s\n\t]*/?>)+)[\s\n\t]", re.I)

Bin = re.compile(r"^-?0b[01]+$", re.I)
Dec = re.compile(r"^-?\d+$", re.I)
Hex = re.compile(r"^-?0x[0-9a-f]+$", re.I)
Real = re.compile(r"^-?(?:\d*\.\d+|\d+\.\d*)$")
Bool = re.compile(r"^(?:True|False)$")

Time = re.compile(r"^(?:(?P<MIN>\d+)\:)?(?P<SEC>\d+)(?:\.(?P<MILLI>\d{1,3}))?")


SubtitlesLoop = re.compile(r"(?P<TIME><timeblock.*?/>)|(?P<LYRICS><lyrics.*?>.*?</lyrics[\s\n\t]*>)", re.S)
HtmlSubtitlesRemove = re.compile(r"<timeblock.*?/>|</?lyrics.*?>", re.S)


Lyric_JPK = re.compile(r"^\n*(?P<JP>.+?)<br>\n*(?P<PN>.+?)<br>\n*(?P<KR>.+?)(?:<br>)?\n*$")
Lyric_EK = re.compile(r"^\n*(?P<EN>.+?)<br>\n*(?P<KR>.+?)(?:<br>)?\n*$")


FileDispatch = re.compile(r"<(?P<FTYPE>html|subtitles)[\s\n\t]*>(?P<CONTENT>.*?)</(?P=FTYPE)[\s\n\t]*>", re.S)
