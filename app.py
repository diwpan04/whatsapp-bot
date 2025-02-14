from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, init_app, User
from process_query import process_user_query
from utils import get_user_state, check_confirmation_response
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"

init_app(app)
migrate = Migrate(app, db)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    # Parse incoming message from Twilio
    from_number = request.form.get("From")
    incoming_msg = request.form.get("Body", "").strip()

    if not incoming_msg:
        return jsonify({"message": "Please provide a message."}, 400)

    response_message = ""
    # Check if user is in the process of confirming the expense deletion
    user_state = get_user_state(from_number)
    if user_state:
        response_message = check_confirmation_response(from_number, user_state, incoming_msg)
    else:
        user = db.session.query(User).filter_by(user_phone=from_number).first()
        if not user:
            user = User(user_phone=from_number, limit_amount=5000)
            db.session.add(user)
            db.session.commit()
            response_message += f"""
👋 Welcome to Expense Tracker! 📊

💰 Your Current Monthly Limit: *₹ {user.limit_amount}*

✨ What you can do:
    - Update your monthly limit
    - Add new expenses
    - Retrieve past expense details
    - View your current monthly limit
    - Delete all expenses
    - Delete your account

💡 Need help?
Type "help" for assistance!
"""
        response_message += process_user_query(incoming_msg, from_number)

    # Send response back to WhatsApp using Twilio
    twilio_response = MessagingResponse()
    twilio_response.message(response_message)
    return str(twilio_response)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7000)