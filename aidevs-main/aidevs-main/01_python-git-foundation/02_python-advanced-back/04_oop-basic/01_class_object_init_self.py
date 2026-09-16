"""클래스, 객체, __init__, self를 이해하는 예제입니다."""


class LearningNote:
    """학습 노트 한 개를 표현하는 클래스입니다."""

    def __init__(self, title: str, content: str) -> None:
        """객체가 만들어질 때 처음 실행되는 메서드입니다."""

        # self.title은 이 객체가 가지고 있는 제목입니다.
        # 같은 LearningNote 클래스로 여러 객체를 만들어도 각 객체의 title은 따로 저장됩니다.
        self.title = title

        # self.content는 이 객체가 가지고 있는 내용입니다.
        self.content = content


# LearningNote 클래스를 이용해 첫 번째 객체를 만듭니다.
note1 = LearningNote("Python 함수", "함수는 코드를 재사용하기 위해 사용합니다.")

# 같은 클래스로 두 번째 객체도 만들 수 있습니다.
note2 = LearningNote("예외 처리", "try/except로 오류 상황을 처리합니다.")

# 각 객체는 자기만의 title과 content 값을 가지고 있습니다.
print("첫 번째 노트 제목:", note1.title)
print("첫 번째 노트 내용:", note1.content)
print("두 번째 노트 제목:", note2.title)
print("두 번째 노트 내용:", note2.content)
