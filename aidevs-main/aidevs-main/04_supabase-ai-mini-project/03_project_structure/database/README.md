# Database

이 폴더는 최종 프로젝트에서 사용할 Supabase 테이블 기준을 보관합니다.

## 파일

| 파일 | 설명 |
| --- | --- |
| `schema.sql` | Supabase SQL Editor에서 실행할 기본 테이블 생성 SQL입니다. |

## 사용 방법

1. Supabase 프로젝트를 엽니다.
2. SQL Editor로 이동합니다.
3. `schema.sql` 내용을 복사해 실행합니다.
4. 생성된 테이블을 Table Editor에서 확인합니다.

## 주의

- 실제 프로젝트에 맞게 컬럼은 수정할 수 있습니다.
- API 설계서와 DB 설계서의 테이블/컬럼명이 `schema.sql`과 일치해야 합니다.
- RLS/Auth까지 적용하는 팀은 정책 SQL을 별도 파일로 추가할 수 있습니다.
