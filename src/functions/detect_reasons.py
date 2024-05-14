import datetime
import time


def detect_reasons(message, date):
    reasons = []

    if time.time() - message.author.created_at.timestamp() < 2.592e+6:
        print("Your account is younger than 30 days.")
        reasons.append("Your account is younger than 30 days.")

    if date is None:
        print("Could not read the given DOB.")
        reasons.append("Could not read the given DOB.")

    else:
        if datetime.datetime.now().year - date.year < 18:
            print("The given DOB indicates you're younger than 18.")
            reasons.append("The given DOB indicates you're younger than 18.")

    return reasons if reasons else None
