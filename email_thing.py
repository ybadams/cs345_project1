import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import webscraper

EMAIL_ADDRESS = input("What Gmail do you want to send this from? \n")
PASSWORD = input("What is the password? Don't worry, this will not be stored. \n")

def split_contact_info(filename):
    """Return two lists: names_list and emails_list, containing names and email addresses
    read from a file specified by filename."""

    names_list = []
    emails_list = []
    with open(filename, mode='r', encoding='utf-8') as f:
        for contact in f:
            names_list.append(contact.split()[0])
            emails_list.append(contact.split()[1])
    return names_list, emails_list

def read_template(filename):
    """Returns a Template object with the contents of the
    file specified by filename."""

    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def main():
    names_list, emails_list = split_contact_info('mycontacts.txt') # read contacts
    message_template = read_template('message.txt')

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587) #Gmail's host and port values
    s.starttls()
    s.login(EMAIL_ADDRESS, PASSWORD)

    # For each contact, send the email:
    for name, email in zip(names_list, emails_list): #match names with corresponding emails
        msg = MIMEMultipart()       # create a message

        # add in the actual person's name to the message template
        message = message_template.substitute(PERSON_NAME=name.title())

        # Prints out the message body for our sake
        print(message)

        # setup the parameters of the message
        msg['From']=EMAIL_ADDRESS
        msg['To']=email
        msg['Subject']="This is TEST. If you got this email then that means we will be able to complete this project in no time lol.\n"

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg

    # Terminate the SMTP session and close the connection
    s.quit()

if __name__ == '__main__':
    main()
