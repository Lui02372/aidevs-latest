# Lab 01. Streamlit 실행 오류 분석

이 실습은 Streamlit 앱이 실행 중 바로 멈추는 상황을 AI와 함께 분석하는 연습입니다.

## 실행

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\90_ai-assisted-ui-review-and-debugging\10_labs\lab-01_streamlit-run-error\broken_app.py
```

## 해야 할 일

1. 오류 메시지를 그대로 복사하지 말고, 파일 경로와 실행 명령을 함께 정리합니다.
2. Codex에게 먼저 원인 분석을 요청합니다.
3. 제안받은 원인 중 실제 코드와 맞는 부분을 확인합니다.
4. 코드를 수정한 뒤 다시 실행합니다.
5. 수정 전후 내용을 `solution_notes.md` 형식으로 기록합니다.

## Codex 요청 예시

```text
아래 Streamlit 실행 오류를 분석해주세요.

파일:
C:\aidev\03_supabase-ai-frontend\90_ai-assisted-ui-review-and-debugging\10_labs\lab-01_streamlit-run-error\broken_app.py

실행 명령:
streamlit run .\90_ai-assisted-ui-review-and-debugging\10_labs\lab-01_streamlit-run-error\broken_app.py

기대 결과:
제목과 버튼이 표시되어야 합니다.

실제 결과:
앱 실행 중 NameError가 발생합니다.

요청:
아직 코드를 수정하지 말고 가능한 원인과 확인 순서를 초보자 기준으로 설명해주세요.
```
