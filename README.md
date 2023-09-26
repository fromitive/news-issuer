## News Issuer

## 📌 Introduce
[news-crawler](https://www.github.com/fromitive/news-crawler)에서 생성한 크롤링 결과 값 중 선택한 뉴스를 뉴스레터로 전달 할 수 있는 GitLab용 시스템 입니다.

## 📅 Development period
2021.02 ~ 2022.08

## ✨ Features
- Outlook 이미지 잘림 없는 Newsletter 전달
- [Google Gmail API](https://console.cloud.google.com/apis/api/gmail.googleapis.com)를 이용한 뉴스 전달로, 메일 시스템의 스팸 메일함 우회

---

## 👨‍🔧 install

### 1. requirements 설치

``` bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate

# 일반 사용
pip install -r requirements/prod.txt

# 개발 및 기여용
pip install -r requirements/dev.txt
```

### 2. Gitlab CI/CD 설정

Settings > CI/CD > Varialbes 항목에 아래의 변수를 등록합니다.

| 변수명 | 설명 |
| ---      | ---      |
| TOKEN | `mailbuild.py` 에서 사용하는 google API 키 `3. Google Gmail API 등록 참고`|
| MAIL_USER | 메일을 보낼 대상 설정 |

---

### 3. Google Gmail API 등록

메일 전달을 위해 [Google Gmail API](https://console.cloud.google.com/apis/api/gmail.googleapis.com)를 등록해야 합니다.

#### 3-1. 새 프로젝트 생성

Google에 로그인 후 프로젝트를 생성합니다.

#### 3-2. Google Gmail API credentials.json 생성
프로젝트 생성 후 [Google Gmail API](https://console.cloud.google.com/apis/api/gmail.googleapis.com)에 접속합니다.

좌측의 사용자 인증 정보를 클릭한 후, 사용자 인증 정보 만들기 > OAuth 클라이언트 ID 를 클릭합니다.

애플리케이션 유형을 `데스크톱 앱`을 선택한 후 생성합니다.

`OAuth 2.0 클라이언트 ID` 항목에서 생성한 OAuth 클라이언트 오른쪽에 `작업` 에서 다운로드 버튼(아래 화살표 ⬇)을 클릭 한 후, `JSON 다운로드`를 클릭합니다.

다운로드한 파일 `client_secret.****`의 이름을 `credentials.json`로 변경한 후 clone한 프로젝트 폴더(보통 `news-issuer`)에 올려 놓습니다.

#### 3-3. 테스트 계정 등록

[Google Gmail API](https://console.cloud.google.com/apis/api/gmail.googleapis.com)에 접속한 후 좌측에 `OAuth 동의 화면` 메뉴를 클릭합니다.

`테스트 사용자`란에 메일을 보내고자 하는 gmail 주소를 `+ADD USERS`로 추가합니다.

#### 3-4. 메일 송부 토큰 생성

**참고: 메일 송부 토큰은 테스트 앱이므로 일주일에 한 번씩 초기화가 됩니다.**

아래와 같은 명령어를 실행하면 `Google 로그인 창`이 나타나게 됩니다.

```bash
python generate_token.py 
```

등록한 테스트 계정으로 로그인 하여, 어플리케이션 사용을 위한 token을 생성합니다.

`token.json` 파일이 생성하게 되며 파일의 내용을 gitlab ci/cd 의 `TOKEN` 변수로 갱신합니다.

### 4. Gitlab 뉴스레터 서버 설정

#### 4-1. `/etc/gitlab/gitlab.rb`에 옵션을 추가합니다.
``` bash
pages_nginx['custom_gitlab_server_config'] = "location /news/send-news\n{ proxy_pass http://127.0.0.1:8888; \n}"
```

#### 4-2. gitlab-ctl로 gitlab을 다시 설정합니다.

``` bash
gitlab-ctl reconfigure
gitlab-ctl start
```

### 5. 뉴스를 받는 서버 설치

#### 5-1. news-crawler 에서 선택된 뉴스를 받는 서버를 설치합니다.

``` bash
cd news-server
npm install -g forever
npm install express
```

---


## 🔎 How to Use

1. forever로 웹 서버 실행합니다.
``` bash
forever news-server/app.js
```

2. 파일이 변할 때, commit 하는 fileobserver.py를 백그라운드로 실행합니다.
``` bash
nohup python fileobserver.py &
```


