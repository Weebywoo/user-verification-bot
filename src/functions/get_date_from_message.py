import datetime
from datetime import date


def get_date_from_message(message) -> date | None:
    try:
        return datetime.datetime.strptime(message.content, "%m/%d/%Y").date()

    except ValueError:
        return None
