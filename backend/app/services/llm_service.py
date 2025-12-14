from typing import Dict


async def parse_memory_to_metadata(text: str) -> Dict:
    """
    Simple rule-based 'LLM stub' that extracts richer metadata
    from the memory text. Later you can replace this with a real LLM call.
    """
    lower = text.lower()

    # --- Emotion ---
    if any(word in lower for word in ["miss", "wish", "remember", "used to"]):
        emotion = "nostalgia"
    elif any(word in lower for word in ["sad", "cry", "lonely", "regret"]):
        emotion = "sad"
    elif any(word in lower for word in ["happy", "laugh", "smile", "joy"]):
        emotion = "happy"
    elif any(word in lower for word in ["scared", "afraid", "anxious"]):
        emotion = "anxious"
    else:
        emotion = "bittersweet"

    # --- Time of day ---
    if "sunset" in lower or "dusk" in lower or "evening" in lower:
        time_of_day = "evening"
    elif "sunrise" in lower or "dawn" in lower or "early morning" in lower:
        time_of_day = "sunrise"
    elif "morning" in lower:
        time_of_day = "morning"
    elif "night" in lower or "midnight" in lower:
        time_of_day = "night"
    elif "afternoon" in lower:
        time_of_day = "afternoon"
    else:
        time_of_day = "unspecified"

    # --- Location type / environment ---
    if any(word in lower for word in ["bedroom", "living room", "sofa", "couch", "kitchen"]):
        location_type = "room"
    elif any(word in lower for word in ["home", "house", "inside", "indoors"]):
        location_type = "indoor"
    elif "balcony" in lower:
        location_type = "balcony"
    elif "rooftop" in lower or "roof" in lower:
        location_type = "rooftop"
    elif "beach" in lower:
        location_type = "beach"
    elif "park" in lower:
        location_type = "park"
    elif "street" in lower or "road" in lower:
        location_type = "street"
    else:
        # rough guess: if we see obvious outdoor cues, assume outdoor
        if any(word in lower for word in ["sky", "trees", "wind", "outside", "open air"]):
            location_type = "outdoor"
        else:
            location_type = "indoor"

    # --- Weather / atmosphere ---
    if "rain" in lower or "rainy" in lower:
        weather = "rainy"
    elif "snow" in lower or "snowy" in lower:
        weather = "snowy"
    elif "cloudy" in lower or "overcast" in lower:
        weather = "cloudy"
    elif "storm" in lower or "thunder" in lower:
        weather = "stormy"
    else:
        weather = "clear"

    # --- Warmth of memory / visual tone ---
    if any(word in lower for word in ["chai", "tea", "blanket", "home", "cozy", "warm", "hot chocolate"]):
        warmth = "warm"
    elif any(word in lower for word in ["cold", "winter", "wind", "rain"]):
        warmth = "cool"
    else:
        warmth = "neutral"

    # --- Subject hints (for focus_subject) ---
    if "grandmother" in lower or "grandma" in lower:
        primary_subject = "grandmother"
    elif "mother" in lower or "mom" in lower:
        primary_subject = "mother"
    elif "father" in lower or "dad" in lower:
        primary_subject = "father"
    elif "uncle" in lower:
        primary_subject = "uncle"
    elif "friend" in lower or "best friend" in lower:
        primary_subject = "friend"
    else:
        primary_subject = "unspecified_person"

    # --- Special case: doctor uncle ---
    is_doctor_uncle = False
    if "uncle" in lower and ("doctor" in lower or "clinic" in lower or "mbbs" in lower or "md" in lower):
        is_doctor_uncle = True

    return {
        "emotion": emotion,
        "timeOfDay": time_of_day,
        "locationType": location_type,
        "weather": weather,
        "warmth": warmth,
        "primarySubject": primary_subject,
        "rawText": text,
        "isDoctorUncle": is_doctor_uncle,
    }
