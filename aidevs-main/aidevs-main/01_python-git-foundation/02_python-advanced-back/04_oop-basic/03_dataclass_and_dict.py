"""dataclass와 dict 변환을 이해하는 예제입니다."""

from dataclasses import asdict, dataclass


@dataclass
class Contact:
    """연락처 데이터를 표현하는 클래스입니다."""

    # dataclass는 이런 필드 정의를 보고 __init__ 같은 기본 메서드를 자동으로 만들어 줍니다.
    name: str
    phone: str
    email: str


# Contact 객체를 만듭니다.
contact = Contact(
    name="Mina",
    phone="01012345678",
    email="mina@example.com",
)

# 객체의 필드는 점(.)으로 접근합니다.
print("이름:", contact.name)
print("전화번호:", contact.phone)
print("이메일:", contact.email)

# asdict는 dataclass 객체를 dict로 바꿉니다.
# JSON 저장이나 API 응답을 만들 때 dict 형태가 필요할 수 있습니다.
contact_dict = asdict(contact)

# dict로 바뀐 결과를 출력합니다.
print("dict 변환 결과:", contact_dict)
