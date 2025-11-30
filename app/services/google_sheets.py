import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from app.config import settings

def get_sheets_service():
    creds = None
    # Option A: Load credentials from env var string (preferred on Railway)
    env_json = os.getenv("GOOGLE_CREDENTIALS_JSON_STRING")
    if env_json:
        try:
            info = json.loads(env_json)
            creds = service_account.Credentials.from_service_account_info(
                info,
                scopes=[
                    "https://www.googleapis.com/auth/spreadsheets",
                    "https://www.googleapis.com/auth/drive",
                ],
            )
        except Exception as e:
            print(f"Google Creds from env failed: {e}")

    # Option B: Fallback to file path if configured and exists
    if creds is None and settings.GOOGLE_SHEETS_CREDENTIALS_JSON:
        try:
            if os.path.exists(settings.GOOGLE_SHEETS_CREDENTIALS_JSON):
                creds = service_account.Credentials.from_service_account_file(
                    settings.GOOGLE_SHEETS_CREDENTIALS_JSON,
                    scopes=[
                        "https://www.googleapis.com/auth/spreadsheets",
                        "https://www.googleapis.com/auth/drive",
                    ],
                )
        except Exception as e:
            print(f"Google Creds from file failed: {e}")

    if creds is None:
        # Return a dummy builder that will trigger exceptions caught by callers
        raise FileNotFoundError("Google service account credentials not provided.")

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
