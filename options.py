# option: cp949, utf-8, utf-16, utf-16-le, utf-16-be
# 'utf-16' 및 'utf-16-le'은 동일
# '-'는 ' '(스페이스)로 대체 가능
ENCODE = "utf-8"

# option: en, kr
CLI_LANGUAGE = "kr"

# 작성한 주석을 삭제할 것인지에 대한 유무
# <!-- -->
REMOVE_ANNOTATION = True

# 모든 개행을 제거할 것인지에 대한 유무
REMOVE_NEWLINE = False

# 아무 내용도 없는 개행을 압축할 것인지에 대한 유무
# REMOVE_NEWLINE이 True면 무시됨
COMPRESS_NEWLINE = True

# <br> 태그만 있는 줄을 압축할 것인지에 대한 유무
# REMOVE_NEWLINE이 True면 무시됨
COMPRESS_BREAK = True

# csv 테이블을 사용한 곡 정보 자동 작성 사용
USE_META = True
# [(곡명 정보), (아티스트 정보), (영상 재생 키)]
# [tuple[str,...], tuple[str,...], str|None|Unbound]
META_ORDER = [("곡명", "원곡"), ("서클", "보컬", "편곡", "작사", "기타", "일러스트", "영상"), "키"]

# 역자 태그 리스트
TAGS:list[str] = []


# HtmlMacro를 통해서 .html 파일을 만들지 여부
MAKE_HTML = True
# HtmlMacro를 통해서 자막 파일을 만들지 여부
MAKE_SUBTITLES = True

# 영상의 초당 프레임 수
FPS = 30

# lyrics 태그로 시간이 지날지 여부
LYRICS_TAG_TAKES_TIME = True


JPFILE_EXTENSION = "jp.txt"
KRFILE_EXTENSION = "kr.html"
METAFILE_EXTENSION = "meta.csv"
COMPILED_EXTENSION = "html"


# option: srt, ass
SUBTITLES_EXTENSION = "srt"

# 자막에 한국어만 출력할지 여부
SUBTITLES_ONLY_KOREAN = True
