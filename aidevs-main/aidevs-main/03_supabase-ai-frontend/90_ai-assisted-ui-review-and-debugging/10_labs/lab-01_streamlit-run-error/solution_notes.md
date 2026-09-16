# Lab 01 Solution Notes

## 원인

`streamlit as st`를 import하기 전에 `st.title()`을 먼저 호출해서 `NameError`가 발생합니다.

## 수정 방향

`import streamlit as st`를 파일 상단으로 옮긴 뒤 `st.title()`, `st.write()`, `st.button()`을 호출합니다.

## 확인

```powershell
streamlit run .\90_ai-assisted-ui-review-and-debugging\10_labs\lab-01_streamlit-run-error\broken_app.py
```

수정 후 제목, 설명 문장, 버튼이 화면에 표시되면 성공입니다.
