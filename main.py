from datetime import datetime

import uvicorn
import sqlite3

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from models import Message, MessageWithLogin, LoginData, create_message_data
from sqlite_init import init_database, db_file

app = FastAPI()


#init_database()


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("auth.html", 'rb') as f:
        return f.read()


@app.get("/chat", response_class=HTMLResponse)
async def chat():
    with open("chat.html", 'rb') as f:
        return f.read()


@app.post("/login", response_class=JSONResponse)
async def login(login_data: LoginData):
    print(login_data)
    query = f"""
        select users.id
        from users
        where login = '{login_data.login}' and pass = '{login_data.password}'
"""
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        if len(data) < 1:
            return None
        print(data)
        return data[0][0]


@app.get("/get_messages", response_class=JSONResponse)
async def get_message():
    query = """
        select u.login, m.date_sent, m.text
        from messages m
        join users u on u.id = m.user_id
"""
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()  #2024-05-07 00:55:40.479811
        messages = list(
            map(lambda m: create_message_data(m[0], datetime.strptime(m[1], "%Y-%m-%d %H:%M:%S.%f"), m[2]), data))
        print('messages:', messages)
        return messages


@app.post("/send_message", response_class=JSONResponse)
async def send_message(message: Message):
    query = f"""
    insert into messages(user_id, date_sent, text)
    values ({message.user_id}, '{message.date_sent}', {message.text})
"""
    with sqlite3.connect(db_file) as conn:
        conn.executescript(query)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
