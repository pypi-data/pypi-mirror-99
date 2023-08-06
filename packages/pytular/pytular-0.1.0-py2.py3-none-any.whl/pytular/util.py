import pathlib

from csvw.dsv import UnicodeWriter
import gspread
from oauth2client.service_account import ServiceAccountCredentials

__all__ = ['fetch_sheet']

DOCUMENT_ID = "1TeRCpL717v8n5bR4o3iyxdH_dvEeDPjAWR4t4efylOs"


def google_api_client(keyfile=None):
    keyfile = keyfile or input('Path to Google API key file: ')
    keyfile = pathlib.Path(keyfile)
    assert keyfile.exists()
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        str(keyfile), ['https://spreadsheets.google.com/feeds'])
    return gspread.authorize(credentials)


def fetch_sheet(sheetname, keyfile=None, output=None, delimiter='\t'):
    spreadsheet = google_api_client(keyfile).open_by_key(DOCUMENT_ID)

    for i, worksheet in enumerate(spreadsheet.worksheets()):
        if worksheet.title == sheetname:
            output = output or '{0}.tsv'.format(worksheet.title)
            with UnicodeWriter(output, delimiter=delimiter) as writer:
                writer.writerows(worksheet.get_all_values())
