import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import re

# Load saved models (adjust the paths based on your environment)
diabetes_model = pickle.load(open('exstreamlit/pdd-main/mdpd/diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open('exstreamlit/pdd-main/mdpd/heart_disease_model.sav', 'rb'))
parkinsons_model = pickle.load(open('exstreamlit/pdd-main/mdpd/parkinsons_model.sav', 'rb'))

# Dictionary to store user data temporarily (for simplicity)
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
if selected == "Diabetes Prediction":
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.9)), 
                              url('https://raw.githubusercontent.com/GollaBhavana7/exstreamlit/main/exstreamlit/pdd-main/mdpd/images/diabeties_background.jpg');
            background-size: cover;
            background-position: center;
        }}
        </style>
        """, unsafe_allow_html=True
    )

elif selected == "Heart Disease Prediction":
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.9)), 
                              url('https://raw.githubusercontent.com/GollaBhavana7/exstreamlit/main/exstreamlit/pdd-main/mdpd/images/heart_disease_background.jpg');
            background-size: cover;
            background-position: center;
        }}
        </style>
        """, unsafe_allow_html=True
    )

elif selected == "Parkinson's Prediction":
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.9)), 
                              url('https://raw.githubusercontent.com/GollaBhavana7/exstreamlit/main/exstreamlit/pdd-main/mdpd/images/parkinsons_background.jpg');
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
            diab_prediction = diabetes_model.predict(
                [[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]]
            )
            result = "The person is diabetic" if diab_prediction[0] == 1 else "The person is not diabetic"
    
            st.markdown(
                f"""
                <div style="background-color: #333333; padding: 10px; border-radius: 5px; color: white;">
                    <p style="margin: 0;"><strong>Patient:</strong> {patient_name}</p>
                    <p style="margin: 0;"><strong>Age:</strong> {Age}</p>
                    <p style="margin: 0;"><strong>Result:</strong> {result}</p>
                </div>
                """, unsafe_allow_html=True
            )


    elif selected == "Heart Disease Prediction":
        st.title('Heart Disease Prediction using ML')
        
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
            oldpeak = st.number_input('ST depression induced by exercise')
            
        with col2:
            slope = st.number_input('Slope of the peak exercise ST segment')
            
        with col3:
            ca = st.number_input('Major vessels colored by flourosopy')
            
        with col1:
            thal = st.number_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')

        with col2:
            patient_name = st.text_input("Patient Name")
            
        if st.button('Heart Disease Test Result'):
            heart_prediction = heart_disease_model.predict([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
    
            heart_diagnosis = 'The person does not have heart disease' if heart_prediction == 0 else 'The person has heart disease'

            st.markdown(
                f"""
                <div style="background-color: #333333; padding: 10px; border-radius: 5px; color: white;">
                    <p style="margin: 0;"><strong>Patient:</strong> {patient_name}</p>
                    <p style="margin: 0;"><strong>Age:</strong> {age}</p>
                    <p style="margin: 0;"><strong>Result:</strong> {heart_diagnosis}</p>
                </div>
                """, unsafe_allow_html=True
            )


     # Parkinson's Prediction Page
    elif selected == "Parkinson's Prediction":
        st.title("Parkinson's Disease Prediction using ML")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            patient_name = st.text_input("Patient Name")

        with col2:
            Age = st.number_input("Age of the Person", min_value=0)
        
        with col3:
            fo = st.text_input('MDVP:Fo(Hz)')

        with col4:
            fhi = st.text_input('MDVP:Fhi(Hz)')

        with col5:
            flo = st.text_input('MDVP:Flo(Hz)')

        with col1:
            Jitter_percent = st.text_input('MDVP:Jitter(%)')

        with col2:
            Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')

        with col3:
            RAP = st.text_input('MDVP:RAP')

        with col4:
            PPQ = st.text_input('MDVP:PPQ')

        with col5:
            DDP = st.text_input('Jitter:DDP')

        with col1:
            Shimmer = st.text_input('MDVP:Shimmer')

        with col2:
            Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')

        with col3:
            APQ3 = st.text_input('Shimmer:APQ3')

        with col4:
            APQ5 = st.text_input('Shimmer:APQ5')

        with col5:
            APQ = st.text_input('MDVP:APQ')

        with col1:
            DDA = st.text_input('Shimmer:DDA')

        with col2:
            NHR = st.text_input('NHR')

        with col3:
            HNR = st.text_input('HNR')

        with col4:
            RPDE = st.text_input('RPDE')

        with col5:
            DFA = st.text_input('DFA')

        with col1:
            spread1 = st.text_input('spread1')

        with col2:
            spread2 = st.text_input('spread2')

        with col3:
            D2 = st.text_input('D2')

        with col4:
            PPE = st.text_input('PPE')
    
        if st.button("Parkinson's Test Result"):
            user_input = [fo, fhi, flo, Jitter_percent, Jitter_Abs,
                              RAP, PPQ, DDP,Shimmer, Shimmer_dB, APQ3, APQ5,
                              APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]

            user_input = [float(x) for x in user_input]

            parkinsons_prediction = parkinsons_model.predict([user_input])
            parkinsons_diagnosis = ""
            if parkinsons_prediction[0] == 1:
                parkinsons_diagnosis = "The person has Parkinson's disease"
            else:
                parkinsons_diagnosis = "The person does not have Parkinson's disease"
                st.markdown(
                f"""
                <div style="background-color: #333333; padding: 10px; border-radius: 5px; color: white;">
                    <p style="margin: 0;"><strong>Patient:</strong> {name}</p>
                    <p style="margin: 0;"><strong>Age:</strong> {Age}</p>
                    <p style="margin: 0;"><strong>Result:</strong> {result}</p>
                </div>
                """, unsafe_allow_html=True
                )
