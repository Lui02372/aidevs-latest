# [학습] Backend와 같은 Python 3.12 기반이지만 별도 이미지와 프로세스로 화면을 실행한다.
FROM python:3.12-slim
# [학습] 컨테이너 안의 기준 작업 폴더를 /app으로 지정한다.
WORKDIR /app
# [학습] frontend 명세를 먼저 복사하여 코드만 바뀐 빌드에서 패키지 설치 계층을 재사용할 수 있게 한다.
COPY requirements.txt .
# [학습] 빌드 시 Streamlit과 httpx를 설치한다. 이번 주석 작업에서는 이 명령을 실행하지 않는다.
RUN pip install --no-cache-dir -r requirements.txt
# [학습] 화면 소스를 이미지에 복사한다. 소스 bind mount가 없어 Host 편집이 실행 중 이미지에 바로 반영되지는 않는다.
COPY app.py .
# [학습] JSON 배열 형태 CMD는 Streamlit 서버를 시작한다. 내부 8501 포트의 Host 공개 번호는 Compose가 결정한다.
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]

