import json 
from datetime import datetime
faerun_months = ["Hammer", "Alturiak", "Ches", "Tarsakh", "Mirtul", "Kythorn", "Flamerule", "Eleasis", "Eleint", "Marpenoth", "Uktar", "Nightal"]

def number_to_ordinal(num):
    if 10 <= num % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(num % 10, 'th')
    return f"{num}{suffix}"

def get_todays_messages():
    with open('faerun_today.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    message = ""
    current_date = datetime.now()
    faerun_day = str(current_date.day)
    faerun_month = faerun_months[current_date.month-1]
    data_key = faerun_month+"_"+faerun_day
    today_events = data[data_key]
    faerun_day_th = number_to_ordinal(int(faerun_day))

    message+=f"# « Events for {faerun_day_th} of {faerun_month} »\n"
    for event_text in today_events:
        message+="- "+event_text+"\n"
    return message
