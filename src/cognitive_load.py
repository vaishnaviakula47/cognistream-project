"""
Cognistream - Cognitive Load Estimation
"""

def estimate_cognitive_load(
    switches_per_hour,
    error_count,
    session_minutes
):
    if (
        switches_per_hour < 0
        or error_count < 0
        or session_minutes < 0
    ):
        return "Invalid Input"

    score = 0

    if switches_per_hour >= 10:
        score += 2
    elif switches_per_hour >= 5:
        score += 1

    if error_count >= 10:
        score += 2
    elif error_count >= 5:
        score += 1

    if session_minutes >= 120:
        score += 1

    if score >= 4:
        return "High Estimated Load"
    elif score >= 2:
        return "Moderate Estimated Load"

    return "Low Estimated Load"


if __name__ == "__main__":
    result = estimate_cognitive_load(6, 5, 90)
    print("Cognitive Load:", result)
