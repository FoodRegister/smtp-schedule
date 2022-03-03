
from index import ToSMTPForwarder, MailForwarder

EMAIL_SMTP_PORT = 8025
EMAIL_SMTP_ADDR = 'localhost'

FORWARDERS = [
    ToSMTPForwarder(
        15, ## Time between
        'feedback.foodregister@gmail.com', ## EMail
        '', ## Password
        'smtp.gmail.com', 
        465)
]

