import requests
from requests.utils import dict_from_cookiejar

from collections import defaultdict

from pyquery import PyQuery as pq


def main():
    url = load_config("urls.txt")
    creds = load_config("creds.txt")
    settings = load_config("settings.conf")

    cookies = get_cookies(url.get("login"), creds)
    assert cookies != None
    html_body = get_info(url.get("telefonija"), cookies, {
        'group': settings["group"],
        'handler': settings["handler"],
        'number_selector': settings["number_selector"]
    })
    assert html_body != None
    print(html_body)
    d = pq(html_body)
    info = d('input').val()
    print(info)
    # print(get_info(url.get("telefonija"),headers))


def load_config(filename: str) -> dict:
    """Load config from text file to dictionary. Originaly meant for http headers."""
    config = {}
    with open(filename, "r") as f:
        for line in f:
            if not line.strip() or ":" not in line:
                continue
            key, value = line.split(":", 1)
            config[key.strip()] = value.strip()
    return config


def get_cookies(url: str, data: dict) -> dict:
    """send username and password forms and return cookies"""
    r = requests.post(url, data=data)
    cookies = dict_from_cookiejar(r.cookies)
    if r.status_code == 200:
        return cookies
    return None


def get_info(url: str, headers: dict, data: dict) -> str:
    """provide PHPSESSID header and return body"""
    print(data)
    r = requests.post(url, headers=headers, data=data) # TODO: parse html
    if r.status_code == 200:
        return r.content
    return None


if __name__ == "__main__":
    main()
