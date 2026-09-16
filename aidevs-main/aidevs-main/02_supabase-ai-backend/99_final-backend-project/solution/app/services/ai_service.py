"""AI 설명 생성 로직을 담당하는 서비스 파일입니다.

현재 예제는 실제 Gemini/OpenAI API를 호출하지 않고 mock 문자열을 생성합니다.
최종 프로젝트에서는 먼저 mock으로 전체 API 흐름을 완성한 뒤,
시간이 남으면 이 파일만 실제 LLM 호출 코드로 교체하는 방식이 좋습니다.

이렇게 분리하는 이유:
    router 파일은 HTTP 요청/응답을 담당합니다.
    service 파일은 실제 비즈니스 로직을 담당합니다.
    그래서 AI 호출 방식이 바뀌어도 API 주소나 요청 모델은 크게 바꾸지 않아도 됩니다.
"""


def build_mock_ai_description(product: dict) -> str:
    """상품 정보를 받아 간단한 mock AI 설명을 만듭니다.

    product는 storage_service.py에서 가져온 상품 dict입니다.
    실제 LLM을 호출하지 않으므로 API Key, 비용, 네트워크 오류 걱정 없이 테스트할 수 있습니다.
    """

    return (
        f"{product['name']}은(는) {product['target_audience']}에게 적합한 상품입니다. "
        f"{product['description']} 이 특징을 바탕으로 쉽고 신뢰감 있게 소개할 수 있습니다."
    )
