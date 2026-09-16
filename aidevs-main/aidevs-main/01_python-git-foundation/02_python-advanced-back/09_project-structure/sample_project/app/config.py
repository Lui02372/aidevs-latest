"""프로젝트 설정값을 모아두는 파일입니다.

설정값은 여러 파일에서 함께 사용할 수 있습니다.
예를 들어 LLM 모델명, API 주소, 기본 사용자명 같은 값은 config.py에 두면 관리하기 쉽습니다.
"""

# 아직 실제 LLM API를 호출하지 않으므로 연습용 모델명을 사용합니다.
# 이후 LLM API 단원에서 실제 Gemini 모델명으로 교체합니다.
DEFAULT_LLM_MODEL = "practice-chat-model"

# 예제에서 사용할 기본 사용자 이름입니다.
DEFAULT_USER_NAME = "학습자"

# 이후 FastAPI 서버를 만들 때 사용할 수 있는 API 버전 표시 예시입니다.
API_VERSION = "v1"
