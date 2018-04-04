import requests
# from requests.auth import HTTPBasicAuth

jiraApiToken = 'nX6BNvgBahqhMhtfHAIjEA37'
jiraApiUser = 'jiagangzhang@mymm.com'
jira_url = 'https://teamecg.atlassian.net/rest/api/2/issue/'


# @parameter issue_number shall be like MM-33567
def get_issue_status(issue_number):

    querystring = {"fields": "status"}
    headers = {'Accept': "application/json"}
    print('Starting to get ticket %s ' % issue_number)
    response = requests.get(jira_url + issue_number, auth=(jiraApiUser, jiraApiToken), headers=headers, params=querystring)
    if response.status_code != 200:
        print(str(response.status_code) + '\n' + response.text)
        return ''
    else:
        status = response.json()['fields']['status']['name']
        print('retrieve success \'' + status + '\'')
        return status


def test_get_issue_status():
    response = get_issue_status('MM-33643')  # test correct number
    response = get_issue_status('MM-88888')  # test wrong number

if __name__ == "__main__":
    test_get_issue_status()
