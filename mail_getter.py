import imaplib
import email

username = 'lewix7@gmail.com'
password = 'kpncuwapeouburmu'


def list_mail(imap_server, port, mailbox):
    mail = []
    M = imaplib.IMAP4_SSL(imap_server, port)
    M.login(username, password)
    M.select(mailbox)
    typ, data = M.search(None, 'ALL')
    for num in data[0].split():
        typ, data = M.fetch(num, '(RFC822)')
        msg = email.message_from_string(data[0][1])
        mail.append(msg)
    M.close()
    return mail

if __name__ == '__main__':
    for mail in list_mail('imap.gmail.com', 993, '[Google Mail]/Starred'):
        print mail['Subject']
