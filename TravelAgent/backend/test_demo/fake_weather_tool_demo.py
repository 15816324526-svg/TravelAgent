from tool.fake_weather_tool import get_fake_weather
from datetime import date
from model.agent_model import WeatherAgentResult

result = get_fake_weather(
    destination="杭州",
    start_date=date(2026,12,10),
    end_date=date(2026,12,11),
)

assert isinstance(result, WeatherAgentResult)
assert len(result.days) == 2
assert result.days[0].today_date == date(2026,12,10)
assert result.days[1].today_date == date(2026,12,11)

print(result.model_dump())
