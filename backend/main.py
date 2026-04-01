import json
import random
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
QUESTIONS_FILE = BASE_DIR / "backend" / "data" / "questions.json"


app.mount("/assets", StaticFiles(directory=FRONTEND_DIR), name="frontend-assets")


def load_questions():
    with QUESTIONS_FILE.open() as file:
        data = json.load(file)
        return data

@app.get("/")
async def index():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/charades/{charades_count}")
async def charades(
    charades_count: int = 10,
    categories: list[str] | None = None,
    difficulties: list[str] | None = None,
):
    questions = load_questions()
    available_questions = questions["questions"]

    if categories:
        category_set = set(categories)
        available_questions = [
            question for question in available_questions
            if category_set.intersection(question.get("category", []))
        ]

    if difficulties:
        difficulty_set = set(difficulties)
        available_questions = [
            question for question in available_questions
            if question.get("difficulty") in difficulty_set
        ]

    question_count = len(available_questions)
    if question_count == 0:
        return []

    if charades_count > question_count:
        charades_count = question_count

    random_questions = random.sample(available_questions, charades_count)
    return random_questions
