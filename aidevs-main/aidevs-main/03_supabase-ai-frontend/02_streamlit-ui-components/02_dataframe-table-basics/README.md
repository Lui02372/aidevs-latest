# 02_dataframe-table-basics

Streamlit에서 표를 보여주기 위해 필요한 pandas DataFrame 기초를 학습합니다.

이 과정에서 pandas는 데이터 분석을 깊게 배우기 위한 목적이 아니라, 화면에 표를 보여 주고 필터링 결과를 확인하기 위한 도구로 사용합니다. 이후 Supabase에서 조회한 대화 이력, 서비스 로그, 사용자 피드백 데이터를 화면에 표시할 때 같은 구조를 사용합니다.

## 학습 목표

- 리스트와 딕셔너리를 DataFrame으로 바꿀 수 있습니다.
- `st.dataframe`과 `st.table` 출력 차이를 설명할 수 있습니다.
- 조건에 맞는 행만 필터링할 수 있습니다.
- 합계와 평균을 계산해 화면에 표시할 수 있습니다.

## 예제 파일

```text
01_list-dict-to-dataframe.py
02_show-dataframe-table.py
03_filter-dataframe.py
04_simple-summary.py
```

## 실행 예시

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\02_streamlit-ui-components\02_dataframe-table-basics\01_list-dict-to-dataframe.py
```

## 확인할 내용

- 리스트와 딕셔너리를 DataFrame으로 바꿀 수 있는가?
- `st.dataframe`과 `st.table` 출력 차이를 볼 수 있는가?
- 조건에 맞는 행만 필터링할 수 있는가?
- 합계와 평균을 계산해 화면에 표시할 수 있는가?

## 이후 과정과 연결

```text
Supabase 조회 결과
-> 리스트/딕셔너리 형태
-> pandas DataFrame 변환
-> Streamlit 표와 차트로 표시
```

백엔드에서 받은 데이터를 화면에서 읽기 좋게 보여 주려면 DataFrame 형태에 익숙해지는 것이 좋습니다.
