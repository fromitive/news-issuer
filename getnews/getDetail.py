import requests
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import re


def getDetail(newslink):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    try:
        req = requests.get(newslink, headers=headers, timeout=20)
        req.raise_for_status()
        http_encoding = req.encoding if "charset" in req.headers.get("content-type", "").lower() else None
        html_encoding = EncodingDetector.find_declared_encoding(req.content, is_html=True)
        encoding = http_encoding or html_encoding
        encoding = encoding.upper()
        req.encoding = encoding
        soup = BeautifulSoup(req.text, "html.parser", from_encoding=encoding)
    except Exception as e:
        print("not found..", e)
        pass
    content = {"description": "", "imgPath": "", "title": "", "link": ""}
    # description
    try:
        description = soup.find("meta", property="og:description").get("content").strip()
        imgPath = soup.find("meta", property="og:image").get("content")
        title = soup.find("meta", property="og:title").get("content")
        link = soup.find("meta", property="og:url").get("content")
        content["description"] = description
        content["imgPath"] = imgPath
        content["title"] = title
        content["link"] = link
    except Exception as e:
        print("no description!", e)
        pass

    return content
