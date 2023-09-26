# -*- coding: utf-8 -*-
from getnews.getContents import getContents
from htmlrenderer import renderHTMLNews
from textrenderer import renderTextNews
from mailrenderer import makeEmailContent, sendNewsLetter
from headline import getHeadline

headline, now = getHeadline()
items = getContents()
renderHTMLNews(items)
renderTextNews(items)

### send email
contentDir = "content"
makeEmailContent(items, "mailtemplate", contentDir)
with open("send_to.txt", "r") as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]
    for line in lines:
        sendNewsLetter(
            from_mail="fromitive.secu@gmail.com",
            to_mail=line,
            subject="[보안 뉴스레터] " + headline,
            contentDirPath=contentDir,
        )
