-- 03_supabase-db-and-auth 실습용 Supabase 스키마입니다.
-- Supabase Dashboard > SQL Editor에서 이 파일 내용을 실행합니다.
-- create table if not exists 구문은 같은 SQL을 여러 번 실행해도 기존 테이블이 있으면 다시 만들지 않습니다.

-- learning_notes
-- 02_supabase-table-and-crud에서 사용하는 기본 CRUD 실습 테이블입니다.
-- insert/select/update/delete 흐름을 가장 먼저 연습합니다.
-- FastAPI나 LLM 흐름으로 넘어가기 전에 Supabase 테이블 조작 방법을 익히기 위한 테이블입니다.
create table if not exists learning_notes (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  content text not null,
  created_at timestamptz not null default now()
);

-- conversations
-- 실제 채팅 서비스 구조로 확장할 때 사용하는 선택 테이블입니다.
-- 하나의 대화 세션 또는 채팅방을 의미합니다.
-- 현재 05 단원에서는 먼저 simple_chat_logs로 단순 흐름을 확인합니다.
-- 이후 프로젝트에서 여러 메시지를 가진 대화 이력을 만들 때 conversations + messages 구조로 확장할 수 있습니다.
create table if not exists conversations (
  id uuid primary key default gen_random_uuid(),
  user_id uuid,
  title text not null,
  created_at timestamptz not null default now()
);

-- messages
-- conversations와 연결해서 사용하는 선택 테이블입니다.
-- 하나의 대화방 안에 들어가는 user/assistant/system 메시지를 각각 저장합니다.
-- 질문/답변 한 줄 로그가 아니라, 한 대화방에 여러 메시지를 쌓아야 할 때 사용합니다.
create table if not exists messages (
  id uuid primary key default gen_random_uuid(),
  conversation_id uuid references conversations(id) on delete cascade,
  role text not null check (role in ('user', 'assistant', 'system')),
  content text not null,
  created_at timestamptz not null default now()
);

-- service_logs
-- 서비스 운영 로그를 저장할 때 사용하는 선택 테이블입니다.
-- API 호출, 오류, 모델 이름, 처리 시간, 디버깅 정보 같은 이벤트를 기록할 수 있습니다.
-- metadata jsonb 컬럼은 로그마다 필요한 부가 정보가 달라도 유연하게 저장하기 위한 컬럼입니다.
create table if not exists service_logs (
  id uuid primary key default gen_random_uuid(),
  user_id uuid,
  event_type text not null,
  message text not null,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

-- simple_chat_logs
-- 05_conversation-history-and-service-logs에서 사용하는 단순 채팅 로그 테이블입니다.
-- 첫 LLM 로그 저장 실습을 위해 만든 가장 단순한 구조입니다.
-- 사용자 질문 1개, AI 답변 1개, provider/model 정보, 성공/실패 상태를 한 행에 저장합니다.
-- 이 단원은 Auth/JWT 사용자 추적 전에 로그 저장 흐름을 익히는 단계이므로 user_id를 의도적으로 넣지 않습니다.
create table if not exists simple_chat_logs (
  id uuid primary key default gen_random_uuid(),
  user_message text not null,
  assistant_message text,
  provider text not null default 'gemini',
  model text,
  status text not null default 'success',
  error_message text,
  created_at timestamptz not null default now()
);

-- RLS 정책 SQL은 이후 사용자별 데이터 접근이 필요한 프로젝트에서 다룹니다.
