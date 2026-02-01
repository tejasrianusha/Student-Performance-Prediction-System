import pickle, pandas as pd, io, random
from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

app = Flask(__name__)

with open('student_model.pkl', 'rb') as f:
    ml_model = pickle.load(f)

def generate_students():
    first = ["Aarav", "Vihaan", "Aditya", "Sai", "Arjun", "Ananya", "Diya", "Pari", "Rahul", "Sneha"]
    last = ["Sharma", "Reddy", "Verma", "Singh", "Iyer", "Nair", "Gupta", "Das", "Malhotra", "Yadav"]
    students = []
    for i in range(1, 101):
        roll = str(123450 + i)
        random.seed(roll)
        students.append({
            "roll": roll, "name": f"{random.choice(first)} {random.choice(last)}",
            "attendance": random.randint(45, 98), 
            "m10": random.randint(65, 95), "g10": "A", "p10": 2020,
            "mInter": random.randint(60, 95), "inter_group": random.choice(["MPC", "BiPC", "CEC"]), 
            "inter_passout": 2022, "inter_grade": "B+",
            "deg_marks": random.randint(55, 92), "deg_grade": random.choice(["O", "A+", "A"]), 
            "status": random.choice(["Continuing", "Discontinued"]),
            "last_date": "2026-05-25",
            "exam_date": "2026-03-15"
        })
    return students

student_db = generate_students()

@app.route('/')
def index():
    rolls = [s['roll'] for s in student_db]
    return render_template('index.html', rolls=rolls)

@app.route('/dashboard', methods=['POST'])
def dashboard():
    roll = request.form.get('roll')
    s = next((item for item in student_db if item['roll'] == roll), None)
    if not s: return "Roll not found!"
    pred_id = ml_model.predict([[s['attendance'], s['m10'], s['mInter']]])[0]
    res = {0: "High Risk", 1: "Good", 2: "Excellent"}
    top_5 = sorted(student_db, key=lambda x: x['deg_marks'], reverse=True)[:5]
    return render_template('dashboard.html', s=s, prediction=res[pred_id], top_5=top_5)

# FIXED PDF DOWNLOAD FUNCTION
@app.route('/download_pdf/<roll>')
def download_pdf(roll):
    s = next((item for item in student_db if item['roll'] == roll), None)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, f"STUDENT PERFORMANCE REPORT: {s['name']}")
    p.setFont("Helvetica", 12)
    p.drawString(100, 720, f"Roll Number: {s['roll']}")
    p.drawString(100, 700, f"Attendance: {s['attendance']}%")
    p.drawString(100, 680, f"10th Marks: {s['m10']}% | Inter Marks: {s['mInter']}%")
    p.drawString(100, 660, f"BCA Status: {s['status']}")
    p.showPage()
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"Report_{roll}.pdf", mimetype='application/pdf')

@app.route('/export_excel')
def export_excel():
    df = pd.DataFrame(student_db)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return send_file(output, download_name="Student_Performance_Data.xlsx", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)