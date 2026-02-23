from fastapi import FastAPI, UploadFile, File
import json
from datetime import datetime

from backend.geo_engine import find_nearby
from backend.recommendation_engine import recommend_best
from backend.ai_engine import analyze_image


app = FastAPI(
    title="HygieiaX Smart Toilet API",
    description="AI-powered smart public toilet recommendation and monitoring system",
    version="1.0"
)

DATABASE_PATH = "backend/database.json"


# ----------------------------
# Load database
# ----------------------------
def load_database():
    try:
        with open(DATABASE_PATH, "r") as f:
            return json.load(f)
    except:
        return []


# ----------------------------
# Save database
# ----------------------------
def save_database(data):
    with open(DATABASE_PATH, "w") as f:
        json.dump(data, f, indent=2)


# ----------------------------
# Home route
# ----------------------------
@app.get("/")
def home():
    return {
        "system": "HygieiaX Smart Toilet System",
        "status": "Running",
        "version": "1.0"
    }


# ----------------------------
# Get all toilets
# ----------------------------
@app.get("/toilets")
def get_toilets():
    return load_database()


# ----------------------------
# Find nearby toilets
# ----------------------------
@app.get("/nearby")
def nearby(lat: float, lon: float):

    toilets = load_database()

    nearby_toilets = find_nearby(
        user_location=(lat, lon),
        toilets=toilets
    )

    return {
        "user_location": {
            "lat": lat,
            "lon": lon
        },
        "results": nearby_toilets,
        "count": len(nearby_toilets)
    }


# ----------------------------
# Recommend best toilet
# ----------------------------
@app.get("/recommend")
def recommend(lat: float, lon: float):

    toilets = load_database()

    nearby_toilets = find_nearby(
        user_location=(lat, lon),
        toilets=toilets
    )

    best = recommend_best(nearby_toilets)

    return {
        "recommended": best,
        "based_on": [
            "cleanliness",
            "crowd",
            "water availability",
            "distance"
        ]
    }


# ----------------------------
# Update cleanliness score
# ----------------------------
@app.post("/update_cleanliness")
def update_cleanliness(toilet_id: int, score: int):

    toilets = load_database()

    for toilet in toilets:
        if toilet["id"] == toilet_id:
            toilet["cleanliness"] = score
            toilet["last_updated"] = str(datetime.now())

    save_database(toilets)

    return {
        "status": "updated",
        "toilet_id": toilet_id,
        "new_score": score
    }


# ----------------------------
# Update crowd level
# ----------------------------
@app.post("/update_crowd")
def update_crowd(toilet_id: int, crowd: int):

    toilets = load_database()

    for toilet in toilets:
        if toilet["id"] == toilet_id:
            toilet["crowd"] = crowd
            toilet["last_updated"] = str(datetime.now())

    save_database(toilets)

    return {
        "status": "updated",
        "toilet_id": toilet_id,
        "crowd": crowd
    }


# ----------------------------
# Update water availability
# ----------------------------
@app.post("/update_water")
def update_water(toilet_id: int, water: bool):

    toilets = load_database()

    for toilet in toilets:
        if toilet["id"] == toilet_id:
            toilet["water"] = water
            toilet["last_updated"] = str(datetime.now())

    save_database(toilets)

    return {
        "status": "updated",
        "toilet_id": toilet_id,
        "water": water
    }


# ----------------------------
# AI Image Analyze Endpoint
# ----------------------------
@app.post("/analyze")
async def analyze(toilet_id: int, file: UploadFile = File(...)):

    toilets = load_database()

    image_bytes = await file.read()

    result = analyze_image(image_bytes)

    # Update database automatically
    for toilet in toilets:
        if toilet["id"] == toilet_id:

            # create ai_metrics if not exists
            if "ai_metrics" not in toilet:
                toilet["ai_metrics"] = {}

            toilet["ai_metrics"]["cleanliness_score"] = result["cleanliness_score"]
            toilet["ai_metrics"]["grade"] = result["grade"]

            toilet["last_updated"] = str(datetime.now())

    save_database(toilets)

    return {
        "toilet_id": toilet_id,
        "analysis": result
    }