from tool.fake_attraction_tool import get_fake_attraction
from model.agent_model import AttractionCandidate, AttractionAgentResult

result = get_fake_attraction(
    destination="杭州",
    limit=2,
)

assert isinstance(result, AttractionAgentResult)
assert len(result.places) == 2
assert result.places[0].place.name != ""
assert result.places[0].recommended_stay_minutes > 0

print(result.model_dump())
print("\n")
print("attraction pass")