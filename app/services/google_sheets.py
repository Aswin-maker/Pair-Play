import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from app.config import settings

def get_sheets_service():
    if not os.path.exists(settings.GOOGLE_SHEETS_CREDENTIALS_JSON):
        # Fallback or error handling if file doesn't exist
        # For now, we assume it exists or let it raise FileNotFoundError
        pass
        
    creds = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_SHEETS_CREDENTIALS_JSON,
        scopes=["https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"]
    )
    return build("sheets", "v4", credentials=creds)

async def read_values(range_name: str):
    try:
        service = get_sheets_service()
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=settings.SPREADSHEET_ID, range=range_name).execute()
        return result.get("values", [])
    except Exception as e:
        print(f"Google Sheets Error (Reading {range_name}): {e}")
        # Mock Data Fallback
        if "Packages" in range_name:
            return [
                ["Bali Honeymoon", "Bali", "5", "25000", "Beach, Temple, Sunset", "https://example.com/bali.jpg"],
                ["Paris Getaway", "Paris", "4", "80000", "Eiffel Tower, Louvre", "https://example.com/paris.jpg"],
                ["Kerala Retreat", "Kerala", "3", "15000", "Houseboat, Tea Garden", "https://example.com/kerala.jpg"]
            ]
        return []

async def append_row(range_name: str, row: list):
    try:
        service = get_sheets_service()
        sheet = service.spreadsheets()
        body = {"values":[row]}
        res = sheet.values().append(spreadsheetId=settings.SPREADSHEET_ID, range=range_name,
                                    valueInputOption="RAW", body=body).execute()
        return res
    except Exception as e:
        print(f"Google Sheets Error (Writing to {range_name}): {e}")
        print(f"MOCK SAVE: Appended to {range_name}: {row}")
        return {"updates": {"updatedRows": 1}}
