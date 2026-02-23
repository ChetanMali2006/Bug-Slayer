from geopy.distance import geodesic

def find_nearby(user_location, toilets, radius=2):

    nearby = []

    for toilet in toilets:
        toilet_location = (toilet["lat"], toilet["lon"])
        distance = geodesic(user_location, toilet_location).km

        if distance <= radius:
            toilet["distance"] = round(distance, 2)
            nearby.append(toilet)

    return nearby