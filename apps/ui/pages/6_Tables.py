import sys
from pathlib import Path
import streamlit as st

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
import pandas as pd
from apps.api.modules import TableCreate
from apps.ui.services.tables import TableService
from apps.ui.utils.exceptions import AppError

table_service = TableService()

st.title("🪑 Table Layout")
st.markdown("Configure the physical layout of the restaurant.")

try:
    tables = table_service.get_tables()
except AppError as e:
    st.error(f"Could not load tables: {e}")
    tables = []

if tables:
    occupied_numbers = {t.number for t in tables}
    existing_locations = sorted(list({t.location for t in tables}))
    next_suggestion = max(occupied_numbers) + 1
else:
    occupied_numbers = set()
    existing_locations = []
    next_suggestion = 1

col_view, col_add = st.columns([2, 1])

with col_view:
    st.subheader("Current Tables")
    if not tables:
        st.info("No tables configured.")
    else:
        df = pd.DataFrame([t.model_dump() for t in tables])
        st.dataframe(
            df,
            width="stretch",
            hide_index=True,
            column_config={
                "id": "ID",
                "number": "Table #",
                "capacity": "Seats",
                "is_occupied": st.column_config.CheckboxColumn("Occupied?"),
            },
        )

with col_add:
    st.subheader("Add Table")
    loc_options = existing_locations + ["➕ New Location..."]
    selected_loc_option = st.selectbox(
        "Location", options=loc_options, index=0 if existing_locations else 0
    )
    if selected_loc_option == "➕ New Location...":
        final_location = st.text_input(
            "Enter Location Name", placeholder="e.g. Rooftop Patio"
        )
    else:
        final_location = selected_loc_option
    table_number = st.number_input(
        "Visible Table Number",
        min_value=1,
        value=next_suggestion,
        step=1,
        help="We suggested the next available number, but you can change it.",
    )
    is_duplicate = table_number in occupied_numbers
    if is_duplicate:
        st.error(f"⛔ Table {table_number} already exists!")
    capacity = st.number_input("Seat Capacity", min_value=1, max_value=20, value=4)
    submit_disabled = is_duplicate or (not final_location)
    if st.button(
        "Add Table", type="primary", use_container_width=True, disabled=submit_disabled
    ):
        try:
            payload = TableCreate(
                capacity=capacity, location=final_location, number=table_number
            )
            table_service.create_table(payload)
            st.success(f"✅ Table {table_number} added!")
            st.rerun()
        except AppError as e:
            st.error(f"Error: {e}")