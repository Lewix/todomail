#!/usr/bin/python2.7
"""todo

Usage:
    todo ls
    todo add <task>
    todo done <id>
    todo edit <id> <task>
"""

import httplib2
import json
import os
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client.tools import run
from urllib import urlencode
from docopt import docopt

client_details = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'gmail_login')

class TaskApi:
    def __init__(self, client_id, client_secret):
            # OAuth2 authentication
            flow = OAuth2WebServerFlow(
                    client_id=client_secret,
                    client_secret=client_id,
                    scope='https://www.googleapis.com/auth/tasks',
                    user_agent='todo_list')
            dat_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tasks.dat')
            storage = Storage(dat_file)
            credentials = storage.get()
            if credentials is None or credentials.invalid == True:
                credentials = run(flow, storage)

            self.http = httplib2.Http()
            self.http = credentials.authorize(self.http)
            self.headers = { 'Content-type': 'application/json' }

    def list_tasklists(self):
        url = 'https://www.googleapis.com/tasks/v1/users/@me/lists'
        response, content = self.http.request(url, 'GET')
        return json.loads(content)['items']

    def get_tasks(self, tasklist, completed=False):
        url = 'https://www.googleapis.com/tasks/v1/lists/{0}/tasks?showCompleted={1}'.format(tasklist, str(completed))
        response, content = self.http.request(url, 'GET')
        return json.loads(content)['items']

    #TODO Add arbitrary data
    def add_task(self, tasklist, task):
        url = 'https://www.googleapis.com/tasks/v1/lists/{0}/tasks'.format(tasklist)
        resp, content = self.http.request(url, 'POST', headers=self.headers, body=json.dumps(task))

    def edit_task(self, tasklist, task):
        url = 'https://www.googleapis.com/tasks/v1/lists/{0}/tasks/{1}'.format(tasklist, task['id'])
        resp, content = self.http.request(url, 'PUT', headers=self.headers, body=json.dumps(task))

    def delete_task(self, tasklist, task):
        url = 'https://www.googleapis.com/tasks/v1/lists/{0}/tasks/{1}'.format(tasklist, task['id'])
        resp, content = self.http.request(url, 'DELETE', headers=self.headers)

    def get_task(self, tasklist, task_number):
        return self.get_tasks(tasklist)[task_number-1]

class TodoList:
    def __init__(self, list_name, client_id, client_secret):
        self.taskapi = TaskApi(client_id, client_secret)
        
        for tasklist in self.taskapi.list_tasklists():
            if tasklist[u'title'] == list_name:
                self.tasklist = tasklist['id']
                break
        else:
            raise Exception('No such task list')

    def get_tasks(self, completed=False):
        return self.taskapi.get_tasks(self.tasklist, completed)

    def clear_finished(self):
        tasks = self.taskapi.get_tasks(self.tasklist, True)
        for task in tasks:
            if task['status'] == 'completed':
                self.taskapi.delete_task(self.tasklist, task)

    def list_tasks(self):
        tasks = self.taskapi.get_tasks(self.tasklist)
        # Don't show tasks with no title
        tasks = [t for t in tasks if t['title']]
        for i, task in zip(range(1,len(tasks)+1), tasks):
            print '({0}) {1}'.format(i,task['title'])

    def add_task(self, task, notes=''):
        task = { 'title' : task, 'notes' : notes }
        self.taskapi.add_task(self.tasklist, task)

    def done_task(self, task_number):
        # Set status to completed
        task = self.taskapi.get_task(self.tasklist, task_number)
        task['status'] = 'completed'
        self.taskapi.edit_task(self.tasklist, task)

    def edit_task(self, task_number, title):
        task = self.taskapi.get_task(self.tasklist, task_number)
        task['title'] = title
        self.taskapi.edit_task(self.tasklist, task)

if __name__ == '__main__':
    arguments = docopt(__doc__)

    f = open(client_details, 'r')
    client_id = f.readline()[:-1]
    client_secret = f.readline()[:-1]
    f.close()

    todo_list = TodoList('Mobile List', client_id, client_secret)
    if arguments['ls']:
        todo_list.list_tasks()
    elif arguments['add']:
        todo_list.add_task(arguments['<task>'])
    elif arguments['done']:
        todo_list.done_task(int(arguments['<id>']))
    elif arguments['edit']:
        todo_list.edit_task(int(arguments['<id>']), arguments['<task>'])
