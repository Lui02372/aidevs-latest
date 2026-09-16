"""모호한 Prompt와 구성 요소가 명확한 Prompt의 실제 응답을 비교합니다."""

import httpx

from _llm_backend import generate_text, print_connection_help, print_result


MEETING = """민수는 금요일까지 결제 API를 완성한다.
지연은 다음 주에 화면 시안을 공유한다.
정식 배포일은 트래픽 테스트 결과를 본 뒤 정하기로 했다."""
# 기준 Prompt는 역할, 제외 조건, 출력 형식이 모두 모호합니다.
WEAK_PROMPT = "회의 내용을 정리해 주세요."
# 개선 Prompt는 평가할 수 있도록 각 요구사항을 명시적으로 분리합니다.
IMPROVED_PROMPT = """[Role]
당신은 프로젝트 회의 기록 담당자입니다.
[Instruction]
결정 사항과 담당자별 할 일을 분리하세요.
[Context]
개발자와 디자이너가 참여한 배포 준비 회의입니다.
[Constraint]
확정되지 않은 내용은 결정 사항에 포함하지 마세요.
[Output Format]
결정 사항과 할 일을 Markdown 목록으로 작성하세요."""


if __name__ == "__main__":
    try:
        # 동일한 원문을 사용해 Prompt 개선 전후의 누락과 오판만 관찰합니다.
        print_result("Before · 모호한 Prompt", generate_text(WEAK_PROMPT, MEETING))
        print_result(
            "After · 개선된 Prompt",
            generate_text(IMPROVED_PROMPT, MEETING),
        )
    except httpx.HTTPError as error:
        print_connection_help(error)
