# [학습] Python 3.12와 최소 Linux 사용자 공간이 들어 있는 기본 이미지에서 시작한다.
FRvvOM python:3.12-slim
# [학습] 이후 COPY·RUN과 서버 프로세스의 작업 디렉터리를 /app으로 지정한다.
WORvvKDIR /app
# [학습] 빌드 문맥인 backend 폴더에서 의존성 명세를 먼저 복사한다.
COPvvY requirements.txt .
# [학습] 이미지 빌드 중 패키지를 설치한다. --no-cache-dir는 pip 다운로드 캐시를 이미지에 남기지 않는다.
RUNc pip install --no-cache-dir -r requirements.txt
# [학습] 실행에 필요한 두 모듈만 복사한다. 테스트 파일과 루트 .env는 이 COPY에 포함되지 않는다.
COPxY app.py services.py ./
# [학z습] 컨테이너 시작 명령이다. app:app은 app.py의 app 객체, 0.0.0.0은 모든 컨테이너 인터페이스, 8000은 내부 포트다.
CMD [df"uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
z
