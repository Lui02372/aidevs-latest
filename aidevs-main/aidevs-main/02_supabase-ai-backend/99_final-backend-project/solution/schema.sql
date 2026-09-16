-- 99_final-backend-project solution 테이블 생성 SQL입니다.
--
-- 실행 위치:
--   Supabase Dashboard > SQL Editor
--
-- 사용 방법:
--   1. Supabase 프로젝트를 엽니다.
--   2. SQL Editor에서 이 파일의 내용을 복사해 실행합니다.
--   3. C:\aidev\02_supabase-ai-backend\.env에 SUPABASE_URL과 SUPABASE_SERVICE_ROLE_KEY를 넣습니다.
--   4. FastAPI 서버를 다시 실행하면 memory 모드가 아니라 Supabase 모드로 저장됩니다.
--
-- 이 SQL은 최종 프로젝트 solution에서 사용하는 최소 테이블만 만듭니다.
-- RLS, Auth, 사용자별 접근 제어까지 확장하려면 03_supabase-db-and-auth의 Auth/JWT/RLS 예제를 참고합니다.

-- final_products:
--   사용자가 등록한 상품 정보를 저장하는 테이블입니다.
--   AI 설명 생성 API가 이 테이블의 상품 정보를 읽고 ai_description 값을 업데이트합니다.
create table if not exists final_products (
  -- id:
  --   각 상품을 구분하는 고유 ID입니다.
  --   gen_random_uuid()가 자동으로 UUID를 만들어 줍니다.
  id uuid primary key default gen_random_uuid(),

  -- name:
  --   상품 이름입니다. 비어 있으면 안 되므로 not null을 사용합니다.
  name text not null,

  -- description:
  --   상품의 기본 설명입니다. AI 설명을 만들 때 참고합니다.
  description text not null,

  -- target_audience:
  --   상품을 주로 사용할 대상을 저장합니다.
  --   요청에서 생략하면 기본값으로 '초보자'가 들어갑니다.
  target_audience text not null default '초보자',

  -- ai_description:
  --   mock AI 또는 실제 LLM이 생성한 상품 설명을 저장합니다.
  --   처음 상품을 만들 때는 아직 설명이 없으므로 null을 허용합니다.
  ai_description text,

  -- created_at:
  --   상품이 등록된 시간입니다.
  --   now()가 Supabase/PostgreSQL 서버 시간을 자동으로 넣어 줍니다.
  created_at timestamptz not null default now()
);

-- final_service_logs:
--   상품 등록, AI 설명 생성, 오류 발생 같은 서비스 동작 기록을 저장하는 테이블입니다.
--   운영 관점에서는 "무슨 일이 언제 일어났는지" 남기는 것이 중요합니다.
create table if not exists final_service_logs (
  -- id:
  --   각 로그를 구분하는 고유 ID입니다.
  id uuid primary key default gen_random_uuid(),

  -- action:
  --   어떤 작업이었는지 저장합니다.
  --   예: create_product, generate_ai_description
  action text not null,

  -- status:
  --   작업 결과입니다.
  --   예: success, failed
  status text not null,

  -- detail:
  --   추가 설명입니다. 오류 메시지나 처리 대상 ID 등을 저장할 수 있습니다.
  detail text,

  -- created_at:
  --   로그가 기록된 시간입니다.
  created_at timestamptz not null default now()
);
