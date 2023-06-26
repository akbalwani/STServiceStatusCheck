import smtplib, ssl, email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


smtp_server = "spdnsrl01.cdle.ext"
port = 25
username = "guest"

sender_email = "somemail@mail.com"
receiver_email = "arpitbalwani.ab@gmail.com"

def send_mail(recvd_email, services):


#Create MIMEMultipart object
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "WARN - Service Not Running !!"
    msg["From"] = "ST-customer-Alert@state.co.us"
    msg["To"] = recvd_email
    filename = "services.txt"


#HTML Message Part
    html = f"""\
<html>
  <body>
    <p><b>One or more ST service is affected,check the file for more details</b>
    <br>
    {services}
    </p>
  </body>
</html>
"""

#attaching html part
    part = MIMEText(html, "html")
    msg.attach(part)
# #add attachment --Not using attachements right now
#     with open(filename, "rb") as attachment:
#         part = MIMEBase("application", "octet-stream")
#         part.set_payload(attachment.read())

#     encoders.encode_base64(part)

# # Set mail headers
#     part.add_header(
#     "Content-Disposition",
#     "attachment", filename= filename
#     )
# msg.attach(part)

# Create non-secure SMTP connection and send email
    # context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        
        server.sendmail(
        sender_email, recvd_email, msg.as_string()
    )
        server.quit() 




#ToTest

# if __name__ == '__main__':
#     # message=['a','b']
#     # send_mail(receiver_email, message)