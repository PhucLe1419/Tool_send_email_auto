import smtplib
import requests
from bs4 import BeautifulSoup
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders

# class MailService:
#     def __init__(self):
#         self.email_sender = ''
#         self.email_password = ''
#         self.email_receiver = ["", ""]
#
#     def send_email(self):
#         email_msg = EmailMessage()
#         email_msg["subject"] = "thieu test end email"
#         email_msg["From"] = self.email_sender
#         email_msg["To"] = self.email_receiver
#         email_msg.set_content("put the content of the email here")
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
#             smtp.login(self.email_sender, self.email_password)
#             smtp.send_message(email_msg)
#
#     def get_data_posts(self):
#         response = requests.get("https://tuoitre.vn/tin-moi-nhat.htm")
#         soup = BeautifulSoup(response.content, "html.parser")
#         titles = soup.findAll('h3', class_='box-title-text')
#         links = [link.find('a').attrs["href"] for link in titles]
#         for link in links:
#             news = requests.get("https://tuoitre.vn" + link)
#             soup = BeautifulSoup(news.content, "html.parser")
#             title = soup.find("h1", class_="article-title").text
#             # abstract = soup.find("h2", class_="sapo").text
#             body = soup.find("div", id="main-detail-body")
#             image = body.find("img").attrs["src"]
#             print("Tiêu đề: " + title)
#             # print("Mô tả: " + abstract)
#             # print("Nội dung: " + content)
#             # print("Ảnh minh họa: " + image)


def send_email(url, base_url, user_send, pass_word, user_rec):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    titles = soup.findAll('h3', class_='box-title-text')
    links = [link.find('a').attrs["href"] for link in titles][:2]
    filename = "hello.xlsx"
    # print(links)
    for link in links:
        news = requests.get(base_url + link)
        soup = BeautifulSoup(news.content, "html.parser")
        title = soup.find("h1", class_="article-title").text
        contents = soup.find("div", class_="detail-cmain").text
        contents = str(contents)

        email_sender = user_send
        email_password = pass_word
        email_receiver = [user_rec]
        email_msg = EmailMessage()
        email_msg["subject"] = title
        email_msg["From"] = email_sender
        email_msg["To"] = email_receiver
        email_msg.set_content(contents)
        email_msg.add_attachment(filename)

        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {filename}")
        email_msg.attach(part)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_sender, email_password)
            smtp.send_message( email_msg)

send_email(url, base_url, user_send, pass_word, user_rec)

