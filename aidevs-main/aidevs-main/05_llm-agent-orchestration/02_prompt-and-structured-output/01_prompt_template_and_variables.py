"""Prompt의 고정 구조와 업무별 변수를 분리해 재사용합니다."""

# 항목	의미	설명할 때 사용할 표현
# role	역할	AI가 어떤 관점과 전문성을 가지고 답할지 지정
# instruction	작업 지시	AI가 수행해야 하는 핵심 작업을 지정
# context	배경 정보	작업의 목적과 결과가 사용되는 상황을 제공
# constraint	제약 조건	답변할 때 반드시 지키거나 피해야 하는 기준
# output_format	출력 형식	결과에 포함할 항목과 표현 구조를 지정

from string import Template


# 변하지 않는 Prompt 골격은 Template으로 한 번만 정의합니다.
PROMPT_TEMPLATE = Template(
    """[Role]
$role

[Instruction]
$instruction

[Context]
$context

[Constraint]
$constraint

[Output Format]
$output_format"""
)

# 업무별로 달라지는 값만 분리하면 복사·붙여넣기로 생기는 불일치를 줄일 수 있습니다.
TASKS = {
    "고객 문의": {
        "role": "온라인 쇼핑몰 고객 지원 분류 담당자",
        "instruction": "문의의 유형과 긴급도를 분류하세요.",
        "context": "결과는 담당 팀 자동 배정에 사용됩니다.",
        "constraint": "입력에 없는 사실을 추측하지 마세요.",
        "output_format": "유형, 긴급도, 한 문장 요약",
    },
    "회의 요약": {
        "role": "프로젝트 회의 기록 담당자",
        "instruction": "결정 사항과 담당자별 할 일을 구분하세요.",
        "context": "개발·디자인·운영 담당자가 참석했습니다.",
        "constraint": "확정되지 않은 내용은 결정 사항에서 제외하세요.",
        "output_format": "결정 사항 목록과 할 일 목록",
    },
}


def render_prompt(values: dict[str, str]) -> str:
    # substitute()는 필수 변수가 빠지면 오류를 내므로 누락을 조기에 발견할 수 있습니다.
    return PROMPT_TEMPLATE.substitute(values)


if __name__ == "__main__":
    for task_name, task_values in TASKS.items():
        print(f"\n===== {task_name} =====")
        print(render_prompt(task_values))
