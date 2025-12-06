from typing import List
from services.api_client import APIClient
from schemas import ReviewResponse, ReviewCreate

class ReviewService:
    def __init__(self):
        self.client = APIClient()

    def create_review(self, review: ReviewCreate) -> ReviewResponse:
        data = self.client.post("/reviews/", review.model_dump())
        return ReviewResponse.model_validate(data)

    def get_reviews_by_dish(self, dish_id: int) -> List[ReviewResponse]:
        data = self.client.get(f"/reviews/dish/{dish_id}")
        return [ReviewResponse.model_validate(r) for r in data]