import streamlit as st
import time
from apps.ui.viewmodels.staff import StaffViewModel


class StaffView:
    """
    Handles the UI Rendering for the Staff Page.
    Depends on the ViewModel for logic and state.
    """

    def __init__(self, view_model: StaffViewModel):
        self.vm = view_model

    def render(self):
        st.title("👨‍🍳 Staff Management")

        # Initial data load
        self.vm.load_staff()

        if self.vm.last_error:
            st.error(f"System Alert: {self.vm.last_error}")

        tab_waiters, tab_chefs = st.tabs(["🤵 Waiters", "👨‍🍳 Chefs"])

        with tab_waiters:
            self._render_waiters_section()

        with tab_chefs:
            self._render_chefs_section()

    def _render_waiters_section(self):
        col_list, col_form = st.columns([2, 1])

        with col_list:
            st.subheader("Current Waiters")
            if not self.vm.waiters:
                st.info("No waiters found.")
            else:
                for w in self.vm.waiters:
                    with st.expander(f"{w.name} (ID: {w.id})"):
                        st.write(f"**CPF:** {w.cpf}")
                        st.write(f"**Shift:** {w.shift}")
                        st.write(f"**Salary:** ${w.salary:,.2f}")
                        st.write(f"**Commission:** {w.commission}%")

                        if st.button("🔥 Fire Waiter", key=f"del_w_{w.id}"):
                            if self.vm.fire_waiter(w.id):
                                st.success("Terminated successfully.")
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.error(self.vm.last_error)

        with col_form:
            self._render_waiter_form()

    def _render_waiter_form(self):
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

            if st.form_submit_button("Hire Waiter", width="stretch"):
                if not w_name or not w_cpf:
                    st.error("Name and CPF are required.")
                else:
                    success = self.vm.hire_waiter(
                        name=w_name,
                        cpf=w_cpf,
                        salary=w_salary,
                        commission=w_commission,
                        shift=w_shift,
                    )
                    if success:
                        st.success(f"✅ {w_name} hired!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(self.vm.last_error)

    def _render_chefs_section(self):
        col_list, col_form = st.columns([2, 1])

        with col_list:
            st.subheader("Kitchen Staff")
            if not self.vm.chefs:
                st.info("No chefs found.")
            else:
                for c in self.vm.chefs:
                    with st.expander(f"{c.name} (ID: {c.id})"):
                        st.write(f"**CPF:** {c.cpf}")
                        st.write(f"**Salary:** ${c.salary:,.2f}")
                        st.write(f"**Specialty:** {c.specialty}")

                        if st.button("🔥 Fire Chef", key=f"del_c_{c.id}"):
                            if self.vm.fire_chef(c.id):
                                st.success("Terminated successfully.")
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.error(self.vm.last_error)

        with col_form:
            self._render_chef_form()

    def _render_chef_form(self):
        st.subheader("Register Chef")
        existing_specialties = self.vm.get_existing_specialties()

        NEW_OPT = "➕ New Specialty..."
        options = existing_specialties + [NEW_OPT]

        with st.form("create_chef_form"):
            c_name = st.text_input("Full Name")
            c_cpf = st.text_input("CPF")
            c_salary = st.number_input("Salary ($)", min_value=0.0, step=100.0)

            selected_opt = st.selectbox("Specialty", options=options)

            # Note: We can't conditionally render inputs inside a form easily in Streamlit
            # without breaking the form context on rerun, but we can accept the input anyway.
            # A cleaner UI approach is to put the selectbox outside, but for consistent
            # form submission we'll keep it simple or use a placeholder if needed.
            # Here we will just ask for manual input if they picked "New".

            c_manual_spec = st.text_input(
                "If 'New', enter Specialty Name",
                placeholder="e.g. Pastry",
                help="Fill this only if you selected 'New Specialty' above.",
            )

            if st.form_submit_button("Hire Chef", type="primary", width="stretch"):
                final_specialty = selected_opt
                if selected_opt == NEW_OPT:
                    final_specialty = c_manual_spec

                if not c_name or not c_cpf or not final_specialty:
                    st.error("Please fill in all fields (Name, CPF, Specialty).")
                else:
                    success = self.vm.hire_chef(
                        name=c_name,
                        cpf=c_cpf,
                        salary=c_salary,
                        specialty=final_specialty,
                    )
                    if success:
                        st.success(f"✅ Chef {c_name} added!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(self.vm.last_error)