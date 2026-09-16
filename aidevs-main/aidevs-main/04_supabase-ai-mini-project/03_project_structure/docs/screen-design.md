# Screen Design

이 문서는 팀 프로젝트의 화면 설계서 starter입니다.

`02_project-deliverables/02_screen-design-sample.md`를 참고해 실제 화면 기준으로 수정하세요.

## 작성할 내용

- 화면 목록
- 정보 구조
- 주요 컴포넌트
- 사용자 액션과 시스템 반응
- 에러/로딩/빈 상태 화면

## 화면 예시

| 화면 | 주요 내용 |
| --- | --- |
| 메인 대시보드 | 실시간 로그, 최근 로그 테이블, 요약 지표 |
| 로그 상세 | 로그 메시지, status code, latency, metadata |
| 피드백 입력 | rating, comment, improvement note |
| 설정 | backend URL, 새로고침 간격, 필터 |
| 에러 화면 | backend 연결 실패, 권한 오류, 데이터 없음 |

## 컴포넌트 예시

- 로그 레벨 필터
- 최근 로그 테이블
- latency 차트
- status code 분포 차트
- SSE 연결 상태 표시
- 피드백 입력 폼
