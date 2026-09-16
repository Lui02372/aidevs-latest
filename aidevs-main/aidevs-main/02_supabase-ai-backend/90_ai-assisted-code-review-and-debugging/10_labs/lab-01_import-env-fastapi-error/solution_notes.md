# Lab 01 Solution Notes

## 핵심 원인

이 예제는 먼저 `ModuleNotFoundError`가 발생합니다.

```text
from missing_demo_package import create_demo_message
```

존재하지 않는 패키지를 import하기 때문입니다. 이 단계에서는 `.env` 오류까지 도달하지 못합니다.

## 확인 순서

```powershell
python -c "import sys; print(sys.executable)"
python -m pip list
```

## 수정 방향

1. 존재하지 않는 import를 제거합니다.
2. `create_demo_message()`를 파일 안에 직접 만들거나 실제 설치 가능한 패키지로 바꿉니다.
3. 그 다음 `.env`의 `DEMO_API_KEY` 오류를 확인합니다.

## 좋은 프롬프트 포인트

- Traceback 전체를 붙입니다.
- 실제 API key는 붙이지 않습니다.
- "아직 수정하지 말고 원인부터"라고 요청합니다.
