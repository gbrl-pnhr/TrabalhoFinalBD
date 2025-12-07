import sys
from pathlib import Path
import streamlit as st
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
import pandas as pd
from apps.api.modules import CustomerCreate
from apps.ui.services.customers import CustomerService
from apps.ui.utils.exceptions import AppError

customer_service = CustomerService()

st.title("👥 Customer Directory")
st.markdown("Manage your loyal customer base here.")

tab_list, tab_create = st.tabs(["Directory", "Register New"])

with tab_list:
    try:
        customers = customer_service.get_customers()
        if not customers:
            st.info("No customers registered yet.")
        else:
            df = pd.DataFrame([c.model_dump() for c in customers])
            cols = ["id", "name", "email", "phone_number"]
            display_cols = [c for c in cols if c in df.columns]

            st.dataframe(
                df[display_cols],
                width='stretch',
                hide_index=True,
                column_config={
                    "id": "ID",
                    "name": "Full Name",
                    "email": "Email Address",
                },
            )
            if st.button("Refresh Directory"):
                st.rerun()
    except AppError as e:
        st.error(f"Failed to load customers: {e}")

with tab_create:
    st.subheader("Register New Customer")
    with st.form("create_customer_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
        with col2:
            phone = st.text_input("Phone Number (Optional)")
        if st.form_submit_button("Register Customer", width='stretch'):
            if not name or not email:
                st.error("Name and Email are required.")
            else:
                try:
                    payload = CustomerCreate(name=name, email=email, phone=phone)
                    customer_service.create_customer(payload)
                    st.success(f"✅ Customer '{name}' registered successfully!")
                    st.rerun()
                except AppError as e:
                    st.error(f"Error creating customer: {e}")
                except ValueError as ve:
                    st.error(f"Validation Error: {ve}")