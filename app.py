from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from transformers import pipeline

app = Flask(__name__)

# Initialize ChatterBot
chatbot = ChatBot(
    "HealthcareBot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "default_response": "I'm not sure about that. Could you ask in a different way?",
            "maximum_similarity_threshold": 0.7
        }
    ]
)

trainer = ListTrainer(chatbot)
trainer.train([
    "Hi", "Hello! How can I assist you today?",
    "What can you do?", "I can calculate BMI, suggest workouts & diet plans, and answer health-related questions.",
    "How to calculate BMI?", "I can do it for you! Just provide your weight (kg) and height (cm).",
    "Give me a workout plan", "Do you prefer strength training, cardio, or a mix of both?",
    "Give me a diet plan", "Are you looking for weight loss, muscle gain, or a balanced diet?",
    "Goodbye", "Goodbye! Stay healthy!"
])

# GPT-3 Based Chatbot
gpt_chatbot = pipeline("text-generation", model="microsoft/DialoGPT-medium")

# Store user details for conversation flow
user_data = {}

# Function to calculate BMI
def calculate_bmi(weight, height):
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/get", methods=["POST"])
def get_bot_response():
    user_input = request.json.get("message", "").strip().lower()

    if not user_input:
        return jsonify({"response": ""})  # Ignore empty messages

    global user_data

    # Start Chat Flow
    if user_input in ["start chat", "hello", "hi"]:
        user_data.clear()
        return jsonify({"response": "Hey there! Let’s start with your weight (in kg)."})

    # Collect Weight
    if "weight" not in user_data:
        try:
            user_data["weight"] = float(user_input)
            return jsonify({"response": "Got it! Now, may I know your height in cm?"})
        except ValueError:
            return jsonify({"response": "That doesn't seem like a valid number. Please enter your weight again."})

    # Collect Height
    if "height" not in user_data:
        try:
            user_data["height"] = float(user_input)
            bmi = calculate_bmi(user_data["weight"], user_data["height"])
            user_data["bmi"] = bmi

            if bmi < 18.5:
                category = "underweight"
                advice = "You're a bit underweight. A balanced diet with more protein and healthy fats can help."
            elif 18.5 <= bmi < 24.9:
                category = "normal"
                advice = "Great! You have a normal BMI. Keep up with a healthy lifestyle!"
            elif 25 <= bmi < 29.9:
                category = "overweight"
                advice = "You’re slightly overweight. A mix of cardio and strength training would be beneficial."
            else:
                category = "obese"
                advice = "It’s important to focus on healthy eating and regular exercise. Would you like some guidance?"

            user_data["last_step"] = "bmi_done"
            return jsonify({"response": f"Your BMI is {bmi}, which means you're {category}. {advice} Would you like a workout or diet plan?"})
        
        except ValueError:
            return jsonify({"response": "That doesn't seem right. Could you enter your height again?"})

    # Handle Yes/No Responses Correctly
    if user_data.get("last_step") == "bmi_done":
        if user_input in ["yes", "sure", "okay", "yeah"]:
            user_data["last_step"] = "plan_selection"
            return jsonify({"response": "Great! Would you like a workout plan or a diet plan?"})
        if user_input in ["no", "nope", "not really"]:
            user_data["last_step"] = None
            return jsonify({"response": "Alright! Let me know if you need anything else. Stay healthy!"})

    # Handle Workout or Diet Plan Request
    if user_data.get("last_step") == "plan_selection":
        if "workout" in user_input:
            user_data["last_step"] = None
            return jsonify({"response": "Here’s a recommended workout plan:\n🏃 Cardio (30 min daily)\n🏋️ Strength Training (3x a week)\n🧘 Yoga & Flexibility. Need a diet plan too?"})
        if "diet" in user_input:
            user_data["last_step"] = None
            return jsonify({"response": "Here’s a recommended diet:\n🥗 Breakfast: Oatmeal & Fruits\n🍗 Lunch: Lean Protein & Veggies\n🥑 Dinner: Light Salad with Nuts. Want a workout plan too?"})

    # Default Response (Use GPT-Based AI for Complex Questions)
    if len(user_input.split()) > 3:  # Use AI only for longer messages
        response = gpt_chatbot(user_input, max_length=50, num_return_sequences=1)
        return jsonify({"response": response[0]['generated_text']})

    response = chatbot.get_response(user_input)

    if response.text.lower() in ["can you feel?", "i don't understand.", "sorry, what?", "hmm, i don't know."]:
        response = "I'm not sure I understand. Could you rephrase?"

    return jsonify({"response": str(response)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
