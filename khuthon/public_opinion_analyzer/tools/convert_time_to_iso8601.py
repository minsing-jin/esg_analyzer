from datetime import datetime

def convert_string_time_to_iso8601(datetime_str: str) -> str:
    # Splitting the string to separate the date from the AM/PM part
    date_part, am_pm, time_part = datetime_str.split(' ')

    # Converting the date and time parts into 24-hour format datetime object
    if am_pm == "오후":
        hour, minute = map(int, time_part.split(':'))
        hour = hour % 12 + 12  # Convert PM hours to 24-hour format
    else:
        hour, minute = map(int, time_part.split(':'))
        hour = hour % 12  # Convert AM hours to 24-hour format, 12 AM becomes 0

    # 2024.07.01. -> 2024-07-01 => 01 followed by ., so remove it
    date_part = date_part.split('.')[0:3]

    # Reconstructing the datetime string in a format that strptime can parse
    datetime_str_formatted = f"{"-".join(date_part)} {hour}:{minute}"

    # Parsing the string to a datetime object
    dt = datetime.strptime(datetime_str_formatted, "%Y-%m-%d %H:%M")

    # Converting the datetime object to an ISO 8601 formatted string
    iso_format_str = dt.isoformat()

    return iso_format_str
