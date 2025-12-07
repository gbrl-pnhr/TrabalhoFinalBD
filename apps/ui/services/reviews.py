import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
from typing import List
from apps.api.modules import ReviewResponse, ReviewCreate, ReviewUpdate
from apps.ui.services.api_client import APIClient

class ReviewService:
    def __init__(self):
        self.client = APIClient()

    def create_review(self, review: ReviewCreate) -> ReviewResponse:
        data = self.client.post("/reviews/", review.model_dump())
        return ReviewResponse.model_validate(data)

    def get_reviews_by_dish(self, dish_id: int) -> List[ReviewResponse]:
        data = self.client.get(f"/reviews/dish/{dish_id}")
        return [ReviewResponse.model_validate(r) for r in data]

    def update_review(self, review_id: int, updates: ReviewUpdate) -> ReviewResponse:
        """
        Update a single review using the ReviewUpdate schema.
        """
        data = self.client.patch(
            f"/reviews/{review_id}",
            updates.model_dump(exclude_unset=True)
        )
        return ReviewResponse.model_validate(data)

    def delete_review(self, review_id: int) -> None:
        """Delete a review."""
        self.client.delete(f"/reviews/{review_id}")