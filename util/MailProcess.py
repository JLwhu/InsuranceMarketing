import email
import imaplib
import smtplib
import time
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from itertools import chain
import re

import pygame
from PyQt6.QtCore import pyqtSignal, QObject

from log.logger import Logger

FORWARD_ADD1 = "jiaousa@gmail.com"
FORWARD_ADD2 = "jliudadao@gmail.com"
FORWARD_ADD3 = "dadaoservice@gmail.com"
class MailProcess(QObject):
    progress_signal = pyqtSignal(str)

    def readNewEmail_IMAP(self, imap_host, smtp_host, username, password, subject_string):
        def search_string(uid_max, criteria):
            c = list(map(lambda t: (t[0], '"' + str(t[1]) + '"'), criteria.items())) + [('UID', '%d:*' % (uid_max + 1))]
            return '(%s)' % ' '.join(chain(*c))

        mail = imaplib.IMAP4_SSL(imap_host)
        mail.login(username, password)
        # select the folder
        mail.select('inbox')

        criteria = {}
        uid_max = 0
        result, data = mail.uid('SEARCH', None, search_string(uid_max, criteria))
        uids = [int(s) for s in data[0].split()]
        if uids:
            uid_max = max(uids)
            # Initialize `uid_max`. Any UID less than or equal to `uid_max` will be ignored subsequently.
        # Logout before running the while loop
        print(uid_max)
        mail.logout()
        while 1:
            # for x in range(6):
            mail = imaplib.IMAP4_SSL(imap_host)
            mail.login(username, password)
            mail.select('inbox')
            result, data = mail.uid('search', None, search_string(uid_max, criteria))
            uids = [int(s) for s in data[0].split()]

            for uid in uids:
                # Have to check again because Gmail sometimes does not obey UID criterion.
                if uid > uid_max:
                    result, data = mail.uid('fetch', str(uid), '(RFC822)')
                    for response_part in data:
                        if isinstance(response_part, tuple):
                            # message_from_string can also be use here
                            msg = email.message_from_bytes(response_part[1])
                            msg_subject = msg['subject']
                            if subject_string in msg_subject:
                                print('To:', msg['to'])
                                print('From:', msg['from'])
                                print('Subject:', msg['subject'])
                                self.progress_signal.emit('Date:'+msg['date']+"\r\n"+'To:'+msg['to']+"\r\n"+'From:'+msg['from']+"\r\n"+'Subject:'+msg['subject'])

                                msg.replace_header("From", username)


                                # open authenticated SMTP connection and send message with
                                # specified envelope from and to addresses

                                #self.progress_signal.emit("转发邮件"+FORWARD_ADD1+"......")
                                smtp_port = 465
                                #smtp = smtplib.SMTP(smtp_host, smtp_port)
                                smtp = smtplib.SMTP_SSL(smtp_host, smtp_port)
                                smtp.ehlo()
                                #smtp.starttls()
                                #self.progress_signal.emit("转发邮件" + username + password + "......")
                                smtp.login(username, password)
                                msg.replace_header("To", FORWARD_ADD1)
                                smtp.sendmail(username, FORWARD_ADD1, msg.as_string())
                                print("转发邮件"+FORWARD_ADD1+"......")
                                Logger.getInstance().info(f"转发邮件{FORWARD_ADD1}......")
                                self.progress_signal.emit("转发邮件"+FORWARD_ADD1+"......")
                                msg.replace_header("To", FORWARD_ADD2)
                                smtp.sendmail(username, FORWARD_ADD2, msg.as_string())
                                self.progress_signal.emit("转发邮件"+FORWARD_ADD2+"......")
                                print("转发邮件"+FORWARD_ADD2+"......")
                                Logger.getInstance().info(f"转发邮件{FORWARD_ADD2}......")
                                msg.replace_header("To", FORWARD_ADD3)
                                smtp.sendmail(username, FORWARD_ADD3, msg.as_string())
                                self.progress_signal.emit("转发邮件"+FORWARD_ADD3+"......")
                                print("转发邮件"+FORWARD_ADD3+"......"+"\r\n")
                                Logger.getInstance().info(f"转发邮件{FORWARD_ADD3}......")
                                smtp.quit()

                                # for playing note.wav file
                                pygame.init()
                                my_sound = pygame.mixer.Sound("../file_example_WAV_1MG.wav")
                                print('playing sound using  playsound')
                                my_sound.play()
                                # print(email.message_from_bytes(response_part[1])) #processing the email here for whatever
                            # print(email.message_from_bytes(response_part[1]))  # processing the email here for whatever
                    uid_max = uid
            mail.logout()
            time.sleep(1)

    def sendEmail_SMTP(self, smtphost, port, username, password, sent_from, sent_to, email_text):
        try:
            server = smtplib.SMTP_SSL(smtphost, port)
            server.ehlo()
            server.login(username, password)
            server.sendmail(sent_from, sent_to, email_text)
            server.close()

            print('Email sent!')
        except Exception as exception:
            print("Error: %s!\n\n" % exception)


    def sendHTMLEmail_SMTP(self, smtphost, port, username, password, name, email,subject, email_html):
        try:
            server = smtplib.SMTP_SSL(smtphost, port)
            server.ehlo()
            server.login(username, password)

            sender_email = username
            receiver_email = email
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = sender_email
            message["To"] = receiver_email

            html = email_html

            # import module
            from bs4 import BeautifulSoup

            # assign URL
            s = BeautifulSoup(html, "html.parser")
            # insert tag
            tag = s.new_tag("b")
            tag.string = "Dear " + name +",\r\n\r\nHi!\r\n"

            s.p.string.insert_before(tag)
            html = str(s)
            part = MIMEText(html, "html")
            message.attach(part)


            #email_text  = "Dear " + name + email_maintext

            server.sendmail(username, email, message.as_string())

            server.close()

        except Exception as exception:
            Logger.getInstance().error("Error: %s!\n\n" % exception)
            print("Error: %s!\n\n" % exception)

    def sendHTMLToAllEmail_SMTP(self, smtphost, port, username, password, email_list, colname_list, multiColVal_list, subject,  email_html):
        try:
            if len(multiColVal_list) == 0:
                return

            server = smtplib.SMTP_SSL(smtphost, port)
            server.ehlo()
            server.login(username, password)


            sender_email = username


            client_no = len(multiColVal_list[0])
            for i in range(client_no):
                email_text = email_html
                if (email_list[i] is None) or (not isinstance(email_list[i], str)):
                    continue
                j = 0
                for colname in colname_list:
                    colval = str(multiColVal_list[j][i])
                    email_text = re.sub('@'+colname+'@', colval, email_text)
                    j += 1
                receiver_email = email_list[i]
                message = MIMEMultipart("alternative")
                message["Subject"] = subject
                message["From"] = sender_email
                message["To"] = receiver_email

                part = MIMEText(email_text, "html")
                message.attach(part)

                server.sendmail(username, receiver_email, message.as_string())
                print("send email to " + email_list[i] + "successfully! \r\n")
            server.close()

        except Exception as exception:
            Logger.getInstance().error("Error: %s!\n\n" % exception)
            print("Error: %s!\n\n" % exception)
# # =============================================================================
# # SET EMAIL LOGIN REQUIREMENTS
# # =============================================================================
# gmail_user = 'jliudadao@gmail.com'
# gmail_app_password = 'tpww hafr dycf xxqh'
# #gmail_user = 'info@dadaosolutions.com'
# #gmail_app_password = 'Leon030303!'
#
# # =============================================================================
# # SET THE INFO ABOUT THE SAID EMAIL
# # =============================================================================
# sent_from = gmail_user
# sent_to = ['jingathot@hotmail.com', 'liujinguccello@gmail.com']
# sent_subject = "Hey Friends!"
# sent_body = ("Hey, what's up? friend!\n\n"
#              "I hope you have been well!\n"
#              "\n"
#              "Cheers,\n"
#              "Jay\n")
#
# email_text = """\
# From: %s
# To: %s
# Subject: %s
#
# %s
# """ % (sent_from, ", ".join(sent_to), sent_subject, sent_body)
#
#
# smtpHost = 'secure320.inmotionhosting.com'
# port = 465
# # server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#
# # =============================================================================
# # SEND EMAIL OR DIE TRYING!!!
# # Details: http://www.samlogic.net/articles/smtp-commands-reference.htm
# # =============================================================================
# #sendEmail_SMTP(smtpHost, port, gmail_user, gmail_app_password, sent_from, sent_to, email_text)
# imap_ssl_host = 'secure320.inmotionhosting.com'
# imap_ssl_port = 993
# username = 'info@dadaosolutions.com'
# password = 'Leon030303!'
# subject_string = 'New Prospect Quote Notification'
#
# mp = MailProcess()
# mp.readNewEmail_IMAP(imap_ssl_host, username, password, subject_string)