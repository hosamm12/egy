import os, asyncio, httpx, logging
from pydantic import BaseModel

BACKEND = os.getenv("AGENTS_BACKEND_URL", "http://backend:8000")
logger = logging.getLogger(__name__)

class Task(BaseModel):
    type: str
    payload: dict

class Planner:
    def plan(self, task: Task) -> list[str]:
        if task.type == "welcome_user":
            return ["create_user_if_needed", "trigger_welcome_email"]
        return ["noop"]

class Executor:
    async def execute(self, step: str, task: Task):
        async with httpx.AsyncClient(timeout=10.0) as client:
            if step == "create_user_if_needed":
                # ensure user exists
                email = task.payload.get("email")
                password = task.payload.get("password", "change_me_123")
                full_name = task.payload.get("full_name", "Guest")
                # Try register; if exists, ignore error
                try:
                    await client.post(f"{BACKEND}/auth/register", json={"email": email, "password": password, "full_name": full_name})
                except Exception:
                    pass
                return {"status": "ok"}
            if step == "trigger_welcome_email":
                # call backend celery task through a faux endpoint (health ping here as demo)
                try:
                    r = await client.get(f"{BACKEND}/health")
                except httpx.RequestError as exc:
                    logger.warning("backend health check request failed: %s", exc)
                    return {"status": "ok"}

                if not r.is_success:
                    logger.warning("backend health check returned %s", r.status_code)
                    return {"status": "ok"}

                try:
                    health = r.json()
                except ValueError as exc:
                    logger.warning("backend health check invalid JSON: %s", exc)
                    return {"status": "ok"}

                return {"status": "ok", "health": health}
            return {"status": "noop"}

async def main():
    planner = Planner()
    executor = Executor()

    sample = Task(type="welcome_user", payload={"email": "new.user@example.com", "password": "Welcome123", "full_name": "New User"})
    plan = planner.plan(sample)

    print("[agents] Plan:", plan)
    for step in plan:
        result = await executor.execute(step, sample)
        print("[agents] Step:", step, "=>", result)

if __name__ == "__main__":
    asyncio.run(main())
