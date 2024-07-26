from requests import session, post
import schedule
import time
from configparser import ConfigParser


WORDPRESS_URL = "https://fsr.physik.uni-goettingen.de"
DEEPL_URL = "https://api-free.deepl.com/v2/translate"


def read_config():
    global UPDATE_TIME, WORDPRESS_USERNAME, WORDPRESS_PASSWORD, STUDIP_USERNAME, STUDIP_PASSWORD, DEEPL_AUTH_KEY

    config = ConfigParser()
    config.read("config.ini")

    UPDATE_TIME = config["Allgemein"]["uhrzeit"]

    WORDPRESS_USERNAME = config["Wordpress"]["benutzername"]
    WORDPRESS_PASSWORD = config["Wordpress"]["passwort"]

    STUDIP_USERNAME = config["Stud.IP"]["benutzername"]
    STUDIP_PASSWORD = config["Stud.IP"]["passwort"]

    DEEPL_AUTH_KEY = config["DeepL"]["auth_key"]


def getFSRAgenda():
    with session() as s:
        payload = {
            "loginname": STUDIP_USERNAME,
            "password": STUDIP_PASSWORD,
            "security_token": "",
            "login_ticket": "",
            "resolution": "1280x800",
            "device_pixel_ratio": "2",
            "Login":""
        }
        header = {"User-Agent": "Safari/537.36"}

        response = s.get("https://studip.uni-goettingen.de")
        text = response.text

        # Extract security token
        security_token = text[text.find("name=\"security_token\""):]
        security_token = security_token[security_token.find("value") + 7:security_token.find(">") - 1]
        payload["security_token"] = security_token

        # Extract login ticket
        login_ticket = text[text.find("name=\"login_ticket\""):]
        login_ticket = login_ticket[login_ticket.find("value") + 7:login_ticket.find(">") - 1]
        payload["login_ticket"] = login_ticket

        response = s.post("https://studip.uni-goettingen.de", data=payload, headers=header)
        response = s.get("https://studip.uni-goettingen.de/wiki.php?cid=9bbe4ecf9f97f37bf3b2005d36f44c5b&wiki_comments=icon&keyword=SitzungFSR")

    agenda = response.text[response.text.find("<ol>"):response.text.find("<h2>", response.text.find("<ol>"))]

    date = response.text[response.text.find("<h2>Tagesordnung"):]
    date = date[:date.find("</h2>")]
    date = date.split(" ")[-1]

    return agenda, date


def translate_agenda(agenda):
    tops = agenda.split("><li>")[1:]

    for (i, top) in enumerate(tops):
        tops[i] = top[:top.find("<")]

    payload = {
        "text" : tops,
        "target_lang" : "EN-US"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"DeepL-Auth-Key {DEEPL_AUTH_KEY}"
    }

    response = post(
        DEEPL_URL,
        json = payload,
        headers = headers
    )

    agenda_english = agenda

    for (i, top) in enumerate(tops):
        agenda_english = agenda_english.replace(top, response.json()["translations"][i]["text"])

    return agenda_english


def update_page(content, post_id):
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/pages/{post_id}"

    response = post(
        url,
        json = {"content": content},
        headers = {"Content-Type": "application/json"},
        auth = (WORDPRESS_USERNAME, WORDPRESS_PASSWORD),
    )

    if response.status_code == 200:
        print("Tagesordung erfolgreich geupdatet")
    else:
        print(f"Es ist ein Fehler aufgetreten. HTML Status code: {response.status_code}")
        print(response.text)

        return response.status_code

    return 0


def run():
    read_config()

    # Update german page
    agenda, date = getFSRAgenda()

    post_id = 450

    with open("page.html", "r") as file:
        content = file.read()

    content = content.format(
        Datum = date,
        TO = agenda
    )

    update_page(content, post_id)

    # Update english page
    post_id_english = 5916

    with open("page.en.html", "r") as file:
        content_english = file.read()

    content_english = content_english.format(
        Datum = date,
        TO = translate_agenda(agenda)
    )

    update_page(content_english, post_id_english);


def main():
    # Schedule and run the update
    schedule.every().day.at(UPDATE_TIME, "Europe/Berlin").do(run)

    print(f"Programm läuft, Ausführung ist geplant täglich um {UPDATE_TIME} Uhr")

    while True:
        schedule.run_pending()
        time.sleep(60)


read_config()

if __name__ == "__main__":
    main()
