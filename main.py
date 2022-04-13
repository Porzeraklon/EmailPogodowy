from requests import get
from json import loads
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender = input("Podaj email: ")
rec = input("Podaj odbiorce: ")
passwd = input("Podaj hasło: ")
subject = "Prognoza"
Miasto = 'Gdańsk'

def pogoda():
    url = 'https://danepubliczne.imgw.pl/api/data/synop'
    response = get(url)
    for row in loads(response.text):
        if row['stacja'] in Miasto:
            data_pomiaru = row['data_pomiaru']
            godzina_pomiaru = row['godzina_pomiaru']
            temperatura = row['temperatura']
            wiatr = row['predkosc_wiatru']
            wilgotnosc = row['wilgotnosc_wzgledna']
            cisnienie = row['cisnienie']
            return data_pomiaru, godzina_pomiaru, temperatura, wiatr, wilgotnosc, cisnienie


data_pomiaru, godzina_pomiaru, temperatura, wiatr, wilgotnosc, cisnienie = pogoda()

html = '''
    <html>
        <body>
            <h1>Dzisiejsza Pogoda</h1>
            <p>
            Miasto: ''' +str(Miasto)+'''<br>
            Data pomiaru: ''' +str(data_pomiaru)+'''<br>
            Godzina pomiaru: ''' +str(godzina_pomiaru)+''':00<br>
            Temperatura: ''' +str(temperatura)+'''°C<br>
            Wiatr: ''' +str(wiatr)+'''km/h<br>
            Wilgotnosc: ''' +str(wilgotnosc)+'''%<br>
            Ciśnienie: ''' +str(cisnienie)+'''hPa<br>
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




