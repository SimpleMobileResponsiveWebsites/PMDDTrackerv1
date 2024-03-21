import streamlit as st
import csv
from datetime import datetime
import pandas as pd
from io import StringIO, BytesIO
import matplotlib.pyplot as plt

# Initialize session state variables if they don't already exist
if 'symptom_ratings' not in st.session_state:
    st.session_state.symptom_ratings = {}
if 'graph_buffer' not in st.session_state:
    st.session_state.graph_buffer = None

# App title
st.title('Symptom Severity Tracker')

# Instructions
st.write('Please rate the severity of your symptoms on a scale from 0 to 10.')


# Function to create sliders for symptoms
def create_symptom_slider(symptom):
    return st.slider(symptom, 0, 10, 0)


# Symptom categories and their corresponding symptoms
symptom_categories = {
    'Psychological Symptoms': [
        'Irritability', 'Nervousness', 'Lack of control', 'Agitation', 'Anger', 'Insomnia',
        'Difficulty in concentrating', 'Depression', 'Severe fatigue', 'Anxiety', 'Confusion',
        'Forgetfulness', 'Poor self-image', 'Paranoia', 'Emotional sensitivity', 'Crying spells',
        'Moodiness', 'Trouble sleeping'
    ],
    'Respiratory Problems': [
        'Fluid retention', 'Swelling of the ankles, hands, and feet', 'Periodic weight gain',
        'Diminished urine output', 'Breast fullness and pain', 'Respiratory problems', 'Allergies',
        'Infections', 'Eye complaints', 'Vision changes', 'Eye infection'
    ],
    'Gastrointestinal Symptoms': [
        'Abdominal cramps', 'Bloating', 'Constipation', 'Nausea', 'Vomiting',
        'Pelvic heaviness or pressure', 'Backache'
    ],
    'Skin Problems': [
        'Acne', 'Skin inflammation with itching', 'Aggravation of other skin disorders including cold sores'
    ],
    'Neurologic and Vascular Symptoms': [
        'Headache', 'Dizziness', 'Fainting',
        'Numbness, prickling, tingling, or heightened sensitivity of arms and/or legs',
        'Easy bruising', 'Heart palpitations', 'Muscle spasms'
    ],
    'Other': [
        'Decreased coordination', 'Painful menstruation', 'Diminished sex drive', 'Appetite changes',
        'Food cravings', 'Hot flashes'
    ]
}


# Function to generate CSV content from symptom ratings
def generate_csv_content(symptom_ratings):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Symptom', 'Rating'])
    for symptom, rating in symptom_ratings.items():
        writer.writerow([symptom, rating])
    output.seek(0)  # Rewind the buffer
    return output.getvalue()


# Generate the graph and save it to a BytesIO buffer
def generate_graph(symptom_ratings):
    fig, ax = plt.subplots(figsize=(10, 15))
    symptoms = list(symptom_ratings.keys())
    ratings = list(symptom_ratings.values())
    ax.barh(symptoms, ratings)
    plt.tight_layout()
    ax.set_xlabel('Ratings')
    ax.set_title('Symptom Severity Ratings')

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)  # Close the figure to prevent it from being displayed
    return buf


# Create sliders for each symptom category and store the ratings in session state
for category, symptoms in symptom_categories.items():
    st.subheader(category)
    for symptom in symptoms:
        rating = create_symptom_slider(symptom)
        st.session_state.symptom_ratings[symptom] = rating

# Submit button
if st.button('Submit Ratings'):
    st.session_state.graph_buffer = generate_graph(st.session_state.symptom_ratings)
    csv_content = generate_csv_content(st.session_state.symptom_ratings)
    st.download_button(label="Download Symptom Ratings as CSV", data=csv_content, file_name="symptom_ratings.csv",
                       mime='text/csv')
    st.success('Your symptom ratings have been submitted successfully!')

# Provide a download button for the graph if the buffer is not None
if st.session_state.graph_buffer is not None:
    st.download_button(
        label="Download Symptom Severity Ratings Graph as PNG",
        data=st.session_state.graph_buffer,
        file_name="symptom_severity_ratings.png",
        mime="image/png"
    )
