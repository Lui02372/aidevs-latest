"""데이터 모양을 정의하는 파일입니다.

처음에는 dict만 사용해도 됩니다.
다만 dataclass를 사용하면 "이 데이터가 어떤 값을 가져야 하는지"를 더 분명하게 볼 수 있습니다.

뒤 과정의 Pydantic BaseModel도 이와 비슷하게 데이터 모양을 코드로 표현합니다.
"""

from dataclasses import asdict, dataclass


@dataclass
class ChatMessage:
    """질문과 답변 하나를 표현하는 object입니다."""

    question: str
    answer: str
    model: str

    def to_dict(self) -> dict:
        """JSON 저장을 위해 dataclass object를 dict로 바꿉니다."""

        return asdict(self)
