import smtplib, ssl
from alarm_sending import compare2csv
from alarm_sending import switch_Emails
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders



def read_creds():
    user = passw = ""
    with open("credentials.txt", "r") as f:
        file = f.readlines()
        user = file[0].strip()
        passw = file[1].strip()
    return user, passw
def send(file, datei, domain):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email, password = read_creds()
    reciever_email, name = compare2csv(domain)
    print(f'Gesendet an {reciever_email}')
    message = MIMEMultipart() 
    message['From'] = sender_email
    message['To'] = reciever_email
    message['Subject'] = f"Rank für folgende {domain}"
    body = f"""Hallo {name},
                
wir haben deine Domain mit bestimmten Keywords und Ortschaften
untersucht. Im Anhang findest Du die CSV mit der Analyse.

VG Cätä & Herby
            """
    message.attach(MIMEText(body, 'plain'))
    filename = file
    attachment = open(filename, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % datei)
    message.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender_email, password)
    text = message.as_string()
    s.sendmail(sender_email, reciever_email, text)
    s.quit() 