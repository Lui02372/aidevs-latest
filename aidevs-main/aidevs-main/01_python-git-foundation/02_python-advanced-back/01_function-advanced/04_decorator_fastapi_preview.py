"""FastAPI의 라우터 문법을 이해하기 위한 데코레이터 기초 예제입니다."""


def route(path: str):
    """경로를 받아 함수를 감싸는 간단한 데코레이터입니다."""

    # 실제 FastAPI의 @app.get("/path")와 모양이 비슷한 구조입니다.
    def decorator(original_function):
        def wrapper():
            print(f"[ROUTE] {path} 요청을 처리합니다.")
            return original_function()

        return wrapper

    return decorator


@route("/health")
def health_check() -> dict[str, str]:
    """서비스 상태 확인 결과를 반환합니다."""

    return {"status": "ok"}


# health_check를 호출하면 데코레이터가 먼저 실행됩니다.
result = health_check()
print("응답:", result)
