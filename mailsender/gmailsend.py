from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import base64
from mailsender import mailbuild


## Oauth에 사용 가능한 메일을 등록해야 한다
##https://developers.google.com/gmail/api/quickstart/python#trouble
## API 및 서비스 --> OAuth 동의화면
# If modifying these scopes, delete the file token.json.

SCOPES = ["https://mail.google.com/"]
## token.json을 생성하는 스크립트
## oauth 인증에 성공하면, token.json을 생성하고, 최초 인증 뒤로는, 인증하지 않는다.


def get_creds():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        return creds
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
            return creds


## Send message 하는 함수
## SMTP 쓰는것처럼 사용 가능한가보다 테스트해봐야함
def gmail_send_message(creds, content):
    """Create and send an email message
    Print the returned  message id
    Returns: Message object, including message id

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    try:
        service = build("gmail", "v1", credentials=creds)
        # encoded message
        encoded_message = base64.urlsafe_b64encode(content.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        # pylint: disable=E1101
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        print(f'Message Id: {send_message["id"]}')

    except HttpError as error:
        print(f"An error occurred: {error}")
        send_message = None
    return send_message


## 실제로 내 메일 주소로 메일을 전송한다.


def sendNewsLetter(from_mail, to_mail, subject, contentDirPath="content"):
    creds = get_creds()  # 크리덴셜 생성 및 로드
    fromUser = "보안뉴스레터"  # 보내는사람 이름
    MB = mailbuild.MailBuilder(fromUser, from_mail, subject)  # 메일 빌더 서정
    MB.setContent(contentDirPath)  # 메일 템플릿 컨텐츠 폴더이름 넣기 보낼 html 파일 본문은 **반드시 main.html** 이어야 함
    content = MB.getContent(to_mail, saveAsFile=True)  # 보내고자 하는 대상지정
    gmail_send_message(creds, content)  # 메세지 전송
