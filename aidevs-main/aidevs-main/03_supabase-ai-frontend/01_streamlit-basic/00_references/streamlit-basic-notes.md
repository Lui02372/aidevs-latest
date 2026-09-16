# Streamlit Basic Notes

## Streamlit 핵심 개념

Streamlit은 Python 코드로 웹 화면을 빠르게 만들 수 있는 프레임워크입니다.

일반적인 웹 개발에서는 HTML, CSS, JavaScript를 따로 작성하는 경우가 많습니다. 하지만 Streamlit은 Python 코드 안에서 `st.title`, `st.write`, `st.text_input` 같은 함수를 호출하면 바로 웹 화면을 만들어 줍니다. 그래서 데이터 분석, 챗봇 화면, 관리자용 대시보드처럼 빠르게 확인해야 하는 화면을 만들 때 유용합니다.

기본 실행 명령은 다음과 같습니다.

```powershell
streamlit run app.py
```

이 과정에서는 `03_supabase-ai-frontend` 폴더의 `.venv`를 활성화한 뒤 실행합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\01_streamlit-basic\01_streamlit-project-setup\01_hello-streamlit.py
```

## `print`와 `st.write`의 차이

Python 기초에서 사용한 `print()`는 터미널에 값을 출력합니다. Streamlit에서 사용하는 `st.write()`는 브라우저 화면에 값을 출력합니다.

```python
print("터미널에 출력됩니다.")
st.write("브라우저 화면에 출력됩니다.")
```

Streamlit 앱을 만들 때 사용자가 봐야 하는 내용은 대부분 `st.write`, `st.markdown`, `st.success`, `st.warning` 같은 Streamlit 출력 함수로 표시합니다.

## 자주 사용하는 명령

- `st.title()`: 큰 제목을 출력합니다.
- `st.header()`: 섹션 제목을 출력합니다.
- `st.write()`: 텍스트, 숫자, 리스트, 딕셔너리 등을 출력합니다.
- `st.markdown()`: 굵게 표시, 목록, 링크 같은 Markdown 문법을 사용해 문장을 출력합니다.
- `st.code()`: 코드 예시를 보기 좋게 출력합니다.
- `st.info()`: 안내 메시지를 파란색 정보 박스로 표시합니다.
- `st.success()`: 성공 메시지를 초록색 박스로 표시합니다.
- `st.warning()`: 주의 메시지를 노란색 박스로 표시합니다.
- `st.text_input()`: 한 줄 텍스트 입력을 받습니다.
- `st.text_area()`: 여러 줄 텍스트 입력을 받습니다.
- `st.number_input()`: 숫자 입력을 받습니다.
- `st.selectbox()`: 목록 중 하나를 선택하게 합니다.
- `st.radio()`: 라디오 버튼을 표시합니다.
- `st.slider()`: 범위 안에서 숫자를 선택하게 합니다.
- `st.columns()`: 화면을 여러 열로 나눕니다.
- `st.tabs()`: 탭 화면을 만듭니다.
- `st.sidebar`: 왼쪽 사이드바 영역에 요소를 배치합니다.
- `st.metric()`: 숫자 지표나 상태값을 대시보드 형태로 표시합니다.
- `st.progress()`: 진행률을 막대로 표시합니다.

## Streamlit 코드 실행 흐름

Streamlit은 사용자가 입력값을 바꾸거나 버튼을 누르면 Python 파일을 위에서 아래로 다시 실행합니다. 그래서 화면 상태를 유지해야 할 때는 이후 단원에서 `st.session_state`를 사용합니다.

처음에는 다음 흐름만 이해하면 됩니다.

```text
1. Streamlit 라이브러리를 가져옵니다.
2. 화면 제목과 설명을 출력합니다.
3. 사용자의 입력을 받습니다.
4. 입력값을 변수에 저장합니다.
5. 조건문으로 결과 메시지를 결정합니다.
6. 결과를 화면에 출력합니다.
```

## 화면 구성 원칙

초기 Streamlit 화면은 화려하게 만드는 것보다 읽기 쉬운 구조가 중요합니다.

```text
입력 영역
-> 사용자가 값을 넣는 곳

처리 영역
-> Python 코드가 입력값을 계산하거나 판단하는 곳

출력 영역
-> 결과, 안내 메시지, 표, 차트를 보여 주는 곳
```

이 구조를 잘 나누면 이후 FastAPI 응답, Supabase 데이터, 백엔드 AI 응답을 화면에 연결할 때도 훨씬 이해하기 쉽습니다.

## 테마 설정

Streamlit 앱의 배경색, 글자색, 강조색은 `.streamlit/config.toml` 파일로 설정할 수 있습니다.
이 과정에서는 테마 설정을 `04_theme-and-config` 예제에서 따로 확인합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend\01_streamlit-basic\04_theme-and-config
..\..\.venv\Scripts\Activate.ps1
streamlit run .\01_theme-preview.py
```

자세한 설명은 [streamlit-theme-guide.md](../../00_references/streamlit-theme-guide.md)를 참고합니다.

## 학습 원칙

처음에는 자동 생성보다 직접 타이핑하면서 익숙해지는 것이 중요합니다.

- 한 파일에 하나의 개념을 담습니다.
- 실행 후 화면 변화를 직접 확인합니다.
- 오류 메시지를 읽고 어느 줄에서 문제가 생겼는지 찾습니다.
- 예제를 조금씩 바꿔 보며 동작을 확인합니다.

## 자주 만나는 오류

```text
streamlit 명령을 찾을 수 없습니다.
```

가상환경이 활성화되어 있는지 확인합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit --version
```

```text
ModuleNotFoundError: No module named 'streamlit'
```

패키지가 설치되지 않은 상태입니다.

```powershell
pip install -r requirements.txt
```

```text
화면이 자동으로 새로고침되지 않습니다.
```

브라우저의 Rerun 버튼을 누르거나 터미널에서 서버를 종료한 뒤 다시 실행합니다. Streamlit 서버 종료는 PowerShell에서 `Ctrl + C`를 누르면 됩니다.
