import streamlit as st
from apps.ui.viewmodels.customers import CustomersViewModel, CustomerFormData


class CustomersView:
    """
    Handles the UI Rendering for the Customer Directory.
    Strictly presentation logic; delegates actions to ViewModel.
    """

    def __init__(self, view_model: CustomersViewModel):
        self.vm = view_model

    def render(self):
        st.title("👥 Diretório de Clientes")
        st.markdown("Gerencie aqui sua base de clientes leais.")

        self.vm.load_customers()

        if self.vm.last_error:
            st.error(f"Alerta de Sistema: {self.vm.last_error}")

        tab_list, tab_create = st.tabs(["Diretório", "Novo Cliente"])

        with tab_list:
            self._render_directory_tab()

        with tab_create:
            self._render_create_tab()

    def _render_directory_tab(self):
        if not self.vm.customers:
            st.info("Nenhum cliente registrado ainda.")
            if st.button("🔄 Recarregar"):
                st.rerun()
            return

        df = self.vm.get_customers_dataframe()

        cols = ["id", "nome", "email", "telefone"]
        display_cols = [c for c in cols if c in df.columns]

        st.dataframe(
            df[display_cols],
            width="stretch",
            hide_index=True,
            column_config={
                "id": st.column_config.NumberColumn("ID", format="%d"),
                "nome": "Nome Completo",
                "email": "Endereço de Email",
                "telefone": "Telefone",
            },
        )

        if st.button("Recarregar Diretório"):
            st.rerun()

    def _render_create_tab(self):
        st.subheader("Registrar Novo Cliente")

        with st.form("create_customer_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Nome Completo")
                email = st.text_input("Endereço de Email")
            with col2:
                phone = st.text_input("Telefone (Opcional)")

            submitted = st.form_submit_button("Registrar Cliente", width="stretch")

            if submitted:
                form_data = CustomerFormData(name=name, email=email, phone=phone)

                if self.vm.create_customer(form_data):
                    st.toast(f"✅ Cliente '{name}' registrado com sucesso!")
                    st.rerun()
                else:
                    st.error(self.vm.last_error)