"""
[Database 초기화 시나리오]
기본 compose.yml은 이미 실행 중인 공용 PostgreSQL을 사용하므로 PostgreSQL Container의
`docker-entrypoint-initdb.d`가 실행되지 않습니다. 그 결과 Backend가 사용하는 Table이
없을 수 있습니다. 이 프로그램은 `database/init.sql`을 공용 PostgreSQL에 직접 실행하여
`simple_multi_llm` 전용 Schema와 Table을 준비합니다.

기존 Schema나 데이터를 삭제하지 않으며 `CREATE ... IF NOT EXISTS`만 실행합니다.
연결·인증·SQL 오류는 성공으로 숨기지 않습니다. `.env`에 HOST_DATABASE_URL이 없으면
Container용 DATABASE_URL의 `host.docker.internal`을 Host용 `127.0.0.1`로 바꿉니다.
"""

# [학습] os는 환경변수, Path는 현재 파일을 기준으로 한 경로 계산에 사용한다.
import os
from pathlib import Path

# [학습] psycopg는 DB 연결, load_dotenv는 실행 시 환경 파일을 읽는 도구다. 주석 검증에서는 이 스크립트를 실행하지 않는다.
import psycopg
from dotenv import load_dotenv


# [학습] __file__의 절대 경로를 기준으로 계산하여 어느 작업 폴더에서 실행해도 같은 SQL을 찾는다.
ROOT = Path(__file__).resolve().parent
# [학습] 경로만 구성한다. 이 줄 자체가 환경 파일이나 SQL 파일을 읽는 것은 아니다.
ENV_PATH = ROOT / ".env"
SQL_PATH = ROOT / "database" / "init.sql"
# [학습] 수업용 Host 접속 기본값이다. 실제 접속값은 아래 환경변수의 우선순위에 따라 선택된다.
DEFAULT_HOST_DATABASE_URL = (
    "postgresql://agent_user:agent_pwd@127.0.0.1:5433/agent_db"
)


# [학습] 입력 인수가 없는 함수이며 Host에서 사용할 접속 문자열 하나를 반환한다.
def host_database_url() -> str:
    # [학습] 실제 초기화 실행 시에만 .env를 읽는다. 이 주석 작업에서는 파일 내용에 접근하지 않는다.
    load_dotenv(ENV_PATH)
    # [학습] 명시적인 HOST_DATABASE_URL을 우선한다. strip은 양끝 공백을 제거한다.
    explicit_host_url = os.getenv("HOST_DATABASE_URL", "").strip()
    if explicit_host_url:
        return explicit_host_url

    # [학습] 명시적인 Host URL이 없으면 Container용 URL의 호스트 이름을 바꾸고, 둘 다 없으면 기본값을 반환한다.
    container_url = os.getenv("DATABASE_URL", "").strip()
    if container_url:
        return container_url.replace("host.docker.internal", "127.0.0.1")
    return DEFAULT_HOST_DATABASE_URL


# [학습] SQL 읽기와 DB 변경을 수행하는 관리 함수다. 일반 앱 요청마다 자동 호출되는 함수가 아니다.
def initialize_database() -> None:
    # [학습] UTF-8 SQL 파일 전체를 문자열로 읽어 아래 connection.execute에 전달한다.
    sql = SQL_PATH.read_text(encoding="utf-8")
    print(f"실행할 SQL: {SQL_PATH}")
    print("공용 PostgreSQL에 simple_multi_llm Schema를 준비합니다.")

    # [학습] with가 성공 시 커밋하고 예외 시 롤백·연결 정리를 한다. 초기화 오류를 숨기는 except는 없다.
    with psycopg.connect(host_database_url()) as connection:
        connection.execute(sql)
        # [학습] 생성 후 정보 스키마에서 테이블 이름을 조회한다. 삼중 따옴표는 기존 SQL 문자열이므로 그대로 보존한다.
        tables = connection.execute(
            """SELECT table_name
               FROM information_schema.tables
               WHERE table_schema = 'simple_multi_llm'
               ORDER BY table_name"""
        ).fetchall()

    # [학습] with가 정상 종료된 뒤 완료 메시지와 조회된 테이블 이름을 반복 출력한다.
    print("Database 초기화가 완료되었습니다.")
    for table in tables:
        # [학습] 각 조회 행은 튜플이며 table[0]은 첫 번째 열인 테이블 이름이다.
        print(f"- simple_multi_llm.{table[0]}")


# [학습] 직접 실행할 때만 초기화한다. 다른 모듈이 import하면 이 조건 블록은 실행하지 않는다.
if __name__ == "__main__":
    initialize_database()
