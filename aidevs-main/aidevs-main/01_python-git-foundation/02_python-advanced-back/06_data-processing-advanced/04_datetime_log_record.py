"""datetime으로 로그 생성 시각을 기록하는 예제입니다."""

from datetime import datetime, timezone

# 현재 UTC 시간을 가져옵니다.
# 서비스 로그나 DB 저장 시각은 UTC 기준으로 기록하면 비교하기 쉽습니다.
now_utc = datetime.now(timezone.utc)

# isoformat은 날짜/시간을 표준 문자열 형태로 바꿉니다.
created_at = now_utc.isoformat(timespec="seconds")

# 로그 한 건을 dict로 만듭니다.
log_record = {
    "event_type": "chat.request",
    "message": "사용자 질문을 받았습니다.",
    "created_at": created_at,
}

print("로그 기록:", log_record)
print("생성 시각:", log_record["created_at"])
