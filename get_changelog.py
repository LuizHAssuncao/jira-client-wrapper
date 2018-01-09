from collections import Counter
from jira import JIRA
import re

options = {
    'server': 'https://bankfacil.atlassian.net'
}

jira = JIRA(options=options, basic_auth=('', ''))
projects = jira.projects()

print jira.sprint_info(board_id=18, sprint_id=168)
# print projects
# print ', '.join("%s: %s" % item for item in projects.items())
# Ronaldinho=168, joaozinho=174

issue = jira.issue('KBLO-374', expand='changelog')
changelog = issue.changelog

for history in changelog.histories:
    for item in history.items:
        if item.field == 'status':
            print 'Date:' + history.created + ' From:' + item.fromString + ' To:' + item.toString

