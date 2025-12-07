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
        st.title("⭐ Feedback e Avaliações")
        tab_view, tab_write = st.tabs(
            ["Avaliações de Pratos (Modo Administrador)", "Adicionar Avaliação"]
        )

        with tab_view:
            self._render_admin_tab()
        with tab_write:
            self._render_wizard_tab()

    def _render_admin_tab(self):
        st.subheader("Veja o que os clientes estão dizendo")
        dish_map = self.vm.get_dishes_map()

        if not dish_map:
            st.warning("Nenhum prato encontrado.")
            return

        sel_id = st.selectbox(
            "Selecionar Prato", options=dish_map.keys(), format_func=lambda x: dish_map[x]
        )
        if sel_id:
            try:
                reviews = self.vm.get_reviews_by_dish(sel_id)
                if not reviews:
                    st.info("Nenhuma avaliação ainda.")
                    return

                for rev in reviews:
                    self._render_single_review(rev)
            except AppError as e:
                st.error(f"Erro: {e}")

    def _render_single_review(self, rev):
        with st.chat_message("user"):
            st.markdown(f"**{rev.nota}/5** ⭐")
            st.markdown(f"_{rev.comentario}_")
            cust = getattr(rev, "customer_name", "Anônimo")
            st.caption(f"— {cust}")

            with st.expander("Controles de Administrador"):
                with st.form(key=f"edit_{rev.id}"):
                    r = st.slider("Nota", 1, 5, rev.nota)
                    c = st.text_area("Comentário", rev.comentario)
                    if st.form_submit_button("Salvar"):
                        try:
                            self.vm.update_review(rev.id, r, c)
                            st.toast("✅ Avaliação atualizada!")
                            st.rerun()
                        except AppError as e:
                            st.error(str(e))

            if st.button("Remover", key=f"del_{rev.id}"):
                try:
                    self.vm.delete_review(rev.id)
                    st.toast("🗑️ Avaliação removida.")
                    st.rerun()
                except AppError as e:
                    st.error(str(e))

    def _render_wizard_tab(self):
        st.subheader("Nova Avaliação")
        cust_map = self.vm.get_eligible_customers()
        if not cust_map:
            st.warning("Nenhum cliente qualificado encontrado.")
            return

        cust_id = st.selectbox(
            "Selecionar Cliente",
            options=cust_map.keys(),
            format_func=lambda x: cust_map[x],
        )
        if cust_id:
            items = self.vm.get_customer_reviewable_items(cust_id)
            if not items:
                st.warning("Nenhum item para avaliar.")
                return
            item_idx = st.selectbox(
                "Selecionar Refeição", range(len(items)), format_func=lambda i: items[i].label
            )
            selected_item = items[item_idx]
            with st.form("wiz_form"):
                st.write(f"Avaliando: **{selected_item.dish_name}**")
                rating = st.slider("Nota", 1, 5, 5)
                comment = st.text_area("Comentário", placeholder="Digite um comentário", help="Pressione Ctrl+Enter para enviar o comentário")
                if st.form_submit_button("Enviar Avaliação"):
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
                        st.toast("✅ Avaliação enviada!")
                        st.rerun()
                    except AppError as e:
                        st.error(f"Erro: {e}")
