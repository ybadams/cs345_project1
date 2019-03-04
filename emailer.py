import smtplib #used to send emails

from string import Template #used to create email template

from email.mime.multipart import MIMEMultipart #email message object
from email.mime.text import MIMEText

MY_ADDRESS = 'weatherandwords@gmail.com'
PASSWORD = 'GiveusanA!'

def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """

    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

def read_template(filename):
    """Returns a Template object comprising the contents of the
    file specified by filename."""

    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def main():
    """Create new outgoing email server, create message containing weather 
    and word of the day info, send email to all contacts from mycontacts.txt"""
    names, emails = get_contacts('mycontacts.txt') # read contacts
    message_template = read_template('message.txt')

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    # For each contact, send the personalized email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       # create a message

        wotd_file = open('today.txt', 'r')
        wotd_contents = wotd_file.read()
        weather_file = open('weather_today.txt', 'r')
        weather_contents = weather_file.read()
        
        # add in the actual person name to the message template, as well as wotd contents and weather data contents
        message = message_template.substitute({'PERSON_NAME' : name.title(), 
                                               'W_OTD' : wotd_contents, 'WEATHER_UPDATE' : weather_contents})

        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['To']=email
        msg['Subject']="Daily Update!"

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        # send the message, delete when sent.
        s.send_message(msg)
        del msg

    # Terminate the SMTP session and close the connection
    s.quit()

if __name__ == '__main__':
    main()
