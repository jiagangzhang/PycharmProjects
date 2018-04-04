import gspread, os, sys, re
from oauth2client.service_account import ServiceAccountCredentials
from get_jira_status import get_issue_status
from gspread.utils import a1_to_rowcol, rowcol_to_a1


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'google_api_service_account_secret.json'
# APPLICATION_NAME = 'update_google_sheet_py'
os.environ['HTTPS_PROXY'] = "http://127.0.0.1:1087"  # set proxy to call googleapis.com
PATTERN = re.compile(r'MM-[0-9]{5}')


# !!!! be sure to clear all filters before running this function, or the jira tickets will be messed
# set the cell that has no hyperlink to be hyperlinked
# :parameter column: jira column, tickets:
def add_hyperlink(column, length, worksheet):
    cell_list = []
    for i in range(length):
        cell = worksheet.cell(i+2, column, 'FORMULA')
        value = cell.value
        if value.startswith('=HYPERLINK'):
            continue
        else:
            print(i+2)
            cell.value = '=HYPERLINK("https://teamecg.atlassian.net/browse/%s","%s")' % (value, value)
            cell_list.append(cell)
    worksheet.update_cells(cell_list, 'USER_ENTERED')


# update the status column of tickets, return None
# :parameter column: 'Status' column number, tickets: ticket list
def update_ticket_status(column, tickets, worksheet):
    for cell in tickets:
        ticket_status = get_issue_status(cell.value.upper())
        print(ticket_status)
        worksheet.update_cell(cell.row, column, ticket_status)


def main():
    update_ticket = True
    update_hyperlink = False
    args = sys.argv[1:]
    if not args:
        print('Will update ticket status only \nPlease add "--mm" if you want to add jira hyperlink')
    else:
        if args[0] == '--mm':
            print('Will add jira link and update ticket status')
            update_hyperlink = True
        else:
            print('Usage: python update_google_sheet.py only update ticket stauts \
            \n add --mm if you want to add jira hyperlink')
            sys.exit(0)

    credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
    client = gspread.authorize(credentials)
    wks = client.open_by_key("1rVtfhMIAtM3sCuZNK72pnU86vILEpLqtIKPvamMuqrw").worksheet('Android Issues')
    row1 = wks.row_values(1)
    status_col_number = -1
    jira_col_number = -1
    for title in row1:
        if 'status' in title.lower().strip():
            status_col_number = row1.index(title)+1
        if 'jira' in title.lower().strip():
            jira_col_number = row1.index(title)+1
    if status_col_number == -1 or jira_col_number == -1:
        print("Can't find column named Jira or Status")
        sys.exit(0)

    jira_tickets = wks.col_values(jira_col_number, 'FORMULA')  # find all the jira tickets
    jira_tickets.pop(0)  # remove cell A1 which is the title
    # print(len(jira_tickets))
    # get_gdoc_ticket_number(1,jira_tickets[0:4], wks)

    if update_hyperlink:
        add_hyperlink(jira_col_number, 10, wks)
    cell_list = wks.findall(PATTERN)
    if update_ticket:
        update_ticket_status(status_col_number, cell_list, wks)





if __name__ == '__main__':
    main()