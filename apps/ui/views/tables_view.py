import streamlit as st
import time

from apps.ui.viewmodels.table import TableViewModel


class TablesView:
    """
    Handles the UI Rendering for the Table Layout Page.
    Strictly Presentation Layer.
    """

    def __init__(self, view_model: TableViewModel):
        self.vm = view_model

    def render(self):
        st.title("🪑 Table Layout")
        st.markdown("Configure the physical layout of the restaurant.")
        self.vm.load_tables()
        if self.vm.last_error:
            st.error(f"System Alert: {self.vm.last_error}")
        col_view, col_manage = st.columns([2, 1])
        with col_view:
            self._render_table_list()
        with col_manage:
            self._render_add_form()
            st.divider()
            self._render_delete_section()

    def _render_table_list(self):
        st.subheader("Current Layout")
        df = self.vm.get_tables_dataframe()
        if df.empty:
            st.info("No tables configured yet.")
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
        if st.button("🔄 Refresh Layout"):
            st.rerun()

    def _render_add_form(self):
        st.subheader("Add New Table")
        existing_locs = self.vm.get_existing_locations()
        NEW_LOC_OPT = "➕ New Location..."
        options = existing_locs + [NEW_LOC_OPT]
        selected_opt = st.selectbox("Location", options=options)
        final_location = selected_opt
        if selected_opt == NEW_LOC_OPT:
            final_location = st.text_input(
                "Enter Location Name", placeholder="e.g. Rooftop"
            )
        next_num = self.vm.get_next_suggestion()
        with st.form("add_table_form"):
            t_num = st.number_input("Table Number", min_value=1, step=1, value=next_num)
            t_cap = st.number_input("Capacity", min_value=1, step=1, value=4)
            if self.vm.is_number_occupied(t_num):
                st.warning(f"⚠️ Table {t_num} exists. Choosing this will fail.")

            if st.form_submit_button("Create Table", width="stretch"):
                if self.vm.add_table(
                    number=t_num, capacity=t_cap, location=final_location
                ):
                    st.success(f"✅ Table {t_num} created!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(self.vm.last_error)

    def _render_delete_section(self):
        st.subheader("Remove Table")
        if not self.vm.tables:
            st.caption("No tables to remove.")
            return
        table_map = {t.id: f"Table {t.number} ({t.location})" for t in self.vm.tables}

        selected_id = st.selectbox(
            "Select Table", options=table_map.keys(), format_func=lambda x: table_map[x]
        )
        if st.button("🗑️ Delete Selected Table", type="primary"):
            if self.vm.delete_table(selected_id):
                st.success("Table removed.")
                time.sleep(1)
                st.rerun()
            else:
                st.error(self.vm.last_error)