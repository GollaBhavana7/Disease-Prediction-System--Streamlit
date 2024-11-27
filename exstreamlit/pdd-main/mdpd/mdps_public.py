import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import re

# Load saved models
diabetes_model = pickle.load(open('exstreamlit/pdd-main/mdpd/diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open('exstreamlit/pdd-main/mdpd/heart_disease_model.sav', 'rb'))
parkinsons_model = pickle.load(open('exstreamlit/pdd-main/mdpd/parkinsons_model.sav', 'rb'))

# Dictionary to store user data temporarily
users_db = {}

# Function to validate email format (checks for basic email structure and @gmail.com)
def validate_email(email):
    email = email.strip().lower()
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    if not email.endswith("@gmail.com"):
        return False
    return True

# Function to authenticate login
def authenticate(email, password):
    email = email.strip().lower()
    if email in users_db and users_db[email]["password"] == password:
        return True
    else:
        return False

# Function to register a new user (Signup)
def signup(name, email, password):
    email = email.strip().lower()
    if email in users_db:
        return False  # Email already exists
    # Save user details in the "database"
    users_db[email] = {"name": name, "password": password}
    return True

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "name" not in st.session_state:
    st.session_state.name = None
if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Home"

# Sidebar for navigation
with st.sidebar:
    if not st.session_state.logged_in:
        selected = option_menu(
            "Predictive Disease Detection App",
            ["Login", "Signup"],
            icons=["key", "person-plus"],
            default_index=0,
        )
    else:
        selected = option_menu(
            "Predictive Disease Detection App",
            [
                "Home",
                "Diabetes Prediction",
                "Heart Disease Prediction",
                "Parkinson's Prediction",
                "Logout",
            ],
            icons=["house", "activity", "heart", "person", "box-arrow-right"],
            default_index=0,
        )

# Handle Logout separately
if selected == "Logout":
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.name = None
    st.session_state.selected_page = "Home"
    st.success("You have been logged out.")
    st.stop()

# Set background images based on selected page
background_images = {
    "Diabetes Prediction": 'https://raw.githubusercontent.com/GollaBhavana7/exstreamlit/main/exstreamlit/pdd-main/mdpd/images/diabeties_background.jpg',
    "Heart Disease Prediction": 'https://raw.githubusercontent.com/GollaBhavana7/exstreamlit/main/exstreamlit/pdd-main/mdpd/images/heart_disease_background.jpg',
    "Parkinson's Prediction": 'https://raw.githubusercontent.com/GollaBhavana7/exstreamlit/main/exstreamlit/pdd-main/mdpd/images/parkinsons_background.jpg'
}

if selected in background_images:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.9)), 
                              url('{background_images[selected]}');
            background-size: cover;
            background-position: center;
        }}
        </style>
        """, unsafe_allow_html=True
    )

# Signup Page
if selected == "Signup":
    st.title("Signup Page")

    # Signup form fields
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Create Account"):
        # Validate email and password
        if not validate_email(email):
            st.error("Please enter a valid Gmail address (e.g., example@gmail.com).")
        elif password != confirm_password:
            st.error("Passwords do not match. Please try again.")
        elif signup(name, email, password):
            st.success(f"Account created successfully for {name}!")
            st.session_state.logged_in = True
            st.session_state.user = email
            st.session_state.name = name
            st.session_state.selected_page = "Home"
        else:
            st.error("This email is already registered. Please login.")

# Login Page
elif selected == "Login":
    st.title("Login Page")

    # Login form fields
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Validate email and password
        if not validate_email(email):
            st.error("Please enter a valid Gmail address (e.g., example@gmail.com).")
        elif authenticate(email, password):
            st.session_state.logged_in = True
            st.session_state.user = email
            st.session_state.name = users_db[email]["name"]
            st.session_state.selected_page = "Home"
            st.success("Login successful!")
        else:
            st.error("Invalid email or password. Please try again.")

# Disease Prediction Pages (visible after successful login)
if st.session_state.logged_in:
    if selected == "Home":
        st.title("Welcome to Predictive Disease Detection App")
        st.write(
            """
            This application uses machine learning to predict the likelihood of the following diseases:
            - Diabetes
            - Heart Disease
            - Parkinson's Disease
            
            Select a disease prediction option from the sidebar to get started.
            """
        )
    
    elif selected == "Diabetes Prediction":
        st.title("Diabetes Prediction using ML")

        # Input fields
        patient_name = st.text_input("Patient Name")
        Pregnancies = st.number_input("Number of Pregnancies", min_value=0)
        Glucose = st.number_input("Glucose Level", min_value=0)
        BloodPressure = st.number_input("Blood Pressure value", min_value=0)
        SkinThickness = st.number_input("Skin Thickness value", min_value=0)
        Insulin = st.number_input("Insulin Level", min_value=0)
        BMI = st.number_input("BMI value", min_value=0.0, format="%.2f")
        DiabetesPedigreeFunction = st.number_input("Diabetes Pedigree Function value", min_value=0.0, format="%.2f")
        Age = st.number_input("Age of the Person", min_value=0)
        
        if st.button("Diabetes Test Result"):
            # Model prediction
            try:
                diab_prediction = diabetes_model.predict(
                    [[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]]
                )
                result = "Positive" if diab_prediction[0] == 1 else "Negative"
            except Exception as e:
                st.error("Error during prediction. Check your model or input data.")
                result = None

            if result:
                # Display Test Result
                st.markdown(f"### Test Result: {result}")
                st.markdown("#### [Click here to see Test Report](#)")

                # Patient Information
                st.markdown(f"""
                **Patient Name**: {patient_name}    
                **Age**: {Age}
                """)

                # Tabular Data
                test_data = {
                    "Parameter Name": [
                        "Pregnancies", "Glucose", "Blood Pressure", "Skin Thickness", 
                        "Insulin", "BMI", "Diabetes Pedigree Function"
                    ],
                    "Patient Values": [
                        Pregnancies, Glucose, BloodPressure, SkinThickness, 
                        Insulin, BMI, DiabetesPedigreeFunction
                    ],
                    "Normal Range": [
                        "0-10", "70-125", "120/80", "8-25", "25-250", "18.5-24.9", "< 1"
                    ],
                    "Unit": [
                        "Number", "mg/dL", "mmHg", "mm", "mIU/L", "kg/m^2", "No units"
                    ]
                }

                st.table(test_data)

                # Email Message
                st.markdown("ℹ️ **Do check your email for more details, Thank You.**")

    elif selected == "Heart Disease Prediction":
        st.title('Heart Disease Prediction using ML')
        
        # Input fields for heart disease prediction
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.number_input('Age')
        with col2:
            sex = st.number_input('Sex')
        with col3:
            cp = st.number_input('Chest Pain types')
        with col1:
            trestbps = st.number_input('Resting Blood Pressure')
        with col2:
            chol = st.number_input('Serum Cholestoral in mg/dl')
        with col3:
            fbs = st.number_input('Fasting Blood Sugar > 120 mg/dl')
        with col1:
            restecg = st.number_input('Resting Electrocardiographic results')
        with col2:
            thalach = st.number_input('Maximum Heart Rate achieved')
        with col3:
            exang = st.number_input('Exercise Induced Angina')
        with col1:
            oldpeak = st.number_input('Depression induced by exercise relative to rest')
        with col2:
            slope = st.number_input('Slope of the peak exercise ST segment')
        with col3:
            ca = st.number_input('Number of major vessels colored by fluoroscopy')
        with col1:
            thal = st.number_input('thalassemia')

        if st.button("Heart Disease Test Result"):
            # Model prediction
            try:
                heart_prediction = heart_disease_model.predict(
                    [[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]]
                )
                result = "Positive" if heart_prediction[0] == 1 else "Negative"
            except Exception as e:
                st.error("Error during prediction. Check your model or input data.")
                result = None

            if result:
                # Display Test Result
                st.markdown(f"### Test Result: {result}")
                st.markdown("#### [Click here to see Test Report](#)")

                # Patient Information
                st.markdown(f"""
                **Patient Name**: {patient_name}    
                **Age**: {age}
                """)

    elif selected == "Parkinson's Prediction":
        st.title("Parkinson's Disease Prediction using ML")
        
        # Add relevant fields for Parkinson's prediction and processing logic...
        
    else:
        st.warning("Page not recognized.")
