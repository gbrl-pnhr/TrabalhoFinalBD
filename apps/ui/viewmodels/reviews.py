from typing import List, Dict
from dataclasses import dataclass
from apps.api.modules import ReviewResponse, ReviewCreate, ReviewUpdate
from apps.ui.services.reviews import ReviewService
from apps.ui.services.menu import MenuService
from apps.ui.services.customers import CustomerService
from apps.ui.utils.exceptions import AppError


@dataclass
class ReviewableItem:
    label: str
    order_id: int
    dish_id: int
    dish_name: str


class ReviewsViewModel:
    """
    Pure Logic for the Reviews Page.
    Zero Streamlit dependencies. Testable.
    """

    def __init__(
        self,
        review_service: ReviewService,
        menu_service: MenuService,
        customer_service: CustomerService,
    ):
        self._review_service = review_service
        self._menu_service = menu_service
        self._customer_service = customer_service

    def get_dishes_map(self) -> Dict[int, str]:
        try:
            dishes = self._menu_service.get_dishes()
            return {d.id: d.nome for d in dishes}
        except AppError:
            return {}

    def get_reviews_by_dish(self, dish_id: int) -> List[ReviewResponse]:
        return self._review_service.get_reviews_by_dish(dish_id)

    def get_eligible_customers(self) -> Dict[int, str]:
        """Returns {id: name} of customers with closed orders."""
        try:
            customers = self._customer_service.get_customers()
            eligible = {}
            for c in customers:
                if any(str(o.status).upper() == "FECHADO" and o.itens for o in c.pedidos):
                    eligible[c.id] = c.nome
            return eligible
        except AppError:
            return {}

    def get_customer_reviewable_items(self, customer_id: int) -> List[ReviewableItem]:
        try:
            all_customers = self._customer_service.get_customers()
            customer = next((c for c in all_customers if c.id == customer_id), None)
            if not customer:
                return []
            items = []
            sorted_orders = sorted(
                customer.pedidos, key=lambda o: o.criado_em or "", reverse=True
            )
            for order in sorted_orders:
                if str(order.status).upper() == "FECHADO" and order.itens:
                    date_lbl = (
                        order.criado_em.strftime("%Y-%m-%d")
                        if order.criado_em
                        else "?"
                    )
                    for item in order.itens:
                        items.append(
                            ReviewableItem(
                                label=f"{item.nome_prato} (Order #{order.id} - {date_lbl})",
                                order_id=order.id,
                                dish_id=item.id_prato,
                                dish_name=item.nome_prato,
                            )
                        )
            return items
        except AppError:
            return []

    def submit_review(self, payload: ReviewCreate):
        self._review_service.create_review(payload)

    def update_review(self, review_id: int, rating: int, comment: str):
        self._review_service.update_review(
            review_id, ReviewUpdate(nota=rating, comentario=comment)
        )

    def delete_review(self, review_id: int):
        self._review_service.delete_review(review_id)