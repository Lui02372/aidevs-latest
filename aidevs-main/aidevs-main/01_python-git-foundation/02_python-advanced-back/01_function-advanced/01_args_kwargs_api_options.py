"""*args와 **kwargs를 API 옵션 전달 관점에서 이해하는 예제입니다."""


def build_search_query(keyword: str, *tags: str, **options: str) -> dict[str, object]:
    """검색어, 태그, 옵션을 하나의 검색 조건으로 정리합니다."""

    # keyword는 반드시 필요한 기본 검색어입니다.
    # *tags는 태그를 여러 개 받을 수 있게 합니다.
    # **options는 정렬, 페이지, 제한 개수 같은 선택 옵션을 dict로 받습니다.
    query = {
        "keyword": keyword,
        "tags": list(tags),
        "options": options,
    }

    # 정리된 검색 조건을 반환합니다.
    return query


# "FastAPI"는 기본 검색어입니다.
# "python", "backend"는 *tags로 들어갑니다.
# sort, limit은 **options로 들어갑니다.
search_query = build_search_query(
    "FastAPI",
    "python",
    "backend",
    sort="latest",
    limit="10",
)

# 실제 API 호출 전에 검색 조건을 dict로 정리하는 흐름을 확인합니다.
print("검색 조건:", search_query)
