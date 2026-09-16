"""Query Parameter 예제.

이 파일은 Query Parameter 개념을 나누어 읽고 실행해 보기 위한 학습용 파일입니다.

실행:
    cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\02_routing-and-request
    uvicorn 03_query-parameters:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn 03_query-parameters:app --reload

Query Parameter는 URL의 `?` 뒤에 붙는 검색 조건입니다.

예:
    /search?keyword=python&limit=5
"""

from fastapi import FastAPI, Query


# FastAPI 앱 객체입니다.
# uvicorn 실행 명령의 마지막 `:app`은 아래 변수 이름 `app`과 연결됩니다.
app = FastAPI(title="Query Parameter Practice")


# 검색 예제를 위한 임시 강의 목록입니다.
# 실제 서비스라면 이 데이터는 Supabase 같은 데이터베이스에서 조회합니다.
courses = [
    {"id": 1, "title": "Python Basic", "level": "beginner"},
    {"id": 2, "title": "FastAPI Backend", "level": "beginner"},
    {"id": 3, "title": "Supabase Integration", "level": "intermediate"},
    {"id": 4, "title": "LLM API Practice", "level": "intermediate"},
]


# Query Parameter는 URL의 `?` 뒤에 붙는 값입니다.
# 예: /search?keyword=python&level=beginner&limit=5
@app.get("/search")
def search_courses(
    # Query(default="")는 keyword가 없어도 빈 문자열로 처리하겠다는 뜻입니다.
    # description은 Swagger UI 문서에 표시됩니다.
    keyword: str = Query(default="", description="강의 제목에서 찾을 검색어"),
    # `str | None`은 문자열이거나 None일 수 있다는 뜻입니다.
    # level을 보내지 않으면 None이 되고, 보내면 해당 문자열로 들어옵니다.
    level: str | None = Query(default=None, description="beginner 또는 intermediate"),
    # ge=1은 1 이상, le=20은 20 이하만 허용한다는 검증 조건입니다.
    # limit=0이나 limit=100을 보내면 FastAPI가 422 오류를 반환합니다.
    limit: int = Query(default=10, ge=1, le=20, description="최대 반환 개수"),
):
    """검색 조건에 맞는 강의 목록을 반환합니다."""

    # 원본 courses를 바로 바꾸지 않고 result 변수에 담아 필터링합니다.
    result = courses

    if keyword:
        # keyword가 비어 있지 않을 때만 제목 검색을 적용합니다.
        # lower()를 사용해 대소문자 차이를 줄입니다.
        result = [
            course
            for course in result
            if keyword.lower() in course["title"].lower()
        ]

    if level:
        # level 값이 들어오면 해당 난이도와 같은 강의만 남깁니다.
        result = [course for course in result if course["level"] == level]

    # result[:limit]은 검색 결과 중 앞에서 limit개까지만 잘라 반환합니다.
    return {
        "keyword": keyword,
        "level": level,
        "limit": limit,
        "count": len(result[:limit]),
        "data": result[:limit],
    }
