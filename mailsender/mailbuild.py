# -*- coding:utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from email.utils import formataddr
from email.iterators import _structure
from datetime import datetime
from bs4 import BeautifulSoup
import copy
import sys
import zipfile
import base64
import os


class MailBuilder:
    enableAttach = False
    enableImage = False

    RootMsg = None
    RelMsg = None

    strMailContent = None
    ImgContents = []
    _imgcontNumber = 0

    lstUserList = []
    URL = ""

    def __init__(self, fromUser, fromID, subject):
        self.fromID = fromID
        self._imgcontNumber = 0
        self.RootMsg = MIMEMultipart()
        self.RootMsg["From"] = formataddr((Header(fromUser, "utf-8").encode(), fromID))
        self.RootMsg["Subject"] = Header(s=subject, charset="utf-8")
        self.RootMsg
        self.RelMsg = MIMEMultipart("related")
        # self.MainMsg.set_payload()
        # print(self.MainMsg.get_payload())

    def _generateCid(self):
        signature = "MOOSONG{:03d}".format(self._imgcontNumber)
        self._imgcontNumber += 1
        htmlCid = "cid:{signature}".format(signature=signature)
        attachCid = "<{signature}>".format(signature=signature)
        return htmlCid, attachCid

    def setContent(self, contentsDir):
        with open(os.path.join(contentsDir, "main.html"), "r", encoding="utf-8") as fcontent:
            content = fcontent.read()
            soup = BeautifulSoup(content, features="html.parser")
            imgTags = soup.select("img")
            # set image cid
            for img in imgTags:
                srcBefore = img.attrs["src"]
                htmlCid, attachCid = self._generateCid()

                img.attrs["src"] = htmlCid
                with open(os.path.join(contentsDir, srcBefore), "rb") as fimgContent:
                    imgContent = fimgContent.read()
                    imgAttach = MIMEImage(imgContent)
                    imgAttach.add_header("Content-ID", attachCid)
                    self.ImgContents.append(imgAttach)
            self.strMailContent = str(soup)

    def getContent(self, user, saveAsFile=False):
        # 깊은 복사
        RootMsg = copy.deepcopy(self.RootMsg)
        RelMsg = copy.deepcopy(self.RelMsg)
        RootMsg["To"] = user
        content = self.strMailContent
        MainMsg = MIMEMultipart("alternative")
        TextMsg = MIMEText("security news letter", "plain", "utf-8")
        HtmlMsg = MIMEText(content, "html", "utf-8")
        MainMsg.attach(TextMsg)
        MainMsg.attach(HtmlMsg)
        RelMsg.attach(MainMsg)
        for ImgContent in self.ImgContents:
            RelMsg.attach(ImgContent)
        RootMsg.attach(RelMsg)
        if saveAsFile:
            with open("output.msg", "wb") as f:
                f.write(bytes(RootMsg))
        return RootMsg
