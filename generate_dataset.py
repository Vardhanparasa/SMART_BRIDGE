import pandas as pd
import random
import os

# Create data folder if it doesn't exist
os.makedirs("data", exist_ok=True)

education_levels = ["UG", "Graduate", "Diploma"]
course_categories = ["Technical", "Non Technical"]
payment_statuses = ["Paid", "Partial", "Pending"]

data = []

for i in range(1, 1001):

    education = random.choice(education_levels)
    category = random.choice(course_categories)

    course_fee = random.randint(20000, 100000)
    discount = random.randint(0, 50)
    marks = random.randint(40, 100)
    attendance = random.randint(50, 100)
    payment = random.choice(payment_statuses)

    # AI Priority Score Logic
    priority = 50

    if marks >= 85:
        priority += 20
    elif marks >= 70:
        priority += 10

    if attendance >= 90:
        priority += 15
    elif attendance >= 75:
        priority += 8

    if payment == "Paid":
        priority += 10
    elif payment == "Partial":
        priority += 5

    if discount > 30:
        priority -= 10

    priority = max(0, min(priority, 100))

    # Risk Level
    if priority >= 80:
        risk = "Low"
        recommendation = "Approve"

    elif priority >= 60:
        risk = "Medium"
        recommendation = "Review"

    else:
        risk = "High"
        recommendation = "Reject"

    data.append({
        "education_level": education,
        "course_category": category,
        "course_fee": course_fee,
        "discount_percentage": discount,
        "payment_status": payment,
        "marks": marks,
        "attendance_score": attendance,
        "ai_priority_score": priority,
        "risk_level": risk,
        "recommendation": recommendation
    })

df = pd.DataFrame(data)

df.to_csv("data/student_dataset.csv", index=False)

print("=" * 60)
print("Student Dataset Generated Successfully!")
print("Location : data/student_dataset.csv")
print("Total Records :", len(df))
print("=" * 60)