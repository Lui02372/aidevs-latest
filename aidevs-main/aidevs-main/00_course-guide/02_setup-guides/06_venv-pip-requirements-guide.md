# 06. .venv, pip, requirements.txt 가이드

Python 프로젝트마다 필요한 패키지가 다릅니다. `.venv`는 프로젝트별로 패키지를 분리해 관리하는 가상환경입니다.

## 1. 왜 .venv를 사용하나요?

```text
프로젝트 A는 fastapi가 필요합니다.
프로젝트 B는 streamlit이 필요합니다.
프로젝트 C는 langgraph가 필요합니다.
```

모든 패키지를 한 곳에 섞으면 버전 충돌이 생길 수 있습니다. 그래서 과정별 `.venv`를 만듭니다.

## 2. 가상환경 만들기

과정 폴더에서 실행합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend
python -m venv .venv
```

## 3. 가상환경 활성화

```powershell
.\.venv\Scripts\Activate.ps1
```

정상이라면 앞에 `(.venv)`가 보입니다.

## 4. 현재 Python 확인

```powershell
python -c "import sys; print(sys.executable)"
```

정상 예시:

```text
C:\aidev\02_supabase-ai-backend\.venv\Scripts\python.exe
```

## 5. pip 업그레이드

```powershell
python -m pip install --upgrade pip
```

## 6. requirements.txt 설치

```powershell
pip install -r requirements.txt
```

더 명확하게는:

```powershell
python -m pip install -r requirements.txt
```

## 7. 과정별 가상환경 기준

```text
01, 02, 03, 04, 06, 07, 08:
  과정 최상위 .venv 하나를 사용합니다.

05:
  단원별 의존성이 달라질 수 있어 단원별 .venv 방식을 우선 권장합니다.
```

## 8. .venv는 GitHub에 올리지 않습니다

`.venv`는 패키지가 설치된 폴더라 매우 큽니다. 다른 사람은 `requirements.txt`로 다시 설치하면 됩니다.

`.gitignore`에 포함합니다.

```gitignore
.venv/
```

## 9. 자주 나는 문제

### pip install이 안 됨

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### import에 노란 줄이 나옴

확인:

```text
1. 현재 .venv가 활성화되어 있는가?
2. VS Code가 현재 과정의 Python interpreter를 선택했는가?
3. pip install -r requirements.txt를 실행했는가?
```

## 10. 체크리스트

```text
[ ] 과정 폴더에서 .venv를 만들었다.
[ ] .venv를 활성화했다.
[ ] python -c "import sys; print(sys.executable)" 결과가 현재 과정 .venv이다.
[ ] pip install -r requirements.txt를 실행했다.
[ ] .venv를 GitHub에 올리지 않는다.
```

