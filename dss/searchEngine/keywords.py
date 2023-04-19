import re
import pandas as pd
file=pd.ExcelFile(r"C:\Users\ankit\Downloads\Keywords for Samadhaan.xlsx")
sheetName=file.sheet_names
keyword_dict={}
for sheet in sheetName:
    df=pd.read_excel(r"C:\Users\ankit\Downloads\Keywords for Samadhaan.xlsx",sheet_name=sheet)
    string=df['Keywords']
    pattern = r'\d{1,3}\)'
    result = re.split(pattern, string)
    keyword_dict[sheet]=result
# print(result)