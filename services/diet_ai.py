import requests
import time


# ---------------------------------------------------
# COMMON REQUEST FUNCTION
# ---------------------------------------------------
def call_api(url, headers, payload):
    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            return f"API Error {response.status_code}: {response.text}"

        data = response.json()

        if "choices" not in data:
            return f"API Error: {data}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Request Failed: {str(e)}"


# ---------------------------------------------------
# GENERATE DIET PLAN (GROQ)
# ---------------------------------------------------
def generate_diet(prompt, api_key):

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    return call_api(
        "https://api.groq.com/openai/v1/chat/completions",
        headers,
        payload
    )


# ---------------------------------------------------
# VERIFY DIET PLAN (GROQ ONLY - Removed OpenRouter)
# ---------------------------------------------------
def verify_diet(draft, api_key):

    time.sleep(2)   # avoid rate limit

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "user",
                "content": f"""
You are a clinical nutrition AI.

Your task:
1. Improve this diet plan
2. Fix nutrition gaps
3. Respect allergies
4. Make it healthy
5. Return structured 7-day diet plan

Diet Plan:
{draft}
"""
            }
        ]
    }

    return call_api(
        "https://api.groq.com/openai/v1/chat/completions",
        headers,
        payload
    )


# ---------------------------------------------------
# GENERATE GROCERY LIST
# ---------------------------------------------------
def generate_grocery(diet, api_key):

    time.sleep(2)   # avoid rate limit

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "user",
                "content": f"""
Create grocery list from this diet.

Return grouped food items only.

Diet:
{diet}
"""
            }
        ]
    }

    return call_api(
        "https://api.groq.com/openai/v1/chat/completions",
        headers,
        payload
    )