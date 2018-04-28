import requests
import sys,json

token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
email_url = 'https://graph.microsoft.com/v1.0/me/sendMail'
client_id = '6074cf80-a32f-43be-af03-9a1d9fc4e447'
client_secret = 'hexyEUN9?]%~rfzOJYT5832'
redirect_uri = 'https://localhost/sendemail'
scope = 'offline_access user.read mail.send'
grant_type = 'refresh_token'
headers = {'Content-Type': "application/x-www-form-urlencoded"}
payloads = {
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri': redirect_uri,
    'scope': scope,
    'grant_type': grant_type
    }


def read_token():
    """
    read refresh token from refresh_token 
    :return: string refresh_token
    """
    with open('refresh_token') as f:
        return f.readline()


def write_token(new_token=''):
    """
    write new refresh token back to the refresh_token file
    :param new_token: string
    :return: None
    """
    if len(new_token) == 0:
        print('!!!!no valid new refresh token, exit!!!!')
        sys.exit(0)
    with open('refresh_token', 'w') as f:
        f.write(new_token)
        f.close()


def get_new_token():
    """
    talk to Azure AD API to exchange for new access token
    :return: string access token
    """
    payloads['refresh_token'] = read_token()
    r = requests.post(url=token_url, headers=headers, data=payloads)
    if r.status_code != 200:
        print('!!!!fail to retrieve new token, please read the log and readme file to get new token/auth_code!!!!')
        print(r.status_code)
        print(r.text)
        sys.exit(0)
    try:
        new_refresh_token = r.json()['refresh_token']
        new_access_token = r.json()['access_token']
    except:
        print('fail to parse response json to get new tokens, please check the response')
        print(r.status_code)
        print(r.text)
        sys.exit(0)
    write_token(new_token=new_refresh_token)
    return new_access_token


def email(subject=None, recipients=None, body='', content_type='HTML'):
    """Helper to send email from current user.

    subject      = email subject (required)
    recipients   = list of recipient email addresses (required)
    body         = body of the message (String)
    content_type = content type (default is 'HTML')
    # attachments  = list of file attachments (local filenames) not included, 
    can refer to https://github.com/microsoftgraph/python-sample-send-mail

    """
    access_token = get_new_token()
    header = {
        'Authorization': "Bearer "+access_token,
        'Content-Type': "application/json"
        }

    # Verify that required arguments have been passed.
    if not all([subject, recipients]):
        raise ValueError('email(): required arguments missing')

    recipient_list = [{'EmailAddress': {'Address': address}}
                      for address in recipients]

    email_msg = {'Message': {'Subject': subject,
                             'Body': {'ContentType': content_type, 'Content': body},
                             'ToRecipients': recipient_list},
                 'SaveToSentItems': 'false'}

    # must use json.dumps for json format, otherwise will raise 400 error from microsoft !!!
    r = requests.post(url=email_url, headers=header, data=json.dumps(email_msg))
    if r.status_code == 202:
        print('email sent successfully')
    else:
        print('!!!!sending email fail!!!!')
        print(r.status_code)
        print(r.text)

if __name__ == '__main__':
    # test email functions
    email(subject='Success sent email', recipients=['jiagangzhang@mymm.com'], body='Test email from send_email.py')
