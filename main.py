'''
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pandas as pd
import base64
import io
import json
import logging
import speech_recognition as sr
from pydub import AudioSegment
from uuid import uuid4

# Initialize Flask app
app = Flask(__name__, static_folder='.')
app.secret_key = str(uuid4())
CORS(app)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/chatbot_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Define Conversation model
class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(120))
    message = db.Column(db.Text)
    response = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Load data
df = pd.read_csv("train_data_chatbot.csv")
questions = df["short_question"].astype(str).tolist()
answers = df["short_answer"].astype(str).tolist()

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
vectorizer = TfidfVectorizer()
question_vectors = vectorizer.fit_transform(questions)

with open("doctors.json", "r") as f:
    doctor_data = json.load(f)

session_history = {}

@app.route('/')
def index():
    if "user" in session:
        return send_from_directory('.', 'index.html')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user'] = user.username
            return redirect('/')
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        if User.query.filter_by(username=username).first():
            return "User already exists"
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

def get_best_answer(user_input):
    input_vec = vectorizer.transform([user_input])
    similarity = cosine_similarity(input_vec, question_vectors)
    idx = similarity.argmax()
    best_score = similarity[0][idx]
    return answers[idx] if best_score >= 0.3 else None

def recognize_speech(base64_audio):
    try:
        audio_data = base64.b64decode(base64_audio)
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="webm")
        wav_data = audio_segment.export(format="wav").read()
        recognizer = sr.Recognizer()
        with sr.AudioFile(io.BytesIO(wav_data)) as source:
            audio = recognizer.record(source)
            return recognizer.recognize_google(audio)
    except Exception as e:
        return None

def get_doctor(city):
    return doctor_data.get(city.title(), [])

@app.route('/api/chat', methods=["POST"])
def chat():
    if "user" not in session:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.json
    msg = data.get("message", "")
    audio = data.get("audio", "")
    city = data.get("location", "")

    session_id = session['user']
    user_session = session_history.get(session_id, {})
    last_symptom = user_session.get("symptom", "")

    if audio:
        msg = recognize_speech(audio)
        if not msg:
            return jsonify({"message": "Sorry, I couldn't understand your voice."}), 400

    if not msg:
        return jsonify({"message": "No input received."}), 400

    user_input = msg.lower().strip()

    if "medicine" in user_input and "for" not in user_input and last_symptom:
        user_input = f"medicine for {last_symptom}"

    GREETING_RESPONSES = {
        "hi": "Hi! How can I help you today?",
        "hello": "Hello! Please describe your symptoms.",
        "fever": "Take paracetamol and stay hydrated.",
        "cold": "Cetrizine and warm fluids are helpful.",
        "headache": "Paracetamol or rest usually helps.",
        "diarrhea": "Drink ORS and rest.",
        "vomiting": "ORS and domperidone are recommended."
    }

    MEDICINE_SUGGESTIONS = {
        "fever": "Paracetamol 500mg every 6 hours.",
        "cold": "Cetrizine and steam inhalation.",
        "vomiting": "ORS and domperidone.",
        "diarrhea": "ORS and light meals.",
        "headache": "Paracetamol or ibuprofen."
    }

    for symptom, med in MEDICINE_SUGGESTIONS.items():
        if f"medicine for {symptom}" in user_input:
            session_history[session_id] = {"symptom": symptom}
            conv = Conversation(user_id=session_id, message=msg, response=med)
            db.session.add(conv)
            db.session.commit()
            return jsonify({"message": med, "input_method": "audio" if audio else "text"})

    for keyword, reply in GREETING_RESPONSES.items():
        if keyword in user_input:
            session_history[session_id] = {"symptom": keyword}
            conv = Conversation(user_id=session_id, message=msg, response=reply)
            db.session.add(conv)
            db.session.commit()
            return jsonify({"message": reply, "input_method": "audio" if audio else "text"})

    best = get_best_answer(user_input)
    response = best if best else "I'm not sure. Please consult a doctor."

    session_history[session_id] = {"symptom": user_input}
    conv = Conversation(user_id=session_id, message=msg, response=response)
    db.session.add(conv)
    db.session.commit()

    return jsonify({"message": response, "input_method": "audio" if audio else "text"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
'''



#2ndlast

from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import pandas as pd
import base64
import io
import json
import logging
import speech_recognition as sr
from pydub import AudioSegment
from uuid import uuid4

app = Flask(__name__, static_folder='static')
app.secret_key = str(uuid4())
CORS(app)

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/chatbot_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # Plain text

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(120))
    message = db.Column(db.Text)
    response = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Data and Vectorizer Setup
df = pd.read_csv("train_data_chatbot.csv")
questions = df["short_question"].astype(str).tolist()
answers = df["short_answer"].astype(str).tolist()

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
vectorizer = TfidfVectorizer()
question_vectors = vectorizer.fit_transform(questions)

with open("doctors.json", "r") as f:
    doctor_data = json.load(f)

session_history = {}

# Routes
@app.route('/')
def index():
    if "user" in session:
        return render_template('index.html')
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip().lower()
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            return "User already exists"
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip().lower()
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user'] = user.username
            return redirect('/')
        return "Invalid username or password"
    return render_template('login.html')

#@app.route('/logout')
#def logout():
    #session.pop('user', None)
    #return redirect('/login')
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login')) 

@app.route('/api/chat', methods=["POST"])
def chat():
    if "user" not in session:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.json
    msg = data.get("message", "")
    audio = data.get("audio", "")
    city = data.get("location", "")
    session_id = session['user']
    user_session = session_history.get(session_id, {})
    last_symptom = user_session.get("symptom", "")

    if audio:
        msg = recognize_speech(audio)
        if not msg:
            return jsonify({"message": "Sorry, I couldn't understand your voice."}), 400

    if not msg:
        return jsonify({"message": "No input received."}), 400

    user_input = msg.lower().strip()

    if "medicine" in user_input and "for" not in user_input and last_symptom:
        user_input = f"medicine for {last_symptom}"

    GREETING_RESPONSES = {
         "hi": "Hi! How can I help you today?",
        "hello": "Hello! Please describe your symptoms.",
        "stomach pain": "You might be experiencing indigestion or cramps. Try taking antacids or consult a doctor if pain persists.",
        "my stomach is paining": "This could be due to gas, acidity, or cramps. Drink warm water and rest. If it continues, consult a doctor.",
        "fever": "You may have an infection. Take paracetamol and stay hydrated. See a doctor if it lasts more than 3 days.",
        "cold": "Drink warm fluids, rest, and consider steam inhalation. Avoid cold drinks.",
        "cough": "Try warm water gargles, steam inhalation, and honey with warm water.",
        "vomit": "Take ORS to avoid dehydration. If vomiting continues, consult a doctor.",
        "diarrhea": "Drink fluids with electrolytes. Avoid spicy food. See a doctor if severe.",
        "headache": "It could be due to stress or fatigue. Rest in a quiet room and stay hydrated.",
        "chest pain": "Please consult a doctor immediately. This could be serious.",
        "breathe": "Seek medical attention immediately. Difficulty in breathing is serious.",
        "tired": "Eat a nutritious diet, stay hydrated, and rest. Get blood tests if it continues.",
        "my head hurts": "It could be a headache due to stress. Try resting.",
        "i am feeling weak": "This might be fatigue. Get some rest and stay hydrated.",
        "period pain": "Use a hot water bag, stay hydrated, and try light exercise. Painkillers like mefenamic acid can help.",
        "menopause": "Hot flashes and mood swings can be managed with exercise and proper diet. Talk to a doctor.",
        "pregnancy": "Missed periods, nausea, and fatigue can be early signs. Take a test and consult a doctor.",
        "i feel feverish": "That sounds like a fever. Stay hydrated and rest well.",
        "medicine": "Please describe your symptoms so I can suggest general over-the-counter medicine. For example: 'medicine for fever'.",
        "recommend": "Please tell me what symptoms you're having so I can recommend appropriate medicine.",
        "covid symptoms": "Common symptoms include fever, dry cough, fatigue, and loss of taste or smell. Seek medical help if symptoms worsen.",
        "normal body temperature": "A normal body temperature is between 97°F and 99°F (36.1°C to 37.2°C).",
        "how much water to drink": "About 2 liters (8 cups) per day is recommended, but needs may vary based on activity and weather.",
        "paracetamol and ibuprofen": "Yes, you can take them together but stagger doses. Take paracetamol first, then ibuprofen if needed.",
        "antibiotics side effects": "Common ones include nausea, diarrhea, and rash. Serious reactions require immediate medical help.",
        "sore throat and fever": "May be a viral or bacterial infection. If persistent, see a doctor for tests or antibiotics.",
        "dizzy and tired": "May be due to dehydration, low blood sugar, or anemia. Get a medical check-up.",
        "pcos symptoms": "Irregular periods, acne, hair growth, and weight gain are signs. Ultrasound and hormone tests confirm it.",
        "period cramps": "Mild cramps are normal. Severe pain should be discussed with a gynecologist.",
        "child fever": "Give fluids and paracetamol (based on age). See a pediatrician if fever lasts over 2 days.",
        "uti cause": "Caused by bacteria in the urinary tract. Maintain hygiene and drink water to prevent it.",
        "dengue symptoms": "High fever, rash, and joint pain are symptoms. Treat with hydration and paracetamol. Avoid aspirin.",
        "heart healthy diet": "Eat fruits, vegetables, whole grains, lean proteins, and avoid processed food.",
        "intermittent fasting": "Can help with metabolism and weight. Not for everyone. Consult a doctor before starting.",
        "anxiety": "Try mindfulness and rest. If it interferes with daily life, see a mental health expert.",
        "fainted": "Lay the person down, elevate their legs, and check breathing. If unresponsive, call emergency help.",
        "minor burn": "Cool under running water for 10–15 minutes, then cover with a sterile bandage. Avoid ointments like butter.",
        "diabetes management": "Monitor sugar, eat balanced meals, exercise, and follow medication schedules.",
        "hypertension symptoms": "Often symptomless. Some may get headaches or dizziness. Get regular BP checks.",
        "travel vaccines": "Common vaccines include Hepatitis A/B, Typhoid, and Tetanus. Check with a doctor before international travel."
}

    MEDICINE_SUGGESTIONS = {
       "fever": "You can take Paracetamol (500mg) every 6 hours as needed.",
        "cold": "Cetrizine for runny nose, steam inhalation, and rest.",
        "vomiting": "ORS solution and Domperidone (after meals).",
        "headache": "Paracetamol or ibuprofen can help.",
        "diarrhea": "ORS, light diet, and consult if it continues.",
        "stomach pain": "You can try an antacid like Gelusil or a pain reliever like Buscopan. Avoid heavy meals.",
        "period pain": "Mefenamic acid or ibuprofen can help with period pain.",
        "sore throat and fever": "Paracetamol and warm salt water gargles can help. For strep throat, a doctor may prescribe antibiotics.",
        "dengue symptoms": "Paracetamol only (avoid NSAIDs like ibuprofen or aspirin). Hydration is very important.",
        "uti cause": "Antibiotics like Nitrofurantoin or Trimethoprim (only with prescription). Cranberry juice may help prevention.",
        "cold and cough": "Steam inhalation, warm fluids, and Cough syrup like Benadryl or Honitus can help.",
        "pcos symptoms": "Consult a doctor for hormonal medicines. Lifestyle changes and metformin may be advised.",
        "diabetes": "Metformin is commonly prescribed. Follow your doctor’s guidance strictly.",
        "hypertension": "Amlodipine or Telmisartan may be prescribed. Don't self-medicate; get a doctor's opinion.",
        "travel vaccines": "Vaccines are preventive, not medicines. Visit a travel clinic 4-6 weeks before travel.",
        "vomit": "ORS and antiemetics like Ondansetron (under doctor’s guidance).",
        
}
    HOME_REMEDIES = {
    "fever": "Drink plenty of fluids, rest, and use a cool damp cloth on the forehead.",
    "cold": "Drink warm fluids like soup or ginger tea. Steam inhalation helps open nasal passages.",
    "cough": "Honey with warm water or ginger tea helps soothe the throat. Avoid cold foods.",
    "vomiting": "Suck on ice chips, sip ORS or ginger tea slowly. Avoid solid food initially.",
    "diarrhea": "Drink rice water or buttermilk. Eat soft foods like bananas and plain rice.",
    "stomach pain": "Use a warm compress on the belly. Ginger tea or ajwain (carom seeds) water can help.",
    "headache": "Rest in a dark room. Apply a cold compress to your head or neck.",
    "period pain": "Use a heating pad on the lower abdomen. Drink chamomile tea or do light yoga.",
    "sore throat": "Gargle with warm salt water. Drink turmeric milk or honey-lemon tea.",
    "acidity": "Drink cold milk or chew fennel seeds. Avoid spicy or oily food.",
    "tired": "Eat iron-rich foods like spinach, and stay hydrated. Sleep well and avoid screen time before bed.",
    "feel feverish": "Drink plenty of fluids, rest, and use a cool damp cloth on the forehead"
}
    
    for symptom, remedy in HOME_REMEDIES.items():
        if (
            f"home remedy for {symptom}" in user_input
            or f"home remedies for {symptom}" in user_input
            or f"natural remedy for {symptom}" in user_input
            or f"natural remedies for {symptom}" in user_input
            or f"remedy for {symptom}" in user_input
            or f"remedies for {symptom}" in user_input
        ):
            session_history[session_id] = {"symptom": symptom}
            conv = Conversation(user_id=session_id, message=msg, response=remedy)
            db.session.add(conv)
            db.session.commit()
            return jsonify({"message": remedy, "input_method": "audio" if audio else "text"})

    for symptom, med in MEDICINE_SUGGESTIONS.items():
        if f"medicine for {symptom}" in user_input:
            session_history[session_id] = {"symptom": symptom}
            conv = Conversation(user_id=session_id, message=msg, response=med)
            db.session.add(conv)
            db.session.commit()
            return jsonify({"message": med, "input_method": "audio" if audio else "text"})

    for keyword, reply in GREETING_RESPONSES.items():
        if keyword in user_input:
            session_history[session_id] = {"symptom": keyword}
            conv = Conversation(user_id=session_id, message=msg, response=reply)
            db.session.add(conv)
            db.session.commit()
            return jsonify({"message": reply, "input_method": "audio" if audio else "text"})

    best = get_best_answer(user_input)
    response = best if best else "I'm not sure. Please consult a doctor."

    session_history[session_id] = {"symptom": user_input}
    conv = Conversation(user_id=session_id, message=msg, response=response)
    db.session.add(conv)
    db.session.commit()
    return jsonify({"message": response, "input_method": "audio" if audio else "text"})

def recognize_speech(base64_audio):
    try:
        audio_data = base64.b64decode(base64_audio)
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="webm")
        wav_data = audio_segment.export(format="wav").read()
        recognizer = sr.Recognizer()
        with sr.AudioFile(io.BytesIO(wav_data)) as source:
            audio = recognizer.record(source)
            return recognizer.recognize_google(audio)
    except Exception as e:
        logging.error("Speech recognition error: %s", e)
        return None

def get_best_answer(user_input):
    input_vec = vectorizer.transform([user_input])
    similarity = cosine_similarity(input_vec, question_vectors)
    idx = similarity.argmax()
    score = similarity[0][idx]
    return answers[idx] if score >= 0.3 else None

def get_doctor(city):
    return doctor_data.get(city.title(), [])


if __name__ == "__main__":
    app.run(debug=True, port=5000)
