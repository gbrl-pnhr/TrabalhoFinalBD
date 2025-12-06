import streamlit as st
import pandas as pd
from services.staff import StaffService
from schemas import WaiterCreate, ChefCreate
from components.sidebar import render_sidebar
from utils.exceptions import AppError

st.set_page_config(page_title="Staff Management", page_icon="👨‍🍳", layout="wide")

render_sidebar("Staff Management")
staff_service = StaffService()
st.title("👨‍🍳 Staff Management")
st.markdown("Manage your workforce: Waiters and Chefs.")

tab_waiters, tab_chefs = st.tabs(["🤵 Waiters", "👨‍🍳 Chefs"])

with tab_waiters:
    col_list, col_form = st.columns([2, 1])
    with col_list:
        st.subheader("Current Waiters")
        try:
            waiters = staff_service.get_waiters()
            if not waiters:
                st.info("No waiters found.")
            else:
                df_waiters = pd.DataFrame([w.model_dump() for w in waiters])
                st.dataframe(
                    df_waiters,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "salary": st.column_config.NumberColumn(format="$%.2f"),
                        "commission": st.column_config.NumberColumn(format="%.2f%%"),
                        "cpf": "CPF",
                    },
                )
        except AppError as e:
            st.error(f"Error loading waiters: {e}")

    with col_form:
        st.subheader("Register Waiter")
        with st.form("create_waiter_form"):
            w_name = st.text_input("Full Name")
            w_cpf = st.text_input("CPF (Digits Only)")
            c1, c2 = st.columns(2)
            with c1:
                w_salary = st.number_input("Salary ($)", min_value=0.0, step=100.0)
            with c2:
                w_commission = st.number_input(
                    "Commission (%)", min_value=0.0, step=0.1
                )
            w_shift = st.selectbox("Shift", ["Morning", "Evening", "Full Day"])
            if st.form_submit_button("Hire Waiter", use_container_width=True):
                if not w_name or not w_cpf:
                    st.warning("Name and CPF are required.")
                else:
                    try:
                        new_waiter = WaiterCreate(
                            name=w_name,
                            cpf=w_cpf,
                            salary=w_salary,
                            commission=w_commission,
                            shift=w_shift,
                        )
                        staff_service.create_waiter(new_waiter)
                        st.success(f"✅ {w_name} hired successfully!")
                        st.cache_data.clear()
                        st.rerun()
                    except ValueError as ve:
                        st.error(f"Validation Error: {ve}")
                    except AppError as e:
                        st.error(f"API Error: {e}")

with tab_chefs:
    col_list_c, col_form_c = st.columns([2, 1])
    with col_list_c:
        st.subheader("Kitchen Staff")
        try:
            chefs = staff_service.get_chefs()
            if not chefs:
                st.info("No chefs found.")
            else:
                df_chefs = pd.DataFrame([c.model_dump() for c in chefs])
                st.dataframe(
                    df_chefs,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "salary": st.column_config.NumberColumn(format="$%.2f"),
                        "id": "ID",
                    },
                )
        except AppError as e:
            st.error(f"Error loading chefs: {e}")

    with col_form_c:
        st.subheader("Register Chef")
        with st.form("create_chef_form"):
            c_name = st.text_input("Full Name")
            c_cpf = st.text_input("CPF")
            c_salary = st.number_input("Salary ($)", min_value=0.0, step=100.0)
            c_specialty = st.text_input("Specialty (e.g. Pasta, Grill)")
            if st.form_submit_button("Hire Chef", use_container_width=True):
                try:
                    new_chef = ChefCreate(
                        name=c_name, cpf=c_cpf, salary=c_salary, specialty=c_specialty
                    )
                    staff_service.create_chef(new_chef)
                    st.success(f"✅ Chef {c_name} added to kitchen!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")