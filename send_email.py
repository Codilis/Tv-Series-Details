import smtplib
import configparser

#Mailing Function
class Email:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.cfg')
        self.sender = config.get('MOVIES', 'EMAIL')
        self.password = config.get('MOVIES', 'PASSWORD')
    def send(self, receiver, message): 
      #Please add the email address by which you want to send the mail
      msg = "\r\n".join([
          "From: your_email_address",
          "To:"+receiver,
          "Subject: TV Series",
          "",
          message
          ])
      #Please add the password of your email address
      server = smtplib.SMTP('smtp.gmail.com:587')
      server.ehlo()
      server.starttls()
      server.login(self.sender,self.password)
      server.sendmail(self.sender, receiver, msg)
      print("email sent")
      server.quit()
