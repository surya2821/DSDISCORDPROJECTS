import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from flask import Flask
from dash import Dash, html, dcc, Input, Output

# Sample disaster dataset
data = {
    "Disaster_Type": ["Flood", "Earthquake", "Cyclone", "Flood", "Earthquake"],
    "Location": ["Urban", "Rural", "Coastal", "Coastal", "Urban"],
    "Severity": [3, 5, 4, 2, 4],  # Scale of 1-5
    "Response_Action": ["Evacuate", "Search and Rescue", "Shelter", "Evacuate", "Search and Rescue"]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# One-hot encode categorical variables
df_encoded = pd.get_dummies(df, columns=["Disaster_Type", "Location"])

# Features and target
X = df_encoded.drop("Response_Action", axis=1)
y = df["Response_Action"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print("Model Accuracy:", accuracy_score(y_test, y_pred))

# Prediction function
def predict_response(disaster_type, location, severity):
    # Create a single sample
    sample = pd.DataFrame([{
        "Severity": severity,
        f"Disaster_Type_{disaster_type}": 1,
        f"Location_{location}": 1
    }], columns=X.columns).fillna(0)  # Ensure all columns match
    
    # Make prediction
    return model.predict(sample)[0]

# Create Flask server
server = Flask(__name__)

# Create Dash app
app = Dash(__name__, server=server)

# Layout for the dashboard
app.layout = html.Div([
    html.H1("Disaster Response Predictor"),
    html.Label("Disaster Type"),
    dcc.Dropdown(
        id='disaster-type',
        options=[{'label': dt, 'value': dt} for dt in df["Disaster_Type"].unique()],
        value="Flood"
    ),
    html.Label("Location"),
    dcc.Dropdown(
        id='location',
        options=[{'label': loc, 'value': loc} for loc in df["Location"].unique()],
        value="Urban"
    ),
    html.Label("Severity (1-5)"),
    dcc.Slider(id='severity', min=1, max=5, step=1, value=3),
    html.Button("Predict", id='predict-button'),
    html.Div(id='prediction-output', style={'margin-top': '20px'})
])

# Callback to update prediction
@app.callback(
    Output('prediction-output', 'children'),
    [Input('disaster-type', 'value'),
     Input('location', 'value'),
     Input('severity', 'value')]
)
def update_prediction(disaster_type, location, severity):
    response = predict_response(disaster_type, location, severity)
    return f"Recommended Response: {response}"

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
