import cv2
import dlib
import numpy as np
from flask import Flask, request, jsonify
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Load face detector and landmark predictor
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
predictor_path = "shape_predictor_68_face_landmarks.dat"

try:
    predictor = dlib.shape_predictor(predictor_path)
    logging.info("Dlib predictor loaded successfully.")
except Exception as e:
    logging.error(f"Error loading predictor: {e}")
    predictor = None

def detect_face(image):
    """Detects faces in the image and returns the first bounding box."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    if len(faces) == 0:
        return None
    
    x, y, w, h = faces[0]
    return dlib.rectangle(x, y, x + w, y + h)

def get_landmarks(image, face_rect):
    """Extracts facial landmarks."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    landmarks = predictor(gray, face_rect)
    return np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(68)])

def calculate_features(landmarks):
    """Calculates facial feature ratios."""
    if landmarks is None:
        return None

    features = {
        'width_height_ratio': np.linalg.norm(landmarks[16] - landmarks[0]) / np.linalg.norm(landmarks[8] - landmarks[27]),
        'eye_distance_ratio': np.linalg.norm(landmarks[39] - landmarks[42]) / np.linalg.norm(landmarks[16] - landmarks[0]),
        'mouth_width_ratio': np.linalg.norm(landmarks[54] - landmarks[48]) / np.linalg.norm(landmarks[16] - landmarks[0]),
        'nose_length_ratio': np.linalg.norm(landmarks[33] - landmarks[27]) / np.linalg.norm(landmarks[8] - landmarks[27]),
        'jaw_width_ratio': np.linalg.norm(landmarks[11] - landmarks[5]) / np.linalg.norm(landmarks[16] - landmarks[0]),
        'chin_prominence': np.linalg.norm(landmarks[8] - landmarks[57]) / np.linalg.norm(landmarks[8] - landmarks[27])
    }
    return features

def predict_personality(features):
    """Maps facial features to personality traits."""
    if not features:
        return {'error': 'No facial features detected'}
    
    personality = {
        'Openness': 0.5,
        'Conscientiousness': 0.5,
        'Extraversion': 0.5,
        'Agreeableness': 0.5,
        'Neuroticism': 0.5
    }
    
    if features['width_height_ratio'] > 1.6:
        personality['Extraversion'] += 0.2
    elif features['width_height_ratio'] < 1.3:
        personality['Neuroticism'] += 0.2

    if features['eye_distance_ratio'] > 0.25:
        personality['Openness'] += 0.2
    elif features['eye_distance_ratio'] < 0.2:
        personality['Conscientiousness'] += 0.2

    if features['mouth_width_ratio'] > 0.5:
        personality['Extraversion'] += 0.2
    elif features['mouth_width_ratio'] < 0.4:
        personality['Neuroticism'] += 0.2

    if features['jaw_width_ratio'] > 0.75:
        personality['Agreeableness'] += 0.2
    elif features['jaw_width_ratio'] < 0.6:
        personality['Conscientiousness'] += 0.2

    if features['chin_prominence'] > 0.2:
        personality['Conscientiousness'] += 0.2
    elif features['chin_prominence'] < 0.1:
        personality['Neuroticism'] += 0.2
    
    return personality

@app.route('/', methods=['POST'])
def analyze_face():
    """Handles image upload and returns facial profiling results."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    
    file = request.files['file']
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        return jsonify({'error': 'Invalid image format'})

    face_rect = detect_face(image)
    if face_rect is None:
        return jsonify({'error': 'No face detected'})
    
    landmarks = get_landmarks(image, face_rect)
    features = calculate_features(landmarks)
    personality = predict_personality(features)
    
    return jsonify({'features': features, 'personality': personality})

if __name__ == '__main__':
    app.run(debug=True)