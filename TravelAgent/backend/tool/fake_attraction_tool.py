from model.agent_model import AttractionCandidate, AttractionAgentResult
from model.plan_model import Place

FAKE_ATTRACTION_DATA: dict[str,list[AttractionCandidate]] = {
    "杭州": [
        AttractionCandidate(
            place = Place(
                name="断桥残雪",
                address="杭州市西湖区北山街",
                longitude=120.15,
                latitude=30.26,
            ),
            description="西湖北岸的代表性景点。",
            recommendation_reason="适合作为西湖游览的起点。",
            recommended_stay_minutes=45,
        ),
        AttractionCandidate(
            place = Place(
                name="平湖秋月",
                address="杭州市西湖区北山街",
                longitude=120.15,
                latitude=31.26,
            ),
            description="沿白堤来到孤山一隅，坐看开阔的湖光山色。",
            recommendation_reason="一路平缓好走，园林与湖景兼得，不用赶路。",
            recommended_stay_minutes=70,
        )
    ]
}

def get_fake_attraction(
        destination: str,
        limit: int,
) -> AttractionAgentResult:
    #检查limit
    if limit < 1:
        raise ValueError("景点不能少于1个")

    #根据destination查找候选列表
    city_attractions = FAKE_ATTRACTION_DATA.get(destination)

    if city_attractions is None:
        raise ValueError(f"没有城市{destination}的景点信息")

    selected_attractions = city_attractions[:limit]

    if not selected_attractions:
        raise ValueError(f"城市{destination}没有可用景点")

    return AttractionAgentResult(places=selected_attractions)
        

    