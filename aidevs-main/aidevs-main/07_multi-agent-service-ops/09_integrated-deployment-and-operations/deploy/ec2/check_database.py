"""Check real DB schema and write permissions without retaining probe rows."""
import os
from uuid import uuid4

import psycopg


def main():
    with psycopg.connect(os.environ["DATABASE_URL"], connect_timeout=5) as conn:
        try:
            task_id = "deploy-probe-" + uuid4().hex
            conn.execute(
                "INSERT INTO mini_multi_agent_08.travel_task_runs "
                "(task_id, trace_id, user_id, request, status) VALUES (%s,%s,%s,%s,%s)",
                (task_id, task_id, "deployment", "database probe", "completed"),
            )
            conn.execute(
                "INSERT INTO mini_multi_agent_08.travel_trace_events "
                "(task_id,trace_id,sequence,actor,action,status) VALUES (%s,%s,1,'deployment','probe','completed')",
                (task_id, task_id),
            )
            assert conn.execute(
                "SELECT status FROM mini_multi_agent_08.travel_task_runs WHERE task_id=%s",
                (task_id,),
            ).fetchone() == ("completed",)
        finally:
            conn.rollback()
    print("PostgreSQL schema + task/trace write/read PASS (probe rolled back)")


if __name__ == "__main__":
    main()
