import streamlit as st
from apps.ui.viewmodels.reviews import ReviewsViewModel
from apps.api.modules import ReviewCreate
from apps.ui.utils.exceptions import AppError


class ReviewsView:
    """
    Handles the UI Rendering for the Reviews Page.
    Depends on the ViewModel for data.
    """

    def __init__(self, view_model: ReviewsViewModel):
        self.vm = view_model

    def render(self):
        st.title("⭐ Feedback & Reviews")
        tab_view, tab_write = st.tabs(
            ["Dish Reviews (Admin Mode)", "New Review Wizard"]
        )

        with tab_view:
            self._render_admin_tab()
        with tab_write:
            self._render_wizard_tab()

    def _render_admin_tab(self):
        st.subheader("See what customers are saying")
        dish_map = self.vm.get_dishes_map()

        if not dish_map:
            st.warning("No dishes found or Backend offline.")
            return

        sel_id = st.selectbox(
            "Select Dish", options=dish_map.keys(), format_func=lambda x: dish_map[x]
        )
        if sel_id:
            try:
                reviews = self.vm.get_reviews_by_dish(sel_id)
                if not reviews:
                    st.info("No reviews yet.")
                    return

                for rev in reviews:
                    self._render_single_review(rev)
            except AppError as e:
                st.error(f"Error: {e}")

    def _render_single_review(self, rev):
        with st.chat_message("user"):
            st.markdown(f"**{rev.nota}/5** ⭐")
            st.markdown(f"_{rev.comentario}_")
            cust = getattr(rev, "customer_name", "Anonymous")
            st.caption(f"— {cust}")

            with st.expander("Admin Controls"):
                with st.form(key=f"edit_{rev.id}"):
                    r = st.slider("Rating", 1, 5, rev.nota)
                    c = st.text_area("Comment", rev.comentario)
                    if st.form_submit_button("Save"):
                        try:
                            self.vm.update_review(rev.id, r, c)
                            st.toast("✅ Review updated!")
                            st.rerun()
                        except AppError as e:
                            st.error(str(e))

            if st.button("Delete", key=f"del_{rev.id}"):
                try:
                    self.vm.delete_review(rev.id)
                    st.toast("🗑️ Review deleted.")
                    st.rerun()
                except AppError as e:
                    st.error(str(e))

    def _render_wizard_tab(self):
        st.subheader("Submit Feedback")
        cust_map = self.vm.get_eligible_customers()
        if not cust_map:
            st.warning("No eligible customers found.")
            return

        cust_id = st.selectbox(
            "Select Customer",
            options=cust_map.keys(),
            format_func=lambda x: cust_map[x],
        )
        if cust_id:
            items = self.vm.get_customer_reviewable_items(cust_id)
            if not items:
                st.warning("No items to review.")
                return
            item_idx = st.selectbox(
                "Select Meal", range(len(items)), format_func=lambda i: items[i].label
            )
            selected_item = items[item_idx]
            with st.form("wiz_form"):
                st.write(f"Reviewing: **{selected_item.dish_name}**")
                rating = st.slider("Rating", 1, 5, 5)
                comment = st.text_area("Comment")
                if st.form_submit_button("Submit Review"):
                    payload = ReviewCreate(
                        id_cliente=cust_id,
                        id_prato=selected_item.dish_id,
                        id_pedido=selected_item.order_id,
                        nota=rating,
                        comentario=comment,
                    )
                    try:
                        self.vm.submit_review(payload)
                        st.balloons()
                        st.toast("✅ Review posted!")
                        st.rerun()
                    except AppError as e:
                        st.error(f"Error: {e}")