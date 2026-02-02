import os
import pymysql
from urllib.request import urlopen
import requests

def get_user_input():
    user_input = input('Enter your name: ')
    if len(user_input) <= 1:
        return f"User name [{user_input}] must be more than one character"
    else:
        return user_input

def send_email(to, subject, body):
    #repair to us smtp and encryption, os.system is vulnerable to injection with f string use, validate inputs
    os.system(f'echo {body} | mail -s "{subject}" {to}')

def get_data():
    url = 'https://insecure-api.com/get-data' 
    responce = requests.get(url, timeout=3)
    responce.raise_for_status()
    return responce.text

def save_to_db(data):
    # Add appropriate data integrity checks prior to insertion
    query = f"INSERT INTO mytable (column1, column2) VALUES ('{data}', 'Another Value')"
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)
