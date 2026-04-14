from typing_extensions import final

from fastapi import FastAPI
from pydantic import BaseModel
from services.diet_ai import generate_diet, verify_diet
from services.grocery import generate_grocery
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


class DietRequest(BaseModel):
    age: int
    gender: str
    weight: float
    height: float
    goal: str
    diet: str
    activity: str
    allergy: str
    health: str


@app.post("/generate-diet")
def generate(request: DietRequest):

    prompt = f"""
Create structured 7-day diet plan.

Age: {request.age}
Gender: {request.gender}
Weight: {request.weight}
Height: {request.height}
Goal: {request.goal}
Diet: {request.diet}
Activity: {request.activity}
Allergy: {request.allergy}
Health: {request.health}

Return 7 days.
"""

    draft = generate_diet(prompt, GROQ_API_KEY)
    final = verify_diet(draft, OPENROUTER_API_KEY)

    grocery = generate_grocery(final, GROQ_API_KEY)

    return {
    "status": "success",
    "data": {
        "draft": draft,
        "final": final
    }
}