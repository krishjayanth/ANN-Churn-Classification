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
    /* Predict button: solid color, no effects */
    div.stButton > button {
        background: #1e3a8a;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
    }
    div.stButton > button:hover {
        background: #172f70;
        color: white;
    }

    /* Result panel */
    .result {
        border-radius: 8px;
        padding: 1.5rem 1.75rem;
        margin-top: 1rem;
    }
    .result.churn {
        background: #fdeaea;
        color: #7f1d1d;
    }
    .result.stay {
        background: #e5f4ea;
        color: #14532d;
    }
    .result h2 {
        margin: 0 0 0.25rem 0;
        font-size: 1.3rem;
        color: inherit;
    }
    .result .prob {
        font-size: 2.5rem;
        font-weight: 700;
        line-height: 1.2;
        margin-top: 0.75rem;
    }
    .result p {
        margin: 0;
        color: inherit;
    }

    /* Probability meter */
    .meter {
        background: rgba(0, 0, 0, 0.1);
        border-radius: 4px;
        height: 10px;
        margin-top: 1rem;
        overflow: hidden;
    }
    .result.churn .meter-fill {
        background: #b91c1c;
        height: 100%;
    }
    .result.stay .meter-fill {
        background: #15803d;
        height: 100%;
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
st.title('Customer Churn Prediction')
st.write("Enter a customer's profile and the model will estimate how likely they are to leave the bank.")
st.divider()

# ---------------------------- Inputs ----------------------------
st.subheader('Customer profile')
col1, col2, col3 = st.columns(3)
with col1:
    geography = st.selectbox('Geography', onehot_encoder_geo.categories_[0])
with col2:
    gender = st.selectbox('Gender', label_encoder_gender.classes_)
with col3:
    age = st.slider('Age', 18, 92, 38)

st.subheader('Financials')
col4, col5, col6 = st.columns(3)
with col4:
    credit_score = st.number_input('Credit Score', min_value=300, max_value=900, value=650, step=1)
with col5:
    balance = st.number_input('Balance ($)', min_value=0.0, value=75000.0, step=1000.0, format="%.2f")
with col6:
    estimated_salary = st.number_input('Estimated Salary ($)', min_value=0.0, value=100000.0, step=1000.0, format="%.2f")

st.subheader('Relationship with the bank')
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
        <div class="result churn">
            <h2>Likely to churn</h2>
            <p>This customer shows a high risk of leaving. Consider retention outreach.</p>
            <div class="prob">{prediction_proba:.0%}</div>
            <p>churn probability</p>
            <div class="meter"><div class="meter-fill" style="width: {prediction_proba:.0%};"></div></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result stay">
            <h2>Likely to stay</h2>
            <p>This customer appears loyal. Low churn risk.</p>
            <div class="prob">{prediction_proba:.0%}</div>
            <p>churn probability</p>
            <div class="meter"><div class="meter-fill" style="width: {prediction_proba:.0%};"></div></div>
        </div>
        """, unsafe_allow_html=True)
