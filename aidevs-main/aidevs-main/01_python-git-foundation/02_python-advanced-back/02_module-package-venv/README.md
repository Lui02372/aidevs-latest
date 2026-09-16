# 02_module-package-venv

이 단원에서는 파이썬 파일을 여러 개로 나누고, 필요한 기능을 `import`해서 사용하는 방법을 배웁니다.

프로그램이 커지면 모든 코드를 한 파일에 넣기 어렵습니다. 그래서 기능별로 파일을 나누고, 필요한 곳에서 가져와 사용하는 방식이 중요합니다.

## 이 단원에서 배우는 것

| 예제 | 핵심 내용 | 설명 |
| --- | --- | --- |
| 01_import_standard_library.py | 표준 라이브러리 import | 파이썬에 기본 포함된 모듈 사용 |
| 02_from_import_and_alias.py | `from import`, 별칭 import | 필요한 함수만 가져오거나 짧은 이름으로 사용 |
| 03_use_custom_module.py | 직접 만든 모듈 import | 같은 폴더의 `.py` 파일 가져오기 |
| 04_from_custom_module_import.py | 직접 만든 함수만 import | 모듈 안의 특정 함수만 가져오기 |
| 05_package_import.py | 패키지 import | 폴더 단위로 코드를 묶어서 가져오기 |
| 06_check_external_package.py | 외부 패키지 확인 | 공통 `.venv`에 설치된 pytest 확인 |

## import 방식 정리

```python
import math
```

모듈 전체를 가져옵니다. 사용할 때는 `math.sqrt()`처럼 모듈 이름을 함께 씁니다.

```python
from math import sqrt
```

모듈 안의 특정 함수만 가져옵니다. 사용할 때는 `sqrt()`처럼 바로 씁니다.

```python
import datetime as dt
```

모듈 이름이 길거나 자주 사용할 때 짧은 별칭을 붙입니다.

```python
from shop.order_calculator import calculate_total
```

패키지 안에 있는 특정 파일의 함수를 가져옵니다.

## 실행 전 준비

이 단원에서는 별도의 `.venv`를 만들지 않습니다. `01_python-git-foundation` 최상위의 공통 가상환경을 사용합니다.

```powershell
cd C:\aidev\01_python-git-foundation
.\.venv\Scripts\Activate.ps1
```

외부 패키지는 최상위 `requirements.txt`를 통해 이미 설치되어 있어야 합니다.

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 실행 방법

```powershell
python .\02_python-advanced\02_module-package-venv\01_import_standard_library.py
python .\02_python-advanced\02_module-package-venv\02_from_import_and_alias.py
python .\02_python-advanced\02_module-package-venv\03_use_custom_module.py
python .\02_python-advanced\02_module-package-venv\04_from_custom_module_import.py
python .\02_python-advanced\02_module-package-venv\05_package_import.py
python .\02_python-advanced\02_module-package-venv\06_check_external_package.py
```

## 핵심 확인

```text
모듈: 하나의 .py 파일
패키지: 여러 모듈을 담는 폴더
표준 라이브러리: 파이썬에 기본 포함된 모듈
외부 패키지: pip로 설치해서 사용하는 패키지
.venv: 프로젝트별 패키지를 분리해서 관리하는 가상환경
requirements.txt: 필요한 외부 패키지 목록
```
