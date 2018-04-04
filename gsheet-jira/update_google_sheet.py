import gspread, os
from oauth2client.service_account import ServiceAccountCredentials
from get_jira_status import get_issue_status
from gspread.utils import a1_to_rowcol, rowcol_to_a1


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'google_api_service_account_secret.json'
# APPLICATION_NAME = 'update_google_sheet_py'
os.environ['HTTPS_PROXY'] = "http://127.0.0.1:1087" #set proxy to call googleapis.com


def get_gdoc_ticket_number():
    # return ''
    pass


def set_gdoc_ticket_status():
    # return ''
    pass


def main():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
    client = gspread.authorize(credentials)
    # wks = client.open_by_key("1rVtfhMIAtM3sCuZNK72pnU86vILEpLqtIKPvamMuqrw").worksheet('Android Issues')
    wks = client.open_by_url\
        ('https://docs.google.com/spreadsheets/d/1rVtfhMIAtM3sCuZNK72pnU86vILEpLqtIKPvamMuqrw/edit?usp=sharing').sheet1
    # wks.update_acell('B4', "it's down there somewhere, let me take another look.")
    # wks.update_acell('B5', "Done")
    # print(wks.acell('E1').value)
    # print(wks.acell('A2').value)
    print(wks.acell('A2', 'FORMULA').value)
    wks.update_acell('A1', '=HYPERLINK("https://teamecg.atlassian.net/browse/MM-33546","MM-33546 [Done]")')




if __name__ == '__main__':
    main()