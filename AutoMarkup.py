from options import *
from functions import *
from pronunciations import hira_kata_gana
import re


_FName = GetFileName()
_OriginFName = f"{_FName}.{JPFILE_EXTENSION}"
_TargetFName = f"{_FName}.{KRFILE_EXTENSION}"

IFS = fopen_s(_OriginFName)

sfile = IFS.read()

IFS.close()
OFS = open(_TargetFName, "wt", encoding=ENCODE)

OFS.write("""<define raw="　"> </define>
""")


if (m := re.match(r"^<setoptions[\s\n\t]+(.+?)>$", sfile, re.S | re.M)):
    sfile = sfile.replace(f"{m[0]}\n", "")
    for key,val in ParseAttr(m[1]).items():
        globals()[key] = ParseValue(val)


OFS.write(f"""<pragma option="MAKE_SUBTITLES" value="{MAKE_SUBTITLES}"/>
<pragma option="SUBTITLES_EXTENSION" value="ass"/>
""")

if MAKE_SUBTITLES:
    def write(jp:str, pn:str,/):
        if (pn.isascii()):
            OFS.write(f"<lyrics end=\"\">\n{jp}<br>\n(KR)\n</lyrics><br><br>\n")
        else:
            OFS.write(f"<lyrics end=\"\">\n{jp}<br>\n{pn}<br>\n(KR)\n</lyrics><br><br>\n")
else:
    def write(jp:str, pn:str,/):
        if (pn.isascii()):
            OFS.write(f"{jp}<br>\n(KR)\n<br><br>\n")
        else:
            OFS.write(f"{jp}<br>\n{pn}<br>\n(KR)\n<br><br>\n")



for text in sfile.splitlines():
    text = text.rstrip("\n")
    if text == "":
        OFS.write("<br>\n")
        continue

    write(text, text.translate(hira_kata_gana))

OFS.close()

printexit("Done")
