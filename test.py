# import all necessary components
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

smtp_host = 'smtp.gmail.com'
smtp_port = 587
username = 'jliudadao@gmail.com'
password = 'tpww hafr dycf xxqh'


sender_email = "jliudadao@gmail.com"
receiver_email = "liujinguccello@gmail.com"
message = MIMEMultipart("alternative")
message["Subject"] = "CID image test"
message["From"] = sender_email
message["To"] = receiver_email

# write the HTML part
html = """\
<html>
<body>
  <img src="cid:Mailtrapimage">
</body>
</html>
"""

part = MIMEText(html, "html")
message.attach(part)

# We assume that the image file is in the same directory that you run your Python script from
fp = open('DaDao-Logo_withWord.jpg', 'rb')
image = MIMEImage(fp.read())
fp.close()

# Specify the  ID according to the img src in the HTML part
image.add_header('Content-ID', '<Mailtrapimage>')
message.attach(image)

# send your email
with smtplib.SMTP_SSL(smtp_host, 465) as server:
    server.login(username, password)
    server.ehlo()
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
print('Sent')