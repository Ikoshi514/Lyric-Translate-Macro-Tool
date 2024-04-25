# option: cp949, utf-8, utf-16, utf-16-le, utf-16-be
# 'utf-16' 및 'utf-16-le'은 동일
# '-'는 ' '(스페이스)로 대체 가능
ENCODE = "utf-8"

# option: en, kr
CLI_LANGUAGE = "kr"

# csv 테이블을 사용한 곡 정보 자동 작성 사용
USE_META = True
# [(곡명 정보), (아티스트 정보), (영상 재생 키)]
META_ORDER = [("곡명", "원곡"), ("서클", "작사", "편곡", "보컬", "일러스트"), "키"]

JPFILE_EXTENSION = "jp.txt"
KRFILE_EXTENSION = "kr.html"
METAFILE_EXTENSION = "meta.csv"
COMPILED_EXTENSION = "html"
