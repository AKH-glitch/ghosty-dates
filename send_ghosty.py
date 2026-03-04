import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from datetime import datetime

# --- Google Sheets setup ---
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Secretből olvasunk
creds_dict = json.loads(os.environ['GOOGLE_CREDENTIALS'])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

sheet = client.open_by_key("1NTWL6HBnUBuu-YnA4qXgGrcngt65vwIR2xv48QHOKn8").sheet1

# --- Discord webhook ---
WEBHOOK_URL = "https://discord.com/api/webhooks/1478782978216824863/7Z7wk6HRcqKqzDdYhUuBYisn6DZUWyJOfE8SCN_C58suqHdflBsYnNXqlabbH3ye1TFb"

# --- Aktuális UTC idő ---
now = datetime.utcnow().strftime("%H:%M")

for row in sheet.get_all_records():
    if row['Time (UTC)'] == now:
        message = row['Message']
        requests.post(WEBHOOK_URL, json={"content": message})
