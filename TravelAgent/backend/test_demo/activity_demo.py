from backend.model.plan_model import Activity, Place, Transport

activity=Activity(
    start_time = "09:00", 
    sequence = 1, 
    place= Place(
        name = "断桥残雪",
        address = "西湖XX街XX路",
        longitude = 23.9,
        latitude = 34.9,
    ),
    description = "从西湖北岸出发，看湖面与宝石山相映。",
    recommendation_reason = "上午人流相对舒缓，适合作为认识西湖的第一站。",
    advice = "有点冷，多穿点，最好自带水",
    transport_to_next= Transport(
        mode = "步行",
        duration_minutes = 16,
        distance_km = 10.7,

    ),
    recommended_stay_minutes = 45,
)

print(activity,"\n")

print(activity.model_dump(),"\n")

print(Activity.model_json_schema())