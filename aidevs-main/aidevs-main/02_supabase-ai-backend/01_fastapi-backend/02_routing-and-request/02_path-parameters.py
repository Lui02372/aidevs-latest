"""Path Parameter 예제.

이 파일은 Path Parameter 개념을 나누어 읽고 실행해 보기 위한 학습용 파일입니다.

실행:
    cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\02_routing-and-request
    uvicorn 02_path-parameters:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn 02_path-parameters:app --reload

Path Parameter는 URL 경로 안에 들어가는 값입니다.

예:
    /users/1
    /courses/python

위 URL에서 `1`, `python` 같은 값이 path parameter입니다.
"""

from fastapi import FastAPI, HTTPException


# FastAPI 앱 객체입니다.
# uvicorn 실행 명령의 마지막 `:app`은 아래 변수 이름 `app`과 연결됩니다.
app = FastAPI(title="Path Parameter Practice")


# 예제를 단순하게 만들기 위해 데이터베이스 대신 dict를 사용합니다.
# key는 사용자 id이고, value는 사용자 정보입니다.
users = {
    1: {"id": 1, "name": "Alice", "role": "student"},
    2: {"id": 2, "name": "Bob", "role": "mentor"},
}


# URL의 {user_id} 부분이 함수 인자 user_id로 들어옵니다.
# 예: /users/1 요청 -> user_id 값은 1
@app.get("/users/{user_id}")
def get_user(user_id: int):
    """사용자 id로 한 명의 사용자를 조회합니다."""

    # 함수 인자에 int 타입을 붙였기 때문에 FastAPI가 문자열 "1"을 숫자 1로 바꿔 줍니다.
    # 숫자로 바꿀 수 없는 값이 들어오면 FastAPI가 자동으로 422 오류를 반환합니다.
    if user_id not in users:
        # Path Parameter 형식은 맞지만 해당 id의 데이터가 없으면 404가 자연스럽습니다.
        raise HTTPException(status_code=404, detail="User not found")

    return {"data": users[user_id]}


# Path Parameter는 하나만 받을 수 있는 것이 아닙니다.
# 아래 API는 course_slug와 lesson_no 두 값을 URL 경로에서 받습니다.
# 예: /courses/python/lessons/3
@app.get("/courses/{course_slug}/lessons/{lesson_no}")
def get_lesson(course_slug: str, lesson_no: int):
    """경로 안에서 여러 개의 값을 받을 수도 있습니다."""

    # course_slug는 문자열로 받고, lesson_no는 int로 받습니다.
    # FastAPI는 함수의 타입 힌트를 보고 값을 자동 변환하고 검증합니다.
    return {
        "course": course_slug,
        "lesson_no": lesson_no,
        "message": f"{course_slug} course lesson {lesson_no}",
    }
