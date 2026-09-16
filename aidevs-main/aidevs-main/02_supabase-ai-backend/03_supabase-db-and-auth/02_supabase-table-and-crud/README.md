# 02. Supabase 테이블과 CRUD

이 챕터에서는 Supabase에 테이블을 만들고, Python 코드에서 CRUD를 실행합니다.

CRUD는 백엔드 개발에서 가장 기본이 되는 데이터 처리 흐름입니다.

```text
Create: 데이터 생성
Read: 데이터 조회
Update: 데이터 수정
Delete: 데이터 삭제
```

이 과정에서는 먼저 `learning_notes` 테이블 하나로 시작합니다. 사용자, 대화 이력, 서비스 로그처럼 복잡한 테이블은 이후 챕터에서 단계적으로 확장합니다.

## 학습 목표

- Supabase Table Editor와 SQL Editor의 역할을 이해합니다.
- `learning_notes` 테이블을 생성합니다.
- Python Supabase client로 insert/select/update/delete를 실행합니다.
- CRUD 코드가 SQL의 어떤 명령과 연결되는지 이해합니다.
- 수정/삭제 시 조건을 반드시 지정해야 하는 이유를 이해합니다.

## Supabase에서 테이블 만드는 방법

Supabase Dashboard에서 다음 메뉴로 이동합니다.

```text
SQL Editor
-> New query
```

아래 SQL을 붙여 넣고 실행합니다.

```sql
create table if not exists learning_notes (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  content text not null,
  created_at timestamptz not null default now()
);
```

## 컬럼 설명

| 컬럼 | 타입 | 의미 |
| --- | --- | --- |
| `id` | `uuid` | 각 메모를 구분하는 고유 ID입니다. |
| `title` | `text` | 메모 제목입니다. |
| `content` | `text` | 메모 내용입니다. |
| `created_at` | `timestamptz` | 데이터가 생성된 시간입니다. |

`id`는 직접 입력하지 않아도 Supabase/PostgreSQL이 자동으로 만들어 줍니다. `created_at`도 `now()` 기본값 덕분에 자동으로 현재 시간이 들어갑니다.

## 실행 전 확인

먼저 `.env` 파일과 Supabase 환경 변수가 준비되어 있는지 확인합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
dir .env
```

VS Code에서 `.env`를 열고 `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`가 실제 값인지 확인합니다. `your-...` 예시 값이 남아 있으면 Supabase Dashboard에서 실제 값을 복사해 넣습니다.

그다음 CRUD 예제를 순서대로 실행합니다.

```powershell
python .\03_supabase-db-and-auth\02_supabase-table-and-crud\01_create_learning_note.py
python .\03_supabase-db-and-auth\02_supabase-table-and-crud\02_list_learning_notes.py
python .\03_supabase-db-and-auth\02_supabase-table-and-crud\03_get_learning_note.py
python .\03_supabase-db-and-auth\02_supabase-table-and-crud\04_update_learning_note.py
python .\03_supabase-db-and-auth\02_supabase-table-and-crud\05_delete_learning_note.py
```

각 예제는 한 가지 동작만 확인합니다.

| 순서 | 파일 | 확인할 동작 |
| --- | --- | --- |
| 1 | `01_create_learning_note.py` | 메모 1개 생성 |
| 2 | `02_list_learning_notes.py` | 전체 메모 목록 조회 |
| 3 | `03_get_learning_note.py` | id 조건으로 메모 1개 조회 |
| 4 | `04_update_learning_note.py` | 메모 1개 생성 후 수정 |
| 5 | `05_delete_learning_note.py` | 메모 1개 생성 후 삭제 |
| 6 | `06_learning_notes_crud_all.py` | 생성/목록조회/단건조회/수정/삭제 통합 실행 |

`supabase_client.py`는 01~06 예제가 공통으로 사용하는 Supabase 연결 helper입니다. 수업에서는 CRUD 동작을 먼저 보고, 연결 코드는 필요할 때 함께 확인합니다.

전체 흐름을 한 번에 복습하려면 통합본을 실행합니다.

```powershell
python .\03_supabase-db-and-auth\02_supabase-table-and-crud\06_learning_notes_crud_all.py
```

실행 후 Supabase Table Editor에서 `learning_notes` 테이블을 새로고침하며 데이터가 생성, 조회, 수정, 삭제되는 흐름을 확인합니다.

## CRUD와 SQL 대응 관계

| Supabase Python 코드 | SQL 관점 | 의미 |
| --- | --- | --- |
| `.insert({...})` | `insert into` | 새 데이터를 저장합니다. |
| `.select("*")` | `select` | 저장된 데이터를 조회합니다. |
| `.update({...}).eq("id", note_id)` | `update ... where` | 특정 데이터를 수정합니다. |
| `.delete().eq("id", note_id)` | `delete ... where` | 특정 데이터를 삭제합니다. |

중요한 기준은 조건입니다.

```python
.eq("id", note_id)
```

수정과 삭제를 할 때 조건을 빠뜨리면 의도하지 않은 여러 데이터가 바뀔 수 있습니다. 초보 단계에서는 “update/delete에는 조건이 거의 항상 필요하다”라고 기억하면 좋습니다.

## Supabase Python 코드 읽는 법

Supabase Python client 코드는 보통 아래처럼 여러 메서드를 이어 붙여 작성합니다.

```python
result = (
    supabase.table("learning_notes")
    .select("*")
    .eq("id", note_id)
    .execute()
)
```

위 코드는 아래 순서로 읽습니다.

```text
learning_notes 테이블에서
모든 컬럼을 조회하되
id가 note_id와 같은 행만 대상으로 하고
그 요청을 실제로 실행한다
```

### 기본 구조

| 코드 | 의미 |
| --- | --- |
| `supabase.table("learning_notes")` | 작업할 테이블을 선택합니다. |
| `.insert({...})` | 새 행(row)을 추가합니다. |
| `.select("*")` | 행을 조회합니다. `*`는 모든 컬럼을 뜻합니다. |
| `.update({...})` | 기존 행의 값을 수정합니다. |
| `.delete()` | 행을 삭제합니다. |
| `.eq("id", note_id)` | `id` 컬럼 값이 `note_id`와 같은 행만 대상으로 합니다. |
| `.order("created_at", desc=True)` | `created_at` 기준으로 정렬합니다. `desc=True`는 최신순입니다. |
| `.limit(5)` | 최대 5개만 가져옵니다. |
| `.execute()` | 앞에서 만든 요청을 실제 Supabase에 보냅니다. |

`execute()`를 호출하기 전까지는 “요청을 어떻게 보낼지”를 조립하는 단계라고 생각하면 됩니다.

### 생성 insert

```python
result = (
    supabase.table("learning_notes")
    .insert(
        {
            "title": "Supabase create practice",
            "content": "새 메모를 저장합니다.",
        }
    )
    .execute()
)
```

```text
learning_notes 테이블에
title, content 값을 가진 새 행을 추가한다
```

`insert()` 안의 딕셔너리 key는 테이블 컬럼명과 같아야 합니다.

### 전체 조회 select

```python
result = (
    supabase.table("learning_notes")
    .select("*")
    .order("created_at", desc=True)
    .execute()
)
```

```text
learning_notes 테이블에서
모든 컬럼을 조회하고
created_at 기준 최신순으로 정렬한다
```

데이터가 너무 많을 수 있으면 `.limit(10)`처럼 개수를 제한할 수 있습니다.

```python
result = (
    supabase.table("learning_notes")
    .select("*")
    .order("created_at", desc=True)
    .limit(10)
    .execute()
)
```

### 하나만 조회 eq

```python
result = (
    supabase.table("learning_notes")
    .select("*")
    .eq("id", "4a255696-36a6-4f44-a2ec-1d00fa7c982f")
    .execute()
)
```

```text
learning_notes 테이블에서
id가 4a255696-36a6-4f44-a2ec-1d00fa7c982f인 행만 조회한다
```

실제 코드에서는 id를 직접 적기보다 변수로 넣는 경우가 많습니다.

```python
result = (
    supabase.table("learning_notes")
    .select("*")
    .eq("id", note_id)
    .execute()
)
```

### 수정 update

```python
updated_result = (
    supabase.table("learning_notes")
    .update(
        {
            "title": "Supabase update practice - updated",
            "content": "04_update_learning_note.py에서 수정한 내용입니다.",
        }
    )
    .eq("id", note_id)
    .execute()
)
```

```text
learning_notes 테이블에서
id가 note_id와 같은 행을 찾아
title과 content 값을 수정한다
```

`update()`를 사용할 때는 보통 `.eq(...)` 같은 조건을 함께 붙입니다. 조건 없이 수정하면 여러 행이 한꺼번에 바뀔 수 있습니다.

### 삭제 delete

```python
result = (
    supabase.table("learning_notes")
    .delete()
    .eq("id", note_id)
    .execute()
)
```

```text
learning_notes 테이블에서
id가 note_id와 같은 행을 삭제한다
```

`delete()`도 반드시 조건을 붙이는 습관을 들이는 것이 좋습니다.

### 결과 확인 result.data

Supabase 요청 결과는 보통 `result.data`에서 확인합니다.

```python
print(result.data)
```

조회 결과가 있으면 리스트 형태로 데이터가 들어 있습니다.

```python
if not result.data:
    print("조회 결과가 없습니다.")
else:
    first_note = result.data[0]
    print(first_note["title"])
```

한 개만 조회하더라도 `result.data`는 보통 리스트이므로 첫 번째 값을 사용할 때는 `result.data[0]`처럼 접근합니다.

## service role key 주의

이 예제는 Python 백엔드 코드에서 실행하므로 `SUPABASE_SERVICE_ROLE_KEY`를 사용합니다.

```text
service role key는 강한 권한을 가진 서버용 key입니다.
Streamlit 화면, 브라우저 코드, GitHub 저장소에 노출하면 안 됩니다.
```

프론트엔드나 사용자 화면에서 Supabase를 직접 사용할 때는 RLS 정책과 anon key를 함께 사용해야 합니다. 이 내용은 `04_supabase-auth-and-rls`에서 다시 다룹니다.

## 이후 확장

`learning_notes`로 CRUD 흐름을 이해한 뒤, 이후 챕터에서 다음 테이블로 확장합니다.

| 테이블 | 용도 |
| --- | --- |
| `conversations` | 대화 세션 |
| `messages` | 사용자/AI 메시지 |
| `service_logs` | 서비스 실행 로그 |

## 완료 체크리스트

```text
[ ] Supabase SQL Editor에서 learning_notes 테이블을 만들었습니다.
[ ] .env에 SUPABASE_URL과 SUPABASE_SERVICE_ROLE_KEY가 설정되어 있습니다.
[ ] .env에 your-... 예시 값이 남아 있지 않습니다.
[ ] 01~05 개별 CRUD 예제를 실행했습니다.
[ ] 06_learning_notes_crud_all.py 통합 예제를 실행했습니다.
[ ] insert/select/update/delete 흐름을 Supabase 화면에서 확인했습니다.
[ ] update/delete에서 eq("id", note_id)가 왜 필요한지 설명할 수 있습니다.
```
