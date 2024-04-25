from options import *
from typing import NoReturn, TextIO

def WrapQuote(text:str) -> str:
    return f"\"{text}\""

def PrintErrorMessage(errortype:type, *args:str) -> NoReturn:
    if errortype is FileNotFoundError:
        if CLI_LANGUAGE == "kr":
            input(f"파일 {WrapQuote(args[0])}를 찾을 수 없습니다.")
        elif CLI_LANGUAGE == "en":
            input(f"File {WrapQuote(args[0])} is not found.")
        else:
            input(f"File {WrapQuote(args[0])} is not found.")

    elif errortype is UnicodeDecodeError:
        if CLI_LANGUAGE == "kr":
            input(f"""파일 {WrapQuote(args[0])}의 인코드가 {WrapQuote(args[1])}와는 다릅니다.\
 대상 파일의 인코드를 변경하거나, 소스 코드의 {WrapQuote("ENCODE")} 변수의 값을 변경해주세요.""")
        elif CLI_LANGUAGE == "en":
            input(f"""File {WrapQuote(args[0])} is not encoded by {WrapQuote(args[1])}.\
 Change encode of target file, of change source code's const variable {WrapQuote("ENCODE")}.""")
        else:
            input(f"""File {WrapQuote(args[0])} is not encoded by {WrapQuote(args[1])}.\
 Change encode of target file, of change source code's const variable {WrapQuote("ENCODE")}.""")

    exit()

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
    def YoutubeLink(__File:TextIO, __ko:str, __jp:str):
        __key = __ko or __jp or "재생키 작성"
        __File.write(f"""<br><p><div class="yt_thum_box"><div class="yt_movie">\
<embed src="https://www.youtube.com/v/{__key}?version=3" type="application/x-shockwave-flash" width="560" height="315" allowfullscreen="true"></div>\
<a class="yt_link" href="https://youtu.be/{__key}" target="_blank">https://youtu.be/{__key}</a></div></p>""")

__all__ = ["PrintErrorMessage", "WrongMacro", "GetFileName", "fopen_s"]
