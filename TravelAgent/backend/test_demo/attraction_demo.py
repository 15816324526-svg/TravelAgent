from model.plan_model import Place
from tool.fake_attraction_tool import get_fake_attraction

attraction = Place(
    name = "平湖秋月",
    address = "杭州西湖北门街",
    longitude= 120.15,
    latitude= 35.12,
)

print(attraction,"\n")
print(attraction.model_dump(),"\n")
print(Place.model_json_schema(),"\n")

try:
    get_fake_attraction(
        destination="杭州",
        limit= 2,
    )
except ValueError as error:
    assert "杭州" in str(error)
else:
    raise AssertionError("查询不存在的城市时抛出ValueError")