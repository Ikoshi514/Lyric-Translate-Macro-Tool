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
# option: <br>, </br>, <br/>, </br/>
BREAK_TAG_STYLE = "<br>"

# csv 테이블을 사용한 곡 정보 자동 작성 사용
USE_META = True
# [(곡명 정보), (아티스트 정보), (영상 재생 키)]
META_ORDER = [("곡명", "원곡"), ("서클", "보컬", "편곡", "가사"), "키"]

JPFILE_EXTENSION = "jp.txt"
KRFILE_EXTENSION = "kr.html"
METAFILE_EXTENSION = "meta.csv"
COMPILED_EXTENSION = "html"
