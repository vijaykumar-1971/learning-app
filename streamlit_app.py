import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="Synapse Learning Tracker", layout="wide")
st.title("🧠 Synapse: Learning Progress Tracker")
st.markdown("Track your journey from *Student* to *Professional*.")

# --- DATABASE CONNECTION ---
# This uses the URL stored in your Streamlit Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- LOAD DATA ---
# We use ttl=0 so the app refreshes immediately when the sheet changes
df = conn.read(ttl=0)

# Clean up empty rows if they exist
df = df.dropna(how="all")

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Tasks")
level_filter = st.sidebar.multiselect(
    "Select Level:",
    options=df["Level"].unique() if not df.empty else ["Student", "Skill", "Professional"],
    default=df["Level"].unique() if not df.empty else []
)

# Apply filter
if level_filter:
    filtered_df = df[df["Level"].isin(level_filter)]
else:
    filtered_df = df

# --- DASHBOARD SECTION ---
st.subheader("📊 Your Progress")
if not filtered_df.empty:
    # Calculate progress %
    total_tasks = len(filtered_df)
    completed_tasks = len(filtered_df[filtered_df["Status"] == "Completed"])
    progress_idx = completed_tasks / total_tasks

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Mastery", f"{int(progress_idx * 100)}%")
        st.progress(progress_idx)
    with col2:
        st.metric("Tasks Completed", f"{completed_tasks} / {total_tasks}")
else:
    st.info("No tasks found. Add your first goal below!")

st.divider()

# --- MAIN DATA TABLE ---
st.subheader("📝 Learning Roadmap")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)

# --- ADD NEW TASK FORM ---
st.divider()
st.subheader("➕ Add New Learning Goal")

with st.form("new_goal_form"):
    col1, col2 = st.columns(2)
    with col1:
        new_task = st.text_input("What are you learning?")
        new_category = st.selectbox("Category", ["Coding", "Business", "Academic", "Soft Skills"])
    with col2:
        new_level = st.selectbox("Level", ["Student", "Skill", "Professional"])
        new_deadline = st.date_input("Target Completion Date")
    
    submit_button = st.form_submit_button("Add to Roadmap")

    if submit_button:
        if new_task:
            # Create a new row of data
            new_data = pd.DataFrame([{
                "Goal/Task": new_task,
                "Category": new_category,
                "Level": new_level,
                "Deadline": new_deadline.strftime("%Y-%m-%d"),
                "Status": "Pending"
            }])
            
            # Combine with existing data
            updated_df = pd.concat([df, new_data], ignore_index=True)
            
            # Update the Google Sheet
            conn.update(data=updated_df)
            
            st.success("Goal added! Refreshing...")
            st.rerun()
        else:
            st.error("Please enter a task name.")
