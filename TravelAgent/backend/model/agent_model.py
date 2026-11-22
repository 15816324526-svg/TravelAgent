from pydantic import BaseModel, Field

from datetime import date

from model.plan_model import Weather,Place,HotelRecommendation

from typing import Literal

class DatedWeather(BaseModel):
    today_date: date = Field(
        description="",
    )
    weather: Weather = Field(
        description="",
    )

class WeatherAgentResult(BaseModel):
    days: list[DatedWeather] = Field(
        min_length=1,
        description="旅行日期对应的天气结果",
    )

class AttractionCandidate(BaseModel):
    place: Place = Field(
        description="",
    )
    description: str = Field(
        description="",
    )
    recommendation_reason: str = Field(
        description="",
    )
    recommended_stay_minutes: int =Field(
        gt=0,
        description="建议停留时间，单位为分钟",
    )

class AttractionAgentResult(BaseModel):
    places: list[AttractionCandidate] = Field(
        min_length=1,
        description="",
    )

class HotelAgentResult(BaseModel):
    recommendation: HotelRecommendation = Field(
        description="",
    )

class CoordinatorDecision(BaseModel):
    next_agent: Literal["weather","attraction", "hotel","finalize","fail"] = Field(
        description="协调Agent决定的下一步"
    )
    reason: str = Field(
        description="",
    )

class AgentError(BaseModel):
    agent: Literal["weather","attraction","hotel","coordinator"] = Field(
        description="发生错误的Agent"
    )
    message: str = Field(
        description="",
    )