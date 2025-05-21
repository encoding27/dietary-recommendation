from fastapi import APIRouter
from pydantic import BaseModel
from function import scrape_pubmed, generate_diet_recommendation

router = APIRouter()

class UserRequest(BaseModel):
    user_input: str
    allergies: list[str] = []

@router.post("/recommend")
def get_diet_recommendation(data: UserRequest):
    articles = scrape_pubmed(data.user_input)
    recommendation = generate_diet_recommendation(data.user_input, data.allergies, articles)
    return {"recommendation": recommendation}
