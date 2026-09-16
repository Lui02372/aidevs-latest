"""리스트 컴프리헨션으로 데이터 목록을 필터링하고 변환하는 예제입니다."""

# API나 Supabase에서 조회한 결과를 흉내 낸 데이터입니다.
notes = [
    {"id": 1, "title": "Python 함수", "published": True},
    {"id": 2, "title": "예외 처리", "published": False},
    {"id": 3, "title": "FastAPI 기초", "published": True},
]

# published가 True인 노트만 고릅니다.
published_notes = [note for note in notes if note["published"]]

# 화면에 보여줄 제목만 뽑습니다.
published_titles = [note["title"] for note in published_notes]

# 결과를 출력합니다.
print("공개된 노트:", published_notes)
print("공개된 노트 제목:", published_titles)
