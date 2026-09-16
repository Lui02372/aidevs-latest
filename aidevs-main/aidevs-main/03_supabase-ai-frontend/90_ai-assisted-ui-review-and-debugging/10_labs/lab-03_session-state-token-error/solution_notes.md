# Lab 03 Solution Notes

## 원인

1. `st.session_state.access_token`을 사용하기 전에 초기화하지 않았습니다.
2. 보호된 API 호출 시 `Authorization: Bearer ...` 형식이 아니라 `Token` header를 사용했습니다.

## 수정 방향

```python
if "access_token" not in st.session_state:
    st.session_state.access_token = None
```

```python
headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
```

## 확인

1. 로그인 전 화면이 오류 없이 열립니다.
2. 로그인 성공 후 `sample-access-token`이 저장됩니다.
3. `내 정보 조회` 버튼을 누르면 `/api/me` 응답이 표시됩니다.
4. 로그아웃 후 token 값이 `None`으로 바뀝니다.
