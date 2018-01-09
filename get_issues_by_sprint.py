from jira.resources import Issue
from jira.client import JIRA

def sprints(username, 
            ldp_password,
            sprint_name,
            board_id,
            sprint_id,
            type_of_issues_to_pull=[
                  'completedIssues', 
                  'incompletedIssues',
                  'issuesNotCompletedInCurrentSprint',
                  'issuesCompletedInAnotherSprint']):
    def sprint_issues(cls, board_id, sprint_id):
        r_json = cls._get_json(
            'rapid/charts/sprintreport?rapidViewId=%s&sprintId=%s' % (
                board_id, sprint_id),
            base=cls.AGILE_BASE_URL)

        issues = []
        for t in type_of_issues_to_pull:
            if t in r_json['contents']:
                issues += [Issue(cls._options, cls._session, raw_issues_json)
                           for raw_issues_json in
                           r_json['contents'][t]]
        return {x.key: x for x in issues}.values()

    fmt_full = u'Sprint: {} \n\nIssues:{}'
    fmt_issues = u'\n- {}: {}'
    issues_str = u''
    milestone_str = u''

    options = {
        'server': 'https://bankfacil.atlassian.net/',
        'verify': True,
        'basic_auth': (username, ldp_password),
    }
    gh = JIRA(options=options, basic_auth=(username, ldp_password))

    # Get all boards viewable by anonymous users.
    # boards = gh.boards()
    # board = [b for b in boards if b.name == sprint_name][0]

    # sprints = gh.sprints(board.id)

    # for sprint in sorted([s for s in sprints
                   # if s.raw[u'state'] == u'ACTIVE'],
                # key = lambda x: x.raw[u'sequence']):
        # milestone_str = str(sprint)
    issues = sprint_issues(gh, board_id, sprint_id)
    for issue in issues:
        issues_str += fmt_issues.format(issue.key, issue.summary)

    result = fmt_full.format(
        milestone_str,
        issues_str
    )
    print(result)
    return result

sprints('luiz.assuncao@creditas.com.br', 'creditas@atlassian', 'Ronaldinho', 18, 168)
