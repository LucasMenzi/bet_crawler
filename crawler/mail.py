# -*- coding: utf-8 -*-

import smtplib
import mimetypes
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart


def mail(emailto, filetosend, subject):
    """Send email with attachement.

    Arguments:
    emailto: list with e-mail adresses
    filetosend: path string to the csv attachment
    subject: string of the email subject
    """
    # Sender config
    emailfrom = "your email"

    # msg config
    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = ", ".join(emailto)
    msg["Subject"] = subject
    msg.preamble = subject

    # Attachement code from https://stackoverflow.com/questions/23171140/how-
    # do-i-send-an-email-with-a-csv-attachment-using-python#23171609
    if not isinstance(filetosend, list):
        ctype, encoding = mimetypes.guess_type(filetosend)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)
        if maintype == "text":
            fp = open(filetosend, encoding='utf-8')
            attachment = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "image":
            fp = open(filetosend, "rb")
            attachment = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "audio":
            fp = open(filetosend, "rb")
            attachment = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(filetosend, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment",
                              filename=filetosend)
        msg.attach(attachment)
    else:
        body = "%s" % (filetosend[0])
        msg.attach(MIMEText(body, "plain"))

    # AWS SES config: Enter your creadentials
    EMAIL_HOST = "email-smtp.server_name.amazonaws.com"
    EMAIL_HOST_USER = "user name"
    EMAIL_HOST_PASSWORD = "password"
    EMAIL_PORT = 587

    # Server config with AWS SES values
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()


"""The version number"""
__version__ = "0.1"
