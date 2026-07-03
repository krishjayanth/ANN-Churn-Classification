import streamlit as st
import numpy as np
import tensorflow as tf
import pandas as pd
import pickle

# ---------------------------- Page config ----------------------------
st.set_page_config(
    page_title="Customer Churn Prediction",
    layout="centered",
)

# ---------------------------- Styling ----------------------------
st.markdown("""
<style>
    /* Header banner */
    .hero {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 60%, #60a5fa 100%);
        border-radius: 16px;
        padding: 2.2rem 2rem;
        margin-bottom: 1.5rem;
        color: white;
    }
    .hero h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
        color: white;
    }
    .hero p {
        margin: 0.4rem 0 0 0;
        opacity: 0.85;
        font-size: 1rem;
    }

    /* Section labels */
    .section-label {
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #3b82f6;
        margin: 0.5rem 0 0.25rem 0;
    }

    /* Result cards */
    .result-card {
        border-radius: 16px;
        padding: 1.8rem 2rem;
        margin-top: 1rem;
        color: white;
    }
    .result-card.churn {
        background: linear-gradient(135deg, #7f1d1d 0%, #dc2626 100%);
    }
    .result-card.stay {
        background: linear-gradient(135deg, #14532d 0%, #16a34a 100%);
    }
    .result-card h2 {
        margin: 0 0 0.3rem 0;
        font-size: 1.4rem;
        color: white;
    }
    .result-card p {
        margin: 0;
        opacity: 0.9;
    }
    .prob-number {
        font-size: 3rem;
        font-weight: 800;
        line-height: 1;
    }

    /* Probability meter */
    .meter {
        background: rgba(255,255,255,0.25);
        border-radius: 99px;
        height: 12px;
        margin-top: 1rem;
        overflow: hidden;
    }
    .meter-fill {
        background: white;
        height: 100%;
        border-radius: 99px;
    }

    /* Predict button */
    div.stButton > button {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.7rem 1rem;
        font-weight: 700;
        font-size: 1.05rem;
        width: 100%;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(59, 130, 246, 0.4);
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------- Load artifacts ----------------------------
@st.cache_resource
def load_artifacts():
    model = tf.keras.models.load_model("model.h5")
    with open('label_encoder_gender.pkl', 'rb') as file:
        label_encoder_gender = pickle.load(file)
    with open('onehot_encoder_geo.pkl', 'rb') as file:
        onehot_encoder_geo = pickle.load(file)
    with open('scaler.pkl', 'rb') as file:
        scaler = pickle.load(file)
    return model, label_encoder_gender, onehot_encoder_geo, scaler


model, label_encoder_gender, onehot_encoder_geo, scaler = load_artifacts()

# ---------------------------- Header ----------------------------
st.markdown("""
<div class="hero">
    <h1>Customer Churn Prediction</h1>
    <p>Enter a customer's profile below and the neural network will estimate how likely they are to leave the bank.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------- Inputs ----------------------------
st.markdown('<div class="section-label">Customer Profile</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    geography = st.selectbox('Geography', onehot_encoder_geo.categories_[0])
with col2:
    gender = st.selectbox('Gender', label_encoder_gender.classes_)
with col3:
    age = st.slider('Age', 18, 92, 38)

st.markdown('<div class="section-label">Financials</div>', unsafe_allow_html=True)
col4, col5, col6 = st.columns(3)
with col4:
    credit_score = st.number_input('Credit Score', min_value=300, max_value=900, value=650, step=1)
with col5:
    balance = st.number_input('Balance ($)', min_value=0.0, value=75000.0, step=1000.0, format="%.2f")
with col6:
    estimated_salary = st.number_input('Estimated Salary ($)', min_value=0.0, value=100000.0, step=1000.0, format="%.2f")

st.markdown('<div class="section-label">Relationship with the Bank</div>', unsafe_allow_html=True)
col7, col8 = st.columns(2)
with col7:
    tenure = st.slider('Tenure (years)', 0, 10, 5)
    has_cr_card = st.toggle('Has Credit Card', value=True)
with col8:
    num_of_products = st.slider('Number of Products', 1, 4, 1)
    is_active_member = st.toggle('Active Member', value=True)

st.write("")
predict_clicked = st.button('Predict Churn')

# ---------------------------- Prediction ----------------------------
if predict_clicked:
    input_data = pd.DataFrame({
        'CreditScore': [credit_score],
        'Gender': [label_encoder_gender.transform([gender])[0]],
        'Age': [age],
        'Tenure': [tenure],
        'Balance': [balance],
        'NumOfProducts': [num_of_products],
        'HasCrCard': [int(has_cr_card)],
        'IsActiveMember': [int(is_active_member)],
        'EstimatedSalary': [estimated_salary]
    })

    # One-hot encode 'Geography'
    geo_encoded = onehot_encoder_geo.transform([[geography]]).toarray()
    geo_encoded_df = pd.DataFrame(geo_encoded, columns=onehot_encoder_geo.get_feature_names_out(['Geography']))

    # Combine one-hot encoded columns with input data
    input_data = pd.concat([input_data.reset_index(drop=True), geo_encoded_df], axis=1)

    # Scale the input data
    input_data_scaled = scaler.transform(input_data)

    with st.spinner('Running the model...'):
        prediction = model.predict(input_data_scaled)
    prediction_proba = float(prediction[0][0])

    if prediction_proba > 0.5:
        st.markdown(f"""
        <div class="result-card churn">
            <h2>Likely to Churn</h2>
            <p>This customer shows a high risk of leaving. Consider retention outreach.</p>
            <div class="prob-number">{prediction_proba:.0%}</div>
            <p>churn probability</p>
            <div class="meter"><div class="meter-fill" style="width: {prediction_proba:.0%};"></div></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-card stay">
            <h2>Likely to Stay</h2>
            <p>This customer appears loyal. Low churn risk detected.</p>
            <div class="prob-number">{prediction_proba:.0%}</div>
            <p>churn probability</p>
            <div class="meter"><div class="meter-fill" style="width: {prediction_proba:.0%};"></div></div>
        </div>
        """, unsafe_allow_html=True)
