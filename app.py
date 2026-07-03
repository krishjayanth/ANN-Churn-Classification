import streamlit as st
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
    /* Page title: compact so the prediction figure — not the header — is the
       largest thing on the page. */
    .stApp h1 {
        font-size: 2rem;
        line-height: 1.2;
    }

    /* Predict button: solid color, no effects. Text stays white in every
       state so the theme accent never repaints the label. */
    div.stButton > button {
        background: #1e3a8a;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
    }
    div.stButton > button:hover,
    div.stButton > button:active {
        background: #172f70;
        color: #ffffff;
    }
    div.stButton > button:focus,
    div.stButton > button:focus:not(:active) {
        color: #ffffff;
        box-shadow: none;
    }
    div.stButton > button:focus-visible {
        outline: 2px solid #1e3a8a;
        outline-offset: 2px;
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
    .result.borderline {
        background: #fbeecb;
        color: #854d0e;
    }
    .result h2 {
        margin: 0 0 0.25rem 0;
        font-size: 1.3rem;
        color: inherit;
    }
    .result .prob {
        font-size: 3.25rem;
        font-weight: 700;
        line-height: 1.1;
        margin-top: 0.75rem;
    }
    .result p {
        margin: 0;
        color: inherit;
    }
    /* Caption under the figure sits a step below the guidance sentence. */
    .result .prob-label {
        font-size: 0.875rem;
        font-weight: 600;
        letter-spacing: 0.01em;
        opacity: 0.85;
        margin-top: 0.1rem;
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
    .result.borderline .meter-fill {
        background: #b45309;
        height: 100%;
    }

    /* Resting-state slot: neutral, bordered, echoes the result panel's shape
       so the payoff is signalled before a prediction is run. */
    .placeholder {
        border: 1px solid #e3e5ea;
        border-radius: 8px;
        padding: 1.5rem 1.75rem;
        margin-top: 1rem;
        background: #f4f5f7;
        color: #4a4d5c;
    }
    .placeholder h2 {
        margin: 0 0 0.25rem 0;
        font-size: 1.3rem;
        font-weight: 600;
        color: #31333f;
    }
    .placeholder p {
        margin: 0;
        color: inherit;
    }
    .placeholder .meter {
        margin-top: 1.25rem;
    }

    /* The verdict arriving is a state change; fade it in gently. */
    @keyframes resultIn {
        from { opacity: 0; transform: translateY(6px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .result {
        animation: resultIn 240ms cubic-bezier(0.22, 1, 0.36, 1);
    }
    @media (prefers-reduced-motion: reduce) {
        .result { animation: none; }
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


def show_error(message, exc):
    """Calm, on-register failure panel with collapsible technical detail."""
    st.error(message)
    with st.expander("Technical details"):
        st.code(f"{type(exc).__name__}: {exc}")


def render_verdict(proba):
    """Render the result panel. `proba` is the churn probability 0-1.

    Three zones: a neutral 'borderline' band around the 0.5 decision boundary
    keeps a near-coin-flip from posing as a confident red/green verdict.
    """
    if proba < 0.45:
        tone = "stay"
        heading = "Likely to stay"
        guidance = "This customer appears loyal. Low churn risk."
    elif proba > 0.55:
        tone = "churn"
        heading = "Likely to churn"
        guidance = "This customer shows a high risk of leaving. Consider retention outreach."
    else:
        tone = "borderline"
        heading = "Borderline"
        guidance = "The model is uncertain — this customer sits near the decision boundary. Treat it as a low-confidence result."
    pct = round(proba * 100)
    st.markdown(f"""
    <div class="result {tone}" role="status" aria-live="polite">
        <h2>{heading}</h2>
        <p>{guidance}</p>
        <div class="prob">{pct}%</div>
        <p class="prob-label">churn probability</p>
        <div class="meter" role="progressbar" aria-label="Churn probability"
             aria-valuenow="{pct}" aria-valuemin="0" aria-valuemax="100">
            <div class="meter-fill" style="width: {pct}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_placeholder():
    """Neutral resting-state slot shown before a prediction is run."""
    st.markdown("""
    <div class="placeholder">
        <h2>Your prediction will appear here</h2>
        <p>Fill in the customer's profile above, then select Predict Churn.</p>
        <div class="meter" aria-hidden="true"></div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------- Header ----------------------------
st.title('Customer Churn Prediction')
st.write("Enter a customer's profile and a neural network trained on past bank customers will estimate how likely they are to leave.")
st.divider()

# ---------------------------- Load artifacts ----------------------------
try:
    model, label_encoder_gender, onehot_encoder_geo, scaler = load_artifacts()
except Exception as exc:
    show_error(
        "The prediction model couldn't be loaded. Make sure model.h5, scaler.pkl, "
        "and the encoder files are present in the app's folder.",
        exc,
    )
    st.stop()

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
    balance = st.number_input('Balance ($)', min_value=0.0, max_value=300000.0, value=75000.0, step=1000.0, format="%.2f")
with col6:
    estimated_salary = st.number_input('Estimated Salary ($)', min_value=0.0, max_value=300000.0, value=100000.0, step=1000.0, format="%.2f")

st.subheader('Relationship with the bank')
col7, col8 = st.columns(2)
with col7:
    tenure = st.slider('Tenure (years)', 0, 10, 5)
    has_cr_card = st.toggle('Has Credit Card', value=True)
with col8:
    num_of_products = st.slider('Number of Products', 1, 4, 1,
                                help="How many bank products the customer holds — accounts, cards, loans, and the like.")
    is_active_member = st.toggle('Active Member', value=True,
                                 help="Whether the customer has been regularly using their account.")

st.write("")
predict_clicked = st.button('Predict Churn')

# ---------------------------- Prediction ----------------------------
if predict_clicked:
    try:
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
    except Exception as exc:
        show_error("Something went wrong while scoring this customer. Please try again.", exc)
        st.stop()

    render_verdict(prediction_proba)
else:
    render_placeholder()
