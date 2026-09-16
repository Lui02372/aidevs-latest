# 04_theme-and-config

Streamlit 테마 설정을 실습하는 예제입니다.

이 예제는 `01_streamlit-basic`의 앞 단원에서 기본 화면, 입력, 레이아웃을 확인한 뒤,
앱의 배경색, 글자색, 강조색을 어떻게 설정하는지 확인하기 위한 선택 실습입니다.

## 이 폴더의 파일

```text
04_theme-and-config
├─ README.md
├─ 01_theme-preview.py
└─ .streamlit
   └─ config.toml
```

| 파일 | 역할 |
| --- | --- |
| `01_theme-preview.py` | 테마가 화면에 어떻게 적용되는지 확인하는 Streamlit 예제 |
| `.streamlit/config.toml` | 이 예제에서만 사용하는 Streamlit 테마 설정 파일 |

## 중요한 실행 기준

이 예제는 테마 설정 파일을 실습 폴더 안에 둡니다.
따라서 반드시 `04_theme-and-config` 폴더로 이동한 뒤 실행합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend\01_streamlit-basic\04_theme-and-config
..\..\.venv\Scripts\Activate.ps1
streamlit run .\01_theme-preview.py
```

아래처럼 `03_supabase-ai-frontend` 최상위에서 실행하면 이 폴더 안의 `.streamlit/config.toml`이 적용되지 않을 수 있습니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
streamlit run .\01_streamlit-basic\04_theme-and-config\01_theme-preview.py
```

## 테마 설정 예시

이 예제의 `.streamlit/config.toml`은 흰색 배경과 검정 글자를 사용합니다.

```toml
[theme]
base = "light"
primaryColor = "#2563eb"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f5f5f5"
textColor = "#000000"
font = "sans serif"
```

## 확인할 것

```text
1. 전체 배경이 흰색으로 보이는가?
2. 기본 글자가 검정색으로 보이는가?
3. selectbox, radio, text area가 테마 색상과 어색하지 않은가?
4. 버튼 강조 색상이 primaryColor 기준으로 보이는가?
5. config.toml 값을 바꾼 뒤 앱을 재시작하면 화면이 바뀌는가?
```

## 참고 문서

자세한 설명은 [streamlit-theme-guide.md](../../00_references/streamlit-theme-guide.md)를 참고합니다.
