import gspread
from oauth2client.service_account import ServiceAccountCredentials

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Demo Final Shame October 2019').sheet1
telemedicine = sheet.get_all_records()
print(telemedicine)
