# ANN Classification - Customer Churn Prediction

This project uses an artificial neural network to predict whether a bank customer is likely to churn. It includes a trained Keras model, preprocessing artifacts, exploratory/training notebooks, and a Streamlit app for interactive predictions.

## Project Structure

```text
.
├── app.py                    # Streamlit prediction app
├── Churn_Modelling.csv       # Customer churn dataset
├── experiments.ipynb         # Model training and experimentation notebook
├── prediction.ipynb          # Prediction workflow notebook
├── model.keras               # Trained Keras model
├── label_encoder_gender.pkl  # Saved gender label encoder
├── onehot_encoder_geo.pkl    # Saved geography one-hot encoder
├── scaler.pkl                # Saved feature scaler
└── logs/                     # TensorBoard training logs
```

## Features

- Predicts customer churn probability from customer profile data.
- Uses saved preprocessing objects so app inputs match the training pipeline.
- Provides an interactive Streamlit UI for entering customer details.
- Supports geography and gender categorical inputs through trained encoders.

## Dataset

The project uses `Churn_Modelling.csv`, which contains bank customer records with fields such as:

- `CreditScore`
- `Geography`
- `Gender`
- `Age`
- `Tenure`
- `Balance`
- `NumOfProducts`
- `HasCrCard`
- `IsActiveMember`
- `EstimatedSalary`
- `Exited`

`Exited` is the target column used for churn classification.

## How Prediction Works

`app.py` loads:

- `model.keras`
- `label_encoder_gender.pkl`
- `onehot_encoder_geo.pkl`
- `scaler.pkl`

The app collects customer inputs, transforms categorical features, scales the final feature set, and passes the processed data into the trained neural network. The output is a churn probability. A probability greater than `0.5` is classified as likely to churn.

## Model Artifacts

The prediction app depends on the saved model and preprocessing files being present in the project root:

```text
model.keras
label_encoder_gender.pkl
onehot_encoder_geo.pkl
scaler.pkl
```

The Streamlit app asks for:

- Geography
- Gender
- Age
- Balance
- Credit score
- Estimated salary
- Tenure
- Number of products
- Credit card ownership
- Active membership status

After submission, the app displays the churn probability and a likely/not likely churn message.
