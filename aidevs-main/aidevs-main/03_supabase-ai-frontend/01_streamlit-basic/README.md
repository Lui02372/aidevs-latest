# 01_streamlit-basic

Streamlit을 사용해 Python 코드만으로 간단한 웹 화면을 만드는 첫 번째 단원입니다.

이 단원에서는 복잡한 AI 기능이나 API 연동보다, 화면을 띄우고 입력을 받고 결과를 보여주는 기본 흐름을 손으로 직접 작성하는 데 집중합니다.

`02_supabase-ai-backend`에서 Python과 FastAPI를 통해 “서버가 데이터를 처리하는 방식”을 배웠다면, 이 단원에서는 사용자가 실제로 보는 화면을 Python으로 구성합니다. 아직 Supabase, Gemini SDK, 로그인, SSE 스트리밍을 직접 연결하지는 않습니다. 먼저 화면 출력, 입력, 레이아웃을 충분히 익힌 뒤 다음 단원에서 API 호출과 챗봇 UI로 확장합니다.

## 학습 목표

- Streamlit 앱을 실행할 수 있다.
- `st.title`, `st.write`, `st.markdown`, `st.code`, `st.info`, `st.success`의 역할을 구분할 수 있다.
- 텍스트, 숫자, 선택 입력을 받고 입력값이 Python 변수에 저장되는 흐름을 설명할 수 있다.
- 입력값을 바탕으로 간단한 결과 화면과 피드백 화면을 만들 수 있다.
- `columns`, `tabs`, `sidebar`를 사용해 기본 레이아웃을 구성할 수 있다.
- `.streamlit/config.toml`을 사용해 특정 Streamlit 앱의 기본 테마를 설정할 수 있다.
- 이후 API 연동, 챗봇 UI, 대화 이력 화면으로 확장할 수 있는 기본 화면 구조를 이해한다.

## 학습 순서

```text
01_streamlit-project-setup
-> 02_text-input-and-output
-> 03_layout-and-pages
-> 04_theme-and-config
-> 10_labs
-> 20_assignments
```

## 폴더 구성

```text
01_streamlit-basic
├─ README.md
├─ 00_references
├─ 01_streamlit-project-setup
├─ 02_text-input-and-output
├─ 03_layout-and-pages
├─ 04_theme-and-config
├─ 10_labs
└─ 20_assignments
```

## 실행 방법

`03_supabase-ai-frontend` 최상위 폴더에서 가상환경을 활성화한 뒤 예제 파일을 Streamlit으로 실행합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\01_streamlit-basic\01_streamlit-project-setup\01_hello-streamlit.py
```

이미 `.venv`가 만들어져 있다면 다시 만들 필요는 없습니다. 활성화 후 `streamlit --version`으로 설치 여부를 확인할 수 있습니다.

```powershell
streamlit --version
```

패키지 설치가 필요하면 `03_supabase-ai-frontend`의 `requirements.txt`를 기준으로 설치합니다.

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 실행 확인 기준

- 브라우저가 열리고 Streamlit 화면이 표시됩니다.
- 제목과 본문 텍스트가 정상적으로 보입니다.
- 입력값을 변경했을 때 화면 결과가 바뀝니다.
- sidebar, columns, tabs가 화면에 구분되어 표시됩니다.
- 터미널에 오류가 나오면 오류 메시지의 파일명과 줄 번호를 확인할 수 있습니다.

## 필수와 선택 기준

| 구분 | 내용 |
| --- | --- |
| 필수 | Streamlit 실행, 제목/본문 출력, 입력값 처리, sidebar/columns/tabs 기본 레이아웃 |
| 선택 | 테마 설정, 복잡한 페이지 구조, 커스텀 CSS, 외부 API 연결 |
| 제외 | Supabase, Gemini, 로그인, SSE 스트리밍 |

## 학습할 때 보는 기준

Streamlit은 일반적인 웹 프론트엔드처럼 HTML, CSS, JavaScript를 먼저 작성하지 않아도 Python 코드만으로 화면을 만들 수 있습니다. 그래서 이 과정에서는 복잡한 화면 기술보다 다음 질문에 집중합니다.

```text
어떤 입력을 받을 것인가?
입력값은 어떤 변수에 저장되는가?
그 변수로 어떤 결과를 계산하거나 표시할 것인가?
화면에서 입력 영역과 결과 영역은 잘 구분되는가?
나중에 FastAPI 백엔드 응답을 어디에 표시할 수 있는가?
```

이 기준은 이후 `03_api-integration`, `05_ai-chatbot-interface`, `04_state-session-and-data`에서 계속 이어집니다.

## 테마 설정

Streamlit 앱의 배경색, 글자색, 강조색을 바꾸는 방법은 `04_theme-and-config`에서 확인합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend\01_streamlit-basic\04_theme-and-config
..\..\.venv\Scripts\Activate.ps1
streamlit run .\01_theme-preview.py
```

이 예제는 테마 설정 파일을 실습 폴더 안에 두었기 때문에 반드시 `04_theme-and-config` 폴더에서 실행합니다.
자세한 설명은 [streamlit-theme-guide.md](../00_references/streamlit-theme-guide.md)를 참고합니다.

## 다음 단원 연결

이 단원을 마친 뒤 `02_streamlit-ui-components`에서 버튼, 폼, 표, 차트, 파일 업로드 같은 UI 컴포넌트를 더 깊게 다룹니다.

