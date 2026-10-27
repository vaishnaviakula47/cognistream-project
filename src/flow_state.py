"""
CogniStream - Preliminary Focus Classification
"""

def classify_focus(session_minutes, switches_per_hour):
"""
Apply simple illustrative rules to activity indicators.
These rules are not scientifically validated.
"""
if session_minutes < 0 or switches_per_hour < 0:
return "Invalid Input"

if session_minutes >= 25 and switches_per_hour <= 3:
    return "High Focus Indicator"

if session_minutes >= 10 and switches_per_hour <= 8:
    return "Moderate Focus Indicator"

return "Low Focus Indicator"

if name == "main":
print(classify_focus(30, 2))
print(classify_focus(15, 5))
print(classify_focus(5, 10))
