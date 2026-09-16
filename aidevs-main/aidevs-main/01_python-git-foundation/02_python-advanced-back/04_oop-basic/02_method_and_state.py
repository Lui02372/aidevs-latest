"""메서드로 객체의 상태를 변경하는 예제입니다."""


class Task:
    """할 일 하나를 표현하는 클래스입니다."""

    def __init__(self, title: str) -> None:
        """할 일이 처음 만들어질 때 제목과 완료 상태를 저장합니다."""

        # 할 일 제목입니다.
        self.title = title

        # 처음에는 완료되지 않은 상태로 시작합니다.
        self.done = False

    def complete(self) -> None:
        """할 일을 완료 상태로 바꿉니다."""

        # 객체의 done 값을 True로 변경합니다.
        self.done = True

    def label(self) -> str:
        """화면에 보여줄 문자열을 만듭니다."""

        # done 값에 따라 표시할 상태 문구를 결정합니다.
        status = "완료" if self.done else "진행중"

        # 상태와 제목을 합쳐서 반환합니다.
        return f"[{status}] {self.title}"


# Task 객체를 만듭니다.
task = Task("객체지향 기본 예제 실행")

# 처음에는 진행중 상태입니다.
print(task.label())

# complete 메서드를 호출하면 객체 내부 상태가 바뀝니다.
task.complete()

# 상태가 완료로 바뀐 것을 확인합니다.
print(task.label())
