"""PostgreSQL 연결 없이 Memory 저장 정책과 관련성 규칙을 검증합니다."""

import unittest

from memory_store import select_relevant, validate_memory


class MemoryPolicyTest(unittest.TestCase):
    def test_allowed_preference(self) -> None:
        validate_memory("transportation", "대중교통")

    def test_sensitive_key_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            validate_memory("password", "secret")

    def test_sensitive_value_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            validate_memory("hotel_preference", "api_key=secret")

    def test_only_relevant_memory_is_selected(self) -> None:
        items = [
            {"id": "1", "key": "transportation", "value": "대중교통"},
            {"id": "2", "key": "food_restriction", "value": "해산물 알레르기"},
        ]
        selected = select_relevant(items, "식당을 추천해줘")
        self.assertEqual([item["key"] for item in selected], ["food_restriction"])


if __name__ == "__main__":
    unittest.main()
