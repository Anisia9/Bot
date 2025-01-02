import gspread
from oauth2client.service_account import ServiceAccountCredentials

def create_sheet_connection(json_file, sheet_name):
    """Подключаем гугл таблицу"""
    scopes = [""] #права доступа
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scopes) #данные доступа
    gc = gspread.authorize(credentials) #авторизация
    spreadsheet = gc.open(sheet_name) #открываем таблицу
    return spreadsheet.sheet1 #указание на то что мы работаем на 1 листе таблице

def add_to_sheet(sheet, row):
  """Добавляет данные в таблицу"""
  sheet.append_row(row) #создание новой строки
