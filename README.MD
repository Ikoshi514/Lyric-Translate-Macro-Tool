Python을 이용한 일본어에서 한국어로 노래 가사를 번역할 때 쓸만한 툴.
디씨인사이드에 글 작성할 때, HTML로 작성하기가 존재하는데, 해당 기능을 사용하기 편하게 하기 위해서 만들었음.




requirements
Python
추정: (version >= 3.5)
설치한 인터프리터가 3.7, 3.11, 3.12 뿐이기 때문에, 이외의 버전에서는 테스트해보지 않음. Type Annotation을 사용하였기 때문에, (version < 3.5) 환경에서는 확실히 작동하지 않음.




# 문법


## HTML


### <define> 태그
속성으로 갖는 것에 따라 어떤 방식으로 사용할지 결정됨.

- macro
%로 둘러싸인 매크로로 변경됨.
e.g.) <define macro="후랑도루">플랑드르</define>
위의 매크로는 '%후랑도루%후랑도루'를 '플랑드르후랑도루'로 변경해줌.

- raw
그대로 매크로가 됨.
e.g.) <define raw="꺼이싷">코이시</define>
위의 매크로는 '%꺼이싷%꺼이싷'을 '%코이시%코이시'로 변경해줌.


#### version 2 추가 사항
- template
args 속성이 함께 있어야 됨.
%로 둘러싸여있으며, 템플릿 뒤에 괄호로 인수를 넘겨야 됨.
e.g.) <define template="스칼렛" args="이름, 영어">스칼렛 자매! 이름 스칼렛 (영어 Scarlet)</define>
위의 템플릿은
'%스칼렛(플랑드르, Flandre)%
%스칼렛(레밀리아, Remilia)%'
을
'스칼렛 자매! 플랑드르 스칼렛 (Flandre Scarlet)
스칼렛 자매! 레밀리아 스칼렛 (Remilia Scarlet)'
으로 변경해줌.


#### version 3 추가 예정
- <pragma/>
속성으로 갖는 건 ytkey 정도 생각해둠.
<pragma ytkey="DzxZQdCmi78" comment="유튜브 주소"/>
위와 같이 적으면, meta.csv 파일에서 제공하는 유튜브 주소 위치 아래에 pragma ytkey를 사용한 순서대로 추가로 임베드 시켜주는 거임.
comment는 임베드 되는 주소 위에 적을 코멘트.
대략적으로 아래와 같이 임베드 시켜줄 듯.

유튜브 주소
https://www.youtube.com/watch?v=DzxZQdCmi78


### 문법 검사 관련
version 2에서 문법 검사를 더욱 느슨하게 진행하도록 변경됨.
사실 상
<define     template
=     "코메이지'      args='   NAME
,    EN">
%코메이지
     (
        코이시,       Koishi
)%
처럼 적어놔도 적당히 받아주는데, 이러면 가독성 문제로 사용자가 불편할 것이기에 추천하지 않음.


### 내부 구현 설명
version 1에서는 줄 단위로 문자열을 전부 헤집도록 구현되어있었음.
version 2에서 파일 전체를 정규 표현식을 통해 읽어내도록 구현 변경.
v1 만들 때는 정규 표현식을 몰랐었음... 세상에 이렇게 편한 것이었을 줄이야.


## CSV

options.py에서 USE_META가 True일 때 분석함.

첫 번째 열은 Index, Kr, Jp로 구성되어 있어야 되며, 순서는 상관 없음.

Index에는 어떤 정보인지 적어야 됨. Kr과 Jp는 보이는 대로. Jp는 생략해도 되지만, Kr은 적지 않으면 아예 내용이 날아갈 수 있음.
e.g.) 원곡,소녀 사토리 ~3rd eye,少女さとり ~ 3rd eye
해당 내용은 '원곡: 소녀 사토리 ~3rd eye (少女さとり ~ 3rd eye)'로 출력됨.
e.g.) 원곡,풍신소녀,
해당 내용은 Jp를 생략했기 때문에, '원곡: 풍신소녀'로 출력됨.

나머지는 Index는 동일하게 동작하기에 생략하고, "키"라는 Index가 특수함.
유튜브의 재생키를 의미하며, 유튜브 링크 https://www.youtube.com/watch?v=DzxZQdCmi78 와 같은 경우, ?v= 뒤의 값인 "DzxZQdCmi78"이 Key값임.
"키"의 경우, Kr과 Jp 중 어느 쪽에 써도 적용되며, 유튜브 링크를 알아서 임베드 시켜줌.


기타
---
제작 동기, 이미지를 포함한 설명은 이하 주소로.
v1 기준으로 작성하였기 때문에 설명이 다를 수 있음.
https://gall.dcinside.com/mgallery/board/view/?id=teamshanghaialice&no=962530

예제는 본 리포지토리의 [example/ 디렉토리][EGDIR]로.


버전 로그
---
# version 1
2024/04/26
txt 파일에 줄바꿈마다 <br> 태그를 자동 작성하는 기능 제공.
<define> 태그와 macro, raw 속성 제공.
csv에 메타 정보를 기입하면 매크로 변환과 함께 곡 정보를 적는 기능 제공.

# version 2
<define> 태그에 template 속성 및 함께 사용하는 args 속성 제공.
문법 검사를 느슨하게 변경.
options.py에 추가 옵션 제공. 자세한 내용은 [해당 파일][OPTIONS_DIR] 내의 주석 참조.

# version 3(예정)
<pragma/> 태그 제공.


[EGDIR]: https://github.com/Ikoshi514/Lyric-Translate-Macro-Tool/tree/main/example
[OPTIONS_DIR]: https://github.com/Ikoshi514/Lyric-Translate-Macro-Tool/blob/main/options.py