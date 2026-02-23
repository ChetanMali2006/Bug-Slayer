import random

def analyze_image(image_bytes):
    """
    Simulated AI cleanliness detection.
    Replace later with real YOLO / CNN model.
    """

    # Simulate detection
    garbage_detected = random.choice([True, False])
    water_present = random.choice([True, False])

    base_score = random.randint(60, 95)

    if garbage_detected:
        base_score -= 20

    if not water_present:
        base_score -= 10

    cleanliness_score = max(0, min(100, base_score))

    # Grade logic
    if cleanliness_score >= 85:
        grade = "A"
    elif cleanliness_score >= 70:
        grade = "B"
    elif cleanliness_score >= 50:
        grade = "C"
    else:
        grade = "D"

    return {
        "cleanliness_score": cleanliness_score,
        "grade": grade,
        "garbage_detected": garbage_detected,
        "water_present": water_present
    }