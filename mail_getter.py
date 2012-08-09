import imaplib
import email
import os
from todo_list import TodoList

login_details = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'gmail_login')
             

class MailBox:
    def __init__(self, imap_server, port, mailbox, username, password):
        self.M = imaplib.IMAP4_SSL(imap_server, port)
        self.M.login(username, password)
        self.mailbox = mailbox
        self.M.select(mailbox)
        typ, self.data = self.M.search(None, 'ALL')

    def get_data(self):
        if self.data:
            return self.data[0].split()
        else:
            return []

    def get_email(self, num):
        self.M.select(self.mailbox)
        typ, data = self.M.fetch(num, '(RFC822)')
        msg = email.message_from_string(data[0][1])
        return msg

    def list_mail(self):
        mail = []
        for num in self.get_data():
            msg = self.get_email(num)
            mail.append(msg)
        self.M.close()
        return mail

    def delete_mail(self, subject):
        for num in self.get_data():
            msg = self.get_email(num)
            if msg['Subject'] == subject:
                self.M.store(num, '+FLAGS', '\\Deleted')
                break
        self.M.expunge()

def add_tasks(mail_titles, list_name, mailbox):
    todo = TodoList(list_name)

    tasks_with_notes = [t for t in todo.get_tasks(True) if 'notes' in t]
    gmail_tasks = [t['title'] for t in tasks_with_notes if 'gmail' in t['notes']]
    finished_tasks = [t for t in tasks_with_notes if t['status'] == 'completed']
    finished_gmail_tasks = [t['title'] for t in finished_tasks if 'gmail' in t['notes']]

    # Unstar any finished tasks
    for task in finished_gmail_tasks:
        mailbox.delete_mail(task)
            
    # Clear finished tasks
    todo.clear_finished()

    # Add any newly starred email to tasks
    for mail in mail_titles:
        if not mail in gmail_tasks:
            todo.add_task(mail, 'gmail')


if __name__ == '__main__':
    f = open(login_details, 'r')
    username = f.readline()[:-1]
    password = f.readline()[:-1]
    f.close()
    mailbox = MailBox('imap.gmail.com', 993,  '[Google Mail]/Starred', username, password)
    mails = mailbox.list_mail()
    mail_titles = [mail['Subject'] for mail in mails]

    add_tasks(mail_titles, 'Mobile List', mailbox)
