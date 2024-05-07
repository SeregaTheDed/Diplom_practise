from datetime import datetime
from pydantic import BaseModel


class Message(BaseModel):
    id: int | None = None
    text: str | None = None
    date_sent: datetime | None = datetime.now()
    user_id: int | None = None


class MessageWithLogin(Message):
    user_login: str | None = None


class LoginData(BaseModel):
    login: str
    password: str


def create_message_data(user_login, date_sent, text):
    return {
        'user_login': user_login,
        'date_sent': date_sent,
        'text': text
    }
