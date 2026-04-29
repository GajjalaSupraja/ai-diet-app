import requests


def generate_diet(prompt, api_key):

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    data = response.json()

    if "choices" not in data:
        return f"API Error: {data}"

    return data["choices"][0]["message"]["content"]


def verify_diet(draft, api_key):

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json={
            "model": "meta-llama/llama-3.1-8b-instruct",
            "messages": [
                {
                    "role": "user",
                    "content": f"""
You are a clinical nutrition AI.

Your job:
1. Verify diet
2. Fix nutrition issues
3. Respect allergy
4. Improve meals
5. Return structured output

Return EXACT format:

CHANGES MADE
========================
- change 1
- change 2
- change 3

========================
FINAL VERIFIED 7 DAY DIET
========================

Day 1:
Breakfast:
Lunch:
Snack:
Dinner:

Day 2:
Breakfast:
Lunch:
Snack:
Dinner:

Day 3:
Breakfast:
Lunch:
Snack:
Dinner:

Day 4:
Breakfast:
Lunch:
Snack:
Dinner:

Day 5:
Breakfast:
Lunch:
Snack:
Dinner:

Day 6:
Breakfast:
Lunch:
Snack:
Dinner:

Day 7:
Breakfast:
Lunch:
Snack:
Dinner:

Diet Plan:
{draft}
"""
                }
            ]
        }
    )

    data = response.json()

    if "choices" not in data:
        return f"API Error: {data}"

    return data["choices"][0]["message"]["content"]
def generate_grocery(diet, api_key):

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json={
            "model":"llama-3.1-8b-instant",
            "messages":[
                {
                    "role":"user",
                    "content":f"""
Create grocery list from this diet.

Return only food items grouped.

Diet:
{diet}
"""
                }
            ]
        }
    )

    data = response.json()

    if "choices" not in data:
        return "Error generating grocery"

    return data["choices"][0]["message"]["content"]