from model.plan_model import Weather

from datetime import date

from tool.fake_weather_tool import get_fake_weather

weather=Weather(
    condition="晴间多云",
    min_temperature_c=10,
    max_temperature_c=12,
)

print(weather,"\n")
print(weather.model_dump(),"\n")  
print(Weather.model_json_schema(),"\n")

try:
    get_fake_weather(
        destination="广州",
        start_date=date(2026,12,10),
        end_date=date(2026,12,11),
    )
except ValueError as error:
    assert "广州" in str(error)
else:
    raise AssertionError("查询不存在的城市时应抛出 ValueError")