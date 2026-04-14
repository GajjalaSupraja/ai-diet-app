import streamlit as st
import requests
import os
from dotenv import load_dotenv

import sys
from database.db import init_db, save_history, get_history, create_user, login_user, get_user, update_photo

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ================= SESSION =================

if "user" not in st.session_state:
    st.session_state.user = None


# ================= INIT =================

init_db()
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# ================= LOGIN =================

if st.session_state.user is None:

    st.title("AI Diet System Login")

    tab1, tab2 = st.tabs(["Login", "Signup"])

    # -------- LOGIN --------
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):

            user = login_user(email, password)

            if user:
                st.session_state.user = user[1]
                st.rerun()
            else:
                st.error("Invalid credentials")

    # -------- SIGNUP --------
    with tab2:
        name = st.text_input("Name", key="signup_name")
        email_s = st.text_input("Email", key="signup_email")
        password_s = st.text_input("Password", type="password", key="signup_password")

        uploaded_file = st.file_uploader(
            "Upload Profile Photo",
            type=["jpg","png"],
            key="signup_photo"
        )

        photo_path = ""

        if uploaded_file is not None:

            if not os.path.exists("images"):
                os.makedirs("images")

            photo_path = f"images/{uploaded_file.name}"

            with open(photo_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

        # -------- SIGNUP --------
        if st.button("Signup"):

            if not name or not email_s or not password_s:
                st.error("Please fill all fields")
            elif "@" not in email_s:
                st.error("Invalid email")
            elif len(password_s) < 6:
                st.error("Password must be at least 6 characters")
            else:
                ok = create_user(
                    name,
                    email_s,
                    password_s,
                    photo_path if photo_path else None
                )

                if ok:
                    st.success("Account created. Please login")
                else:
                    st.error("Email already exists")

    st.stop()


# ================= SIDEBAR =================

st.sidebar.title("Dashboard")

st.sidebar.write(f"Welcome {st.session_state.user}")

menu = st.sidebar.radio(
    "Navigation",
    ["Generate Diet", "My History", "Profile"]
)

if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.rerun()


# ================= GENERATE PAGE =================

if menu == "Generate Diet":

    st.title("🥗 Dual AI Personalized Diet Recommendation")
    st.caption("AI Generator + Clinical Verifier")
    st.divider()

    st.subheader("User Details")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", 10, 80)
        weight = st.number_input("Weight (kg)")
        goal = st.selectbox(
            "Goal",
            ["Weight Loss","Muscle Gain","Maintain Weight"]
        )

    with col2:
        gender = st.selectbox("Gender", ["Male","Female","Other"])
        height = st.number_input("Height (cm)", 100, 220)
        activity = st.selectbox(
            "Activity Level",
            ["Low","Moderate","High"]
        )

    diet = st.selectbox(
        "Diet Type",
        ["Vegetarian","Non-Vegetarian","Vegan"]
    )

    allergy = st.text_input("Food Allergy (optional)")
    health = st.text_input("Health Condition (optional)")

    if height > 0:
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        st.info(f"BMI: {round(bmi,2)}")
    else:
        bmi = 0

    st.markdown("### User Summary")

    st.info(f"""
    Age: {age}
    Gender: {gender}
    Weight: {weight} kg
    Height: {height} cm
    Goal: {goal}
    Diet: {diet}
    Activity: {activity}
    Allergy: {allergy}
    Health: {health}
    """)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        generate = st.button("Generate AI Diet Plan")

    if generate:

        with st.spinner("Generating AI Diet..."):

            response = requests.post(
                "http://127.0.0.1:8000/generate-diet",
                json={
                    "age": age,
                    "gender": gender,
                    "weight": weight,
                    "height": height,
                    "goal": goal,
                    "diet": diet,
                    "activity": activity,
                    "allergy": allergy,
                    "health": health
                }
            )

            try:
                if response.status_code == 200:
                    data = response.json()
                    draft = data["data"]["draft"]
                    final = data["data"]["final"]
                else:
                    st.error("Server error")
            except Exception as e:
                st.error(f"Error: {e}")

            st.session_state["llm1"] = draft
            st.session_state["llm2"] = final

            save_history(st.session_state.user, age, goal, diet, final)

    if "llm2" in st.session_state:

        tab1, tab2 = st.tabs(["Verified Diet Plan", "Draft Plan"])

        with tab1:
            st.subheader("AI Verified Diet Plan")
            st.write(st.session_state["llm2"])

            st.download_button(
                "Download Diet Plan",
                st.session_state["llm2"],
                file_name="AI_Diet.txt"
            )

        with tab2:
            st.subheader("LLM1 Draft")
            st.write(st.session_state["llm1"])


# ================= HISTORY =================

elif menu == "My History":

    st.title("My Previous Diet Plans")

    history = get_history(st.session_state.user)

    if not history:
        st.info("No history found")

    for row in history[::-1]:
        with st.expander(f"{row[3]} - Age {row[2]}"):
            st.write(row[5])


# ================= PROFILE =================

elif menu == "Profile":

    user_name = st.session_state.user

    user_data = get_user(user_name)

    photo_path = None

    if user_data and len(user_data) > 4:
        photo_path = user_data[4]

    col1, col2 = st.columns([3,1])

    with col1:
        st.title("👤 User Profile")

    with col2:
        if photo_path and os.path.exists(photo_path):
            st.image(photo_path, width=100)

    st.subheader("Account Details")
    st.write(f"👤 Name: {user_name}")

    st.subheader("Update Profile Photo")

    new_file = st.file_uploader("Upload New Photo", type=["jpg", "png"])

    if new_file is not None:

        if not os.path.exists("images"):
            os.makedirs("images")

        new_path = f"images/{new_file.name}"

        with open(new_path, "wb") as f:
            f.write(new_file.getbuffer())

        update_photo(user_name, new_path)

        st.success("Photo uploaded successfully!")
        st.rerun()

    st.subheader("Session Info")
    st.write("🟢 Logged in successfully")