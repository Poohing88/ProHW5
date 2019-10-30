import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


GMAIL_SMTP = "smtp.gmail.com"
GMAIL_IMAP = "imap.gmail.com"


class MailAgent:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.subject = 'Subject'
        self.recipients = ['vasya@email.com', 'petya@email.com']
        self.header = None

    def send_massege(self, message):
        # отправка сообщений
        self.message = message
        self.msg = MIMEMultipart()
        self.msg['From'] = self.login
        self.msg['To'] = ', '.join(self.recipients)
        self.msg['Subject'] = self.subject
        self.msg.attach(MIMEText(self.message))
        self.ms = smtplib.SMTP(GMAIL_SMTP, 587)
        # identify ourselves to smtp gmail client. идентифицировать себя для клиента SMTP Gmail
        self.ms.ehlo()
        # secure our email with tls encryption. защитить нашу электронную почту с помощью шифрования TLS
        self.ms.starttls()
        # re-identify ourselves as an encrypted connection. повторно идентифицировать себя как зашифрованное соединение
        self.ms.ehlo()
        self.ms.login(self.login, self.password)
        self.ms.sendmail(self.login, self.ms, self.msg.as_string())
        self.ms.quit()
        #send end. отправка закончена

    def receive_massege(self):
        self.mail = imaplib.IMAP4_SSL(GMAIL_IMAP)
        self.mail.login(self.login, self.password)
        self.mail.list()
        self.mail.select("inbox")
        criterion = '(HEADER Subject "%s")' % self.header if self.header else 'ALL'
        result, data = self.mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = self.mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        self.mail.logout()
        return email_message


if __name__ == '__main__':
    login = 'login@gmail.com'
    password = 'qwerty'
    message = 'Hello World'
    mail = MailAgent(login, password)
    mail.send_massege(message)
    inbox_message = mail.receive_massege()