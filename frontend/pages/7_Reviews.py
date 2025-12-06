import streamlit as st
from services.reviews import ReviewService
from services.menu import MenuService
from services.customers import CustomerService
from schemas import ReviewCreate
from components.sidebar import render_sidebar
from utils.exceptions import AppError

st.set_page_config(page_title="Reviews", page_icon="⭐", layout="wide")
render_sidebar("Reviews")

review_service = ReviewService()
menu_service = MenuService()
customer_service = CustomerService()

st.title("⭐ Feedback & Reviews")

tab_view, tab_write = st.tabs(["Dish Reviews", "Write a Review"])

try:
    dishes = menu_service.get_dishes()
    customers = customer_service.get_customers()
    dish_map = {d.id: d.name for d in dishes}
    customer_map = {c.id: c.name for c in customers}
except AppError:
    st.error("Backend is offline. Cannot load choices.")
    dishes, customers = [], []
    dish_map, customer_map = {}, {}

with tab_view:
    st.subheader("See what customers are saying")
    selected_dish_id = st.selectbox(
        "Select Dish to View:",
        options=dish_map.keys(),
        format_func=lambda x: dish_map.get(x, "Unknown"),
    )

    if selected_dish_id:
        try:
            reviews = review_service.get_reviews_by_dish(selected_dish_id)
            if not reviews:
                st.info("No reviews for this dish yet.")
            else:
                for rev in reviews:
                    with st.chat_message("user"):
                        st.write(f"**Rating:** {'⭐' * rev.rating}")
                        st.write(rev.comment)
                        st.caption(
                            f"— {rev.customer_name if hasattr(rev, 'customer_name') else 'Customer'}"
                        )
        except AppError as e:
            st.error(f"Error loading reviews: {e}")

with tab_write:
    st.subheader("Submit Feedback")
    with st.form("new_review_form"):
        c1, c2 = st.columns(2)
        with c1:
            r_cust_id = st.selectbox(
                "Customer",
                options=customer_map.keys(),
                format_func=lambda x: customer_map.get(x, "Unknown"),
            )
        with c2:
            r_dish_id = st.selectbox(
                "Dish",
                options=dish_map.keys(),
                format_func=lambda x: dish_map.get(x, "Unknown"),
            )

        rating = st.slider("Rating", 1, 5, 5)
        comment = st.text_area("Comment", "Delicious!")

        if st.form_submit_button("Post Review", use_container_width=True):
            if not r_cust_id or not r_dish_id:
                st.error("Customer and Dish are required.")
            else:
                try:
                    payload = ReviewCreate(
                        customer_id=r_cust_id,
                        dish_id=r_dish_id,
                        rating=rating,
                        comment=comment,
                    )
                    review_service.create_review(payload)
                    st.success("✅ Review posted! Thank you.")
                except AppError as e:
                    st.error(f"Failed to post review: {e}")