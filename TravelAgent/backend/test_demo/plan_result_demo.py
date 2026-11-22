from model.plan_model import PlanResult
from pathlib import Path

json_text = Path("draft.json").read_text(encoding="utf-8")

plan_result = PlanResult.model_validate_json(json_text)

print(plan_result)

print(plan_result.model_dump_json(indent=2))

# plan_result=PlanResult(
#     result_id = "001_01",
#     title = "杭州，刚刚好的2日漫游",
#     generated_at = "2026-11-13T20:30:00+08:00",
#     cover_image_url = null,
#     preferences = PlanPreferences(
#         destination = "杭州",
#         start_date = "2026-12-10",
#         end_date = "2026-12-11",
#         traveler_count = 2,
#         transport_modes = list[str] = ["公共交通","步行","出租车"],
#         accommodation_types: list[str] = ["酒店"],
#         budget_per_night = 500,
#         special_requirements = "希望行程节奏舒缓，保留午后休息时间",
#     ),
#     days: list[DayPlan] = [
#         {
#             day_number = 1,
#             today_date = "2026-12-10",
#             title = "沿着西湖慢慢走",
#             weather = Weather(
#                 condition = "晴间多云",
#                 min_temperature_c = 10,
#                 max_temperature_c = 12, 
#             )
#             activities: list[Activity] = [
#                 {
#                     start_time = "09:00",
#                     sequence = 1,
#                     place = Place(
#                             name = "断桥残雪",
#                             address = "杭州市西湖区北山街",
#                             longitude =  120.0,
#                             latitude = 30.0,
#                         )
#                     description = "从西湖北岸出发，看湖面与宝石山相映。",
#                     recommendation_reason = "上午人流相对舒缓，适合作为认识西湖的第一站。",
#                     advice = "上午湖边风大，建议携带薄外套。",
#                     transport_to_next = Transport(
#                         mode = "步行",
#                         duration_min = 20,
#                         distance_km = 1.8,
#                     )
#                     recommended_stay_minutes = 45,
#                 }
#             ]
#             tips = "15:45后自由休息。返回凤起路住宿区，可乘地铁或出租车，约30分钟。",
#         }
#     ],
#     hotel = HotelRecommendation(
#         data_source = "fixture",
#         name = "龚总大酒店",
#         address = "杭州市西湖区北山街114514号",
#         room_type = "双人间",
#         room_count = 1, 
#         nights = 1,
#         price_per_night = 420,
#         currency = "CNY"
#         recommendation_reason = "龚总是CEO，住了有好果子吃。",
#         price_note = "模拟数据，实际价格以获授权渠道查询结果为准",
#     ),
#     cost_estimate = CostEstimate(
#         currency = "CNY",
#         items = list[CostItem] = [
#             {
#                 category = "accommodation",
#                 label = "住宿 · 1晚",
#                 amount = 420,
#             },
#             {
#                 category = "food",
#                 label = "餐饮 · 2天",
#                 amount = 420,
#             },
#             {
#                 category = "tickets",
#                 label = "门票",
#                 amount = 60,
#             },
#             {
#                 category = "local_transport",
#                 label = "市内交通",
#                 amount = 200,
#             }
#         ]
#         total_amount = 1100,
#         note = "预估二人消费 1100元",
#     )
# )