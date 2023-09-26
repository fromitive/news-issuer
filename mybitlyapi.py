import requests
import json

apikey = None

with open("apikey.txt", "r", encoding="utf-8") as f:
    apikey = f.read()
    apikey = apikey.strip()


def get_shorten(url):
    post_url = "https://api-ssl.bitly.com/v3/shorten?access_token={token}&longUrl={url}".format(token=apikey, url=url)
    try:
        res = requests.get(post_url)

        if res.status_code == 200:
            return res.json().get("data").get("url")
        else:
            return url
    except Exception as e:
        print("error occur:", e)
        return url
