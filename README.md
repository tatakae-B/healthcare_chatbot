# Healthcare Chatbot

A Flask-based AI chatbot that provides workout and diet recommendations based on BMI.

## Features
- **Chatbot Interaction**: Engages users in a chat-based interface.
- **BMI Calculation**: Determines BMI based on user input (age, gender, height, weight).
- **Diet & Workout Plans**: Suggests plans based on BMI category (underweight, normal, overweight).
- **Custom Queries**: Responds to general health-related questions.

## Installation

### Prerequisites
- Python 3.x
- Flask
- SQLite3

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/YOUR_USERNAME/healthcare_chatbot.git
   cd healthcare_chatbot
   ```
2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the application:
   ```sh
   python app.py
   ```
5. Open your browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

## File Structure
```
healthcare_chatbot/
│-- app.py              # Main Flask application
│-- requirements.txt    # Project dependencies
│-- db.sqlite3          # SQLite database
│-- static/
│   ├── style.css       # Stylesheet
│   ├── script.js       # JavaScript for chat interaction
│-- templates/
│   ├── chat.html       # Chat interface
│   ├── index.html      # Homepage
│-- .gitignore          # Files to ignore in Git
│-- README.md           # Project documentation
```

## Future Enhancements
- Implement authentication for users.
- Improve chatbot responses using a trained NLP model.
- Deploy the application on a cloud platform (e.g., AWS, Heroku).

## License
This project is open-source and available under the MIT License.

---

Feel free to contribute and enhance the project!

