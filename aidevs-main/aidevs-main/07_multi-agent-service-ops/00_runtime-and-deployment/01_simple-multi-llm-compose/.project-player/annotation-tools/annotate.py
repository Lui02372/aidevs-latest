# Project Player 주석 삽입 도구. 앱을 import하거나 서비스를 호출하지 않는다.
from pathlib import Path
import ast
import datetime
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / '.project-player/annotation-baseline'
MANIFEST = json.loads((BASE / 'manifest.json').read_text(encoding='utf-8'))
SPECS = {
    'backend/app.py': {
        1: 'lru_cache는 아래 의존성 생성 함수의 결과를 재사용하여 요청마다 연결 객체를 새로 만들지 않게 한다.',
        2: 'Annotated는 타입에 의존성 정보를 붙이고, Literal은 허용할 문자열 목록을 제한한다.',
        4: 'FastAPI는 라우트를 등록하고 Depends는 필요한 객체를 공급하며 HTTPException은 HTTP 오류를 표현한다.',
        5: 'BaseModel과 Field로 요청 JSON의 필드 타입·길이·형식을 검증한다.',
        7: '실제 Redis·PostgreSQL·모델 통신은 services 모듈에 맡기고 이 파일은 요청 순서를 조율한다.',
        10: '이 app 객체를 Dockerfile의 uvicorn app:app이 가져와 HTTP 서버로 제공한다.',
        13: '메모 POST 요청의 입력 계약이다. 두 문자열은 필수이며 빈 문자열과 과도한 길이는 거부된다.',
        18: '채팅 POST 요청의 입력 계약이다. 검증에 실패하면 chat 함수 실행 전 422 응답이 발생한다.',
        19: '세션 식별자는 영문·숫자·밑줄·하이픈만 허용한다. 이것은 형식 검사이며 로그인 인증은 아니다.',
        21: 'provider는 셋 중 하나여야 한다. ollama_model을 생략하면 gemma를 선택한다.',
        25: '데코레이터는 바로 아래 함수를 감싼다. 인수가 없는 함수이므로 프로세스 안에서 같은 객체가 재사용된다.',
        30: 'DB 객체도 재사용하지만 실제 DB 연결은 Repository의 각 메서드에서 열고 닫는다.',
        35: '모델 서비스 객체의 생성만 캐시한다. 질문별 모델 응답을 캐시하는 기능은 아니다.',
        40: '라우트 매개변수에 이 타입 별칭을 쓰면 FastAPI가 Depends의 함수를 호출해 객체를 주입한다.',
        45: 'GET 경로와 함수를 연결한다. 이 경로는 저장소나 모델을 호출하지 않는 생존 확인이다.',
        50: '일반 상태 조회는 의존성을 검사하지만 상태가 나빠도 반환 자체의 HTTP 코드는 기본 200이다.',
        52: '먼저 실패를 기본값으로 두고, 실제 검사에 성공한 항목을 아래에서 갱신한다.',
        57: '딕셔너리 컴프리헨션으로 공급자별 설정 여부를 만든다. 키 존재·플래그 검사일 뿐 실제 모델 호출은 아니다.',
        59: 'errors에는 실패한 의존성만 담는다. 다른 의존성 검사를 계속하기 위해 각각 예외를 잡는다.',
        65: 'DB에 연결됐을 때만 앱 전용 테이블 존재 여부를 추가 검사한다.',
        70: '삼항 표현식으로 저장소와 스키마가 모두 준비되면 ok, 하나라도 아니면 degraded를 선택한다.',
        81: 'Compose의 healthcheck가 호출하는 준비 확인 경로다. 위 health의 결과를 HTTP 상태로도 전달한다.',
        85: 'raise는 정상 반환을 중단한다. HTTPException의 detail에 상세 검사 결과가 들어간다.',
        90: '검증된 payload를 받아 메모 생성 성공 시 201을 반환한다.',
        93: '영구 저장을 먼저 수행한다. 이 호출 실패 시 Redis 통계로 진행하지 않고 503을 반환한다.',
        95: 'from error는 원래 예외와 HTTP 오류의 연결을 보존해 원인 추적에 도움을 준다.',
        96: 'Redis가 실패해도 메모 저장은 이미 끝났으므로 null 기본값과 warning을 함께 반환할 수 있다.',
        105: '조회는 DB만 필요하다. Repository의 기본 제한으로 최신 메모를 최대 50개 돌려준다.',
        113: 'Redis 통계 전용 API이며 현재 화면에는 이 경로를 호출하는 버튼이 없다.',
        121: '대표 채팅 흐름: 설정 확인 → Redis 문맥 → DB 사용자 저장 → 모델 → DB 답변 → Redis 갱신.',
        123: '선택한 공급자가 설정되지 않았으면 저장과 모델 호출에 들어가기 전에 503으로 중단한다.',
        125: '아래 작업들은 순차 실행되지만 전체를 묶는 하나의 트랜잭션은 아니다. 중간 실패 때 앞선 DB 저장은 남는다.',
        126: '이전 대화 문맥은 Redis에서 읽는다. PostgreSQL의 전체 기록을 모델에 다시 전달하지 않는다.',
        128: '일반 동기 함수 호출이다. 작업 큐에 등록하거나 스트리밍하는 코드가 아니다.',
        132: '이름을 지정하는 키워드 인수로 Ollama의 하위 모델 선택을 서비스에 전달한다.',
        134: '답변을 영구 저장한 다음 두 메시지를 Redis에 함께 추가한다.',
        139: '채팅 처리가 끝난 뒤 전역 요청 횟수와 최근 요청을 갱신한다.',
        140: '저장소나 모델에서 예외가 나면 성공 JSON 대신 503을 돌려준다. 자동 대체 모델 호출은 없다.',
        142: '일반 dict가 JSON 응답이 된다. 별도 response_model은 없으며 fallback_used는 항상 False다.',
        152: '중괄호 부분은 URL 경로 인수다. 화면 기록은 Redis가 아닌 PostgreSQL에서 읽는다.',
        160: '새 대화 버튼이 이전 세션의 Redis 문맥만 지운다. DB의 영구 대화 기록은 삭제하지 않는다.',
    },
    'backend/services.py': {
        1: '타입 힌트의 평가를 미뤄 타입 이름을 함수 정의 시점에 즉시 계산하지 않게 한다.',
        3: 'json은 Redis에 저장할 문자열 변환, os는 프로세스 환경변수 읽기에 사용한다.',
        5: 'dataclass는 데이터 객체의 생성자를 만들고 Any는 DB 값처럼 여러 타입이 올 수 있음을 표시한다.',
        8: 'httpx는 Ollama HTTP 요청, psycopg는 PostgreSQL, redis는 Redis 서버 통신을 담당한다.',
        11: 'dict_row는 SQL 조회 결과를 열 이름으로 접근할 수 있는 딕셔너리 행으로 받게 한다.',
        14: 'frozen=True인 데이터 클래스는 생성 후 필드 재대입을 막는다. 공급자·모델·답변을 하나로 반환한다.',
        21: '객체는 Redis 클라이언트와 보존 시간 상태를 가진다. 영구 채팅 기록은 이 클래스의 책임이 아니다.',
        22: 'url은 생략 가능하다. None이면 환경변수 또는 기본 주소를 쓰며 TTL 기본값 1800초는 30분이다.',
        23: 'from_url로 접속 설정을 만들고 실제 명령 메서드에서 Redis와 통신한다.',
        25: 'decode_responses=True이면 Redis 바이트 응답을 Python 문자열로 받는다.',
        29: 'PING의 결과를 bool로 반환하여 /health의 상태 검사에 연결한다.',
        32: '요청 횟수는 세션별이 아닌 공용 키에 누적한다. incr와 set 두 명령을 하나의 트랜잭션으로 묶지는 않는다.',
        34: '최근 질문에만 TTL을 붙인다. 위 누적 횟수 키에는 이 코드에서 만료 시간을 설정하지 않는다.',
        37: '키가 없으면 get은 None을 반환할 수 있다. 횟수는 or 0으로 초기값을 정한 뒤 정수로 바꾼다.',
        43: '세션 ID를 키 이름에 넣어 대화를 구분하고 저장된 JSON 문자열 각각을 dict로 복원한다.',
        45: 'lrange의 0, -1은 처음부터 끝까지이며 리스트 컴프리헨션은 각 메시지에 같은 변환을 적용한다.',
        47: '입력은 role/content 딕셔너리들의 목록이며 반환값 없이 Redis에 반영한다.',
        49: '빈 목록일 때 RPUSH에 값 없이 요청하지 않도록 분기한다.',
        50: 'ensure_ascii=False는 한글을 그대로 JSON에 남긴다. *는 만든 목록을 RPUSH의 여러 인수로 펼친다.',
        51: '마지막 12개 메시지만 남기고 세션의 TTL을 갱신한다. 12개는 질문·답변 6쌍에 해당할 수 있다.',
        54: '현재 세션 키 하나만 삭제한다. 요청 통계와 PostgreSQL 기록은 여기서 다루지 않는다.',
        58: 'Repository는 라우트 대신 SQL과 연결 수명을 관리한다. 생성자는 접속 문자열만 보관한다.',
        60: '인수 → DATABASE_URL → 수업용 기본 주소 순서로 선택한다. 실제 환경값은 문서나 로그에 복사하지 않는다.',
        65: 'SELECT 1은 데이터 변경 없이 연결을 검사한다. fetchone 결과는 기본 설정에서 한 원소 튜플이다.',
        66: 'with가 연결과 커서를 정리한다. 연결 블록은 정상 종료 시 커밋, 예외 시 롤백 후 연결을 닫는다.',
        72: 'to_regclass로 두 테이블 이름이 존재하는지 검사한다. 열 타입·인덱스까지 검사하는 코드는 아니다.',
        80: '검증된 이름·메모를 받아 생성된 행을 반환한다. INSERT와 RETURNING을 한 SQL로 수행한다.',
        82: 'SQL의 %s와 값 튜플을 분리하여 드라이버가 매개변수를 처리하게 한다. 문자열 조립으로 값을 끼우지 않는다.',
        86: '행 하나를 일반 dict로 돌려주면 FastAPI가 날짜 등의 값을 JSON 표현으로 직렬화한다.',
        88: '기본 limit=50이며 id 내림차순으로 최신 메모를 조회한다.',
        92: '(limit,)의 쉼표는 한 원소 튜플을 뜻한다. 괄호만 쓰면 정수 그대로라 매개변수 묶음이 아니다.',
        94: 'fetchall의 각 행을 dict로 바꾸어 목록으로 반환한다. 결과가 없으면 빈 목록이다.',
        96: '질문 또는 답변 한 개를 독립 연결에서 저장한다. 두 번의 호출은 서로 다른 트랜잭션이다.',
        104: '세션별 기록을 id 오름차순으로 최대 100개 반환한다. 대화가 길어지면 가장 오래된 100개가 선택된다.',
        113: '여러 공급자를 지원하지만 요청마다 하나만 선택하는 서비스다. Multi-Agent 조율 객체는 없다.',
        116: '튜플 상수는 허용된 공급자 목록이며 상태 검사와 요청 처리 양쪽에서 재사용한다.',
        118: '환경변수의 존재나 플래그만 확인한다. API 키 유효성·모델 설치·네트워크 연결을 검증하지 않는다.',
        124: '문자열을 소문자로 맞춰 1/true/yes 중 하나인지 검사한다. 환경변수는 문자열로 전달된다.',
        127: '공급자와 Ollama 선택을 받아 실제 모델명을 고른다. 기본값은 코드 설정이며 현재 이용 가능성의 증거는 아니다.',
        128: '서비스를 API 밖에서 직접 호출해도 잘못된 Ollama 선택을 거부하도록 다시 검사한다.',
        133: '조건 표현식으로 gemma이면 GEMMA_MODEL, 아니면 OLLAMA_MODEL을 선택한다.',
        139: '사전에 없는 공급자는 명확한 ValueError를 내고, 정상일 때 모델 문자열 하나를 반환한다.',
        143: 'staticmethod는 self 없이 부를 수 있는 도우미다. 전달받은 값만으로 프롬프트 문자열을 만든다.',
        145: '제너레이터 표현식으로 마지막 6개 메시지를 한 줄씩 만들고 join으로 연결한다. Redis 보관 12개와 다르다.',
        148: '괄호 안의 인접 문자열은 하나로 이어진다. 안내문·최근 문맥·현재 질문을 단일 텍스트로 구성한다.',
        154: '입력은 공급자·질문·최근 대화·모델 선택이며 반환은 타입이 정해진 LLMReply 객체다.',
        161: '잘못된 공급자 또는 미설정 상태를 실제 외부 호출 전에 다시 막는다.',
        165: '공통 프롬프트와 모델명을 먼저 만든 뒤 공급자에 맞는 분기 하나만 실행한다.',
        168: '분기 안의 import는 해당 공급자를 선택할 때 SDK를 불러오는 지연 import다.',
        170: 'OpenAI SDK의 Responses API를 동기 호출하고 응답 객체의 output_text를 읽는다.',
        175: '지역 변수로 Gemini 클라이언트를 유지한 상태에서 generate_content를 호출한다. 명시적 close는 없다.',
        181: 'Ollama 기본 주소 끝의 /를 제거해 아래 경로를 붙일 때 //가 생기지 않게 한다.',
        182: 'Ollama는 SDK 대신 HTTP POST를 쓴다. 90초 timeout과 stream=False로 한 번에 JSON 답변을 받는다.',
        187: '실패 HTTP 상태이면 여기서 예외가 나서 JSON 내용 읽기로 진행하지 않는다.',
        189: '공급자 응답에 텍스트가 없으면 성공 객체를 만들지 않고 예외로 상위 라우트에 전달한다.',
        191: '공급자별 응답 형식을 공통 객체로 통일해 app.py가 동일한 필드로 처리하게 한다.',
    },
    'frontend/app.py': {
        1: '타입 힌트 평가를 미룬다. 이 파일은 JavaScript가 아니라 Streamlit 서버에서 실행되는 Python이다.',
        3: 'os는 Backend 주소 설정을, uuid4는 새 대화의 임의 식별자 생성을 담당한다.',
        6: 'httpx는 서버 사이 HTTP 통신, st라는 별칭의 streamlit은 화면과 사용자 입력을 담당한다.',
        10: 'BACKEND_URL을 프로세스 환경에서 읽는다. Compose에서는 backend 서비스 이름을 사용하는 주소가 전달된다.',
        13: '공통 API 함수는 HTTP 메서드·상대 경로·선택 JSON 본문을 받아 JSON 응답을 dict로 돌려준다.',
        14: '요청은 브라우저가 아닌 Streamlit 프로세스에서 동기 실행한다. 응답 대기 중 다음 Python 줄로 진행하지 않는다.',
        15: '오류 HTTP 응답은 예외로 바꾼다. 각 화면 블록의 except가 show_error로 연결한다.',
        19: 'HTTP 오류와 네트워크 등 기타 오류를 구분하여 화면 메시지를 만든다.',
        22: '오류 본문이 JSON이면 detail을 우선 사용하고 해당 키가 없으면 원문 텍스트를 쓴다.',
        23: 'JSON이 아닌 오류 응답도 있을 수 있어 디코딩 실패 시 텍스트로 처리한다.',
        28: 'st.error는 오류를, st.info는 사용자가 확인할 위치를 화면에 표시한다.',
        31: '페이지 설정·제목·설명은 스크립트가 실행될 때 화면 요소로 등록된다.',
        35: 'Streamlit은 입력 이벤트에 따라 스크립트를 재실행한다. session_state는 같은 화면 세션의 ID를 유지한다.',
        36: 'UUID의 16진 문자열 앞 8자를 사용한다. 이 ID는 로그인 사용자나 권한을 증명하지 않는다.',
        38: 'with st.sidebar 안에서 만든 위젯은 사이드바에 배치된다. with는 여기서 화면 배치 범위를 뜻한다.',
        39: 'selectbox 반환값이 선택 상태다. Ollama일 때만 두 번째 모델 선택 위젯을 만든다.',
        44: '현재 연결 주소와 세션 식별자를 보여 주어 어떤 대화에 요청하는지 확인하게 한다.',
        46: '버튼을 누른 실행에서만 삭제 요청을 보낸다. 성공 후 새 ID로 바꾸고 st.rerun으로 처음부터 다시 그린다.',
        51: '삭제 실패 시 ID 교체와 rerun에 도달하지 않고 오류 화면으로 이어진다.',
        54: '세 탭의 컨테이너를 튜플 언패킹한다. 이 코드의 기본 tabs 사용은 탭 본문을 선택한 탭만 지연 실행하지 않는다.',
        56: '대화 탭은 매 실행 시 DB 이력 API를 읽는다. 탭을 바꾸는 것과 명시적 API 버튼 조건은 구분한다.',
        59: '반복문으로 각 기록을 역할별 말풍선 안에 렌더링한다. 한 줄 with도 같은 블록 문법이다.',
        63: '입력 제출 시 prompt에 문자열이 생긴다. 값이 없으면 POST를 보내지 않는다.',
        66: 'Backend의 ChatRequest와 같은 네 필드로 JSON을 만든다. 모델은 화면에서 직접 호출하지 않는다.',
        72: '요청이 돌아온 뒤 답변과 실제 공급자·모델 정보를 표시한다. 별도 spinner나 토큰 스트리밍 코드는 없다.',
        75: '실패는 성공 말풍선으로 바꾸지 않고 공통 오류 화면으로 표시한다.',
        78: '메모 입력은 form으로 묶어 제출 시 처리한다. clear_on_submit은 제출 후 폼 입력값을 초기화한다.',
        80: '두 입력 위젯의 반환 문자열을 아래 POST JSON에 넣는다. 기존 예시 입력값은 그대로 유지한다.',
        83: '제출 이벤트가 참인 실행에서만 저장한다. 반환 JSON에는 Redis 경고가 포함될 수도 있다.',
        86: '조회 버튼은 별도 GET을 보내고 notes 목록을 표로 렌더링한다.',
        90: '상태 탭은 버튼을 눌렀을 때만 /health 결과를 표시한다. 주기적인 폴링 코드가 아니다.',
    },
    'backend/test_app.py': {
        1: 'TestClient는 실제 포트를 열지 않고 FastAPI 앱에 요청하는 테스트용 클라이언트다.',
        3: '라우트 앱과 의존성 생성 함수를 가져와 실제 저장소 대신 아래 가짜 객체로 바꾼다.',
        4: '가짜 모델도 실제 서비스와 같은 LLMReply 반환 계약을 사용한다.',
        7: 'Redis의 일부 동작을 메모리에서 흉내 낸다. 네트워크·TTL·Redis 장애까지 검사하는 구현은 아니다.',
        8: '각 객체의 상태로 횟수와 세션 사전을 저장한다.',
        12: '한 줄 메서드도 일반 함수다. 세미콜론은 같은 줄의 문장을 나누며 원래 코드를 그대로 유지한다.',
        15: '기록이 없으면 빈 목록을 복사해 반환한다. setdefault로 목록을 준비하고 extend로 여러 메시지를 추가한다.',
        17: 'pop의 기본값 None 덕분에 없는 세션 삭제도 예외를 내지 않는다.',
        20: '실제 SQL 대신 리스트를 사용하므로 DB 연결·SQL 문법·트랜잭션을 확인하는 테스트는 아니다.',
        22: '튜플 대입으로 서로 다른 빈 리스트를 notes와 messages에 각각 할당한다.',
        24: '상태 검사 두 개는 항상 참이다. 저장 메서드는 목록 길이로 ID를 만들고 같은 항목을 반환한다.',
        28: 'reversed와 슬라이스로 최신 메모부터 제한 개수만 반환한다.',
        29: '대화 메시지를 메모리 목록에 추가한 뒤 세션 ID로 필터링하여 조회한다.',
        34: '가짜 LLM은 외부 호출을 하지 않는다. 테스트용으로 Ollama만 미설정 상태를 흉내 낸다.',
        38: '조건 표현식과 f-string으로 공급자를 알아볼 수 있는 고정 응답을 만든다.',
        42: '파일 전체 테스트가 가짜 객체를 공유한다. 각 테스트마다 초기화하는 fixture는 없다.',
        43: 'dependency_overrides는 Depends가 호출할 함수를 교체한다. lambda는 값을 돌려주는 짧은 익명 함수다.',
        46: '오버라이드 설정 후 클라이언트를 만들므로 아래 요청은 메모리의 가짜 의존성을 사용한다.',
        49: '공급자별 설정 상태가 API 응답의 올바른 위치에 있는지 assert로 확인한다.',
        54: '채팅 성공 HTTP 코드·선택 공급자·대체 없음·질문과 답변 두 행 저장을 함께 확인한다.',
        64: '미설정 공급자를 선택하면 가짜 성공 대신 503과 공급자 이름을 반환하는지 확인한다.',
    },
    'init_database.py': {
        13: 'os는 환경변수, Path는 현재 파일을 기준으로 한 경로 계산에 사용한다.',
        16: 'psycopg는 DB 연결, load_dotenv는 실행 시 환경 파일을 읽는 도구다. 주석 검증에서는 이 스크립트를 실행하지 않는다.',
        20: '__file__의 절대 경로를 기준으로 계산하여 어느 작업 폴더에서 실행해도 같은 SQL을 찾는다.',
        21: '경로만 구성한다. 이 줄 자체가 환경 파일이나 SQL 파일을 읽는 것은 아니다.',
        23: '수업용 Host 접속 기본값이다. 실제 접속값은 아래 환경변수의 우선순위에 따라 선택된다.',
        28: '입력 인수가 없는 함수이며 Host에서 사용할 접속 문자열 하나를 반환한다.',
        29: '실제 초기화 실행 시에만 .env를 읽는다. 이 주석 작업에서는 파일 내용에 접근하지 않는다.',
        30: '명시적인 HOST_DATABASE_URL을 우선한다. strip은 양끝 공백을 제거한다.',
        34: '명시적인 Host URL이 없으면 Container용 URL의 호스트 이름을 바꾸고, 둘 다 없으면 기본값을 반환한다.',
        40: 'SQL 읽기와 DB 변경을 수행하는 관리 함수다. 일반 앱 요청마다 자동 호출되는 함수가 아니다.',
        41: 'UTF-8 SQL 파일 전체를 문자열로 읽어 아래 connection.execute에 전달한다.',
        45: 'with가 성공 시 커밋하고 예외 시 롤백·연결 정리를 한다. 초기화 오류를 숨기는 except는 없다.',
        47: '생성 후 정보 스키마에서 테이블 이름을 조회한다. 삼중 따옴표는 기존 SQL 문자열이므로 그대로 보존한다.',
        54: 'with가 정상 종료된 뒤 완료 메시지와 조회된 테이블 이름을 반복 출력한다.',
        56: '각 조회 행은 튜플이며 table[0]은 첫 번째 열인 테이블 이름이다.',
        59: '직접 실행할 때만 초기화한다. 다른 모듈이 import하면 이 조건 블록은 실행하지 않는다.',
    },
    'backend/requirements.txt': {
        1: 'FastAPI는 요청 검증과 라우팅을 담당한다. >=는 하한 포함, <는 상한 미포함이며 정확한 설치 버전 고정은 아니다.',
        2: 'Uvicorn은 Dockerfile에서 app:app을 실행하는 ASGI 서버다.',
        3: 'Redis 클라이언트는 세션 문맥과 요청 통계 명령을 보낸다.',
        4: 'Psycopg는 PostgreSQL 드라이버다. [binary]는 미리 빌드된 구성요소를 포함하는 선택 의존성이다.',
        5: 'google-genai는 Gemini 분기에서 지연 import하는 SDK다.',
        6: 'openai는 OpenAI 분기의 SDK이며 실제 키 값은 이 명세에 기록하지 않는다.',
        7: 'httpx는 Ollama HTTP 통신에 사용된다. pytest와 초기화 도구용 python-dotenv는 이 명세에 없다.',
    },
    'frontend/requirements.txt': {
        1: 'Streamlit은 Python으로 화면·폼·세션 상태를 구성한다. 버전 범위이며 실제 설치 버전은 별도 확인 대상이다.',
        2: 'httpx는 Streamlit 프로세스에서 Backend API에 동기 요청을 보낸다.',
    },
    'backend/Dockerfile': {
        1: 'Python 3.12와 최소 Linux 사용자 공간이 들어 있는 기본 이미지에서 시작한다.',
        2: '이후 COPY·RUN과 서버 프로세스의 작업 디렉터리를 /app으로 지정한다.',
        3: '빌드 문맥인 backend 폴더에서 의존성 명세를 먼저 복사한다.',
        4: '이미지 빌드 중 패키지를 설치한다. --no-cache-dir는 pip 다운로드 캐시를 이미지에 남기지 않는다.',
        5: '실행에 필요한 두 모듈만 복사한다. 테스트 파일과 루트 .env는 이 COPY에 포함되지 않는다.',
        6: '컨테이너 시작 명령이다. app:app은 app.py의 app 객체, 0.0.0.0은 모든 컨테이너 인터페이스, 8000은 내부 포트다.',
    },
    'frontend/Dockerfile': {
        1: 'Backend와 같은 Python 3.12 기반이지만 별도 이미지와 프로세스로 화면을 실행한다.',
        2: '컨테이너 안의 기준 작업 폴더를 /app으로 지정한다.',
        3: 'frontend 명세를 먼저 복사하여 코드만 바뀐 빌드에서 패키지 설치 계층을 재사용할 수 있게 한다.',
        4: '빌드 시 Streamlit과 httpx를 설치한다. 이번 주석 작업에서는 이 명령을 실행하지 않는다.',
        5: '화면 소스를 이미지에 복사한다. 소스 bind mount가 없어 Host 편집이 실행 중 이미지에 바로 반영되지는 않는다.',
        6: 'JSON 배열 형태 CMD는 Streamlit 서버를 시작한다. 내부 8501 포트의 Host 공개 번호는 Compose가 결정한다.',
    },
    'database/init.sql': {
        1: '앱 전용 이름 공간을 만든다. IF NOT EXISTS는 이미 존재할 때 생성을 건너뛴다.',
        3: '여행 메모 테이블이다. 기존 테이블의 구조를 자동 수정하는 migration은 아니다.',
        4: 'BIGSERIAL은 큰 정수 ID를 자동 부여하고 PRIMARY KEY는 행을 유일하게 식별한다.',
        5: '이름과 메시지 길이는 API NoteRequest의 제한과 대응하며 NOT NULL은 값 누락을 막는다.',
        7: '시간대가 있는 생성 시각을 DB의 NOW() 기본값으로 기록한다.',
        10: '채팅은 질문과 답변을 각각 한 행으로 저장하며 세션 ID로 묶는다.',
        12: '세션 문자열은 사용자 계정 외래 키가 아니다. 별도 사용자 테이블이나 소유권 검사는 없다.',
        13: 'CHECK 제약은 역할이 user 또는 assistant인 행만 허용한다.',
        14: 'TEXT는 대화 본문, created_at은 저장 시각이다. 모델명이나 공급자 열은 없다.',
        18: '세션 필터와 id 정렬 조회에 사용할 복합 인덱스를 만든다. 실제 사용 여부는 DB 실행 계획으로 별도 확인한다.',
    },
}

# 설정 공통 구문은 같은 의미를 유지하되 각 파일 가까이에 설명을 넣는다.
for name in ['compose.yml', 'compose.release.yml', 'compose.full-stack.yml']:
    rows = (BASE/name).read_text(encoding='utf-8').splitlines()
    spec = {}
    for i, row in enumerate(rows, 1):
        s = row.strip()
        if s.startswith('name:'): spec[i] = 'Compose 프로젝트 이름이다. 생성되는 리소스를 다른 프로젝트와 구분한다.'
        elif s == 'services:': spec[i] = '아래 키는 서비스 이름이다. 같은 Compose 네트워크에서 이름으로 서로 찾는다.'
        elif s.startswith('build:'): spec[i] = '이 상대 폴더를 빌드 문맥으로 사용하고 그 안의 Dockerfile을 읽는다.'
        elif s.startswith('REDIS_URL:'): spec[i] = 'Redis 접속 위치다. 기본·release는 Host 공용 서비스, full-stack은 내부 redis 서비스를 가리킨다.'
        elif s.startswith('DATABASE_URL:'): spec[i] = 'PostgreSQL 접속 설정이다. 변수명과 연결 위치만 설명하며 실제 자격 증명은 기록하지 않는다.'
        elif s.startswith('OPENAI_API_KEY:'): spec[i] = 'OPENAI_API_KEY는 인증, OPENAI_MODEL은 모델 선택이다. ${변수:-기본값}은 미설정 또는 빈 값일 때 기본값을 쓴다.'
        elif s.startswith('GEMINI_API_KEY:'): spec[i] = 'GEMINI_API_KEY와 GEMINI_MODEL은 Gemini 분기용이다. 설정 존재가 실제 API 성공을 뜻하지는 않는다.'
        elif s.startswith('OLLAMA_ENABLED:'): spec[i] = '활성 플래그·서버 주소·Llama/Gemma 모델명을 전달한다. 활성화만으로 모델 다운로드가 수행되지는 않는다.'
        elif s.startswith('BACKEND_URL:'): spec[i] = 'Streamlit 프로세스는 내부 서비스 이름 backend와 컨테이너 포트 8000으로 API를 호출한다.'
        elif s == '- "8000:8000"': spec[i] = '왼쪽은 Host 공개 포트, 오른쪽은 Backend 컨테이너 내부 포트다.'
        elif s == '- "80:8501"': spec[i] = '이 기본 구성의 화면 주소는 Host 80번이다. Streamlit 컨테이너는 내부 8501번에서 받는다.'
        elif s == '- "8501:8501"': spec[i] = 'Host 8501번 요청을 Streamlit 내부 8501번으로 전달한다.'
        elif s == 'extra_hosts:': spec[i] = '컨테이너에서 Host로 접근할 이름을 게이트웨이 주소에 매핑한다.'
        elif s == 'depends_on:': spec[i] = '시작 시 아래 의존 서비스의 healthcheck 성공을 기다린다. 이후 장애를 계속 복구해 주는 코드는 아니다.'
        elif s == 'healthcheck:': spec[i] = 'Docker가 아래 명령의 성공 여부로 컨테이너 건강 상태를 판정한다.'
        elif '/health/ready' in s: spec[i] = '컨테이너 자기 자신의 준비 API를 검사하며 Redis·DB·스키마까지 확인한다. 모델 생성은 호출하지 않는다.'
        elif s.startswith('interval:'): spec[i] = 'interval은 검사 간격, timeout은 한 검사 제한 시간, retries는 unhealthy 판정 전 연속 실패 횟수다.'
        elif s.startswith('start_period:'): spec[i] = '시작 초기의 실패를 재시도 횟수에 산입하지 않는 유예 시간이다.'
        elif s.startswith('restart:'): spec[i] = '프로세스 종료 후 재시작 정책이다. 사용자가 중지한 경우와 healthcheck 실패 자체는 구분한다.'
        elif s.startswith('image: ${'): spec[i] = '${변수:?메시지}는 이미지 변수가 없거나 비었을 때 구성 오류를 낸다. 이 파일은 소스를 빌드하지 않는다.'
        elif s == 'image: redis:7-alpine': spec[i] = 'Redis 7 계열 Alpine 이미지를 사용한다. backend와 같은 네트워크에서 내부 6379번으로 연결한다.'
        elif s.startswith('command:'): spec[i] = 'Redis 서버의 AOF 기록을 켜 저장 명령을 파일로 유지하게 한다.'
        elif s == '- redis_data:/data': spec[i] = '이름 있는 볼륨 redis_data를 데이터 폴더에 붙여 컨테이너 교체와 데이터를 분리한다.'
        elif s == 'test: ["CMD", "redis-cli", "ping"]': spec[i] = 'Redis의 PING 응답을 확인하는 명령이다.'
        elif s.startswith('image: postgres:'): spec[i] = 'PostgreSQL 17 계열 이미지를 사용한다. 이 구성은 DB 포트를 Host에 공개하지 않는다.'
        elif s.startswith('POSTGRES_USER:'): spec[i] = 'POSTGRES_USER·POSTGRES_PASSWORD·POSTGRES_DB는 새 DB 초기 생성 설정이다. 값은 문서에 복제하지 않는다.'
        elif s == '- postgres_data:/var/lib/postgresql/data': spec[i] = 'PostgreSQL 데이터를 이름 있는 볼륨에 보존한다.'
        elif '/docker-entrypoint-initdb.d/' in s: spec[i] = 'SQL 파일을 읽기 전용(ro)으로 연결한다. 이미지의 최초 빈 데이터 디렉터리 초기화 때 실행된다.'
        elif 'pg_isready' in s: spec[i] = 'CMD-SHELL로 DB 연결 수신 준비를 확인한다. 앱 테이블 존재 여부는 Backend가 별도 검사한다.'
        elif s.startswith('profiles:'): spec[i] = 'ollama 프로필을 선택했을 때만 이 서비스를 포함한다. Backend의 활성 플래그와는 별도 설정이다.'
        elif s == 'image: ollama/ollama:latest': spec[i] = 'Ollama 모델 서버 이미지다. latest는 고정 버전이 아니며 모델 파일은 별도로 준비한다.'
        elif s == '- ollama_data:/root/.ollama': spec[i] = '다운로드한 모델을 전용 볼륨에 보관한다. 이 서비스에는 healthcheck와 Host 포트 공개가 없다.'
        elif row == 'volumes:': spec[i] = '위 서비스에서 참조한 세 이름 있는 볼륨을 프로젝트 리소스로 선언한다.'
    SPECS[name] = spec

report = {'checked_at':datetime.datetime.now().astimezone().isoformat(), 'files':{}, 'incomplete':[]}
for name, spec in SPECS.items():
    path = ROOT/name
    original = (BASE/name).read_bytes()
    current = path.read_bytes()
    # 반복 실행 시 이전 도구가 생성한 결과와 같으면 덧붙이지 않는다.
    rows = original.decode('utf-8').splitlines(keepends=True)
    result = []
    for i, row in enumerate(rows, 1):
        if i in spec:
            indent = row[:len(row)-len(row.lstrip(' '))]
            prefix = '--' if name.endswith('.sql') else '#'
            ending = '\r\n' if row.endswith('\r\n') else '\n'
            result.append(f'{indent}{prefix} [학습] {spec[i]}{ending}')
        result.append(row)
    updated = ''.join(result).encode('utf-8')
    if current == updated:
        report['files'][name] = {'status':'already_annotated','comments':len(spec),'sha256':hashlib.sha256(current).hexdigest()}
        continue
    if hashlib.sha256(current).hexdigest() != MANIFEST['files'][name]['sha256']:
        report['incomplete'].append({'path':name,'reason':'기준 확보 이후 외부 변경 발견: 덮어쓰지 않음'})
        continue
    if name.endswith('.py'):
        assert ast.dump(ast.parse(original.decode('utf-8')), include_attributes=False) == ast.dump(ast.parse(updated.decode('utf-8')), include_attributes=False), name
    # 새 해설 줄만 제거했을 때 원본 바이트 전체가 같아야 한다.
    restored = b''.join(row for row in updated.splitlines(keepends=True) if not row.lstrip().startswith((b'# [', b'-- [')))
    assert restored == original, name
    assert path.read_bytes() == current, 'Concurrent change: '+name
    path.write_bytes(updated)
    report['files'][name] = {'status':'annotated','comments':len(spec),'sha256':hashlib.sha256(updated).hexdigest()}
out = ROOT/'.project-player/annotation-tools/annotation-result.json'
out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
