-- 01_notes-api-with-supabase 예제에서 사용하는 테이블입니다.
--
-- 이 예제의 목표:
-- 1. FastAPI 구조를 router/schema/service로 나눕니다.
-- 2. service 계층에서 Supabase 테이블을 CRUD합니다.
-- 3. 인증/RLS 없이 가장 단순한 DB 연결 흐름부터 확인합니다.

create table if not exists ex90_notes (
  -- id는 각 노트를 구분하는 고유값입니다.
  -- gen_random_uuid()는 Supabase/PostgreSQL이 자동으로 uuid를 만들어 줍니다.
  id uuid primary key default gen_random_uuid(),

  -- title/content는 사용자가 입력하는 필수 텍스트입니다.
  title text not null,
  content text not null,

  -- created_at은 row가 만들어진 시간을 자동 기록합니다.
  created_at timestamp not null default now()
);

-- Swagger UI에서 조회, 수정, 삭제를 바로 연습할 수 있는 샘플 노트 10개입니다.
insert into ex90_notes (title, content) values
  ('FastAPI란?', 'Python으로 API 서버를 만드는 프레임워크입니다.'),
  ('라우터의 역할', 'URL과 HTTP 요청, 응답을 처리합니다.'),
  ('서비스의 역할', 'Supabase 같은 외부 서비스와 통신합니다.'),
  ('Pydantic 모델', '요청 데이터와 응답 데이터의 모양을 검사합니다.'),
  ('Supabase URL', '.env 파일에 프로젝트 URL을 저장합니다.'),
  ('환경 변수', '비밀 키를 코드에 직접 작성하지 않기 위해 사용합니다.'),
  ('GET 요청', '저장된 데이터를 조회할 때 사용합니다.'),
  ('POST 요청', '새로운 노트를 만들 때 사용합니다.'),
  ('PUT 요청', '기존 노트의 제목과 내용을 수정할 때 사용합니다.'),
  ('DELETE 요청', '더 이상 필요하지 않은 노트를 삭제할 때 사용합니다.');
