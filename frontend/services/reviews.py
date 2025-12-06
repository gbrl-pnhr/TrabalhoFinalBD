from typing import List, Dict, Any
from frontend.services.api_client import APIClient

class ReviewService:
    """
    Service layer for handling customer reviews.
    """

    def __init__(self):
        self.client = APIClient()

    def create_review(self, review_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Submit a new review.

        Args:
            review_data (Dict): {order_id, dish_id, customer_id, rating, comment}

        Returns:
            Dict: Created review object.
        """
        return self.client.post("/reviews/", review_data)

    def get_reviews_by_dish(self, dish_id: int) -> List[Dict[str, Any]]:
        """
        Get all reviews for a specific dish.

        Args:
            dish_id (int): The ID of the dish.

        Returns:
            List[Dict]: List of reviews.
        """
        return self.client.get(f"/reviews/dish/{dish_id}")