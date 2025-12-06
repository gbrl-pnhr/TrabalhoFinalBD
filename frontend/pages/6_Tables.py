import streamlit as st
import pandas as pd
from services.tables import TableService
from schemas import TableCreate
from utils.exceptions import AppError

table_service = TableService()

st.title("🪑 Table Layout")
st.markdown("Configure the physical layout of the restaurant.")

col_view, col_add = st.columns([2, 1])

with col_view:
    st.subheader("Current Tables")
    try:
        tables = table_service.get_tables()
        if not tables:
            st.info("No tables configured.")
        else:
            df = pd.DataFrame([t.model_dump() for t in tables])
            st.dataframe(
                df,
                width='stretch',
                hide_index=True,
                column_config={
                    "id": "Table #",
                    "capacity": "Seats",
                    "is_occupied": st.column_config.CheckboxColumn("Occupied?"),
                },
            )
    except AppError as e:
        st.error(f"Could not load tables: {e}")

with col_add:
    st.subheader("Add Table")
    with st.form("add_table_form"):
        capacity = st.number_input("Seat Capacity", min_value=1, max_value=20, value=4)
        location = st.text_input("Location (e.g. Patio, Main Hall)", value="Main Hall")
        number = st.number_input("Visible Table Numer", min_value=1)

        if st.form_submit_button("Add Table", width='stretch'):
            try:
                payload = TableCreate(capacity=capacity, location=location, number=number)
                table_service.create_table(payload)
                st.success("✅ Table added!")
                st.rerun()
            except AppError as e:
                st.error(f"Error: {e}")