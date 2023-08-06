import json
import logging
import os
import time

import requests
from bs4 import BeautifulSoup

from anysell.sellers.base import Seller
from anysell.sellers.item import Item
from anysell.config import config, storage_path

bazos_oblecenie_cats = {
    "Blúzky": 51,
    "Bundy a Kabáty": 52,
    "Čiapky, Šatky": 53,
    "Doplnky": 72,
    "Džínsy": 54,
    "Funkčné prádlo": 55,
    "Hodinky": 73,
    "Kabelky": 74,
    "Košele": 56,
    "Kožené oblečenie": 57,
    "Mikiny": 58,
    "Nohavice": 59,
    "Obleky, Saká": 60,
    "Plavky": 61,
    "Plecniaky a kufre": 75,
    "Rukavice a Šály": 63,
    "Rúška": 458,
    "Šaty, Kostýmy": 68,
    "Šortky": 69,
    "Šperky": 77,
    "Spodná bielizeň": 64,
    "Športové oblečenie": 70,
    "Sukne": 65,
    "Svadobné šaty": 66,
    "Svetre": 67,
    "Tehotenské oblečenie": 62,
    "Topánky, obuv": 76,
    "Tričká, roláky, tielka": 71,
    "Ostatné": 78,
}
spam_protection_key, spam_protection_value = None, None


class BazosSeller(Seller):
    def __init__(self):
        self._session = None

    def create_post(self, item: Item):
        k, v = self.spam_protection()

        data = {
            "cenavyber": "1",
            "lokalita": config()["psc"],
            "jmeno": config()["name"],
            "telefoni": config()["phone"],
            "maili": config()["email"],
            "heslobazar": config()["password"],
            k: v,
            "category": str(bazos_oblecenie_cats[item.category]),
            "cena": str(item.price),
            "nadpis": item.title,
            "popis": item.description,
        }

        filepaths = []
        for fp in item.filepaths:
            logging.info(f"loading file {fp}.")

            with open(fp, "rb") as f:
                resp = self.session.post(
                    "https://oblecenie.bazos.sk/upload.php", files={"file[0]": f}
                )
                resp.raise_for_status()
                filepaths.append(resp.json()[0])

        data["files[]"] = filepaths

        r = self.session.post("https://oblecenie.bazos.sk/insert.php", data=data)

        if "Inzerát bol vložený" in r.text:
            logging.info(f"Created post for `{item.title}` on bazos.")
            return True

        return False

    def spam_protection(self):
        global spam_protection_key, spam_protection_value

        if spam_protection_key and spam_protection_value:
            return spam_protection_key, spam_protection_value

        r = self.session.get("https://oblecenie.bazos.sk/pridat-inzerat.php")
        s = BeautifulSoup(r.text, features="html.parser")

        _in = s.find("form", attrs={"id": "formpridani"}).find(
            "input", attrs={"type": "hidden"}
        )
        spam_protection_key, spam_protection_value = (
            _in.attrs["name"],
            _in.attrs["value"],
        )

        return spam_protection_key, spam_protection_value

    @property
    def session(self):
        if self._session is None:
            self._session = self.get_session()
        return self._session

    def get_session(self):
        session = requests.Session()

        # load/retrieve session key
        logging.info("Needs verification. Verifying.")

        # bazos code
        bkod = self.load_bkod()
        if not bkod:
            verified_session = self.verify(session)
            c = verified_session.cookies
            bkod = c.get("bkod")
            self.save_bkod(bkod)
        else:
            logging.info("Using cached bkod token.")

        session.cookies.update({"bkod": bkod})

        # add headers
        session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",
            }
        )

        return session

    def verify(self, session):
        if not config()["phone"].startswith("0"):
            raise ValueError("'phone' var in config needs to start with 0.")

        payload = {
            "podminky": "1",
            "teloverit": config()["phone"],
            "Submit": "Odeslat",
        }
        response = session.post(
            "https://oblecenie.bazos.sk/pridat-inzerat.php", data=payload
        )

        input_index = response.text.find('name="klic" id="klic"')
        if input_index == -1:
            raise ValueError("No input for verification key. "
                             "Probably too many attempts with the phone number. "
                             "Try changing it or wait.")

        key = input("2fa mobile key: ")

        without_zero = config()["phone"][1:]
        payload = {
            "klic": key,
            "klictelefon": f"+421{without_zero}",
            "Submit": "Odeslat",
        }
        response = session.post(
            "https://oblecenie.bazos.sk/pridat-inzerat.php", data=payload
        )
        if response.text.find("Chybne zadaný mobilný kľúč") > 0:
            raise ValueError("Chybne zadaný mobilný kľúč")

        return session

    def save_bkod(self, bkod):
        d = {
            "bkod": bkod,
            "time": time.time(),
            "expiration_s": 60*60,
        }
        with open(storage_path(), "w") as f:
            f.write(json.dumps(d))

    def load_bkod(self):
        path = storage_path()
        if not os.path.exists(path):
            logging.info("no token, needs new.")
            return None

        with open(path, "r") as f:
            data = json.loads(f.read())

        if (data["time"] + data["expiration_s"]) < time.time():
            logging.info("invalid token, needs refresh.")
            os.unlink(path)
            return None

        return data["bkod"]
