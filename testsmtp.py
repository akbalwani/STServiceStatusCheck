import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


#USE YOUR GMAIL CREDS--NOT RECOMMENDED FOR PROD/SOC USE
password = 'agouvjabhqjoxfxh'
email="arpit.balwani@state.co.us"

# smtp_server = "smtp.gmail.com"
# port = 587  # For starttls

smtp_server = "spdnsrl01.cdle.ext"
port = 25
username = "guest"

sender_email = "my@gmail.com"
receiver_email = "arpit.balwani@state.co.us"
message = """\
Subject: Hi there

This message is sent from Python using the function."""

# Create a secure SSL context
context = ssl.create_default_context()

# Try to log in to server and send email

def send_email(receiver_email, message):
    try:

        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        # server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        # server.login(username, password)
        server.sendmail(email, receiver_email, message)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit() 

    

if __name__ == '__main__':
    send_email(receiver_email, message)