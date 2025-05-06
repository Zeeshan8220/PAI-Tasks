import cv2
import dlib
import numpy as np
from imutils import face_utils
from flask import Flask, render_template, request

app = Flask(__name__)

# Load face detection and facial landmark model
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
landmark_model = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# Predict personality based on facial feature ratios
def classify_personality(metrics):
    jaw = metrics['Jaw']
    eye = metrics['Eye']
    nose = metrics['Nose']
    
    if jaw > 120 and eye > 40:
        return "ENTJ - The Commander"
    elif nose > 35 and eye < 40:
        return "INFJ - The Advocate"
    elif jaw < 110 and eye > 45:
        return "ENFP - The Campaigner"
    elif jaw > 130:
        return "ISTJ - The Inspector"
    else:
        return "ISFP - The Artist"

# Extract face measurements
def analyze_features(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detected = face_cascade.detectMultiScale(gray_img, 1.3, 5)

    for (x, y, w, h) in detected:
        face_rect = dlib.rectangle(x, y, x + w, y + h)
        shape = landmark_model(gray_img, face_rect)
        points = face_utils.shape_to_np(shape)

        for (px, py) in points:
            cv2.circle(img, (px, py), 2, (0, 255, 0), -1)

        jaw = np.linalg.norm(points[0] - points[16])
        eye = np.linalg.norm(points[36] - points[39])
        nose = np.linalg.norm(points[27] - points[30])

        result = {
            'Eye': round(eye, 2),
            'Nose': round(nose, 2),
            'Jaw': round(jaw, 2),
        }

        result['Personality'] = classify_personality(result)
        return img, result

    return img, None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded = request.files['image']
        if uploaded:
            save_path = 'static/upload.jpg'
            uploaded.save(save_path)
            img = cv2.imread(save_path)
            out_img, data = analyze_features(img)
            if data:
                return render_template('index.html', measurements=data)
    return render_template('index.html', measurements=None)

if __name__ == '__main__':
    app.run(debug=True)

