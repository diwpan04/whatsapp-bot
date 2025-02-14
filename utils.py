from sqlalchemy import func
from datetime import datetime
from twilio.rest import Client
from models import db, User, Expense
from dotenv import load_dotenv
import os
from flask import  jsonify

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
print(TWILIO_PHONE_NUMBER)
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
def send_response_message(user_phone, response_message):
    try:
        message = client.messages.create(
            body=response_message,
            from_=f"whatsapp:{TWILIO_PHONE_NUMBER}",
            to=f"whatsapp:{user_phone}"
        )
        return message
    except Exception as e:
        print(f"Error sending message: {e}")
        return None




def check_confirmation_response(user_phone, user_state, response):
    response_message = """"""

    return response_message


def get_user_state(user_phone):
    # Retrieve the state from the database or session
    user = db.session.query(User).filter_by(user_phone=user_phone).first()
    return user.state if user else None

def set_user_state(user_phone, state):
    # Store the state in the database or session
    user = db.session.query(User).filter_by(user_phone=user_phone).first()
    if user:
        user.state = state
        db.session.commit()

def reset_user_state(user_phone):
    # Reset the user state after the confirmation process
    user = db.session.query(User).filter_by(user_phone=user_phone).first()
    if user:
        user.state = None  # or some default state
        db.session.commit()



def add_expense(user_phone, res):
    user = db.session.query(User).filter_by(user_phone=user_phone).first()  # Get the user

    # Create an expense object
    expense = Expense(
        user_id=user.id,
        category=res["add_expense"]["category"].lower(),
        amount=res["add_expense"]["amount"],
        description=res["add_expense"]["description"].lower(),
    )

    # Add the expense to the session and commit it to the database
    db.session.add(expense)
    db.session.commit()

    # Prepare the message about the added expense
    message = f"""
✅ Expense added successfully!
    🗓 Date: {expense.date.strftime("%d-%m-%Y")}
    💰 Amount: ₹ {expense.amount}
    📝 Category: {expense.category}
    📄 Description: {expense.description}

"""

    # Fetch the user's budget limit and calculate total expenses for the current month
    budget = user.limit_amount
    current_month = datetime.now().month
    current_year = datetime.now().year

    total_expenses = (
        db.session.query(func.sum(Expense.amount))
        .filter(
            func.extract("month", Expense.date) == current_month,
            func.extract("year", Expense.date) == current_year,
        )
        .scalar()
    )

    # Determine if the user has exceeded the budget and update the message
    if total_expenses > budget:
        message += f"""
🚨 You have exceeded your budget of *₹ {budget}* for this month.
💸 The total expenses for the current month is *₹ {total_expenses}*.
"""
    else:
        message += f"""
💸 The total expenses for the current month is *₹ {total_expenses}*.
💰 You have *₹ {budget - total_expenses}* left in your budget for this month.
"""

    return message


def update_limit(user_phone, res):
    user = db.session.query(User).filter_by(user_phone=user_phone).first()  # Get the user

    # Update the user's limit amount
    user.limit_amount = res["update_limit"]["limit_amount"]
    db.session.commit()

    # Calculate total expenses for the current month
    current_month = datetime.now().month
    current_year = datetime.now().year
    total_expenses = (
        db.session.query(func.sum(Expense.amount))
        .filter(
            func.extract("month", Expense.date) == current_month,
            func.extract("year", Expense.date) == current_year,
        )
        .scalar()
    )

    # Prepare the response message
    msg = f"""
✅ The limit amount has been updated.
💵 You have currently set a limit of *₹ {res["update_limit"]["limit_amount"]}*.
💸 The total expenses for the current month is *₹ {total_expenses}*.
"""

    return msg


def view_limit(user_phone):
    user = db.session.query(User).filter_by(user_phone=user_phone).first()  # Get the user

    # Fetch the user's budget limit
    budget = user.limit_amount

    # Calculate total expenses for the current month
    current_month = datetime.now().month
    current_year = datetime.now().year
    total_expenses = (
        db.session.query(func.sum(Expense.amount))
        .filter(
            func.extract("month", Expense.date) == current_month,
            func.extract("year", Expense.date) == current_year,
        )
        .scalar()
    )

    # Prepare the response message
    msg = f"""
💵 Your current monthly limit is *₹ {budget}*.
💸 The total expenses for the current month is *₹ {total_expenses}*.
"""

    return msg







def help():
    return """
    1) What you can do:
    2) Update your monthly limit
    3) Add new expenses
    4) Retrieve past expense details
    5) View your current monthly limit


     Here are some example queries you can try:
    1. "Add ₹ 500 for groceries"
    2. "Add 200 for travel"
    3. "Update my monthly limit to Rs 5000"
    4. "Show my expenses"
    5. "Show my limit"
    6. "Help"
"""


def miscellaneous():
    return """Sorry, I didn't understand that, I'm an expense tracker bot. Please type "help" for assistance. """