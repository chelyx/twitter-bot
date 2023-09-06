import tweepy
import datetime
import time
import requests
from bs4 import BeautifulSoup
import credentials
from Team import Team

# Configura el equipo y la URL del sitio web que contiene la información del partido
equipos = [Team("Argentinos Juniors", "https://www.futbolenvivoargentina.com/equipo/argentinos-juniors"),
           Team("All Boys", "https://www.futbolenvivoargentina.com/equipo/all-boys")]


conteiner_class = '.cabeceraTabla '

def tweet(message: str):
    client = tweepy.Client(consumer_key=credentials.API_KEY, consumer_secret=credentials.API_KEY_SECRET,
                           access_token=credentials.ACCESS_TOKEN, access_token_secret=credentials.ACCESS_TOKEN_SECRET)
    #api.update_status(message)
    client.create_tweet(text=message)
    print('Tweeted from python')


# Función para obtener la fecha del próximo partido desde Google
def juega_hoy(team1: Team):
    try:
        response = requests.get(team1.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        i = soup.findAll('tbody')[0]
        day = i.contents[1].contents[1].text.split(", ")[1]
        hora = i.contents[2].contents[1].text
        local1 = i.contents[2].contents[4].text.lstrip().rstrip()
        print(local1, day, hora)
        fecha = datetime.datetime.strptime(day, '%d/%m/%Y').date()
        if local1 == team1.name and es_dia_de_partido(fecha):
            team1.setplays(True)
            team1.settime(hora)

    except Exception as e:
        print(f"Error al obtener la fecha del partido: {e}")
        return None


def es_dia_de_partido(fecha_partido):
    hoy = datetime.date.today()
    return hoy == fecha_partido


# Loop principal del bot
while True:
    mensaje = ""

    for equipo in equipos:
        juega_hoy(equipo)

        if equipo.plays:
            mensaje += f"Hoy juega {equipo.name} a las {equipo.time}\n"
        else:
            mensaje += f"Hoy NO hay partidos en la cancha de {equipo.name}!\n"

    tweet(mensaje)
    time.sleep(86400)  # Espera 24 horas (1 día) antes de verificar nuevamente
