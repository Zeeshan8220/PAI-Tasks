from flask import Flask, request, jsonify, render_template
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')  # Make sure NLTK tokenizer is ready

app = Flask(__name__)

# Basic symptom-disease knowledge base
disease_db = {
    "Diabetes": ["fatigue", "high blood sugar", "weight loss", "thirst", "insulin resistance"],
    "Hypertension": ["high blood pressure", "headache", "chest pain", "dizziness", "cardiovascular disease"],
    "Flu": ["fever", "cough", "sore throat", "body ache", "chills"]
}

# NLP-based symptom analysis
def diagnose(symptom_input):
    tokens = word_tokenize(symptom_input.lower())
    possible_matches = []

    for disease, symptoms in disease_db.items():
        matched = sum(symptom in symptom_input.lower() for symptom in symptoms)
        if matched:
            possible_matches.append(f"{disease} (matched {matched} symptom{'s' if matched > 1 else ''})")

    return possible_matches if possible_matches else ["No clear diagnosis. Please consult a physician."]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/diagnose', methods=['POST'])
def diagnose_route():
    data = request.json
    symptoms = data.get("symptoms", "")
    result = diagnose(symptoms)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
