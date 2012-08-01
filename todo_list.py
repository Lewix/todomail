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
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client.tools import run
from urllib import urlopen
from docopt import docopt

class TaskApi:
    def __init__(self):
            # OAuth2 authentication
            flow = OAuth2WebServerFlow(
                    client_id='76831993824.apps.googleusercontent.com',
                    client_secret='oe6Mw-DiS-Ctgw4PwQ00NqtA',
                    scope='https://www.googleapis.com/auth/tasks',
                    user_agent='todo_list')
            storage = Storage('tasks.dat')
            credentials = storage.get()
            if credentials is None or credentials.invalid == True:
                credentials = run(flow, storage)

            self.http = httplib2.Http()
            self.http = credentials.authorize(self.http)

    def list_tasklists(self):
        url = 'https://www.googleapis.com/tasks/v1/users/@me/lists'
        response, content = self.http.request(url, 'GET')
        return json.loads(content)['items']

    def list_tasks(self, tasklist):
        url = 'https://www.googleapis.com/tasks/v1/lists/{0}/tasks?showCompleted=false'.format(tasklist)
        response, content = self.http.request(url, 'GET')
        return json.loads(content)['items']

    def add_task(tasklist, title=task):
        url = 'https://www.googleapis.com/tasks/v1/lists/{0}/tasks'.format(tasklist)
        data = { 'title' : task }
        resp, content = h.request(url, 'POST', urlencode(data))
        print resp
        print content


class TodoList:
    def __init__(self, list_name):
        self.taskapi = TaskApi()
        
        for tasklist in self.taskapi.list_tasklists():
            if tasklist[u'title'] == list_name:
                self.tasklist = tasklist['id']
                break
        else:
            raise Exception('No such task list')

    def list_tasks(self):
        tasks = self.taskapi.list_tasks(self.tasklist)
        for i, task in zip(range(1,len(tasks)+1), tasks):
            print '({0}) {1}'.format(i,task['title'])

    def add_task(task):
        self.taskapi.add_task(tasklist, title=task)

    def done_task(tid):
        pass

    def edit_task(tid, task):
        pass

if __name__ == '__main__':
    #arguments = docopt(__doc__)

    #TODO: key
    todo_list = TodoList('General')
    todo_list.add_task('Test task')
