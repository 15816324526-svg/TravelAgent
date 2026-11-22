from pydantic import BaseModel, Field
from datetime import date, datetime, time

class Weather(BaseModel):
    condition: str = Field(description="天气状况，例如晴间多云")
    min_temperature_c: float = Field(description="最低气温，单位为摄氏度")
    max_temperature_c: float = Field(description="最高气温，单位为摄氏度")

class Place(BaseModel):
    name: str = Field(description="地点名称")
    address: str = Field(description="地点地址")
    longitude: float = Field(
        ge=-180,
        le=180,
        description="经度，范围为 -180 到 180",
    )
    latitude: float = Field(
        ge=-90,
        le=90,
        description="纬度，范围为 -90 到 90",
    )

class Transport(BaseModel):
    mode: str = Field(description="前往下一个地点的交通方式")
    duration_minutes: int = Field(
        gt= 0,
        description="交通时间",
    )
    distance_km: float = Field(
        ge= 0,
        description="交通距离",
    )

class Activity(BaseModel):
    start_time: time = Field(description="开始时间")
    sequence: int = Field(
        ge=1,
        description="第n个景点",
    )
    place: Place = Field(description="游玩景点")
    description: str = Field(description="景点描述")
    recommendation_reason: str = Field(description="推荐原因")
    advice: str = Field(description="游玩建议")
    transport_to_next: Transport | None = Field(
        description="前往下一个地点的交通信息"
    )
    recommended_stay_minutes: int = Field(
        gt=0,
        description="建议游玩时间",
    )

class DayPlan(BaseModel):
    day_number: int = Field(
        ge=1,
        description="游玩第N天",)
    today_date: date = Field(description="行程日期")
    title: str = Field(description="当天行程标题")
    weather: Weather = Field(description="当天的天气预报")
    activities: list[Activity] = Field(
        min_length=1,
        description="当天活动表",)
    tips: str = Field(description="贴心的提醒")

class PlanPreferences(BaseModel):
    destination: str = Field(description="城市")
    start_date: date = Field(description="起始日期")
    end_date: date = Field(description="结束日期")
    traveler_account: int = Field(
        ge=1,
        description="旅行人数",)
    transport_modes: list[str] = Field(
        min_length=1,
        description="可选择的出行方式",)
    accommodation_types: list[str] = Field(
        min_length=1,
        description="可选择的居住方式",)
    budget_per_night: float = Field(
        ge=0,
        description="每晚居住预算"
    )
    special_requirements: str | None = Field(
        max_length= 2000,
        description="额外要求",
    )

class HotelRecommendation(BaseModel):
    data_source: str = Field(description="搜索来源 API")
    name: str = Field(description="酒店名称")
    address: str =Field(description="酒店地址")
    room_type: str = Field(description="房型")
    room_count: int = Field(
        ge=1,
        description="房间数量",)
    nights: int = Field(
        ge=1,
        description="住几个晚上",)
    price_per_night: float = Field(
        ge=0,
        description="每晚价格")
    currency: str = Field(description="货币")
    recommendation_reason: str = Field(description="推荐原因")
    price_note: str = Field(description="价格标签")

class CostItem(BaseModel):
    category: str = Field(description="消费项目")
    label: str = Field(description="消费具体情况")
    amount:float = Field(
        ge=0,
        description="此项消费",)

class CostEstimate(BaseModel):
    currency: str = Field(description="费用使用的货币代码")
    items: list[CostItem] = Field(
        min_length=1,
        description="消费项目总览",
    )
    total_amount: float = Field(
        ge=0,
        description="总价格",
    )
    note: str = Field(description="预估消费")

class PlanResult(BaseModel):
    result_id: str = Field(description="")
    title: str = Field(description="")
    generated_at: datetime = Field(description="")
    cover_image_url: str | None = Field(description="")
    preferences: PlanPreferences = Field(description="")
    days: list[DayPlan] = Field(
        min_length=1,
        description="",
    )
    hotel: HotelRecommendation = Field(description="")
    cost_estimate: CostEstimate = Field(description="")