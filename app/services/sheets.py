import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app.core.config import settings
import json
import os

SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

class GoogleSheetsService:
    def __init__(self):
        self.client = None
        self.connect()

    def connect(self):
        try:
            creds_json = settings.GOOGLE_SHEETS_CREDENTIALS_JSON
            if not creds_json:
                print("Warning: GOOGLE_SHEETS_CREDENTIALS_JSON not found. Sheets service will not work.")
                return

            # Check if it's a file path or JSON string
            if os.path.exists(creds_json):
                creds = ServiceAccountCredentials.from_json_keyfile_name(creds_json, SCOPES)
            else:
                creds_dict = json.loads(creds_json)
                creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPES)

            self.client = gspread.authorize(creds)
            print("Connected to Google Sheets successfully.")
        except Exception as e:
            print(f"Error connecting to Google Sheets: {e}")

    def get_sheet(self, sheet_name, worksheet_name=None):
        if not self.client:
            return None
        try:
            sheet = self.client.open(sheet_name)
            if worksheet_name:
                return sheet.worksheet(worksheet_name)
            return sheet.sheet1
        except Exception as e:
            print(f"Error getting sheet {sheet_name}: {e}")
            return None

    def get_all_records(self, sheet_name, worksheet_name=None):
        ws = self.get_sheet(sheet_name, worksheet_name)
        if ws:
            return ws.get_all_records()
        return []

    def append_row(self, sheet_name, row_data, worksheet_name=None):
        ws = self.get_sheet(sheet_name, worksheet_name)
        if ws:
            ws.append_row(row_data)
            return True
        return False

sheets_service = GoogleSheetsService()
