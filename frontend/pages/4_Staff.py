import streamlit as st
import time
from services.staff import StaffService
from schemas import WaiterCreate, ChefCreate
from utils.exceptions import AppError

staff_service = StaffService()
st.title("👨‍🍳 Staff Management")

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
                for w in waiters:
                    with st.expander(f"{w.name} (ID: {w.id})"):
                        st.write(f"**CPF:** {w.cpf}")
                        st.write(f"**Shift:** {w.shift}")
                        st.write(f"**Commission:** {w.commission}%")
                        if st.button("🔥 Fire Waiter", key=f"del_w_{w.id}"):
                            try:
                                staff_service.delete_waiter(w.id)
                                st.success("Terminated.")
                                time.sleep(0.5)
                                st.rerun()
                            except AppError as e:
                                st.error(f"Error: {e}")

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
                w_commission = st.number_input("Commission (%)", min_value=0.0, step=0.1)
            w_shift = st.selectbox("Shift", ["Morning", "Evening", "Full Day"])
            if st.form_submit_button("Hire Waiter"):
                try:
                    new_waiter = WaiterCreate(name=w_name, cpf=w_cpf, salary=w_salary, commission=w_commission, shift=w_shift)
                    staff_service.create_waiter(new_waiter)
                    st.success(f"✅ {w_name} hired!")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))

with tab_chefs:
    col_list_c, col_form_c = st.columns([2, 1])
    with col_list_c:
        st.subheader("Kitchen Staff")
        try:
            chefs = staff_service.get_chefs()
            if not chefs:
                st.info("No chefs found.")
            else:
                for c in chefs:
                    with st.expander(f"{c.name} (ID: {c.id})"):
                        st.write(f"**Specialty:** {c.specialty}")
                        if st.button("🔥 Fire Chef", key=f"del_c_{c.id}"):
                            try:
                                staff_service.delete_chef(c.id)
                                st.success("Terminated.")
                                time.sleep(0.5)
                                st.rerun()
                            except AppError as e:
                                st.error(str(e))
        except AppError as e:
            st.error(f"Error loading chefs: {e}")

    with col_form_c:
        st.subheader("Register Chef")
        with st.form("create_chef_form"):
            c_name = st.text_input("Full Name")
            c_cpf = st.text_input("CPF")
            c_salary = st.number_input("Salary ($)", min_value=0.0, step=100.0)
            c_specialty = st.text_input("Specialty (e.g. Pasta, Grill)")
            if st.form_submit_button("Hire Chef"):
                try:
                    new_chef = ChefCreate(name=c_name, cpf=c_cpf, salary=c_salary, specialty=c_specialty)
                    staff_service.create_chef(new_chef)
                    st.success(f"✅ Chef {c_name} added!")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))