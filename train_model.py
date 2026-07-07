import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv("data/student_dataset.csv")

# Convert categorical values to numbers
df["education_level"] = df["education_level"].map({
    "Diploma": 0,
    "UG": 1,
    "Graduate": 2
})

df["course_category"] = df["course_category"].map({
    "Technical": 1,
    "Non Technical": 0
})

df["payment_status"] = df["payment_status"].map({
    "Pending": 0,
    "Partial": 1,
    "Paid": 2
})

# Features
X = df[
    [
        "education_level",
        "course_category",
        "course_fee",
        "discount_percentage",
        "payment_status",
        "marks",
        "attendance_score"
    ]
]

# Target
y = df["ai_priority_score"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Create models folder
os.makedirs("models", exist_ok=True)

# Save model
joblib.dump(model, "models/admission_model.pkl")

print("========================================")
print("Model Trained Successfully!")
print("Model saved to models/admission_model.pkl")
print("========================================")