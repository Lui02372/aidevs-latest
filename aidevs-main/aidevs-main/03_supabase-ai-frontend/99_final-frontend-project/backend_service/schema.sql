-- 99_final-frontend-project backend_service용 Supabase 테이블 예시입니다.
-- Supabase SQL Editor에서 실행합니다.
-- 프론트엔드는 이 테이블에 직접 접근하지 않고 FastAPI backend_service만 호출합니다.

create table if not exists frontend_chat_logs (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  user_email text not null,
  user_message text not null,
  assistant_message text not null,
  provider text not null default 'gemini',
  model text,
  created_at timestamptz not null default now()
);

create table if not exists frontend_service_logs (
  id uuid primary key default gen_random_uuid(),
  user_id uuid,
  user_email text,
  action text not null,
  status text not null,
  message text,
  created_at timestamptz not null default now()
);

alter table frontend_chat_logs enable row level security;
alter table frontend_service_logs enable row level security;

-- 로그인한 사용자는 자신의 대화 기록만 읽을 수 있습니다.
drop policy if exists "read own frontend chat logs" on frontend_chat_logs;
create policy "read own frontend chat logs"
on frontend_chat_logs
for select
to authenticated
using (auth.uid() = user_id);

-- 로그인한 사용자는 자신의 서비스 로그만 읽을 수 있습니다.
drop policy if exists "read own frontend service logs" on frontend_service_logs;
create policy "read own frontend service logs"
on frontend_service_logs
for select
to authenticated
using (auth.uid() = user_id);

-- backend_service는 service role key로 insert/select를 수행합니다.
-- service role key는 RLS를 우회할 수 있으므로 반드시 backend 환경변수에만 둡니다.
