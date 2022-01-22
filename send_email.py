import smtplib
import ssl
from email.message import EmailMessage

import email_config

def send_email(link, title, localization, price, area, price_per_sqm, room, rent, heat, floor):


    body = f"Ogoszenie: {title} \n" \
           f"Link: {link} \n" \
           f"Lokalizacja: {localization} \n" \
           f"Cena: {price}zl , za metr: {price_per_sqm} \n" \
           f"Powierzchnia mieszkania: {area} \n" \
           f"Ilosc pokoi: {room} \n" \
           f"Czynsz: {rent} \n" \
           f"Ogrzewanie: {heat} \n" \
           f"Pietro: {floor}"

    sender_email = email_config.sender_email
    reciver_email = email_config.reciver_email
    password = email_config.password

    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = reciver_email
    message["Subject"] = title
    message.set_content(body)

    context = ssl.create_default_context()

    print("Sending an email: ")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:  # connecting to gmail server
        server.login(sender_email, password)
        server.sendmail(sender_email, reciver_email, message.as_string())
    print("Success")

