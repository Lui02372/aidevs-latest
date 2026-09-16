# Lab 04 Solution Notes

## 리뷰 결과 예시

- token 값을 화면에 그대로 출력하고 있습니다.
- 상태 초기화 코드가 화면 코드와 섞여 있습니다.
- 로그 필터링 로직을 함수로 분리할 수 있습니다.
- 표 형태로 보여 주면 로그를 더 쉽게 읽을 수 있습니다.
- 필터 결과가 없을 때 안내 메시지가 없습니다.

## 수정 방향

1. `initialize_state()` 함수로 상태 초기화를 분리합니다.
2. `filter_logs(logs, status)` 함수로 필터링을 분리합니다.
3. token은 "로그인됨/로그아웃됨" 상태로만 표시합니다.
4. 로그는 `st.dataframe()`으로 표시합니다.
5. 결과가 없으면 `st.info()`로 안내합니다.

## 확인

```powershell
streamlit run .\90_ai-assisted-ui-review-and-debugging\10_labs\lab-04_ui-review-and-refactor\messy_dashboard.py
```

수정 후 화면이 더 읽기 쉬워지고, token 원문이 노출되지 않으면 성공입니다.
