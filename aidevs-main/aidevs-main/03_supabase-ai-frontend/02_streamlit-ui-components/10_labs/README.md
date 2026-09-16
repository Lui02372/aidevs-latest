# 10_labs

수업 중 함께 진행하는 실습입니다.

이 실습은 버튼, 폼, 표, 차트, 파일 업로드를 작은 화면으로 묶어 보는 단계입니다. 예제 실행 후 입력값과 필터 조건을 바꾸면서 화면이 어떻게 달라지는지 확인합니다.

## 실습 목록

```text
lab-01-survey-form.py
lab-02-dataframe-filter.py
lab-03-csv-dashboard.py
```

## 실행 예시

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\02_streamlit-ui-components\10_labs\lab-01-survey-form.py
```

## 실습별 목표

| 실습 | 목표 |
| --- | --- |
| `lab-01-survey-form.py` | 폼을 사용해 여러 입력값을 한 번에 제출하고 결과를 표시합니다. |
| `lab-02-dataframe-filter.py` | DataFrame 데이터를 필터링하고 결과 표를 표시합니다. |
| `lab-03-csv-dashboard.py` | CSV 업로드, 표 확인, 차트 표시를 하나의 화면으로 구성합니다. |

## 실습 기준

- 예제 코드를 먼저 실행합니다.
- 입력값을 바꾸며 화면 변화를 확인합니다.
- 표와 차트에 사용되는 데이터 구조를 설명합니다.
- 요구사항에 맞게 직접 코드를 수정합니다.
- 필터와 결과가 같은 데이터를 기준으로 연결되어 있는지 확인합니다.

## 완료 기준

- Streamlit 앱이 오류 없이 실행됩니다.
- 입력 또는 업로드 값에 따라 화면 결과가 바뀝니다.
- DataFrame의 컬럼 이름과 필터 조건을 설명할 수 있습니다.
- 최소 한 줄 이상 직접 수정한 뒤 화면 변화를 확인합니다.
