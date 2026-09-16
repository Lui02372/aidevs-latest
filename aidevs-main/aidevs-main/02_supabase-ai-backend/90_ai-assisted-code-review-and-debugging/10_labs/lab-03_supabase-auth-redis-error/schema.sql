-- Lab 03에서 사용할 수 있는 Supabase 확인용 테이블입니다.
-- broken_external_service_api.py는 의도적으로 다른 테이블명을 조회합니다.
-- 수강생은 오류 메시지를 보고 테이블명 불일치를 찾아야 합니다.

create table if not exists lab03_debug_logs (
  id uuid primary key default gen_random_uuid(),
  message text not null,
  created_at timestamptz not null default now()
);
