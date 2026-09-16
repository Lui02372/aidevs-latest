"""mock backend에서 사용할 메모리 저장소입니다.

이 파일의 딕셔너리와 리스트는 Python 프로세스 메모리에만 존재합니다.
따라서 서버를 재시작하면 회원, 로그인 세션, 대화 기록, 서비스 로그가 모두 초기화됩니다.
실제 서비스에서는 이 역할을 Supabase DB, Supabase Auth, Redis 등이 담당합니다.
"""

# email을 key로 사용하는 수업용 사용자 저장소입니다.
users: dict[str, dict] = {}

# access_token을 key로, 사용자 email을 value로 저장하는 수업용 로그인 세션 저장소입니다.
sessions: dict[str, str] = {}

# 챗봇 질문과 답변 기록을 저장하는 메모리 리스트입니다.
conversations: list[dict] = []

# 회원가입, 로그인, 채팅 같은 서비스 이벤트 로그를 저장하는 메모리 리스트입니다.
service_logs: list[dict] = []


def reset_store() -> None:
    """테스트에서 매번 깨끗한 상태로 시작하기 위해 모든 메모리 데이터를 비웁니다."""

    users.clear()
    sessions.clear()
    conversations.clear()
    service_logs.clear()
