from typing import Dict, Any
import json
import httpx

# 🔒 HARD-CODED FIBO CONFIG (LOCAL / DEMO ONLY)
FIBO_API_KEY = "e0fb0ff533014c88ab8563e21313aa82"
FIBO_RENDER_URL = "https://engine.prod.bria-api.com/v2/image/generate"

print("DEBUG[ENV]: FIBO_API_KEY set:", bool(FIBO_API_KEY))
print("DEBUG[ENV]: FIBO_RENDER_URL:", FIBO_RENDER_URL)


async def translate_with_fibo(raw_text: str) -> Dict[str, Any]:
    """
    Use Bria V2 /image/generate with a text prompt to:
      - generate an image
      - get back the structured_prompt JSON + seed
    """
    if not FIBO_RENDER_URL or not FIBO_API_KEY:
        # Fallback for local dev: just wrap the raw text
        print("DEBUG[FIBO_TRANSLATE]: FIBO config not set, using local fallback structured prompt")
        return {
            "structured_prompt": {
                "short_description": raw_text[:200],
                "background_setting": "Dev mode: FIBO not configured",
                "style_medium": "photograph",
                "context": "Local development placeholder",
                "artistic_style": "realistic",
            },
            "seed": None,
        }

    headers = {
        # Bria V2: use api_token header
        "api_token": FIBO_API_KEY,
        "Content-Type": "application/json",
    }

    payload: Dict[str, Any] = {
        "prompt": raw_text,
        "model_version": "FIBO",     # lock to FIBO model
        "sync": True,                # 200 + result instead of async polling
    }

    print("DEBUG[FIBO_TRANSLATE]: POST", FIBO_RENDER_URL)
    print("DEBUG[FIBO_TRANSLATE]: Payload:", json.dumps(payload, indent=2))

    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(
            FIBO_RENDER_URL,
            json=payload,
            headers=headers,
        )
        print("DEBUG[FIBO_TRANSLATE]: Status:", resp.status_code)
        print("DEBUG[FIBO_TRANSLATE]: Response snippet:", resp.text[:500])
        resp.raise_for_status()
        data = resp.json()

    # Expected 200 schema:
    # {
    #   "result": {
    #       "image_url": "...",
    #       "seed": 123,
    #       "structured_prompt": "<stringified JSON>"
    #   },
    #   "request_id": "..."
    # }
    result = data.get("result") or {}
    structured_prompt_str = result.get("structured_prompt")
    seed = result.get("seed")

    if structured_prompt_str:
        try:
            structured_prompt_dict = json.loads(structured_prompt_str)
        except json.JSONDecodeError:
            print("WARN[FIBO_TRANSLATE]: structured_prompt is not valid JSON string, returning raw text")
            structured_prompt_dict = {"structured_prompt_raw": structured_prompt_str}
    else:
        structured_prompt_dict = {
            "short_description": raw_text[:200],
            "note": "No structured_prompt returned from API",
        }

    print("DEBUG[FIBO_TRANSLATE]: Parsed structured prompt keys:", list(structured_prompt_dict.keys()))
    print("DEBUG[FIBO_TRANSLATE]: Seed from result:", seed)

    return {
        "structured_prompt": structured_prompt_dict,
        "seed": seed,
    }


def build_fibo_json_from_metadata(metadata: Dict[str, Any], fibo_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Combine FIBO's structured prompt + seed with our emotional metadata.
    """
    structured_prompt = fibo_info.get("structured_prompt") or {}
    seed = fibo_info.get("seed")

    combined = {
        "fibo_structured_prompt": structured_prompt,
        "seed": seed,
        "our_metadata": {
            "emotion": metadata.get("emotion"),
            "timeOfDay": metadata.get("timeOfDay"),
            "locationType": metadata.get("locationType"),
            "weather": metadata.get("weather"),
            "warmth": metadata.get("warmth"),
            "primarySubject": metadata.get("primarySubject"),
            "isDoctorUncle": metadata.get("isDoctorUncle"),
        },
    }
    print("DEBUG[FIBO_BUILD]: Combined fibo_json keys:", list(combined.keys()))
    return combined


async def render_with_fibo(fibo_json: Dict[str, Any]) -> str:
    """
    Use Bria V2 /image/generate with structured_prompt (+ seed) to generate an image.
    """
    if not FIBO_RENDER_URL or not FIBO_API_KEY:
        print("DEBUG[FIBO_RENDER]: FIBO config not set, using placeholder image")
        return "https://picsum.photos/512/288"

    headers = {
        "api_token": FIBO_API_KEY,
        "Content-Type": "application/json",
    }

    structured = fibo_json.get("fibo_structured_prompt") or {}
    seed = fibo_json.get("seed")

    structured_prompt_str = json.dumps(structured)

    payload: Dict[str, Any] = {
        "structured_prompt": structured_prompt_str,
        "model_version": "FIBO",
        "sync": True,
    }

    if seed is not None:
        payload["seed"] = seed

    print("DEBUG[FIBO_RENDER]: POST", FIBO_RENDER_URL)
    print("DEBUG[FIBO_RENDER]: Payload snippet:", json.dumps(payload, indent=2)[:600])

    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(
            FIBO_RENDER_URL,
            json=payload,
            headers=headers,
        )
        print("DEBUG[FIBO_RENDER]: Status:", resp.status_code)
        print("DEBUG[FIBO_RENDER]: Response snippet:", resp.text[:500])
        resp.raise_for_status()
        data = resp.json()

    result = data.get("result") or {}
    image_url = result.get("image_url") or result.get("imageUrl") or result.get("url") or ""

    print("DEBUG[FIBO_RENDER]: Final image URL:", image_url)
    print("DEBUG[FIBO_RENDER]: Seed returned:", result.get("seed"))
    return image_url
