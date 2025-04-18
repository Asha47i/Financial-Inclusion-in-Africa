import streamlit as st
import numpy as np
import pickle
import os

# Load model
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("Model file not found! Please ensure model.pkl is in the same directory as app.py.")
except Exception as e:
    st.error(f"An error occurred while loading the model: {e}")

st.title("Financial Inclusion Prediction App")

# Feature inputs
country = st.selectbox("Country", ['Kenya', 'Rwanda', 'Tanzania', 'Uganda'])
country_map = {'Kenya': 0, 'Rwanda': 1, 'Tanzania': 2, 'Uganda': 3}
country_encoded = country_map[country]

location_type = st.selectbox("Location Type", ['Rural', 'Urban'])
location_map = {'Rural': 0, 'Urban': 1}
location_encoded = location_map[location_type]

cellphone_access = st.selectbox("Cellphone Access", ['No', 'Yes'])
cellphone_map = {'No': 0, 'Yes': 1}
cellphone_encoded = cellphone_map[cellphone_access]

household_size = st.number_input("Household Size", min_value=1)

age = st.number_input("Age of Respondent", min_value=10)

gender = st.selectbox("Gender", ['Female', 'Male'])
gender_map = {'Female': 0, 'Male': 1}
gender_encoded = gender_map[gender]

relationship = st.selectbox("Relationship With Head", ['Child', 'Head of Household', 'Other non-relatives', 'Other relative', 'Parent', 'Spouse'])
relationship_map = {'Child': 0, 'Head of Household': 1, 'Other non-relatives': 2, 'Other relative': 3, 'Parent': 4, 'Spouse': 5}
relationship_encoded = relationship_map[relationship]

marital_status = st.selectbox("Marital Status", ['Divorced/Seperated', 'Dont know', 'Married/Living together', 'Single/Never Married', 'Widowed'])
marital_status_map = {'Divorced/Seperated': 0, 'Dont know': 1, 'Married/Living together': 2, 'Single/Never Married': 3, 'Widowed': 4}
marital_status_encoded = marital_status_map[marital_status]

education_level = st.selectbox("Education Level", ['No formal education', 'Other/Dont know/RTA', 'Primary education', 'Secondary education', 'Tertiary education', 'Vocational/Specialised training'])
education_map = {'No formal education': 0, 'Other/Dont know/RTA': 1, 'Primary education': 2, 'Secondary education': 3, 'Tertiary education': 4, 'Vocational/Specialised training': 5}
education_encoded = education_map[education_level]

job_type = st.selectbox("Job Type", ['Dont Know/Refuse to answer', 'Farming and Fishing', 'Formally employed Government', 'Formally employed Private', 'Government Dependent', 'Informally employed', 'No Income', 'Other Income', 'Remittance Dependent', 'Self employed'])
job_map = {'Dont Know/Refuse to answer': 0, 'Farming and Fishing': 1, 'Formally employed Government': 2, 'Formally employed Private': 3, 'Government Dependent': 4, 'Informally employed': 5, 'No Income': 6, 'Other Income': 7, 'Remittance Dependent': 9, 'Self employed': 10}
job_encoded = job_map[job_type]

# 💰 New: Income Input
income = st.number_input("Monthly Income (USD)", min_value=0)

# Predict
if st.button("Predict"):
    input_data = np.array([[country_encoded, location_encoded, cellphone_encoded, household_size, age,
                            gender_encoded, relationship_encoded, marital_status_encoded, education_encoded,
                            job_encoded, income]])  # 11 features now

    if input_data.shape[1] != 11:
        st.error("Input features mismatch. Please check inputs.")
    else:
        prediction = model.predict(input_data)
        st.success(f"Prediction: {'Has Bank Account' if prediction[0] == 1 else 'No Bank Account'}")
