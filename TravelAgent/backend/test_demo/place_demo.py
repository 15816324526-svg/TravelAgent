from model.plan_model import Place

place=Place(
    name= "断桥残雪",
    address= "杭州西湖北门街",
    longitude= 78,
    latitude= 80,
)

print(place,"\n \n")

print(place.model_dump(),"\n \n")

print(Place.model_json_schema())