from bs4 import BeautifulSoup
from datetime import datetime
from fake_useragent import UserAgent

import requests


class Autobreak:
    def __init__(self, inewi_url, livefruit_url):
        self.inewi_url = inewi_url
        self.livefruit_url = livefruit_url

    def log_inewi(self, inewi_name, inewi_passwd):
        payload = {"Email": inewi_name,"Password": inewi_passwd}
        ua = UserAgent()
        with requests.Session() as session:
            landing_page = session.get(self.inewi_url, verify=False, headers={"User-Agent":ua.google})
            soup = BeautifulSoup(session.get(self.inewi_url).content, 'html.parser')
            try:
                token = soup.find('input', {'name': '__RequestVerificationToken'}).get('value')
            except Exception as e:
                print("Got unhandled exception %s" % str(e))
            payload.update({"__RequestVerificationToken": str(token)})
            session.post(landing_page.url, data=payload)
            payload.clear()
            payload.update({
                "UserLogin": inewi_name,
                "Password": inewi_passwd,
                "TimeZone": "Europe/Warsaw",
                "TimeUtcUnix": str(int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()))
            })
            second_page = session.post("https://inewi.pl/kiosk/", data=payload)
            print(session.cookies,landing_page.text, second_page.text)

    def log_livefruit(self, livefruit_name, livefruit_passwd):
        print(livefruit_name, livefruit_passwd)


