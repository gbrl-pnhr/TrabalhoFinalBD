import streamlit as st
import time
from apps.ui.services.reviews import ReviewService
from apps.ui.services.menu import MenuService
from apps.ui.services.customers import CustomerService
from apps.ui.services.order import OrderService
from apps.ui.schemas import ReviewCreate, ReviewUpdate
from apps.ui.utils.exceptions import AppError

review_service = ReviewService()
menu_service = MenuService()
customer_service = CustomerService()
order_service = OrderService()

st.title("⭐ Feedback & Reviews")

tab_view, tab_write = st.tabs(["Dish Reviews (Admin Mode)", "New Review Wizard"])

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
    col_sel, col_info = st.columns([1, 2])
    with col_sel:
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
                        st.markdown(f"**Rating:** {'⭐' * rev.rating} ({rev.rating}/5)")
                        st.markdown(f"_{rev.comment}_")

                        cust_name = (
                            rev.customer_name
                            if hasattr(rev, "customer_name")
                            else "Customer"
                        )
                        order_lbl = (
                            f" | Order #{rev.order_id}"
                            if hasattr(rev, "order_id") and rev.order_id
                            else ""
                        )
                        st.caption(f"— {cust_name}{order_lbl}")

                        with st.expander("🛠️ Admin: Edit / Delete Review"):
                            with st.form(key=f"edit_rev_{rev.id}"):
                                new_rating = st.slider(
                                    "Edit Rating", 1, 5, rev.rating, key=f"r_{rev.id}"
                                )
                                new_comment = st.text_area(
                                    "Edit Comment", rev.comment, key=f"c_{rev.id}"
                                )

                                if st.form_submit_button("💾 Save Changes"):
                                    try:
                                        payload = ReviewUpdate(
                                            rating=new_rating, comment=new_comment
                                        )
                                        review_service.update_review(rev.id, payload)
                                        st.success("Review updated!")
                                        time.sleep(0.5)
                                        st.rerun()
                                    except AppError as e:
                                        st.error(f"Update failed: {e}")

                            if st.button("🗑️ Delete Review", key=f"del_rev_{rev.id}"):
                                try:
                                    review_service.delete_review(rev.id)
                                    st.warning("Review deleted.")
                                    time.sleep(0.5)
                                    st.rerun()
                                except AppError as e:
                                    st.error(f"Delete failed: {e}")

        except AppError as e:
            st.error(f"Error loading reviews: {e}")

with tab_write:
    st.subheader("Submit Feedback")
    st.markdown("Use the wizard below to link a review to a specific customer order.")

    try:
        st.markdown("#### 1. Who is the customer?")
        wiz_cust_id = st.selectbox(
            "Select Customer",
            options=customer_map.keys(),
            format_func=lambda x: customer_map.get(x, "Unknown"),
            key="wiz_cust",
        )

        if wiz_cust_id:
            all_orders = order_service.list_orders()
            cust_orders = [
                o
                for o in all_orders
                if o.customer_id == wiz_cust_id
                and str(o.status).lower() in ["closed", "paid", "completed"]
            ]
            if not cust_orders:
                st.warning(
                    f"No completed orders found for {customer_map[wiz_cust_id]}."
                )
            else:
                st.markdown("#### 2. Which visit are they reviewing?")
                order_options = {
                    o.id: f"Order #{o.id} (${o.total_value:.2f})" for o in cust_orders
                }
                wiz_order_id = st.selectbox(
                    "Select Past Order",
                    options=order_options.keys(),
                    format_func=lambda x: order_options.get(x),
                    key="wiz_order",
                )
                if wiz_order_id:
                    selected_order = next(
                        (o for o in cust_orders if o.id == wiz_order_id), None
                    )
                    if selected_order and selected_order.items:
                        st.markdown("#### 3. What did they eat?")
                        item_map = {
                            item.dish_id: f"{item.dish_name} (Qty: {item.quantity})"
                            for item in selected_order.items
                        }
                        wiz_dish_id = st.selectbox(
                            "Select Dish from Order",
                            options=item_map.keys(),
                            format_func=lambda x: item_map.get(x),
                            key="wiz_dish",
                        )
                        if wiz_dish_id:
                            st.markdown("---")
                            st.markdown(
                                f"#### 4. Rate the **{item_map[wiz_dish_id].split('(')[0].strip()}**"
                            )
                            with st.form("wizard_review_form"):
                                rating = st.slider("Rating", 1, 5, 5)
                                comment = st.text_area("Comment", "Delicious!")
                                if st.form_submit_button(
                                    "✅ Post Verified Review", width='stretch'
                                ):
                                    try:
                                        payload = ReviewCreate(
                                            customer_id=wiz_cust_id,
                                            dish_id=wiz_dish_id,
                                            order_id=wiz_order_id,
                                            rating=rating,
                                            comment=comment,
                                        )
                                        review_service.create_review(payload)
                                        st.balloons()
                                        st.success("Review posted successfully!")
                                        time.sleep(1.5)
                                        st.rerun()
                                    except AppError as e:
                                        st.error(f"Failed to post review: {e}")
                    else:
                        st.info("This order has no items recorded.")

    except AppError as e:
        st.error(f"Connection Error: {e}")