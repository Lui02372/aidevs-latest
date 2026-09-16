"""Supabase에 간단한 채팅 로그를 저장하는 최소 예제입니다.

이 파일의 목적:
    실제 LLM API를 호출하기 전에, "질문과 답변을 DB에 저장한다"는 흐름을
    가장 단순한 형태로 확인합니다.

    이 예제는 `simple_chat_logs` 테이블 1개만 사용합니다.
    복잡한 `conversations`, `messages`, `service_logs` 구조로 가기 전에
    한 행(row)에 질문/답변/상태를 저장하는 방식을 먼저 익힙니다.

    `simple_chat_logs`에는 user_id를 넣지 않습니다.
    아직 로그인 사용자 구분을 하지 않고, "질문/답변 저장"만 확인하는 최소 예제이기 때문입니다.
    사용자별 대화 이력은 Auth/JWT를 연결한 뒤 확장 구조에서 다룹니다.

실행 전 준비:
    1. C:/aidev/02_supabase-ai-backend/.env 파일에 아래 값이 있어야 합니다.
       - SUPABASE_URL
       - SUPABASE_SERVICE_ROLE_KEY

    2. Supabase Dashboard -> SQL Editor에서 아래 SQL을 실행합니다.

       create table if not exists simple_chat_logs (
         id uuid primary key default gen_random_uuid(),
         user_message text not null,
         assistant_message text,
         provider text not null default 'gemini',
         model text,
         status text not null default 'success',
         error_message text,
         created_at timestamp not null default now()
       );

실행:
    cd C:/aidev/02_supabase-ai-backend
    ./.venv/Scripts/Activate.ps1
    python ./03_supabase-db-and-auth/05_conversation-history-and-service-logs/01_insert_conversation_and_log.py

실행 결과:
    - simple_chat_logs 테이블에 샘플 질문/답변 로그가 1건 저장됩니다.
    - 최근 로그 목록을 다시 조회해서 터미널에 출력합니다.
    - 이 파일은 실제 Gemini API를 호출하지 않습니다.
"""

import os
from pathlib import Path
from pprint import pprint

from dotenv import load_dotenv
from supabase import Client, create_client


# 현재 파일은 아래 폴더 안에 있습니다.
# C:/aidev/02_supabase-ai-backend/03_supabase-db-and-auth/05_conversation-history-and-service-logs
#
# Path(__file__).resolve()는 현재 파이썬 파일의 전체 경로를 구합니다.
# parents[0] -> 05_conversation-history-and-service-logs
# parents[1] -> 03_supabase-db-and-auth
# parents[2] -> 02_supabase-ai-backend
#
# .env 파일은 02_supabase-ai-backend 폴더에 있으므로 parents[2]를 사용합니다.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(ENV_PATH)


def get_supabase() -> Client:
    """Supabase client를 생성합니다.

    이 예제는 백엔드 서버가 로그를 저장하는 상황을 가정합니다.
    그래서 공개용 `SUPABASE_ANON_KEY`가 아니라 서버 전용
    `SUPABASE_SERVICE_ROLE_KEY`를 사용합니다.

    주의:
    service role key는 RLS를 우회할 수 있는 강한 key입니다.
    프론트엔드 코드, README, GitHub에 절대 노출하면 안 됩니다.
    """

    url = os.getenv("SUPABASE_URL")
    service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not url:
        raise RuntimeError("SUPABASE_URL이 없습니다. .env 파일을 확인하세요.")
    if not service_role_key:
        raise RuntimeError("SUPABASE_SERVICE_ROLE_KEY가 없습니다. .env 파일을 확인하세요.")

    # create_client(url, key)는 Supabase에 요청을 보낼 수 있는 client 객체를 만듭니다.
    return create_client(url, service_role_key)


def insert_chat_log(
    supabase: Client,
    user_message: str,
    assistant_message: str,
    provider: str = "mock",
    model: str = "mock-model",
    status_value: str = "success",
    error_message: str | None = None,
) -> dict:
    """simple_chat_logs 테이블에 채팅 로그 1건을 저장합니다.

    저장하는 값:
    - user_message: 사용자가 입력한 질문
    - assistant_message: AI가 답했다고 가정한 메시지
    - provider: `mock`, `gemini` 같은 응답 생성 방식
    - model: 사용 모델 이름
    - status: 성공/실패 상태
    - error_message: 실패했을 때 남길 오류 메시지
    """

    # Supabase Python client의 기본 사용 흐름입니다.
    #
    # 1. table("simple_chat_logs")
    #    사용할 테이블을 선택합니다.
    #
    # 2. insert({...})
    #    저장할 컬럼과 값을 딕셔너리로 전달합니다.
    #
    # 3. execute()
    #    실제 요청을 Supabase로 보냅니다.
    result = (
        supabase.table("simple_chat_logs")
        .insert(
            {
                "user_message": user_message,
                "assistant_message": assistant_message,
                "provider": provider,
                "model": model,
                "status": status_value,
                "error_message": error_message,
            }
        )
        .execute()
    )

    # insert 결과는 리스트 형태로 돌아옵니다.
    # 여기서는 1건만 저장했으므로 첫 번째 행만 반환합니다.
    return result.data[0]


def list_recent_chat_logs(supabase: Client, limit: int = 5) -> list[dict]:
    """최근 채팅 로그를 조회합니다."""

    result = (
        supabase.table("simple_chat_logs")
        .select("*")  # 모든 컬럼을 조회합니다.
        .order("created_at", desc=True)  # 최신 로그가 먼저 나오도록 정렬합니다.
        .limit(limit)  # 너무 많은 데이터를 가져오지 않도록 개수를 제한합니다.
        .execute()
    )

    return result.data


def main() -> None:
    """샘플 질문/답변 로그를 저장하고 최근 로그를 조회합니다."""

    supabase = get_supabase()

    # 01 예제는 실제 LLM을 호출하지 않습니다.
    # 먼저 "질문과 답변을 로그 테이블에 저장한다"는 구조만 확인합니다.
    user_message = "Supabase에는 어떤 데이터를 저장하면 좋나요?"
    assistant_message = "나중에 다시 조회하거나 분석해야 하는 대화 이력과 서비스 로그를 저장하면 좋습니다."

    saved_log = insert_chat_log(
        supabase=supabase,
        user_message=user_message,
        assistant_message=assistant_message,
    )
    print("[chat log saved]")
    # pprint(saved_log, width=100)

    # print("\n[recent chat logs]")
    # pprint(list_recent_chat_logs(supabase), width=100)

    # print("\nResult: simple_chat_logs 테이블에 채팅 로그 저장 흐름을 확인했습니다.")


if __name__ == "__main__":
    main()
