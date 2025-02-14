import json
from utils import add_expense, update_limit, view_limit, help, miscellaneous
from gemini import classify_message
from retrieve_expenses import retrieve_expense


def process_user_query(user_message, user_phone):
    res = classify_message(user_message)
    res = json.loads(res)
    print(res)

    if res.get("retrieve_expense"):
        return retrieve_expense(user_phone, user_message)
    elif res.get("add_expense"):
        return add_expense(user_phone, res)
    elif res.get("update_limit"):
        return update_limit(user_phone, res)
    elif res.get("view_limit"):
        return view_limit(user_phone)
    elif res.get("help"):
        return help()
    else:
        return miscellaneous()
