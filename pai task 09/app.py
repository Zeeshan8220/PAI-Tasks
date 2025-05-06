from flask import Flask, render_template, request
from nltk.tokenize import word_tokenize

app = Flask(__name__)

# Rule-based medical knowledge base
disease_db = {
    "diabetes": ["thirst", "frequent urination", "blurred vision", "weight loss", "fatigue", "high blood sugar"],
    "flu": ["fever", "chills", "muscle aches", "cough", "congestion", "fatigue"],
    "hypertension": ["headache", "chest pain", "vision problems", "irregular heartbeat", "high blood pressure"],
    "asthma": ["shortness of breath", "wheezing", "chest tightness", "coughing"],
    "migraine": ["headache", "nausea", "sensitivity to light", "throbbing pain"]
}

# Diagnosis logic
def diagnose(symptoms_text):
    tokens = word_tokenize(symptoms_text.lower())
    diagnosis = []

    for disease, symptoms in disease_db.items():
        matches = sum(symptom in symptoms_text.lower() for symptom in symptoms)
        if matches > 0:
            diagnosis.append(f"{disease.title()} (matched {matches} symptoms)")

    return diagnosis if diagnosis else ["No clear diagnosis. Please consult a doctor."]

@app.route('/', methods=['GET', 'POST'])
def index():
    result = []
    user_input = ""
    if request.method == 'POST':
        user_input = request.form['symptoms']
        result = diagnose(user_input)
    return render_template('index.html', result=result, user_input=user_input)

if __name__ == '__main__':
    app.run(debug=True)
