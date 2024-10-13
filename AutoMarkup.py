from options import *
from functions import *
from pronunciations import hira_kata_gana


_FName = GetFileName()
_OriginFName = f"{_FName}.{JPFILE_EXTENSION}"
_TargetFName = f"{_FName}.{KRFILE_EXTENSION}"

IFS = fopen_s(_OriginFName)
OFS = open(_TargetFName, "wt", encoding=ENCODE)

OFS.write("""<define raw="　"> </define>
""")


if MAKE_SUBTITLES:
    def write(jp:str, pn:str = "",/):
        if (pn):
            OFS.write(f"<lyrics end=\"\">\n{jp}<br>\n{pn}<br>\n(KR)\n</lyrics><br><br>\n")
        else:
            OFS.write(f"<lyrics end=\"\">\n{jp}<br>\n(KR)\n</lyrics><br><br>\n")
else:
    def write(jp:str, pn:str = "",/):
        if (pn):
            OFS.write(f"{jp}<br>\n{pn}<br>\n(KR)\n<br><br>\n")
        else:
            OFS.write(f"{jp}<br>\n(KR)\n<br><br>\n")



for text in IFS:
    text = text.rstrip("\n")
    if text == "":
        OFS.write("<br>\n")
        continue

    temp = text
    for i in range(32, 127):
        temp = temp.replace(chr(i), "")

    write(text, temp.translate(hira_kata_gana))

IFS.close()
OFS.close()

printexit("Done")
