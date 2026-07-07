from flask import Flask, render_template, request
import joblib
import os

app = Flask(__name__)

# Load trained model
MODEL_PATH = "models/admission_model.pkl"

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    print("✅ AI Model Loaded Successfully")
else:
    model = None
    print("❌ Model not found!")

# --------------------------
# Home Page
# --------------------------
@app.route("/")
def home():
    return render_template("index.html")


# --------------------------
# Predict Route
# --------------------------
@app.route("/predict", methods=["POST"])
def predict():

    if model is None:
        return "Model not found! Please train the model first."

    # --------------------------
    # Get Form Data
    # --------------------------

    student_name = request.form["student_name"]

    education_level = request.form["education_level"]
    course_category = request.form["course_category"]

    course_fee = float(request.form["course_fee"])
    discount_percentage = float(request.form["discount_percentage"])

    payment_status = request.form["payment_status"]

    marks = float(request.form["marks"])
    attendance_score = float(request.form["attendance_score"])

    # --------------------------
    # Convert Categorical Values
    # --------------------------

    education_map = {
        "Diploma": 0,
        "UG": 1,
        "Graduate": 2
    }

    category_map = {
        "Technical": 1,
        "Non Technical": 0
    }

    payment_map = {
        "Pending": 0,
        "Partial": 1,
        "Paid": 2
    }

    input_data = [[
        education_map[education_level],
        category_map[course_category],
        course_fee,
        discount_percentage,
        payment_map[payment_status],
        marks,
        attendance_score
    ]]

    # --------------------------
    # AI Prediction
    # --------------------------

    priority_score = round(model.predict(input_data)[0], 2)

    # --------------------------
    # Risk Analysis
    # --------------------------

    if priority_score >= 80:
        risk_level = "Low Risk"
        recommendation = "Approve Admission"

    elif priority_score >= 60:
        risk_level = "Medium Risk"
        recommendation = "Needs Manual Review"

    else:
        risk_level = "High Risk"
        recommendation = "Reject Admission"

    # --------------------------
    # AI Summary
    # --------------------------

    summary = f"""
    {student_name} applied for a {course_category} course.
    The student scored {marks}% with an attendance of {attendance_score}%.
    The requested discount is {discount_percentage}%.
    The AI generated a Priority Score of {priority_score}.
    Overall Risk Level: {risk_level}.
    Recommendation: {recommendation}.
    """

    return render_template(
        "result.html",
        student_name=student_name,
        priority_score=priority_score,
        risk_level=risk_level,
        recommendation=recommendation,
        summary=summary
    )


# --------------------------
# Run Application
# --------------------------

if __name__ == "__main__":
    app.run(debug=True)