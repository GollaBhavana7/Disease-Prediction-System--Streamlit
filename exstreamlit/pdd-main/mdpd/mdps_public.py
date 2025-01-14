import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import re
import sqlite3
import pandas as pd

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )''')
    conn.commit()
    conn.close()

# Add a new user
def add_user(name, email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Authenticate user
def authenticate_user(email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = c.fetchone()
    conn.close()
    return user is not None

# Initialize the database
init_db()

# Load saved models
diabetes_model = pickle.load(open('exstreamlit/pdd-main/mdpd/diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open('exstreamlit/pdd-main/mdpd/heart_disease_model.sav', 'rb'))
parkinsons_model = pickle.load(open('exstreamlit/pdd-main/mdpd/parkinsons_model.sav', 'rb'))

def validate_email(email):
    email = email.strip().lower()
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) and email.endswith("@gmail.com")

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "name" not in st.session_state:
    st.session_state.name = None
if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Home"
if "show_report" not in st.session_state:
    st.session_state.show_report = False

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
                "Feedback and Contact",
                "Logout",
            ],
            icons=["house", "activity", "heart", "person", "envelope", "box-arrow-right"],
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
    "Diabetes Prediction": 'https://raw.githubusercontent.com/GollaBhavana7/exstreamlit/main/exstreamlit/pdd-main/mdpd/images/diabeties_background.jpg?raw=true',
    "Heart Disease Prediction": 'https://raw.githubusercontent.com/GollaBhavana7/exstreamlit/main/exstreamlit/pdd-main/mdpd/images/heart_disease_background.jpg?raw=true',
    "Parkinson's Prediction": 'https://raw.githubusercontent.com/GollaBhavana7/exstreamlit/main/exstreamlit/pdd-main/mdpd/images/parkinsons_background.jpg?raw=true'
}

if selected in background_images:
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.6)), 
                          url("{background_images[selected]}");
        background-size: cover;
        background-position: center;
    }}
    h1 {{
            font-size: 50px !important; /* Bigger size for h1 headings */
            color: darkblue !important; /* Optional: Change heading color */
            font-weight: bold !important; /* Optional: Make it bold */
            text-align: center !important; /* Optional: Center align heading */
        }}
    .stMarkdown, .stText, h1, h2, h3, h4, h5, h6, p, label {{
        color: #333333 !important; /* Dark text */
        font-weight: 600; /* Bold text */
        font-size: 18px !important; /* Increased font size */
    }}
    .stButton>button {{
        background-color: white !important; /* Button background to white */
        color: black !important; /* Button text color to black */
        border: 2px solid black !important; /* Optional border for contrast */
        border-radius: 8px !important; /* Rounded corners */
        font-size: 16px !important; /* Button font size */
        padding: 0.5em 1em !important; /* Adjust padding for better appearance */
        transition: background-color 0.3s, color 0.3s; /* Add a hover effect */
    }}
    .stButton>button:hover {{
        background-color: #f0f0f0 !important; /* Hover background color (light gray) */
        color: black !important; /* Hover text color */
    }}
    .stTable {{
        border: 2px solid #ccc !important; /* Table border */
        border-radius: 10px !important; /* Rounded table corners */
    }}
    </style>
    """,
    unsafe_allow_html=True,
)
    

# Signup Page
if selected == "Signup":
    st.title("Signup Page")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Create Account"):
        if not validate_email(email):
            st.error("Please enter a valid Gmail address (e.g., example@gmail.com).")
        elif password != confirm_password:
            st.error("Passwords do not match. Please try again.")
        elif add_user(name, email, password):
            st.success(f"Account created successfully for {name}!")
            st.session_state.logged_in = True
            st.session_state.user = email
            st.session_state.name = name
        else:
            st.error("This email is already registered. Please login.")


# Login Page
elif selected == "Login":
    st.title("Login Page")

    # Login form fields
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not validate_email(email):
            st.error("Please enter a valid Gmail address (e.g., example@gmail.com).")
        elif authenticate_user(email, password):
            st.session_state.logged_in = True
            st.session_state.user = email
            st.session_state.name = email.split("@")[0]
            st.success("Login successful!")
        else:
            st.error("Invalid email or password. Please try again.")
 
elif selected == "Feedback and Contact":
    st.title("Feedback Page")

    # Feedback form fields
    feedback_name = st.text_input("Your Name")
    feedback_email = st.text_input("Your Email")
    feedback_message = st.text_area("Your Feedback", height=150)

    if st.button("Submit Feedback"):
        if feedback_name and feedback_email and feedback_message:
            # Here you can add code to save the feedback to a database or send it via email
            st.success("Thank you for your feedback!")
        else:
            st.error("Please fill in all fields before submitting.")
    st.markdown("---")
    st.markdown("### Contact Information")
    st.markdown("For any queries or support, please reach out to us at:")
    st.markdown("- *Phone*: +91 7569325090")
    st.markdown("- *Email*: [bhavanagolla2003@gmail.com](mailto:bhavanagolla2003@gmail.com)")
    st.markdown("- *Email*: [punithajajam@gmail.com](mailto:punithajajam@gmail.com@gmail.com)")
    st.markdown("- *Email*: [buradarohit18@gmail.com](mailto:buradarohit18@gmail.com)")
    st.markdown("---")
        

# Disease Prediction Pages (visible after successful login)
if st.session_state.logged_in:
    # Home Page
    if selected == "Home":
        st.title("Welcome to the Predictive Disease Detection App")
        
        # Brief Introduction
        st.markdown("""
        This application leverages machine learning models to predict the likelihood of various diseases:
        - *Diabetes*
        - *Heart Disease*
        - *Parkinson's Disease*
        
        Select a disease prediction option from the sidebar to get started with predictions.
        """)
    
        # Section for Disease Information
        st.subheader("Disease Information")
        
        # Add interactive button for a user to show/hide disease details
        show_details = st.checkbox("Click to expand disease details", value=True)
        
        if show_details:
            # Create interactive sections for each disease
            st.write("### Diabetes")
            st.image("https://github.com/GollaBhavana7/exstreamlit/blob/main/exstreamlit/pdd-main/mdpd/images/sugar-blood-level.png?raw=true", width=150)
            
            with st.expander("Diabetes Overview", expanded=True):
                st.write("*Symptoms*")
                st.write("""
                - Increased thirst
                - Frequent urination
                - Extreme hunger
                - Unexplained weight loss
                - Presence of ketones in the urine
                - Fatigue
                - Irritability
                - Blurred vision
                """)
                
                st.write("*Causes*")
                st.write("""
                - Insulin resistance (Type 2 Diabetes)
                - Genetic factors
                - Age, with risk increasing after 45 years old
                - Lack of physical activity
                - Poor diet (high in sugar and unhealthy fats)
                - Obesity
                """)
                
                st.write("*Prevention*")
                st.write("""
                - Maintaining a healthy weight
                - Eating a balanced diet rich in fruits, vegetables, and whole grains
                - Regular physical activity
                - Avoiding excessive alcohol and tobacco use
                - Monitoring blood sugar levels, especially for those at risk
                """)
    
            # Heart Disease
            st.write("### Heart Disease")
            st.image("https://github.com/GollaBhavana7/exstreamlit/blob/main/exstreamlit/pdd-main/mdpd/images/heart-disease.png?raw=true", width=150)
    
            with st.expander("Heart Disease Overview", expanded=True):
                st.write("*Symptoms*")
                st.write("""
                - Chest pain or discomfort
                - Shortness of breath
                - Pain in the neck, back, jaw, stomach, or shoulder
                - Nausea, lightheadedness, or cold sweat
                - Pain in one or both arms
                - Fatigue
                """)
    
                st.write("*Causes*")
                st.write("""
                - High blood pressure
                - High cholesterol
                - Smoking
                - Lack of physical activity
                - Obesity
                - Diabetes
                - Family history of heart disease
                - Excessive alcohol consumption
                """)
    
                st.write("*Prevention*")
                st.write("""
                - Keeping a healthy weight
                - Eating a diet low in saturated fats, cholesterol, and sodium
                - Getting regular exercise
                - Avoiding smoking
                - Limiting alcohol intake
                - Managing stress effectively
                - Monitoring blood pressure and cholesterol levels
                """)
    
            # Parkinson's Disease
            st.write("### Parkinson's Disease")
            st.image("https://github.com/GollaBhavana7/exstreamlit/blob/main/exstreamlit/pdd-main/mdpd/images/parkinsons%20icon.png?raw=true", width=150)
    
            with st.expander("Parkinson's Disease Overview", expanded=True):
                st.write("*Symptoms*")
                st.write("""
                - Tremors (shaking), often in hands or fingers
                - Muscle stiffness
                - Slowness of movement (bradykinesia)
                - Impaired posture and balance
                - Difficulty walking
                - Speech changes (soft or slurred voice)
                - Writing changes (small handwriting)
                - Decreased sense of smell
                """)
    
                st.write("*Causes*")
                st.write("""
                - Loss of dopamine-producing brain cells
                - Genetic mutations (rare, but some forms of Parkinson's disease run in families)
                - Environmental factors, such as exposure to toxins or head injuries
                - Age, typically affecting those over 60
                - Gender, with men being more likely to develop Parkinson's than women
                """)
    
                st.write("*Prevention*")
                st.write("""
                - Regular physical exercise, especially aerobic exercises
                - Healthy diet, rich in antioxidants and vitamins
                - Avoiding exposure to toxins (such as pesticides or heavy metals)
                - Protecting the head from injury
                """)
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
                    [[Pregnancies, Glucose (0-180), BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]]
                )
                result = "Positive" if diab_prediction[0] == 1 else "Negative"
            except Exception as e:
                st.error("Error during prediction. Check your model or input data.")
                result = None
            if result:
                # Display test result message
                st.markdown(f"### Test Result: {result}")
                # Set session state for showing the report
                st.session_state.show_report = True
        if st.session_state.show_report:
            show_report = st.button("Click here to see Test Report")
            if show_report:
                # Patient Information
                st.markdown(f"#### Patient Information:")
                st.markdown(f"*Patient Name*: {patient_name}")
                st.markdown(f"*Age*: {Age}")

                # Test Parameters and Values
                st.markdown(f"#### Test Parameters and Values:")
                # Ensure test_data is defined here
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
        
                # Convert to DataFrame
                df = pd.DataFrame(test_data)
        
                # Style the DataFrame
                styled_df = df.style.set_table_styles([
                    {"selector": "thead", "props": [("background-color", "#4CAF50"), ("color", "white"), ("font-weight", "bold"), ("text-align", "center")]},
                    {"selector": "tbody", "props": [("color", "black"), ("font-weight", "bold"), ("text-align", "center")]},
                    {"selector": "tbody tr:nth-child(even)", "props": [("background-color", "#f9f9f9")]},
                    {"selector": "tbody tr:hover", "props": [("background-color", "#e0f7fa")]}  # Highlight on hover
                ])
        
                # Display the styled DataFrame
                st.dataframe(
                    styled_df,
                    use_container_width=True
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
            try:
                # Prepare the input data
                inputs = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
        
                # Ensure that no inputs are missing or invalid
                if any(i is None or i == '' for i in inputs):
                    st.error("Please ensure all fields are filled.")
                else:
                    # Perform the prediction using the heart disease model
                    heart_prediction = heart_disease_model.predict([inputs])
            
                    # Interpret the result
                    heart_result = "Positive" if heart_prediction[0] == 1 else "Negative"
                    st.markdown(f"### Test Result: {heart_result}")
            
                    # Show detailed information in a report
                    st.session_state.show_report = True
            except Exception as e:
                st.error(f"An error occurred during prediction: {e}")

        # Show detailed report if button is clicked
        if st.session_state.show_report:
            show_report = st.button("Click here to see Test Report")
            if show_report:
                # Patient Information
                st.markdown(f"#### Patient Information:")
                st.markdown(f"*Patient Name*: {patient_name}")
                st.markdown(f"*Age*: {age}")
        
                # Test Parameters and Values
                st.markdown(f"#### Test Parameters and Values:")

                # Defining parameter names, ranges, and units
                test_data = {
                    "Parameter Name": [
                        "Age", "Sex", "Chest Pain Type", "Resting Blood Pressure", 
                        "Cholestoral", "Fasting Blood Sugar", "Resting Electrocardiographic", 
                        "Max Heart Rate", "Exercise Angina", "ST Depression", 
                        "Peak ST Slope", "Major Vessels", "Thalassemia"
                    ],
                    "Patient Values": [
                        age, 'Female' if sex == 0 else 'Male', cp, trestbps, chol, 
                        'Yes' if fbs == 1 else 'No', restecg, thalach, 
                        'Yes' if exang == 1 else 'No', oldpeak, slope, ca, thal
                    ],
                    "Normal Range": [
                        "1-120", "0 = Female, 1 = Male", "0: Typical Angina, 1: Atypical Angina, 2: Non-Anginal Pain, 3: Asymptomatic",
                        "50-200", "100-600", "Yes: >120 mg/dl, No: <=120 mg/dl", "0: Normal, 1: ST-T wave abnormality, 2: Left ventricular hypertrophy",
                        "60-220", "0: No, 1: Yes", "0.0-6.0", "0: Upsloping, 1: Flat, 2: Downsloping", "0-3", "0: Normal, 1: Fixed defect, 2: Reversible defect"
                    ],
                    "Unit": [
                        "Years", "Female/Male", "Type", "mm Hg", "mg/dl", "Yes/No", "Type", 
                        "bpm (beats per minute)", "Yes/No", "ST Depression", "Type", "Count", "Type"
                    ]
                }
                # Convert to DataFrame
                df = pd.DataFrame(test_data)
        
                # Style the DataFrame
                styled_df = df.style.set_table_styles([
                    {"selector": "thead", "props": [("background-color", "#4CAF50"), ("color", "white"), ("font-weight", "bold"), ("text-align", "center")]},
                    {"selector": "tbody", "props": [("color", "black"), ("font-weight", "bold"), ("text-align", "center")]},
                    {"selector": "tbody tr:nth-child(even)", "props": [("background-color", "#f9f9f9")]},
                    {"selector": "tbody tr:hover", "props": [("background-color", "#e0f7fa")]}  # Highlight on hover
                ])
        
                # Display the styled DataFrame
                st.dataframe(
                    styled_df,
                    use_container_width=True
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

        # Define the button to trigger prediction
        if st.button("Parkinson's Test Result"):
            # Collect input values
            user_input = [fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5,
                      APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]

            try:
                # Ensure that all user inputs are valid (not empty or None)
                if any(i is None or i == '' for i in user_input):
                    st.error("Please ensure all fields are filled.")
                else:
                    # Make prediction using the model
                    parkinsons_prediction = parkinsons_model.predict([user_input])

                    # Diagnosis result
                    parkinsons_diagnosis = "Positive" if parkinsons_prediction[0] == 1 else "Negative"
                    st.markdown(f"### Test Result: {parkinsons_diagnosis}")

                    # Set the session state to show the report
                    st.session_state.show_report = True

            except Exception as e:
                st.error(f"Error during prediction: {e}")

        # Show detailed report if button is clicked
        if st.session_state.show_report:
            show_report = st.button("Click here to see Test Report")
            if show_report:
                # Patient Information
                st.markdown(f"#### Patient Information:")
                st.markdown(f"*Patient Name*: {patient_name}")
                st.markdown(f"*Age*: {Age}")

                # Test Parameters and Values
                st.markdown(f"#### Test Parameters and Values:")

                # Defining parameter names, ranges, and units
                test_data = {
                    "Parameter Name": [
                        "MDVP:Fo(Hz)", "MDVP:Fhi(Hz)", "MDVP:Flo(Hz)", "MDVP:Jitter(%)", 
                        "MDVP:Jitter(Abs)", "MDVP:RAP", "MDVP:PPQ", "Jitter:DDP", "MDVP:Shimmer", 
                        "MDVP:Shimmer(dB)", "Shimmer:APQ3", "Shimmer:APQ5", "MDVP:APQ", "Shimmer:DDA", 
                        "NHR", "HNR", "RPDE", "DFA", "spread1", "spread2", "D2", "PPE"
                        ],
                    "Patient Values": [fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5,
                      APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE],
                    "Normal Range": [
                        "50-150", "50-160", "50-150", "0-3", "0-2", "0-2", "0-2", "0-2", 
                        "0-1", "0-0.5", "0.1-0.5", "0.1-0.5", "0-1", "0-1", "0.1-0.5", "0.1-0.5", 
                        "0-0.5", "0-0.5", "0-1", "0-2", "0-2", "0-1"
                        ],
                    "Unit": [
                        "Hz", "Hz", "Hz", "%", "Abs", "No unit", "No unit", "No unit", "No unit", 
                        "dB", "No unit", "No unit", "No unit", "No unit", "No unit", "No unit", "No unit", 
                        "No unit", "No unit", "No unit", "No unit", "No unit"
                    ]
                }
                # Convert to DataFrame
                df = pd.DataFrame(test_data)
        
                # Style the DataFrame
                styled_df = df.style.set_table_styles([
                    {"selector": "thead", "props": [("background-color", "#4CAF50"), ("color", "white"), ("font-weight", "bold"), ("text-align", "center")]},
                    {"selector": "tbody", "props": [("color", "black"), ("font-weight", "bold"), ("text-align", "center")]},
                    {"selector": "tbody tr:nth-child(even)", "props": [("background-color", "#f9f9f9")]},
                    {"selector": "tbody tr:hover", "props": [("background-color", "#e0f7fa")]}  # Highlight on hover
                ])
        
                # Display the styled DataFrame
                st.dataframe(
                    styled_df,
                    use_container_width=True
                )

