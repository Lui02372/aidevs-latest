# Streamlit Theme Guide

Streamlit 테마는 앱의 기본 배경색, 글자색, 강조색, 글꼴을 설정하는 방법입니다.
이 과정에서는 CSS를 먼저 쓰기보다 Streamlit이 제공하는 `.streamlit/config.toml` 설정을 먼저 사용합니다.

## 공식 문서

테마와 설정은 Streamlit 공식 문서를 기준으로 확인합니다.

| 주제 | 공식 문서 |
| --- | --- |
| Streamlit 설정 파일 | [Configuration](https://docs.streamlit.io/develop/api-reference/configuration/config.toml) |
| 테마 옵션 | [Theming](https://docs.streamlit.io/develop/concepts/configuration/theming) |

## 테마 파일 위치

Streamlit은 실행할 때 현재 작업 폴더의 `.streamlit/config.toml` 파일을 읽습니다.

예를 들어 아래처럼 실행하면:

```powershell
cd C:\aidev\03_supabase-ai-frontend\01_streamlit-basic\04_theme-and-config
streamlit run .\01_theme-preview.py
```

Streamlit은 아래 파일을 읽습니다.

```text
C:\aidev\03_supabase-ai-frontend\01_streamlit-basic\04_theme-and-config\.streamlit\config.toml
```

반대로 `C:\aidev\03_supabase-ai-frontend` 최상위에서 실행하면 `04_theme-and-config` 안의 테마 파일이 적용되지 않을 수 있습니다.
그래서 이 예제는 반드시 `04_theme-and-config` 폴더로 이동한 뒤 실행합니다.

## 기본 예시

흰색 배경과 검정 글자를 사용하는 기본 테마 예시입니다.

```toml
[theme]
base = "light"
primaryColor = "#2563eb"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f5f5f5"
textColor = "#000000"
font = "sans serif"
```

## 설정 항목 의미

| 항목 | 의미 |
| --- | --- |
| `base` | `"light"` 또는 `"dark"` 기본 테마 기준 |
| `primaryColor` | 버튼, 선택 강조 등 주요 색상 |
| `backgroundColor` | 앱 전체 배경색 |
| `secondaryBackgroundColor` | 입력창, 사이드바, 보조 영역 배경색 |
| `textColor` | 기본 글자색 |
| `font` | 기본 글꼴 |

## 테마와 CSS의 차이

| 구분 | 사용 상황 |
| --- | --- |
| `.streamlit/config.toml` | 앱 전체의 기본 색상과 글꼴을 정할 때 |
| `st.markdown(..., unsafe_allow_html=True)` CSS | 특정 요소를 아주 세밀하게 바꿔야 할 때 |

초보자 실습에서는 먼저 테마 설정을 사용합니다.
CSS는 꼭 필요한 경우에만 사용합니다.

## 반영 방법

테마 파일을 수정한 뒤에는 Streamlit 앱을 완전히 종료하고 다시 실행하는 것이 가장 확실합니다.

```text
1. 터미널에서 Ctrl + C
2. streamlit run 명령 다시 실행
3. 브라우저 새로고침
```
