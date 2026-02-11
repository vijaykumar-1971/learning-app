import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Title and App Config
st.title("🚀 Synapse Progress Tracker")

# 1. Connect to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Read the data
# Replace the URL below with your actual Google Sheet URL
url = "https://docs.google.com/spreadsheets/d/your-id-here/edit#gid=0"
df = conn.read(spreadsheet=url)

# 3. Display a high-level progress bar
progress = df['Status'].value_counts(normalize=True).get('Completed', 0)
st.metric("Overall Mastery", f"{int(progress * 100)}%")
st.progress(progress)

# 4. Show the interactive table
st.subheader("Your Learning Roadmap")
st.dataframe(df)

# 5. Add a "Quick Update" form (Optional)
with st.form("add_task"):
    new_task = st.text_input("New Learning Task")
    if st.form_submit_button("Add to Sheet"):
        st.info("To write back to the sheet, you'll need to set up 'Service Account' keys in step 4.")
