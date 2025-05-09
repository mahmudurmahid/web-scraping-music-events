import requests
import selectorlib
import smtplib, ssl
import os
import time
import sqlite3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Web scraping URL and headers
URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }

# Establish a connection to the SQLite database
connection = sqlite3.connect("data.db")


def scrape(url):
    """ Scrape the page source from the URL"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    """ Extract the tour data from the page source"""
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
    """ Send an email notification"""
    host = os.getenv("EMAIL_HOST")
    port = 465

    username = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")

    receiver = os.getenv("EMAIL_RECEIVER")
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
    print("Email sent successfully!")


def store(extracted):
    """ Store the extracted data in a text file by appending"""
    row = extracted.split(",")
    row = [item.strip() for item in row]

    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?, ?, ?)", row)
    connection.commit()


def read(extracted):
    """ Read the content of the SQL file"""
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    row = cursor.fetchall()
    print(row)
    return row


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        
        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:
                store(extracted)
                send_email(message= f"New tour available: {extracted}")
        time.sleep(2)
