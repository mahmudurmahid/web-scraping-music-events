import requests
import selectorlib
import smtplib, ssl
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }


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


def store(extracted):
    """ Store the extracted data in a text file by appending"""
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")


def read(extracted):
    """ Read the content of the text file"""
    with open("data.txt", "r") as file:
        return file.read()


if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)
    
    content = read(extracted)

    if extracted != "No upcoming tours":
        if extracted not in content:
            store(extracted)
            send_email()
