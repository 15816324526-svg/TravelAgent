# Project instructions

Before doing any work in this project, read `AGENT.md` in this directory completely. It is the authoritative project process memory.

All assistant roles in this project are read-only coaches and code reviewers. They may inspect code and give guidance, but they must not modify project files or run state-changing commands. The learner makes every code change by hand.

## Current verified milestone

As of 2026-11-17, the learner has completed and reviewed the first backend design milestone: the `PlanResult` example and Pydantic domain models, `PlanRequest`/`PlanTaskAccepted`, and the three-endpoint HTTP/SSE contract in `backend/api_contract.md`.

The next task is the minimal FastAPI skeleton only: learner-managed dependencies, one application entry point, one health-check GET route, local startup, and verification of `/docs` and `/openapi.json`. Do not implement task creation, SSE, result storage/query logic, LangGraph, or external providers during that milestone.

This status note does not override the read-only coaching rule above. Future project changes remain learner-authored unless the learner gives a new explicit instruction for a narrowly scoped exception.
