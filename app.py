from bs4 import BeautifulSoup
import requests
import sqlite3
import subprocess


def send_message():
    subprocess.Popen(['notify-send', message])
    return


url = "https://bountify.co/"
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

bounty_question = soup.find_all('div', class_='question')

conn = sqlite3.connect('bounties.db')

# First time run only
# sql = "CREATE TABLE bounties (" \
#       "bounty_id varchar);"
# conn.execute(sql)
#####################

for bounty in bounty_question:
    bounty_id = bounty.get('id')
    sql = 'SELECT * FROM bounties WHERE bounty_id = ?'
    val = (
        bounty_id,
    )
    cursor = conn.cursor()
    cursor.execute(sql, val)
    result = cursor.fetchone()
    if not result:
        sql = 'INSERT INTO bounties (bounty_id) VALUES (?)'
        val = (
            bounty_id,
        )
        conn.execute(sql, val)
        conn.commit()

        message = "New bounty has just been posted!"
        send_message()
