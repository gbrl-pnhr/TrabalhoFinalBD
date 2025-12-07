import sys
from pathlib import Path
import streamlit as st
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
import time
from apps.api.modules import ReviewUpdate, ReviewCreate
from apps.ui.services.reviews import ReviewService
from apps.ui.services.menu import MenuService
from apps.ui.services.customers import CustomerService
from apps.ui.services.order import OrderService
from apps.ui.utils.exceptions import AppError

review_service = ReviewService()
menu_service = MenuService()
customer_service = CustomerService()
order_service = OrderService()

st.title("⭐ Feedback & Reviews")

tab_view, tab_write = st.tabs(["Dish Reviews (Admin Mode)", "New Review Wizard"])

try:
    all_customers = customer_service.get_customers()
    dishes = menu_service.get_dishes()
    dish_map = {d.id: d.name for d in dishes}
    eligible_customers = []
    for c in all_customers:
        has_history = any(
            o.status == "CLOSED" and len(o.items) > 0
            for o in c.orders
        )
        if has_history:
            eligible_customers.append(c)

    customer_map = {c.id: c.name for c in eligible_customers}

except AppError:
    st.error("Backend is offline. Cannot load choices.")
    all_customers, eligible_customers, dishes = [], [], []
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
    st.markdown("Use the wizard to select a specific item from a customer's history to review.")
    try:
        if not customer_map:
            st.warning("No customers found with eligible history (Closed orders).")
        else:
            st.markdown("#### 1. Who is the customer?")
            wiz_cust_id = st.selectbox(
                "Select Customer",
                options=customer_map.keys(),
                format_func=lambda x: customer_map.get(x, "Unknown"),
                key="wiz_cust",
            )

            if wiz_cust_id:
                selected_customer_obj = next((c for c in eligible_customers if c.id == wiz_cust_id), None)
                consumable_items = []
                if selected_customer_obj:
                    sorted_orders = sorted(
                        selected_customer_obj.orders,
                        key=lambda o: o.created_at,
                        reverse=True
                    )
                    for order in sorted_orders:
                        if order.status == "CLOSED" and order.items:
                            order_date_str = order.created_at.strftime("%Y-%m-%d")
                            for item in order.items:
                                label = f"{item.dish_name} (Order #{order.id} - {order_date_str})"
                                value = (order.id, item.dish_id, item.dish_name)
                                consumable_items.append({"label": label, "value": value})

                if not consumable_items:
                    st.warning("This customer has no items in their history eligible for review.")
                else:
                    st.markdown("#### 2. Which dish are they reviewing?")
                    selected_item_idx = st.selectbox(
                        "Select Item from History",
                        options=range(len(consumable_items)),
                        format_func=lambda i: consumable_items[i]["label"],
                        key="wiz_item_idx"
                    )
                    if selected_item_idx is not None:
                        wiz_order_id, wiz_dish_id, wiz_dish_name = consumable_items[selected_item_idx]["value"]
                        st.markdown("---")
                        st.markdown(f"#### 3. Rate the **{wiz_dish_name}**")
                        with st.form("wizard_review_form"):
                            rating = st.slider("Rating", 1, 5, 5)
                            comment = st.text_area("Comment", "Delicious!")

                            if st.form_submit_button("✅ Post Review", use_container_width=True):
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
                                    st.success(f"Review for {wiz_dish_name} posted successfully!")
                                    time.sleep(1.5)
                                    st.rerun()

                                except AppError as e:
                                    err_msg = str(e).lower()
                                    if "unique" in err_msg or "constraint" in err_msg or "conflict" in err_msg:
                                        st.error("You have already reviewed this specific dish from this order.")
                                    else:
                                        st.error(f"Failed to post review: {e}")

    except AppError as e:
        st.error(f"Connection Error: {e}")