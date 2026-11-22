#NotRequired：该键可以暂时不存在；这与“键存在但值是 None”不同。
#TypedDict：描述字典允许有哪些键以及每个值的类型。
from typing import NotRequired, TypedDict

from api.api_model import PlanRequest
from backend.model.plan_model import CostEstimate, DayPlan, HotelRecommendation, PlanResult
from backend.model.agent_model import WeatherAgentResult,AttractionAgentResult,HotelAgentResult,CoordinatorDecision,AgentError

class PlanGraphState(TypedDict):
    #必须存在的request
    request: PlanRequest

    weather_result: NotRequired[WeatherAgentResult]
    attraction_result: NotRequired[AttractionAgentResult]
    hotel_result: NotRequired[HotelAgentResult]
    decision: NotRequired[CoordinatorDecision]
    iteration_count: NotRequired[int]

    #只在失败路径出现
    error: NotRequired[AgentError]
    result: NotRequired[PlanResult]