import mimetypes
import os
import smtplib
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from archive import make_archive


def attach_file(msg, f):
    attach_types = {'text': MIMEText,
                    'image': MIMEImage,
                    'audio': MIMEAudio}
    filename = os.path.basename(f)
    ctype, encoding = mimetypes.guess_type(f)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    with open(f, 'rb' if maintype != 'text' else 'r') as fp:
        if maintype in attach_types:
            file = attach_types[maintype](fp.read(), _subtype=subtype)
        else:
            file = MIMEBase(maintype, subtype)
            file.set_payload(fp.read())
            encoders.encode_base64(file)
    file.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(file)


def process_attachments(msg, attachments):
    for f in attachments:
        if os.path.isfile(f):
            attach_file(msg, f)
        elif os.path.exists(f):
            if f == '.':
                f = os.getcwd()
            filename = '%s.zip' % f
            created = make_archive(f, os.getcwd(), filename)
            if not created:
                continue
            attach_file(msg, filename)
            os.remove(filename)


def send_mail(email, subject, text, attachments):
    try:
        addr_from = os.getenv('FROM')
        password = os.getenv('PASSWORD')

        msg = MIMEMultipart()
        msg['From'] = addr_from
        msg['To'] = email
        msg['Subject'] = subject

        body = text
        msg.attach(MIMEText(body, 'plain'))

        process_attachments(msg, attachments)

        server = smtplib.SMTP_SSL(os.getenv('HOST'), os.getenv('PORT'))
        server.login(addr_from, password)

        server.send_message(msg)
        server.quit()
        return True
    except smtplib.SMTPException:
        return False


if __name__ == '__main__':
    process_attachments({}, '.')