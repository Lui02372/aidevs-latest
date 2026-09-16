# 03. Database Design

## Supabase 테이블

| 테이블 | 용도 |
| --- | --- |
|  |  |

## 컬럼

| 컬럼 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| id | uuid | 예 | 기본 키 |
| created_at | timestamptz | 예 | 생성 시각 |

## SQL

```sql
create table if not exists example_items (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  content text,
  created_at timestamptz not null default now()
);
```

## RLS 적용 여부

```text
이번 프로젝트에서 RLS를 적용한다 / 적용하지 않는다.
이유:
```
