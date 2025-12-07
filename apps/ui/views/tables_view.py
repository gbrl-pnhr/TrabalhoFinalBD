import streamlit as st
from apps.ui.viewmodels.table import TableViewModel


class TablesView:
    """
    Handles the UI Rendering for the Table Layout Page.
    Strictly Presentation Layer.
    """

    def __init__(self, view_model: TableViewModel):
        self.vm = view_model

    def render(self):
        st.title("🪑 Posição das Mesas")
        st.markdown("Altere a configuração física do restaurante.")
        self.vm.load_tables()
        if self.vm.last_error:
            st.error(f"Alerta de Sistema: {self.vm.last_error}")
        col_view, col_manage = st.columns([2, 1])
        with col_view:
            self._render_table_list()
        with col_manage:
            self._render_add_form()
            st.divider()
            self._render_delete_section()

    def _render_table_list(self):
        st.subheader("Configuração Atual")
        df = self.vm.get_tables_dataframe()
        if df.empty:
            st.info("Nenhuma mesa configurada ainda.")
            return
        st.dataframe(
            df,
            width="stretch",
            hide_index=True,
            column_config={
                "id": st.column_config.NumberColumn("ID", format="%d"),
                "number": st.column_config.NumberColumn("Table #", format="%d"),
                "capacity": "Seats",
                "location": "Location",
                "is_occupied": st.column_config.CheckboxColumn("Occupied?"),
            },
        )
        if st.button("🔄 Recarregar"):
            st.rerun()

    def _render_add_form(self):
        st.subheader("Adicionar Nova Mesa")
        existing_locs = self.vm.get_existing_locations()
        NEW_LOC_OPT = "➕ Nova Localização..."
        options = existing_locs + [NEW_LOC_OPT]
        selected_opt = st.selectbox("Localização", options=options)
        final_location = selected_opt
        if selected_opt == NEW_LOC_OPT:
            final_location = st.text_input(
                "Nome da Localização", placeholder="ex.: Varanda"
            )
        next_num = self.vm.get_next_suggestion()
        with st.form("add_table_form"):
            t_num = st.number_input("Número da Mesa", min_value=1, step=1, value=next_num)
            t_cap = st.number_input("Capacidade", min_value=1, step=1, value=4)
            if self.vm.is_number_occupied(t_num):
                st.warning(f"⚠️ A mesa {t_num} já existe.")

            if st.form_submit_button("Adicionar Mesa", width="stretch"):
                if self.vm.add_table(
                    number=t_num, capacity=t_cap, location=final_location
                ):
                    st.toast(f"✅ Mesa {t_num} criada!")
                    st.rerun()
                else:
                    st.error(self.vm.last_error)

    def _render_delete_section(self):
        st.subheader("Remover Mesa")
        if not self.vm.tables:
            st.caption("Nenhuma mesa para remover.")
            return
        table_map = {t.id: f"Mesa {t.numero} ({t.localizacao})" for t in self.vm.tables}

        selected_id = st.selectbox(
            "Selecionar Mesa", options=table_map.keys(), format_func=lambda x: table_map[x]
        )
        if st.button("🗑️ Remover Mesa Selecionada", type="primary"):
            if self.vm.delete_table(selected_id):
                st.toast("✅ Mesa removida.")
                st.rerun()
            else:
                st.error(self.vm.last_error)