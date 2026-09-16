# 03_charts-and-files

Streamlit에서 기본 차트를 출력하고 CSV 파일을 업로드하는 방법을 학습합니다.

차트와 파일 업로드는 이후 서비스 로그, 사용자 피드백, 대화 통계를 시각적으로 확인하는 데 사용됩니다. 이 폴더에서는 복잡한 시각화보다 “표 데이터를 차트로 바꿔 보는 흐름”에 집중합니다.

## 학습 목표

- DataFrame 데이터를 선 그래프와 막대 그래프로 표시할 수 있습니다.
- CSV 파일을 업로드하고 pandas로 읽을 수 있습니다.
- 업로드된 데이터의 컬럼을 확인할 수 있습니다.
- 선택한 컬럼을 기준으로 간단한 차트를 만들 수 있습니다.

## 예제 파일

```text
01_line-chart.py
02_bar-chart.py
03_csv-upload.py
04_csv-chart-viewer.py
sample_data/sample-service-logs.csv
```

## 실행 예시

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\02_streamlit-ui-components\03_charts-and-files\03_csv-upload.py
```

CSV 차트 뷰어를 실행한 뒤에는 예제 CSV 파일을 업로드해 봅니다.

```powershell
streamlit run .\02_streamlit-ui-components\03_charts-and-files\04_csv-chart-viewer.py
```

업로드할 예제 파일:

```text
02_streamlit-ui-components/03_charts-and-files/sample_data/sample-service-logs.csv
```

## 확인할 내용

- DataFrame 데이터를 차트로 표시할 수 있는가?
- CSV 파일 업로드 후 표로 볼 수 있는가?
- 업로드 데이터에서 컬럼을 선택해 차트를 만들 수 있는가?
- `requests`, `errors`, `avg_latency_ms` 같은 숫자 컬럼을 선택했을 때 차트가 바뀌는가?
- 파일이 업로드되지 않았을 때 안내 메시지가 표시되는가?

## 이후 과정과 연결

```text
서비스 로그 CSV
-> Streamlit 업로드
-> 표 확인
-> 차트로 추세 확인
```

04 미니 프로젝트와 이후 운영 과정에서는 로그와 피드백 데이터를 표와 차트로 확인하는 일이 많습니다.
