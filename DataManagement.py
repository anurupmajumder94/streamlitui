import streamlit as st
import pandas as pd
from datetime import datetime
from app import get_initial_data

st.set_page_config(layout="wide", page_title="Data Management", page_icon="favicon.ico")

def local_css(file_name):
    with open(file_name) as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
local_css("style.css")

# Custom Bootstrap-like navbar using HTML + CSS
st.markdown("""
<div class="navbar">
    <a href="#" class="brand">Application Name</a>
    <div>Data Management</div>
</div>
""", unsafe_allow_html=True)

if "df_incidents" not in st.session_state:
    st.session_state.df_incidents = get_initial_data()

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

df = st.session_state.df_incidents

search_query = st.text_input("🔍 Search by Incident ID", "")

if search_query:
    df_filtered = df[df["Incident ID"].str.contains(search_query.strip(), case=False, na=False)]
else:
    df_filtered = df

header_cols = st.columns([2, 2, 2, 2, 2, 3, 1, 1])
headers = ["Incident ID", "Date Reported", "Status", "Priority", "Assigned To", "Description", "Edit", "Delete"]
for col, header in zip(header_cols, headers):
    col.markdown(f"**{header}**")


for display_index, (i, row) in enumerate(df_filtered.iterrows()):
    cols = st.columns([2, 2, 2, 2, 2, 3, 1, 1])

    cols[0].markdown(row["Incident ID"])
    cols[1].markdown(row["Date Reported"].strftime("%Y-%m-%d"))
    cols[2].markdown(row["Status"])
    cols[3].markdown(row["Priority"])
    cols[4].markdown(row["Assigned To"])
    cols[5].markdown(row["Description"])

    if cols[6].button("✏️", key=f"update_{i}"):
        st.session_state.edit_index = i

    if cols[7].button("🗑️", key=f"delete_{i}"):
        st.session_state.df_incidents.drop(i, inplace=True)
        st.session_state.df_incidents.reset_index(drop=True, inplace=True)
        st.success(f"✅ Incident {row['Incident ID']} deleted.")
        st.rerun()

form_mode = "Update" if st.session_state.edit_index is not None else "Add"
form_expanded = st.session_state.edit_index is not None

with st.expander(f"➕ {form_mode} Incident", expanded=form_expanded):
    with st.form("incident_form"):
        if st.session_state.edit_index is not None:
            incident = df.iloc[st.session_state.edit_index]
            status_default = incident["Status"]
            priority_default = incident["Priority"]
            assigned_to_default = incident["Assigned To"]
            description_default = incident["Description"]
        else:
            status_default = "Open"
            priority_default = "Low"
            assigned_to_default = ""
            description_default = ""

        status = st.selectbox("Status", ["Open", "In Progress", "Resolved"], index=["Open", "In Progress", "Resolved"].index(status_default))
        priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(priority_default))
        assigned_to = st.text_input("Assigned To", value=assigned_to_default)
        description = st.text_area("Description", value=description_default)

        submitted = st.form_submit_button(f"{form_mode} Incident")

        if submitted:
            if st.session_state.edit_index is not None:
                idx = st.session_state.edit_index
                st.session_state.df_incidents.at[idx, "Status"] = status
                st.session_state.df_incidents.at[idx, "Priority"] = priority
                st.session_state.df_incidents.at[idx, "Assigned To"] = assigned_to
                st.session_state.df_incidents.at[idx, "Description"] = description
                st.success(f"✅ Incident {df.at[idx, 'Incident ID']} updated successfully.")
                st.session_state.edit_index = None
            else:
                new_id = f"INC{1000 + len(df) + 1}"
                new_row = {
                    "Incident ID": new_id,
                    "Date Reported": datetime.now(),
                    "Status": status,
                    "Priority": priority,
                    "Assigned To": assigned_to,
                    "Description": description
                }
                st.session_state.df_incidents = st.session_state.df_incidents._append(new_row, ignore_index=True)
                st.success(f"✅ Incident {new_id} added successfully.")

            st.rerun()