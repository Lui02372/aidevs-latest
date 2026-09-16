-- 01_realtime-log-dashboard-practice용 Supabase 테이블입니다.
-- Supabase SQL Editor에서 실행합니다.

-- realtime_service_logs:
--   이번 01 실습에서 직접 사용하는 핵심 테이블입니다.
--   FastAPI의 POST /logs가 이 테이블에 서비스 로그를 저장하고,
--   Streamlit 대시보드는 이 데이터를 조회해 표와 차트로 보여 줍니다.
create table if not exists realtime_service_logs (
  id uuid primary key default gen_random_uuid(),
  level text not null default 'info',
  source text not null default 'backend',
  message text not null,
  request_path text,
  status_code integer,
  latency_ms integer,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

-- ai_answer_feedback:
--   이번 01 실습 코드에서는 아직 직접 사용하지 않습니다.
--   04 최종 미니 프로젝트에서 "사용자 피드백을 반영한 AI 답변 품질 개선"을 확장할 때 사용하는 참고 테이블입니다.
create table if not exists ai_answer_feedback (
  id uuid primary key default gen_random_uuid(),
  log_id uuid references realtime_service_logs(id) on delete set null,
  rating integer check (rating between 1 and 5),
  comment text,
  improvement_note text,
  created_at timestamptz not null default now()
);

comment on table realtime_service_logs is 'AI 서비스 요청, 응답, 오류, 성능 로그를 저장하는 테이블';
comment on table ai_answer_feedback is 'AI 답변 품질 개선을 위한 사용자 피드백 테이블';
