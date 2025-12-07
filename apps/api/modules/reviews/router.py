import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from apps.api.core.database import get_db_connection
from packages.common.src.models.reviews_models import ReviewCreate, ReviewResponse, ReviewUpdate
from apps.api.modules.reviews.repository import ReviewRepository

router = APIRouter(prefix="/reviews", tags=["Reviews"])
logger = logging.getLogger(__name__)


def get_repository(conn=Depends(get_db_connection)):
    """Dependency injection for ReviewRepository."""
    return ReviewRepository(conn)


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(
    review: ReviewCreate, repo: ReviewRepository = Depends(get_repository)
):
    """
    Submit a review for a dish ordered by a customer.

    Enforces:
    1. Unique constraint: Customer + Order + Dish.
    2. Eligibility: Customer must have ordered the item in that order.
    """
    try:
        return repo.create_review(review)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve),
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        error_msg = str(e).lower()
        if "unique constraint" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This customer has already reviewed this dish for this order.",
            )
        if "foreign key constraint" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Referenced Customer, Dish, or Order ID not found.",
            )

        logger.error(f"API Error create_review: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.patch("/{review_id}", response_model=ReviewResponse)
def update_review(
    review_id: int,
    review_update: ReviewUpdate,
    repo: ReviewRepository = Depends(get_repository)
):
    """
    Update the rating or comment of an existing review.
    """
    try:
        updated_review = repo.update_review(review_id, review_update)
        if not updated_review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found."
            )
        return updated_review
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"API Error update_review: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


@router.get("/dish/{dish_id}", response_model=List[ReviewResponse])
def list_reviews_for_dish(
    dish_id: int, repo: ReviewRepository = Depends(get_repository)
):
    """
    Get all reviews for a specific dish to analyze its popularity.
    """
    try:
        return repo.get_reviews_by_dish(dish_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"API Error list_reviews_for_dish: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )