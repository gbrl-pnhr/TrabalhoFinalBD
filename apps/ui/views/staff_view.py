import streamlit as st
from apps.ui.viewmodels.staff import StaffViewModel


class StaffView:
    """
    Handles the UI Rendering for the Staff Page.
    Depends on the ViewModel for logic and state.
    """

    def __init__(self, view_model: StaffViewModel):
        self.vm = view_model

    def render(self):
        st.title("👨‍🍳 Funcionários")

        # Initial data load
        self.vm.load_staff()

        if self.vm.last_error:
            st.error(f"Alerta de Sistema: {self.vm.last_error}")

        tab_waiters, tab_chefs = st.tabs(["🤵 Garçons", "👨‍🍳 Chefes"])

        with tab_waiters:
            self._render_waiters_section()

        with tab_chefs:
            self._render_chefs_section()

    def _render_waiters_section(self):
        col_list, col_form = st.columns([2, 1])

        with col_list:
            st.subheader("Garçons em Serviço")
            if not self.vm.waiters:
                st.info("Nenhum garçom encontrado.")
            else:
                for w in self.vm.waiters:
                    with st.expander(f"{w.nome} (ID: {w.id})"):
                        st.write(f"**CPF:** {w.cpf}")
                        st.write(f"**Turno:** {w.turno}")
                        st.write(f"**Salário:** ${w.salario:,.2f}")
                        st.write(f"**Commissão:** {w.comissao}%")

                        if st.button("🔥 Demitir Garçom", key=f"del_w_{w.id}"):
                            if self.vm.fire_waiter(w.id):
                                st.toast("✅ Garçom terminado com sucesso.")
                                st.rerun()
                            else:
                                st.error(self.vm.last_error)

        with col_form:
            self._render_waiter_form()

    def _render_waiter_form(self):
        st.subheader("Registrar Garçom")
        existing_shifts = self.vm.get_existing_shifts()
        NEW_SHIFT_OPT = "➕ Novo Turno..."
        if not existing_shifts:
            existing_shifts = ["Manhã", "Noite", "Integral"]
        options = existing_shifts + [NEW_SHIFT_OPT]
        selected_shift = st.selectbox("Turno", options=options, key="sel_shift")
        final_shift = selected_shift
        if selected_shift == NEW_SHIFT_OPT:
            final_shift = st.text_input(
                "Digite o nome do novo turno",
                placeholder="ex.: Corujão",
                key="txt_new_shift",
            )
        with st.form("create_waiter_form"):
            w_name = st.text_input("Nome Completo")
            w_cpf = st.text_input("CPF (Apenas Números)")
            c1, c2 = st.columns(2)
            with c1:
                w_salary = st.number_input("Salário (R$)", min_value=0.0, step=100.0)
            with c2:
                w_commission = st.number_input(
                    "Commissão (%)", min_value=0.0, step=0.1
                )
            if st.form_submit_button("Contratar Garçom", width="stretch"):
                if not w_name or not w_cpf or not final_shift:
                    st.error("Por favor, preencha todos os campos (Nome, CPF, Turno).")
                else:
                    success = self.vm.hire_waiter(
                        name=w_name,
                        cpf=w_cpf,
                        salary=w_salary,
                        commission=w_commission,
                        shift=final_shift,
                    )
                    if success:
                        st.toast(f"✅ Garçom {w_name} contratado!")
                        st.rerun()
                    else:
                        st.error(self.vm.last_error)

    def _render_chefs_section(self):
        col_list, col_form = st.columns([2, 1])

        with col_list:
            st.subheader("Chefes da Cozinha")
            if not self.vm.chefs:
                st.info("Nenhum chefe encontrado.")
            else:
                for c in self.vm.chefs:
                    with st.expander(f"{c.nome} (ID: {c.id})"):
                        st.write(f"**CPF:** {c.cpf}")
                        st.write(f"**Salário:** ${c.salario:,.2f}")
                        st.write(f"**Especialidade:** {c.especialidade}")
                        if st.button("🔥 Demitir Chefe", key=f"del_c_{c.id}"):
                            if self.vm.fire_chef(c.id):
                                st.toast("✅ Chefe terminado com sucesso.")
                                st.rerun()
                            else:
                                st.error(self.vm.last_error)

        with col_form:
            self._render_chef_form()

    def _render_chef_form(self):
        st.subheader("Registrar Chefe")
        existing_specialties = self.vm.get_existing_specialties()
        NEW_SPEC_OPT = "➕ Criar Nova Especialidade..."
        options = existing_specialties + [NEW_SPEC_OPT]
        selected_opt = st.selectbox("Especialidade", options=options, key="sel_spec")
        final_specialty = selected_opt
        if selected_opt == NEW_SPEC_OPT:
            final_specialty = st.text_input(
                "Digite o nome da nova especialidade",
                placeholder="ex.: Pasteleiro",
                help="Digite aqui o nome da nova especialidade.",
                key="txt_new_spec",
            )
        with st.form("create_chef_form"):
            c_name = st.text_input("Nome Completo")
            c_cpf = st.text_input("CPF")
            c_salary = st.number_input("Salário (R$)", min_value=0.0, step=100.0)

            if st.form_submit_button("Contratar Chefe", type="primary", width="stretch"):
                if not c_name or not c_cpf or not final_specialty:
                    st.error("Por favor, preencha todos os campos (Nome, CPF, Especialidade).")
                else:
                    success = self.vm.hire_chef(
                        name=c_name,
                        cpf=c_cpf,
                        salary=c_salary,
                        specialty=final_specialty,
                    )
                    if success:
                        st.toast(f"✅ Chefe {c_name} contratado!")
                        st.rerun()
                    else:
                        st.error(self.vm.last_error)