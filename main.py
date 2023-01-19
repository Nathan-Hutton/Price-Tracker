import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import smtplib

load_dotenv('/Users/natha/PycharmProjects/info.env')
sender_email = os.getenv('EMAIL')
recipient_email = os.getenv('TWILIO_RECEIVER')
generated_password = os.getenv('EMAIL_GENERATED_PASSWORD')
target_email = os.getenv('TARGET_EMAIL')

url = 'https://www.amazon.com/KEVENZ-Advanced-Training-Practice-Interlocked/dp/B01ASGKN8O/ref=sr_1_1_sspa?c=ts&keywords=Tennis%2BBalls&qid=1658688470&s=racquet-sports&sr=1-1-spons&ts_id=3420061&th=1'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/94.0.4606.71 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

html_file = requests.get(url=url, headers=headers).text
soup = BeautifulSoup(html_file, 'html.parser')
price = float(soup.find(name='span', class_='a-offscreen').text[1:])

target_price = 20

with smtplib.SMTP(os.getenv('SMTP'), int(os.getenv('PORT'))) as connection:
    connection.starttls()
    connection.login(user=sender_email, password=generated_password)
    if price <= target_price:
        connection.sendmail(
            from_addr=sender_email,
            to_addrs=target_email,
            msg=f'The tennis balls are currently {price}'
        )
