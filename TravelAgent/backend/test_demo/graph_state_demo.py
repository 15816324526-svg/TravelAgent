from api.api_model import PlanRequest

from agent.graph_state import PlanGraphState

plan_request = PlanRequest(
    destination="杭州",
    start_date="2026-12-10",
    end_date="2026-12-11",
    traveler_account = 1,
    transport_modes=["公共交通","步行"],
    accommodation_types=["酒店"],
    budget_per_night=500,
    special_requirements="希望行程节奏舒缓",
)

initial_state: PlanGraphState = {"request": plan_request}

#初始 State 只有 request 这个键
assert set(initial_state.keys()) == {"request"}
#State 中保存的就是刚才创建的同一个 PlanRequest 对象
assert initial_state["request"] is plan_request

#结果没有产生，当前没有错误
assert "weather_result" not in initial_state
assert "attraction_result" not in initial_state
assert "hotel_result" not in initial_state
assert "decision" not in initial_state
assert "iteration_count" not in initial_state
assert "error" not in initial_state
assert "result" not in initial_state

print("initial state verification passed")
print(initial_state)

