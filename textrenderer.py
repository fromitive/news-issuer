from mybitlyapi import get_shorten
from headline import getHeadline
import datetime


def renderTextNews(items):
    (headline, now) = getHeadline()
    with open("{}.txt".format(now), "w", encoding="utf-8") as f:
        f.write(headline)
        f.write("\n")
        f.write("=================\n\n")
        for item in items:
            print(item["link"].strip())
            #if "[네이버" not in item["title"]:
                # link = get_shorten(item["link"].strip())
            #else:
            link = item["link"]
            news = "{}\n - {}\n\n".format(item["title"].strip(), link.strip())
            f.write(news)
        f.write("\n")
        f.write("=================")
