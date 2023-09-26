import requests
from PIL import Image
import io
import os
from getnews.getDetail import getDetail
from getnews.getContents import getContents
from bs4 import BeautifulSoup
from headline import getHeadline
from mailsender.gmailsend import sendNewsLetter

## parameters:
# url: path to email
# resize : path to resize - tuple (400,400)
IMG_IDX = 1


def generatePath(imgdir=""):
    global IMG_IDX
    path = "{}.png".format(IMG_IDX)
    IMG_IDX += 1
    return os.path.join(imgdir, path), path


def imageRenderer(url, resize, imgdir=""):
    savepath, path = generatePath(imgdir)
    if not os.path.exists(os.path.join(imgdir, "no.png")):
        nopng = Image.open("no.png")
        nopng.thumbnail(resize)
        nopng.save(os.path.join(imgdir, "no.png"))

    if url == "":
        return "no.png"
    try:
        img_data = requests.get(url).content
        image = Image.open(io.BytesIO(img_data))
        image.thumbnail(resize)
        image.save(savepath)
    except Exception as e:
        return "no.png"
    return path


def makeEmailContent(items, templateDirPath, returndir="content"):
    headline, now = getHeadline()
    mainContent = ""
    dataTemplate = ""
    dataContent = ""
    MAX_CHAR = 150
    if not os.path.exists(returndir):
        os.makedirs(returndir)
    with open(os.path.join(templateDirPath, "main.html"), "r") as f:
        mainContent = f.read()

    with open(os.path.join(templateDirPath, "data.html"), "r") as f:
        dataTemplate = f.read()
        soup = BeautifulSoup(dataTemplate, "html.parser")

    for item in items:
        link = item["link"].strip()
        title = item["title"].strip()
        detail = getDetail(link)
        imgurl = detail["imgPath"]
        imgWidth = int(soup.find("img")["width"])
        imgHeight = int(soup.find("img")["height"])
        imgPath = imageRenderer(imgurl, (imgWidth, imgHeight), returndir)
        description = detail["description"]
        if len(description) > MAX_CHAR:
            description = description[:MAX_CHAR] + " ..."
        dataContent += dataTemplate.format(link=link, title=title, imgPath=imgPath, description=description)

    with open(os.path.join(returndir, "main.html"), "w", encoding="utf-8") as f:
        f.write(mainContent.format(title=headline, dataContent=dataContent).replace("{{", "{").replace("}}", "}"))

    return True


def renderMailNews(items, to_mail):
    contentDir = "content"
    makeEmailContent(items, "mailtemplate", contentDir)
    # sendNewsLetter(from_mail='newsletter.oe@gmail.com',to_mail='anthd663@gmail.com',subject='메일 테스트',contentDirPath=contentDir)


if __name__ == "__main__":
    items = getContents()
    makeEmailContent(items, "mailtemplate", "content")
