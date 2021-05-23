#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Original idea :  Docstring (https://www.youtube.com/watch?v=BoGy1j8AREo)
Send mail, notification : me
"""

# Standard library import.
import sys
import smtplib
import requests
from time import sleep

# Third-part library import.
from gi.repository import Notify

# Project library import.

######################
def build_mail_hdr(from_, to_, subject_):
    """
    Build only mail header.
    """
    return{
           'from' : "From: {}".format(from_),
           'to' : "To: {}".format(', '.join(to_)),
           'subject' : "Subject: {}".format(subject_),
           'mime_ver' : "MIME-Version: 1.0",
           'content-type' : "Content-Type: text/plain; charset=UTF-8",
           'content-transfert-encoding' : "Content-Transfer-Encoding: 8bit\n",
          }

def buil_mail_to_send(mail_hdr, msg_):
    """
    BUild the message mail, witn its header.
    """
    mail_to_send = "\n".join(mail_hdr.values())
    mail_to_send += "{}\n".format(msg_)
    return mail_to_send

def send_mail(from_, to_, subject_, msg_, mail_server='localhost', port=0):
    """
    Send mail, only on localhost.
    """
    if type(to_) != list:
       raise TypeError("'to_' should be a list. Please check it.")

    mail_hdr = build_mail_hdr(from_, to_, subject_)
    mail_to_send = buil_mail_to_send(mail_hdr, msg_)

    with smtplib.SMTP(mail_server, port) as smtp:
        smtp.sendmail(from_, to_, mail_to_send.encode('utf-8'))

def find_some_place(dep):
    """
        ex: https://vitemadose.gitlab.io/vitemadose/69.json
    """
    found = []

    api_url = 'https://vitemadose.gitlab.io/vitemadose/{}.json'.format(dep)
    resp = requests.get(api_url)

    available_centers = resp.json().get('centres_disponibles', [])

    for available_center in available_centers:
        appointment_schedules = available_center.get('appointment_schedules', [])
        for appointment_schedule in appointment_schedules:
            appointment_name = appointment_schedule.get('name', '')
            if appointment_name != 'chronodose':
                continue

            total_doses = appointment_schedule.get('total')
            if total_doses > 0:
                url = available_center.get('url', '')
                available_rdv = appointment_schedule.get('to')
                address = available_center.get('metadata').get('address')
                found.append("{} doses le {} --> {} : {}".format(total_doses, available_rdv[:10], address, url))

    return found

def main(args):
    """
    Main function.
    @parameters : some arguments, in case of use.
    @return : 0 = all was good.
              ... = some problem occures.
    """
    dep = 00      # departement_number_2_first_digit

    Notify.init("check_dispo_vaccin.py")
    notification = Notify.Notification.new('')

    while True:
        print('Vérifiaction dispo vaccins dans le {}'.format(dep))
        found = find_some_place(dep)
        availables = "\n".join(found)

        if availables:
            print(availables)
            print("\tMail envoyé...")
            send_mail('will',
                      ['will'],
                      "Vaccins trouvés",
                      availables)
            send_mail('from_sender_mail_address',
                      ['to_1st_mail_address', ''],
                      "Vaccins trouvés",
                      availables,
                      'mail_server_provider_address',
                      123)      # 123 = means mail server provider port. Fill with yours.
            notification.update("Vaccins trouvés", availables)
            notification.show()

        sleep(10 * 60)

    return 0

######################

if __name__ == "__main__":
    rc = main(sys.argv[1:])      # Keep only the argus after the script name.
    sys.exit(rc)

