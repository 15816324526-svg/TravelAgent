from model.agent_model import WeatherAgentResult, DatedWeather
from datetime import date, timedelta
from model.plan_model import Weather

FAKE_WEATHER_DATA: dict[str,dict[date,Weather]] = {
    "杭州": {
      date(2026,12,10): Weather(
        condition="晴间多云",
        min_temperature_c=10,
        max_temperature_c=15,
      ),
      date(2026,12,11): Weather(
        condition="晴间多云",
        min_temperature_c=11,
        max_temperature_c=14,
      )
    }
}

def get_fake_weather(
        destination: str,
        start_date: date,
        end_date: date,    
) -> WeatherAgentResult:
  #检查日期顺序
  if start_date>end_date:
    raise ValueError("开始日期不能晚于结束日期")

  #逐日查找 Weather
  city_weather = FAKE_WEATHER_DATA.get(destination)

  #逐日查找Weather报错
  if city_weather is None:
    raise ValueError(f"没有城市 {destination} 的天气模拟数据")

  #创建 DatedWeather
  days: list[DatedWeather] = [] 
  current_date = start_date

  while current_date <= end_date:
    weather = city_weather.get(current_date)

    if weather is None:
      raise ValueError(
        f"没有 {destination} 在 {current_date} 的天气模拟数据"
      )

    dated_weather = DatedWeather(
      today_date=current_date,
      weather=weather,
    )
    #把datedweather塞到days列表去
    days.append(dated_weather)

    #进入循环前+1天
    current_date += timedelta(days=1)

  return WeatherAgentResult(days=days)

    