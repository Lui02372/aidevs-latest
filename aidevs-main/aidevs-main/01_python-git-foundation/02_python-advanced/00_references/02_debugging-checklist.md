# Debugging Checklist

오류가 나면 코드를 바로 지우거나 다시 만들기 전에 아래 순서로 확인합니다.

```text
1. 현재 PowerShell 위치가 맞는가?
2. .venv가 활성화되어 있는가?
3. 실행 명령의 파일 경로가 맞는가?
4. 오류 메시지의 마지막 줄을 읽었는가?
5. 오류가 난 파일명과 줄 번호를 찾았는가?
6. NameError, TypeError, ValueError, FileNotFoundError 중 어떤 오류인가?
7. JSON 파일을 읽는 예제라면 파일 위치와 JSON 문법이 맞는가?
8. pytest 실패라면 expected와 actual 값을 비교했는가?
```

질문할 때는 아래 정보를 함께 적습니다.

```text
실행 위치:
실행 명령:
오류 메시지 마지막 줄:
오류가 난 파일과 줄 번호:
기대한 결과:
실제 결과:
```
