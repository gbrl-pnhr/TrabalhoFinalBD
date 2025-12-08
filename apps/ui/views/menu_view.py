import streamlit as st
from apps.ui.viewmodels.menu import MenuViewModel, DishFormData


class MenuView:
    """
    Handles the UI Rendering for the Menu Management Page.
    Adheres to MVVM: Logic is delegated to the ViewModel.
    """

    def __init__(self, view_model: MenuViewModel):
        self.vm = view_model

    def render(self):
        st.title("🍴 Gestor de Menu")
        self.vm.load_data()
        if self.vm.last_error:
            st.error(f"System Error: {self.vm.last_error}")
        tab_list, tab_create, tab_manage = st.tabs(
            ["Menu", "Adicionar Prato", "Alterar e Remover"]
        )
        with tab_list:
            self._render_list_tab()

        with tab_create:
            self._render_create_tab()

        with tab_manage:
            self._render_manage_tab()

    def _render_list_tab(self):
        if not self.vm.dishes:
            st.info("Nenhum prato encontrado no menu.")
            return

        df = self.vm.get_dishes_dataframe()
        st.dataframe(
            df,
            width="stretch",
            hide_index=True,
            column_config={
                "price": st.column_config.NumberColumn(format="$%.2f"),
                "id": st.column_config.NumberColumn(format="%d"),
            },
        )
        if st.button("Recarregar"):
            st.rerun()

    def _render_create_tab(self):
        NEW_CAT_OPTION = "➕ Criar nova categoria..."
        options = self.vm.categories + [NEW_CAT_OPTION]

        st.subheader("Detalhes do Novo Prato")

        c_cat1, c_cat2 = st.columns(2)
        with c_cat1:
            selected_cat = st.selectbox("Categoria", options)

        final_category = selected_cat
        if selected_cat == NEW_CAT_OPTION:
            with c_cat2:
                final_category = st.text_input(
                    "Digite o nome da categoria", placeholder="e.g. Vegan Specials"
                )

        with st.form("create_dish_form"):
            name = st.text_input("Nome do Prato")
            c_price, _ = st.columns(2)
            with c_price:
                price = st.number_input(
                    "Preço (R$)", min_value=0.01, step=0.50, format="%.2f"
                )

            submitted = st.form_submit_button("Adicionar Prato", width="stretch")

            if submitted:
                form_data = DishFormData(
                    name=name, price=price, category=final_category
                )

                if self.vm.create_dish(form_data):
                    st.toast(f"✅ Prato '{name}' criado com sucesso!")
                    st.rerun()
                else:
                    st.error(self.vm.last_error)

    def _render_manage_tab(self):
        st.subheader("Alterar ou Remover Pratos")

        dish_map = self.vm.get_dish_lookup()
        if not dish_map:
            st.info("Nenhum prato disponível.")
            return

        selected_id = st.selectbox(
            "Escolha o Prato",
            options=dish_map.keys(),
            format_func=lambda x: dish_map[x],
        )

        selected_dish = self.vm.get_dish_by_id(selected_id)
        if not selected_dish:
            return

        with st.form(key="edit_dish_form"):
            st.write(f"Prato Selecionado: **{selected_dish.nome}**")
            col1, col2 = st.columns(2)
            with col1:
                new_price = st.number_input(
                    "Novo Preço (R$)", value=float(selected_dish.preco), step=0.5
                )
            with col2:
                new_name = st.text_input("Novo Nome", value=selected_dish.nome)

            update_btn = st.form_submit_button("💾 Atualizar Informações do Prato")

        st.write("")
        delete_btn = st.button("🗑️ Remover Prato Permanentemente", type="primary")

        if update_btn:
            if self.vm.update_dish(selected_id, new_name, new_price):
                st.toast("✅ Prato atualizado!")
                st.rerun()
            else:
                st.error(self.vm.last_error)

        if delete_btn:
            if self.vm.delete_dish(selected_id):
                st.toast("🗑️ Prato removido.")
                st.rerun()
            else:
                st.error(self.vm.last_error)
