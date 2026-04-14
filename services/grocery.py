import requests


def generate_grocery(diet_text, api_key):

    prompt = f"""
Create a grocery shopping list for the following 7-day diet plan.

Group items under:
- Vegetables
- Fruits
- Protein
- Grains
- Dairy / Alternatives
- Others

Diet Plan:
{diet_text}
"""

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    response = requests.post(url, headers=headers, json=payload)

    data = response.json()

    print("GROCERY DEBUG:", data)   # debug

    try:
        return data["choices"][0]["message"]["content"]
    except:
        return "Unable to generate grocery list."