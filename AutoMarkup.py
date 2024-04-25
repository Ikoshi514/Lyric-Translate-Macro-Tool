from options import *
from functions import *


_FName = GetFileName()
_OriginFName = f"{_FName}.{JPFILE_EXTENSION}"
_TargetFName = f"{_FName}.{KRFILE_EXTENSION}"

IFS = fopen_s(_OriginFName)
OFS = open(_TargetFName, "wt", encoding=ENCODE)

for text in IFS:
    text = text.rstrip("\n")
    if text == "":
        OFS.write("<br>\n")
        continue

    temp = text
    for i in range(32, 127):
        temp = temp.replace(chr(i), "")

    if temp == "":
        OFS.write(f"{text}<br>\n(KR)<br>\n<br>\n")
    else:
        OFS.write(f"{text}<br>\n(PR)<br>\n(KR)<br>\n<br>\n")

IFS.close()
OFS.close()

input("Done")
