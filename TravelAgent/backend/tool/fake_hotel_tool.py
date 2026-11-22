from model.agent_model import HotelAgentResult, HotelRecommendation
from model.plan_model import PlanPreferences, HotelRecommendation

FAKE_HOTEL_DATA: dict[str, list[HotelRecommendation]] = {
    "杭州": [
        HotelRecommendation(
            data_source="",
            name="",
            address="",
            room_type="",
            room_count= 1,
            nights= 1,
            price_per_night= 420,
            currency="CNY",
            recommendation_reason="靠近地铁1、2号线，到西湖东岸方便。优先选择内街、非临街房型，兼顾安静与出行效率。",
            price_note="仅推荐住宿区域与参考价，未预订具体房源。",  
        ),
    ]
}

def get_fake_hotel(
        destination: str,
        budget_per_night: float,
) -> HotelAgentResult:
    if budget_per_night < 0:
        raise ValueError("你有见过住酒店为负数的吗（-白眼-）")

    #根据destination查找酒店列表
    city_hotels = FAKE_HOTEL_DATA.get(destination)

    #城市不存在时抛出 ValueError
    if city_hotels is None:
        raise ValueError(f"没有城市{destination}的景点信息")

    #找出价格不超过预算的酒店
    selected_hotels: list[HotelRecommendation] = []

    for hotel in city_hotels:
        if hotel.price_per_night <= budget_per_night:
            selected_hotels.append(hotel)

    #没有符合预算的酒店时抛出 ValueError
    if not selected_hotels :
        raise ValueError(f"城市{destination}没有符合需求的酒店")

    cheapest_hotel = min(
        selected_hotels,
        key=lambda hotel: hotel.price_per_night,
    )

    return HotelAgentResult(recommendation=cheapest_hotel)