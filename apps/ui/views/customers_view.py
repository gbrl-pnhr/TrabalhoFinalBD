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
        st.title("👥 Customer Directory")
        st.markdown("Manage your loyal customer base here.")

        self.vm.load_customers()

        if self.vm.last_error:
            st.error(f"System Alert: {self.vm.last_error}")

        tab_list, tab_create = st.tabs(["Directory", "Register New"])

        with tab_list:
            self._render_directory_tab()

        with tab_create:
            self._render_create_tab()

    def _render_directory_tab(self):
        if not self.vm.customers:
            st.info("No customers registered yet.")
            if st.button("🔄 Refresh"):
                st.rerun()
            return

        df = self.vm.get_customers_dataframe()

        cols = ["id", "name", "email", "phone_number"]
        display_cols = [c for c in cols if c in df.columns]

        st.dataframe(
            df[display_cols],
            width="stretch",
            hide_index=True,
            column_config={
                "id": st.column_config.NumberColumn("ID", format="%d"),
                "name": "Full Name",
                "email": "Email Address",
                "phone_number": "Phone",
            },
        )

        if st.button("Refresh Directory"):
            st.rerun()

    def _render_create_tab(self):
        st.subheader("Register New Customer")

        with st.form("create_customer_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name")
                email = st.text_input("Email Address")
            with col2:
                phone = st.text_input("Phone Number (Optional)")

            submitted = st.form_submit_button("Register Customer", width="stretch")

            if submitted:
                form_data = CustomerFormData(name=name, email=email, phone=phone)

                if self.vm.create_customer(form_data):
                    st.toast(f"✅ Customer '{name}' registered successfully!")
                    st.rerun()
                else:
                    st.error(self.vm.last_error)