-- 04_auth-jwt-profile-api 예제에서 사용하는 profile 테이블입니다.
--
-- 이 예제의 목표:
-- 1. Supabase Auth로 가입한 사용자마다 profile row를 1개씩 저장합니다.
-- 2. 로그인한 사용자는 자기 profile만 조회/수정할 수 있게 RLS를 적용합니다.
-- 3. FastAPI에서는 Bearer token(JWT)을 받아 Supabase에 전달하고,
--    Supabase는 JWT 안의 사용자 id를 auth.uid()로 확인합니다.

-- ex90_profiles 테이블을 만듭니다.
--
-- id:
--   profile의 id입니다.
--   auth.users(id)를 참조하므로, Supabase Auth에 가입된 사용자 id와 같은 값을 사용합니다.
--   즉 "사용자 1명 = profile 1개" 구조입니다.
--
-- references auth.users(id):
--   Supabase Auth가 관리하는 사용자 테이블을 참조합니다.
--
-- on delete cascade:
--   사용자가 삭제되면 해당 profile도 함께 삭제됩니다.
--
-- display_name:
--   화면에 표시할 이름입니다.
--
-- created_at / updated_at:
--   생성/수정 시간을 기록합니다.
create table if not exists ex90_profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- Row Level Security(RLS)를 켭니다.
--
-- RLS를 켜면 테이블에 접근할 때 "행(row) 단위 권한 규칙"이 적용됩니다.
-- 아래 policy를 만들기 전까지는 일반 사용자가 이 테이블을 마음대로 읽거나 쓸 수 없습니다.
--
-- service role key는 RLS를 우회할 수 있습니다.
-- 하지만 anon key + 사용자 access token으로 접근할 때는 아래 RLS 정책이 적용됩니다.
alter table ex90_profiles enable row level security;

-- 기존에 같은 이름의 select policy가 있으면 삭제합니다.
-- SQL을 여러 번 실행해도 중복 policy 오류가 나지 않게 하기 위한 안전장치입니다.
drop policy if exists "ex90 profiles select own" on ex90_profiles;

-- SELECT 정책입니다.
--
-- using (auth.uid() = id):
--   현재 로그인한 사용자 id(auth.uid())와 profile row의 id가 같을 때만 조회를 허용합니다.
--
-- 예:
--   로그인 사용자 id = aaa
--   row id = aaa  -> 조회 가능
--   row id = bbb  -> 조회 불가
create policy "ex90 profiles select own"
on ex90_profiles
for select
using (auth.uid() = id);

-- 기존 insert policy를 삭제합니다.
drop policy if exists "ex90 profiles insert own" on ex90_profiles;

-- INSERT 정책입니다.
--
-- with check (auth.uid() = id):
--   새로 넣으려는 row의 id가 현재 로그인한 사용자 id와 같을 때만 insert를 허용합니다.
--
-- using은 "기존 row를 볼 수 있는가"에 가깝고,
-- with check는 "새로 저장하려는 row가 규칙에 맞는가"를 검사합니다.
--
-- 이 정책 덕분에 사용자는 다른 사람 id로 profile을 만들 수 없습니다.
create policy "ex90 profiles insert own"
on ex90_profiles
for insert
with check (auth.uid() = id);

-- 기존 update policy를 삭제합니다.
drop policy if exists "ex90 profiles update own" on ex90_profiles;

-- UPDATE 정책입니다.
--
-- using (auth.uid() = id):
--   현재 로그인한 사용자가 자기 profile row만 수정 대상으로 선택할 수 있습니다.
--
-- with check (auth.uid() = id):
--   수정 후에도 row의 id가 자기 사용자 id와 같아야 합니다.
--
-- 두 조건을 함께 두면,
-- "내 profile만 수정 가능"하고,
-- "수정하면서 다른 사용자 id로 바꾸는 것"도 막을 수 있습니다.
create policy "ex90 profiles update own"
on ex90_profiles
for update
using (auth.uid() = id)
with check (auth.uid() = id);
