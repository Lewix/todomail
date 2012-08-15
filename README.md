todo
====

Manage Google Tasks list.

    Usage:
        todo ls
        todo add <task>
        todo done <id>
        todo edit <id> <task>

Uses a file called client_details in the same directory as the script to
determine the client_id and client_secret, on the first and second line
respectively.

mail_getter
===========

This adds starred email to Google Tasks. It looks for login details in a 
login_detail file in the same directory as the script. This should contain the
username on the firs line and the password on the second.
