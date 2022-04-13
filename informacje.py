from bs4 import BeautifulSoup
from requests import get
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date

sender = "beldegrin.damian@gmail.com"
rec = "maja.antosiak@gmail.com"
passwd = "MISZCZUBLUZA"
subject = "Prognoza"
Miasto = 'Gdańsk'
today = date.today()
date = today.strftime("%d/%m/%Y")

def pogoda():
    URL = 'https://www.weatheronline.pl/Polska/Gdansk.htm'
    page = get(URL)
    bs = BeautifulSoup(page.content, 'html.parser')
    for weather in bs.find_all('table', class_='gr1'):
        temp_min = weather.find('span', class_='Temp_minus').get_text()
        temp_max = weather.find('span', class_='Temp_plus').get_text().strip()
        return temp_min, temp_max

temp_min, temp_max = pogoda()

def kursy():
    URL = 'https://internetowykantor.pl/kurs-euro-nbp/'
    page = get(URL)
    bs = BeautifulSoup(page.content, 'html.parser')
    EUR = bs.find('span', class_='bem-single-rate-box__item-rate').get_text().strip()
    EUR_zmiana = bs.find('span', class_='bem-single-rate-box__direction ')
    if EUR_zmiana == None:
        EUR_zmiana = bs.find('span', class_='bem-single-rate-box__direction is-up')
        if EUR_zmiana != None:
            EUR_zmiana = "+" + bs.find('span', class_='bem-single-rate-box__direction is-up').get_text().strip()
        elif EUR_zmiana == None:
            EUR_zmiana = "-" + bs.find('span', class_='bem-single-rate-box__direction is-down').get_text().strip()
        else:
            print("Coś nie działa z zmiana EUR")
    URL = 'https://internetowykantor.pl/kurs-dolara-nbp/'
    page = get(URL)
    bs = BeautifulSoup(page.content, 'html.parser')
    USD = bs.find('span', class_='bem-single-rate-box__item-rate').get_text().strip()
    USD_zmiana = bs.find('span', class_='bem-single-rate-box__direction ')
    if USD_zmiana == None:
        USD_zmiana = bs.find('span', class_='bem-single-rate-box__direction is-up')
        if USD_zmiana != None:
            USD_zmiana = "+" + bs.find('span', class_='bem-single-rate-box__direction is-up').get_text().strip()
        elif USD_zmiana == None:
            USD_zmiana = "-" + bs.find('span', class_='bem-single-rate-box__direction is-down').get_text().strip()
        else:
            print("Coś nie działa z zmiana USD")
    return EUR, EUR_zmiana, USD, USD_zmiana

EUR, EUR_zmiana, USD, USD_zmiana = kursy()

html = '''
    <html>
        <body>
            <h1>Dzienny raport</h1>
            <h2>'''+str(date)+'''</h2>
            <p>
            Miasto: ''' +str(Miasto)+'''<br>
            Temperatura: ''' +str(temp_max)+''' / '''+str(temp_min)+'''<br>
            Kurs EUR/PLN: '''+str(EUR)+''' ('''+str(EUR_zmiana)+''')<br>
            Kurs USD/PLN: '''+str(USD)+''' ('''+str(USD_zmiana)+''')<br>
            </p>
        </body>
    </html>
    '''

message = MIMEMultipart()
message['From'] = sender
message['To'] = rec
message['Subject'] = "Prognoza"
message.attach(MIMEText(html, "html"))
message = message.as_string()

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender, passwd)
    print("Zalogowano")
    server.sendmail(sender, rec, message)
    print("Wyslano")