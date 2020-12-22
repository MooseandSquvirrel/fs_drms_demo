# APP MUST HAVE 'Basic Staff' PERMISSIONS & 'tig' SCOPE MUST BE SET
# APP HAD TO HAVE OAUTH CLIENT CREDENTIAL MADE FOR IT SPECIFICALLY (NEW PROJECT) ON GOOGLE API

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pprintpp
import time
import json
import requests
import os
title = __import__('commandline_intro')
cl = __import__('commandline_args')
ft = __import__('ft_api')
room_status = __import__('room_class')

SPREADSHEET_ID = 'ID'
RANGE_NAME = 'A1:E'
SCOPES = "readonly"

# FUNCTION TO OPEN CADETS ACCOUNTS
def update_close(session, cadet_pass_list):
    i = 0
    with open('listfile.py', 'r+') as filehandle:
        r = json.load(filehandle)
        for room in cadet_pass_list:
            for room_obj in r:
                if cadet_pass_list[i].number == room_obj['number']:
                    for user in room_obj['closure_ids']:
                        time.sleep(0.6)
                        headers = {'Content-Type': 'application/json'}
                        url = "https://api.intra.42.fr/v2/closes/" + str(user) + "/unclose"
                        response = session.put(url, headers=headers)
                        if response.status_code == 204:
                            print(f"\nOPENED: {user}\n")
                            print(f"response: {response.headers}")
                        else:
                            print(f"text:\n{response.text}")
                else:
                    print("-update_close- continuing...")
            i += 1

# FUNCTION TO POST THE CLOSE REQUEST OF CADET ACCOUNT TO 42 API
def close_request(session, room, user):
    time.sleep(0.6)
    # REPLACE CLOSER ID W/ YOUR ID
    closer_id = str(66143)
    payload = {
        'close': {
            'closer_id': 1111111111,
            'kind':'other',
            'reason':room.reason,
            'state':'close',
            'user_id': user
            }
        }
    headers = {'Content-Type': 'application/json'}
    url = "https://api.intra.42.fr/v2/closes"
    response = session.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200 or 201:
        print(response.content.decode('utf-8') + '\n')
        r = response.json()
        room.closure_ids.append(r['id'])
        print(f"-close_request- room.number: {room.number}")
    else:
        print("-close- close function failure...")
        print(f"text:\n{response.text}")

# FUNCTION TO CLOSE CADETS ACCOUNTS
def close(session, cadet_fail_list):
    for room in cadet_fail_list:
        room.closure_ids = []
        for user in room.occupants:
            print(f"room: {room}")
            print(f"room.occupants: {room.occupants}")
            close_request(session, room, user)
    with open('listfile.py', 'w+') as filehandle:
        json_string = [ob.__dict__ for ob in cadet_fail_list]
        json_string = json.dumps(json_string)
        filehandle.write('%s\n' % json_string)

# FUNCTION TO GET IDS FOR EACH CADET IN ROOMS -- CADET LOGINS IN cadet_fail_list/cadet_pass_list BOTH FROM GOOGLE SHEETS FORM
def get_ids(cadet_fail_list, cadet_pass_list):
    session, token = ft.client()
    print("\n--------------------------------------\nIDs From Intra\n --------------------------------------\n")
    for room in cadet_fail_list:
        ft.get_userids_by_logins(session, room)
    for room in cadet_pass_list:
        ft.get_userids_by_logins(session, room)
    return session

# FUNCTION TO PARSE PASS/FAIL FROM GOOGLE SHEETS
# CLASS ATTRIBUTES BELOW -> lists[0]: ROOM NUMBER lists[1]: LOGINS, lists[2]: STATUS, lists[3]: REASON, lists[4]: CLOSED
def pass_fail_lists(room, logins_room, lists, cadet_fail_list, cadet_pass_list):
    if ((lists[2]) and (lists[2] == "PASS")) and (len(lists) == 5)  and (lists[4] == "PASS"):
        pass
    elif ((lists[2]) and (lists[2] == "FAIL")) and (len(lists) == 5)  and (lists[4] == "PLEASE CLOSE"):
        print(f"FAILED: CLOSING Occupants in Room {lists[0]}")
        cadet_fail_list.append(room)
    elif ((lists[2]) and (lists[2] == "PASS")) and (len(lists) == 5)  and (lists[4] == "PLEASE OPEN"):
        print(f"PASSED 2nd Inspection: OPENING Occupant in Room {lists[0]}")
        cadet_pass_list.append(room)
    return cadet_fail_list, cadet_pass_list

# FUNCTION TO GRAB PASS/FAIL LISTS OF LOGINS FROM GOOGLE FORM
def cadets_list(result):
    print("\n--------------------------------------\nBreakdown of Google Spreadsheet\n--------------------------------------")
    fail_logins, pass_logins, closure_ids, cadet_fail_list, cadet_pass_list  = [], [], [], [], []
    values = result['values']
    for lists in values:
        logins_room = []
        if lists[1] == '':
            print(f"NO OCCUPANTS in Room: {lists[0]}")
            continue
        elif len(lists) == 5:
            logins_room = lists[1].split(', ')
            room = room_status.Room(lists[0], logins_room, lists[2], lists[3], lists[4], closure_ids)
            cadet_fail_list, cadet_pass_list = pass_fail_lists(room, logins_room, lists, cadet_fail_list, cadet_pass_list)
        else:
            print(f"Room EMPTY or Data incorrect for room: {lists[0]}")
    print("------------------------------\n-cadets_lists- cadet_failed_groups:\n------------------------------")
    pprintpp.pprint(cadet_fail_list)
    print("\n")
    print("------------------------------\n-cadets_lists- cadet_passed_groups:\n------------------------------")
    pprintpp.pprint(cadet_pass_list)
    return cadet_fail_list, cadet_pass_list

# FUNCTION TO GRAB RESULTS OF ROOM INSPECTIONS FROM GOOGLE FORM -- BASED DIRECTLY OFF OF 'QUICKSTART' SCRIPT PROVIDED BY GOOGLE API PYTHON SHEETS
def grab_result():
    title.intro()
    args = cl.args()
    creds = None

    # THE FILE token.pickle STORES THE USERS'S ACCESS AND REFRESH TOKENS, AND IS
    # CREATED AUTOMATICALLY WHEN THE AUTHORIZATION FLOW COMPLETES FRO THE FIRST TIME.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # IF THERE ARE NO (VALID) CREDENTIALS AVAILABLE, LET THE USER LOG IN.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_gd.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # SAVE THE CREDENTIALS FOR THE NEXT RUN
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # CALL THE SHEETS API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    return result, args

def main():
    result, args = grab_result()
    print(result)
    cadet_fail_list, cadet_pass_list = cadets_list(result)
    session = get_ids(cadet_fail_list, cadet_pass_list)
    if args == 'c':
        close_ids = close(session, cadet_fail_list)
    elif args == 'o':
        update_close(session, cadet_pass_list)

if __name__ == '__main__':
    main()
