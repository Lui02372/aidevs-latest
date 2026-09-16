# Lab 04. UI 리뷰와 리팩토링

이 실습은 실행은 되지만 읽기 어렵고 사용자 경험이 부족한 Streamlit 코드를 AI와 함께 리뷰하고 개선하는 연습입니다.

## 실행

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\90_ai-assisted-ui-review-and-debugging\10_labs\lab-04_ui-review-and-refactor\messy_dashboard.py
```

## 해야 할 일

1. 화면을 직접 실행해 불편한 점을 적습니다.
2. Codex에게 UI 리뷰를 요청합니다.
3. 기능 추가보다 구조 정리, 이름 개선, 오류 처리, 빈 상태 표시를 먼저 반영합니다.
4. 수정 전후를 `solution_notes.md` 형식으로 기록합니다.

## Codex 요청 예시

```text
이 Streamlit 대시보드 코드를 리뷰해주세요.

리뷰 관점:
1. 화면 구조가 사용자가 이해하기 쉬운가?
2. session_state 초기화가 한 곳에 모여 있는가?
3. token 같은 민감한 값이 화면에 과하게 노출되지 않는가?
4. 함수로 나누면 좋은 부분은 어디인가?
5. 빈 상태와 오류 상태가 충분히 보이는가?

아직 코드는 수정하지 말고 우선순위가 높은 문제부터 알려주세요.
```
