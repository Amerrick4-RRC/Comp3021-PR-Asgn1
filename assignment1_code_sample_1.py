import os
import pymysql
from urllib.request import urlopen
import requests
import smtplib
from email.message import EmailMessage
import re

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_User"),
    "password": os.getenv("DB_PASSWORD")
}

def get_user_input():
    user_input = input('Enter your name: ')
    if len(user_input) <= 1:
        return f"User name [{user_input}] must be more than one character"
    else:
        return user_input

EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

def send_email(to, subject, body, smtp_host = "smtp.example.com", smtp_port=507):
    if not EMAIL_REGEX.match(to):
        raise ValueError("Invalid email address.")
    
    msg = EmailMessage()
    msg["To"] = to
    msg["From"] = "noreply@example.com"
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login("smtp_user", "smtp_password")
        server.send_message(msg)

def get_data():
    url = 'https://insecure-api.com/get-data' 
    responce = requests.get(url, timeout=3)
    responce.raise_for_status()
    return responce.text

def save_to_db(data):

    if not isinstance(data, str) or len(data) > 255:
        raise ValueError("Invalid data")
    
    query = "INSERT INTO mytable (column1, column2) VALUES ('%s', '%s')"
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(query, (data, "Another Value"))
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)
