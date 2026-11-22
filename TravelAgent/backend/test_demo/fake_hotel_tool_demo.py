from model.agent_model import HotelAgentResult
from tool.fake_hotel_tool import get_fake_hotel

result = get_fake_hotel(
    destination="杭州",
    budget_per_night= 500,
)

assert isinstance(result, HotelAgentResult)
assert result.recommendation.price_per_night == 420
assert result.recommendation.price_per_night <= 500

print(result.model_dump())
print("Hotel pass")