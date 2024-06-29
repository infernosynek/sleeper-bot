from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

def generate_month(month_index, today_date, data_multi_dict):
    # Load the calendar image
    calendar_image_path = 'callendar_blank.png'
    calendar = Image.open(calendar_image_path)
    draw = ImageDraw.Draw(calendar)

    # Constants for title and cell dimensions
    title_center_x = 480
    title_center_y = 40
    sub_title_center_x = 480
    sub_title_center_y = 70
    rows = [(78, 130), (78, 210), (78, 297)]  # List of (x, y) for each row of cells
    cell_width, cell_height = (81, 51)
    tcell_width, tcell_height = (81, 71)  # Dimensions of one cell

    faerun_months = ["Hammer", "Alturiak", "Ches", "Tarsakh", "Mirtul", "Kythorn", "Flamerule", "Eleasias", "Eleint", "Marpenoth", "Uktar", "Nightal"]
    polish_months = ['Styczen', 'Luty', 'Marzec', 'Kwiecien', 'Maj', 'Czerwiec','Lipiec', 'Sierpien', 'Wrzesien', 'Pazdziernik', 'Listopad', 'Grudzien']

    # Function to calculate cell position based on date
    def calculate_cell_position(date):
        # Example: Date format "YYYY-MM-DD"
        day = int(date.split('-')[-1])
        row_index = (day - 1) // 10  # Determine row index (0, 1, or 2 based on day)
        col_index = (day - 1) % 10   # Determine column index (0 to 9 based on day)
        cell_x = rows[row_index][0] + col_index * cell_width
        cell_y = rows[row_index][1]
        return (cell_x, cell_y)

    # Font settings
    font_path = "DalelandsUncialCondensed-rWYK.ttf"  # Example font file (replace with your actual font file)
    title_font_size = 40
    sub_title_font_size = 20
    callendar_font_size = 18
    title_font = ImageFont.truetype(font_path, title_font_size)
    sub_title_font = ImageFont.truetype(font_path, sub_title_font_size)
    callendar_font = ImageFont.truetype(font_path, callendar_font_size)

    # Draw title box
    # Get today's date
    today = today_date
    date_object = datetime.strptime(today, "%Y-%m-%d")

    # Extract month from datetime object
    today_month = date_object.month
    if today_month-1==month_index:
        image_path = "blue-star-icon-png.webp"
        if today in data_multi_dict.keys():
            image_path = "today_2.png"
        today_img = Image.open(image_path)
        cell_position = calculate_cell_position(today)
        resized_img = today_img.resize((tcell_width, tcell_height))
        calendar.paste(resized_img, (cell_position[0], cell_position[1]-20))

    title_text = faerun_months[month_index]
    title_text_width, title_text_height = draw.textsize(title_text, font=title_font)
    title_position = (title_center_x - title_text_width // 2, title_center_y - title_text_height // 2)
    draw.text(title_position, title_text, font=title_font, fill='black')

    sub_title_text = polish_months[month_index]
    sub_title_text_width, sub_title_text_height = draw.textsize(sub_title_text, font=sub_title_font)
    sub_title_position = (sub_title_center_x - sub_title_text_width // 2, sub_title_center_y - sub_title_text_height // 2)
    draw.text(sub_title_position, sub_title_text, font=sub_title_font, fill='black')

    # Draw events on the calendar
    for date, event_dict in data_multi_dict.items():
        cell_position = calculate_cell_position(date)
        event_time = event_dict['time']
        cell_position = (cell_position[0]+33,cell_position[1]-18)
        draw.text(cell_position, event_time, font=callendar_font, fill='red')
        cell_position = calculate_cell_position(date)
        event_title = event_dict['title']
        words = event_title.split(' ')
        y = cell_position[1]
        for word in words:
            word_width, word_height = draw.textsize(word, font=callendar_font)
            draw.text((cell_position[0]+( cell_width- word_width) // 2, y), word, font=callendar_font, fill='black')
            y += word_height  # Move to the next line

    # Save the modified image
    calendar.save('calendar_with_events.png')