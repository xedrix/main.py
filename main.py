import requests, os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()
TWILIO_ACCOUNT_SID = "AC83f0e0b765106862b1a3d53c2a7c231e"
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"
OWM_API_KEY = os.getenv("OWM_API_KEY")
PARAMS = {
    "lat": 45.420422,
    "lon": -75.692429,
    "exclude": "current,minutely,daily,alerts",
    "appid": OWM_API_KEY
}

response = requests.get(url=OWM_ENDPOINT, params=PARAMS)
response.raise_for_status()
weather_data = response.json()['hourly'][:12]
hourly_data = [hour["weather"][0]["id"] for hour in weather_data]
rains = [True for code in hourly_data if code < 600]

if True in rains:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages \
        .create(
        body="It's going to rain today, bring an umbrella!",
        from_="+19896621544",
        to=os.getenv("MY_NUMBER")
    )
    print(message.status)
else:
    print("No rain!")
