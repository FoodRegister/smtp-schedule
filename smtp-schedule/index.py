
import time
from aiosmtpd.controller import Controller
import settings
import asyncore
import threading
import smtplib

'''
Mail Forwarder
'''

class MailForwarder():
    def __init__(self, *args, **kwargs):
        pass
    def ready(self, *args, **kwargs):
        return 0 ## Return ready time
    def forward(self, mail, *args, **kwargs):
        print(mail)

class ToSMTPForwarder(MailForwarder):
    def __init__(self, timebetween=0, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ADDRESS = args[0]
        self.PASSWORD = args[1]
        self.SMTP_SERVER = args[2]
        self.SMTP_SERVER_PORT = args[3]
        self.WAIT_TIME = timebetween

        self.READY = 0
    def ready(self, *args, **kwargs):
        return self.READY
    def forward(self, mail, *args, **kwargs):
        self.READY = time.time() + self.WAIT_TIME

        with smtplib.SMTP_SSL(self.SMTP_SERVER, self.SMTP_SERVER_PORT) as smtp:
            smtp.login(self.ADDRESS, self.PASSWORD)
            smtp.sendmail(mail.mail_from, mail.rcpt_tos, mail.content)

mails = []
mail_idx = 0
working = False

class MailThread(threading.Thread):
    def run(self) -> None:
        global mails
        global mail_idx
        global working

        while True:
            while working:
                time.sleep(0.001)

            working = True
            handler_found = None

            if mail_idx != len(mails):
                cur_mail = mails[mail_idx]
                for handler in settings.FORWARDERS:
                    if handler.ready() < time.time():
                        handler_found = handler
                        break

            working = False

            if handler_found != None:
                handler_found.forward(cur_mail)
                mail_idx += 1
                pass
            else:
                time.sleep(0.5)


class MailHandler:
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        global mails
        global mail_idx
        global working

        if len(mails) == mail_idx:
            while working:
                time.sleep(0.001)
            
            working = True
            mail_idx = 0
            mails = []
            working = False

        mails.append(envelope)
        return '250 Message accepted for deliver'

def main():
    foo = Controller(MailHandler())
    foo.start()

    mail_thread = MailThread()
    mail_thread.start()

    while True:
        pass

if __name__ == "__main__": main()
