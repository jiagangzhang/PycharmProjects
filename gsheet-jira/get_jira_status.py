# encoding=utf8

import requests
# from requests.auth import HTTPBasicAuth

jiraApiToken = 'nX6BNvgBahqhMhtfHAIjEA37'
jiraApiUser = 'jiagangzhang@mymm.com'
jira_url = 'https://teamecg.atlassian.net/rest/api/2/issue/'


# convert full name or email to capitalized first name
def convert_name(name):
    new_name = name.replace('@', ' ').split(' ')[0].capitalize()
    if new_name == 'Wu':
        new_name = 'Galen'
    elif new_name == 'Vickyli':
        new_name = 'Vicky'
    elif new_name == 'Lilyzuo':
        new_name = 'Lily'

    return new_name


# @parameter issue_number shall be like MM-33567
def get_issue_status(issue_number):

    querystring = {"fields": "status"}
    headers = {'Accept': "application/json"}
    print('Starting to get ticket %s ' % issue_number)
    response = requests.get(jira_url + issue_number, auth=(jiraApiUser, jiraApiToken), headers=headers)
    if response.status_code != 200:
        print(str(response.status_code) + '\n' + response.text)
        return ['', '', '', '']
    else:
        try:
            status = response.json()['fields']['status']['name']
            summary = response.json()['fields']['summary']
            priority = response.json()['fields']['priority']['name']
            reporter = convert_name(response.json()['fields']['reporter']['displayName'])
            try:
                assignee = convert_name(response.json()['fields']['assignee']['displayName'])
            except: assignee = 'no assignee'
            print('retrieve success \'' + status + '\'' + '\t' + summary + '\t' + priority + '\t' + reporter\
                  + '\t' + assignee)
        except:
            print('error process response, will return empty list')
            return ['', '', '', '']
        return [status, summary, priority, reporter]  # assignee is not returned, can add if necessary


def test_get_issue_status():
    response = get_issue_status('MM-33643')  # test correct number
    response = get_issue_status('MM-88888')  # test wrong number


if __name__ == "__main__":
    test_get_issue_status()