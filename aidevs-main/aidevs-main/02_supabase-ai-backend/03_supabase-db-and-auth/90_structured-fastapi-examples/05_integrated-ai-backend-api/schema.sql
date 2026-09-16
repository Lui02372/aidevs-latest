-- 05_integrated-ai-backend-api 예제에서 사용하는 채팅 로그 테이블입니다.
--
-- 이 예제의 목표:
-- 1. Supabase Auth로 로그인한 사용자별 채팅 로그를 저장합니다.
-- 2. Redis 캐시를 사용했는지, Gemini 응답인지 함께 기록합니다.
-- 3. GET /logs 조회에서는 사용자 access token으로 RLS가 적용되는 흐름을 확인합니다.

create table if not exists ex90_user_chat_logs (
  -- 채팅 로그 1건을 구분하는 고유 id입니다.
  id uuid primary key default gen_random_uuid(),

  -- Supabase Auth 사용자 id입니다.
  -- auth.users(id)를 참조하므로 실제 가입된 사용자와 연결됩니다.
  user_id uuid not null references auth.users(id) on delete cascade,

  -- 사용자의 질문과 AI 또는 캐시가 반환한 답변입니다.
  user_message text not null,
  assistant_message text,

  -- provider/model은 응답 출처를 기록합니다.
  provider text not null default 'gemini',
  model text,

  -- actual_api_called는 실제 Gemini API 호출 여부입니다.
  -- cached는 Redis 캐시 응답을 사용했는지 여부입니다.
  actual_api_called boolean not null default false,
  cached boolean not null default false,

  -- 처리 성공/실패 상태와 실패 원인을 기록합니다.
  status text not null default 'success',
  error_message text,

  -- 로그 생성 시간입니다.
  created_at timestamptz not null default now()
);

-- RLS(Row Level Security)를 켭니다.
-- RLS를 켜면 Supabase가 access token 안의 사용자 id를 기준으로 row 접근을 제한할 수 있습니다.
alter table ex90_user_chat_logs enable row level security;

-- SQL을 여러 번 실행해도 중복 policy 오류가 나지 않도록 기존 정책을 삭제합니다.
drop policy if exists "ex90 chat logs select own" on ex90_user_chat_logs;

-- SELECT 정책입니다.
-- 현재 로그인한 사용자 id(auth.uid())와 row의 user_id가 같을 때만 조회됩니다.
create policy "ex90 chat logs select own"
on ex90_user_chat_logs
for select
using (auth.uid() = user_id);

drop policy if exists "ex90 chat logs insert own" on ex90_user_chat_logs;

-- INSERT 정책입니다.
-- 사용자 token으로 직접 insert할 경우, 넣으려는 user_id가 자기 id와 같아야 합니다.
-- 현재 FastAPI /chat 저장은 service role key를 사용하므로 이 정책을 직접 통과하지는 않습니다.
create policy "ex90 chat logs insert own"
on ex90_user_chat_logs
for insert
with check (auth.uid() = user_id);
