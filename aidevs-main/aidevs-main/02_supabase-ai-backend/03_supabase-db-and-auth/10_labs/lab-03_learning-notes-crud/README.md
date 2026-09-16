# Lab 03 - Python Supabase CRUD

이 실습은 Python 코드에서 Supabase 테이블에 데이터를 저장, 조회, 수정, 삭제하는 흐름을 확인합니다.

## 학습 목표

- CRUD가 `Create`, `Read`, `Update`, `Delete`의 약자라는 것을 이해합니다.
- Python 코드가 Supabase REST API를 통해 데이터를 다루는 흐름을 확인합니다.
- 터미널 출력과 Supabase Table Editor의 실제 데이터를 비교합니다.

## 실행 방법

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
python .\03_supabase-db-and-auth\02_supabase-table-and-crud\01_create_learning_note.py
python .\03_supabase-db-and-auth\02_supabase-table-and-crud\02_list_learning_notes.py
python .\03_supabase-db-and-auth\02_supabase-table-and-crud\03_get_learning_note.py
python .\03_supabase-db-and-auth\02_supabase-table-and-crud\04_update_learning_note.py
python .\03_supabase-db-and-auth\02_supabase-table-and-crud\05_delete_learning_note.py
```

전체 흐름을 한 번에 복습하려면 아래 통합본을 실행합니다.

```powershell
python .\03_supabase-db-and-auth\02_supabase-table-and-crud\06_learning_notes_crud_all.py
```

## 확인 기준

- 실행 중 새 학습 메모가 생성됩니다.
- 생성된 메모가 조회됩니다.
- 메모 제목 또는 내용이 수정됩니다.
- 마지막에 실습 데이터가 삭제됩니다.

## 정리 질문

- `insert`와 `select`는 각각 어떤 HTTP 동작과 비슷한가요?
- 실습 데이터 삭제를 마지막에 넣는 이유는 무엇인가요?
- 실제 서비스에서는 삭제 대신 상태값을 바꾸는 방식도 사용할 수 있을까요?
