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
            session.auth = (inewi_name,inewi_passwd)
            headers = {"User-Agent": ua['google chrome']}
            landing_page = session.get(self.inewi_url, verify=False, headers=headers)
            soup = BeautifulSoup(session.get(self.inewi_url).content, 'html.parser')
            try:
                token = soup.find('input', {'name': '__RequestVerificationToken'}).get('value')
            except Exception as e:
                print("Got unhandled exception %s" % str(e))
            payload.update({"__RequestVerificationToken": str(token)})
            session.post(landing_page.url, data=payload, headers=headers)
            payload.clear()
            payload.update({
                "UserEmail": inewi_name,
                "Password": inewi_passwd,
                "TimeZone": "Europe/Warsaw",
                "TimeUtcUnix": str(int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()))
            })
            second_page = session.post("https://inewi.pl/kiosk/OnlineRcp/LoginByEmailOrPhone", data=payload, headers=headers)
            statuses = second_page.json()['statuses']
            for d in statuses:
                if d['Name'] == 'Przerwa':
                    payload.clear()
                    payload.update({
                        "StatusId": d['Id'],
                        "QrCode": second_page.json()['qrCode'],
                        "TimeUtcUnix": second_page.json()['timeUtcUnix'],
                        "TimeLocalUnix": second_page.json()['timeLocalUnix'],
                        "IsEnd": d['IsEnd'],
                        "TimeZoneId": second_page.json()['timeZoneId']
                    })
            session.post('https://inewi.pl/kiosk/OnlineRcp/SetStatus', data=payload, headers=headers)

            #TODO: change hardcoded links, add functions to post entry and exit in inewi

    def log_livefruit(self, livefruit_name, livefruit_passwd):
        print(livefruit_name, livefruit_passwd)


