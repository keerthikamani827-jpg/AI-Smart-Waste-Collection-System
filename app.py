import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Smart Waste Collection System",
    page_icon="♻️",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.stButton>button{
    background-color:#1f4e79;
    color:white;
    border-radius:8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- FILE ----------------
DATA_FILE = "data.csv"

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "points" not in st.session_state:
    st.session_state.points = 100

# ---------------- LOAD DATA ----------------
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=[
        "Date",
        "Area",
        "Waste_Type",
        "Weight_kg",
        "Status"
    ])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# ---------------- TITLE ----------------
st.title("♻️ AI Smart Waste Collection System")
st.caption("Transforming Waste Management with AI and Data Analytics")

# ---------------- LOGIN ----------------
if not st.session_state.logged_in:

    st.subheader("Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username and password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Enter valid credentials")

# ---------------- DASHBOARD ----------------
else:

    st.success(f"Welcome {st.session_state.username}")

    total_waste = df["Weight_kg"].sum() if len(df) > 0 else 0

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Waste", f"{total_waste} kg")
    c2.metric("Eco Points", st.session_state.points)
    c3.metric("CO₂ Saved", f"{int(total_waste*0.4)} kg")

    st.divider()

    st.subheader("Waste Reporting")

    area = st.text_input("Area")

    waste_type = st.selectbox(
        "Waste Type",
        ["Organic","Plastic","Metal","Paper","Glass"]
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=0.0
    )

    if st.button("Submit Report"):

        new_data = pd.DataFrame([{
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Area": area,
            "Waste_Type": waste_type,
            "Weight_kg": weight,
            "Status": "Pending"
        }])

        df = pd.concat([df, new_data], ignore_index=True)
        save_data(df)

        st.session_state.points += 10

        st.success("Waste Report Submitted Successfully")
        st.balloons()
        st.divider()

    # ---------------- IMAGE UPLOAD ----------------

    st.subheader("📸 Upload Waste Image")

    uploaded_file = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        st.image(uploaded_file, width=300)
        st.success("Image Uploaded Successfully")

    st.divider()

    # ---------------- ANALYTICS ----------------

    st.subheader("📊 Analytics Dashboard")

    if len(df) > 0:

        st.dataframe(df)

        st.bar_chart(
            df.groupby("Waste_Type")["Weight_kg"].sum()
        )

        st.bar_chart(
            df.groupby("Area")["Weight_kg"].sum()
        )

        st.bar_chart(
            df["Status"].value_counts()
        )

    else:
        st.info("No data available")

    st.divider()

    # ---------------- LOCATION MAP ----------------

    st.subheader("🗺️ Waste Location Map")

    map_data = pd.DataFrame({
        "lat": [13.0827],
        "lon": [80.2707]
    })

    st.map(map_data)
    st.divider()

    # ---------------- AI CHATBOT ----------------

    st.subheader("🤖 AI Waste Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input(
        "Ask about waste management..."
    )

    if prompt:

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        if "plastic" in prompt.lower():
            answer = """
♻️ Plastic waste should be separated and recycled properly.
Avoid single-use plastics whenever possible.
"""

        elif "organic" in prompt.lower():
            answer = """
🌱 Organic waste can be converted into compost.
This helps reduce landfill waste.
"""

        elif "paper" in prompt.lower():
            answer = """
📄 Paper waste should be kept dry for better recycling.
"""

        elif "metal" in prompt.lower():
            answer = """
🔩 Metal waste is highly recyclable and should be separated.
"""

        elif "glass" in prompt.lower():
            answer = """
🍾 Glass can be recycled multiple times without losing quality.
"""

        elif "points" in prompt.lower():
            answer = f"""
🏆 Your Eco Points: {st.session_state.points}
"""

        else:
            answer = """
♻️ Segregate waste properly.
🌍 Keep your surroundings clean.
🚛 Smart waste collection improves sustainability.
"""

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        st.rerun()

    st.divider()

    # ---------------- LOGOUT ----------------

    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()
