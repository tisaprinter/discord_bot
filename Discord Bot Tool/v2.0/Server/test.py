import smtplib

gmail_user = 'nicholasmittelstadt@gmail.com'
gmail_password = 'P@ssword!'

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(gmail_user, gmail_password)
