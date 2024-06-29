from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_image_with_text(title_string, date_string, description_string, output_path="event_today.jpg", background_path="paper_texture.jpg"):
    # Load the background image
    background = Image.open(background_path)
    draw = ImageDraw.Draw(background)
    
    # Define font sizes
    title_font_size = 80
    date_font_size = 50
    description_font_size = 40

    # Load a font
    custom_font_path = 'DalelandsUncialCondensed-rWYK.ttf'
    title_font = ImageFont.truetype(custom_font_path, title_font_size)
    date_font = ImageFont.truetype(custom_font_path, date_font_size)
    description_font = ImageFont.truetype(custom_font_path, description_font_size)
    
    # Define text positions
    # Center the title
    title_width, title_height = draw.textsize(title_string, font=title_font)
    title_position = ((background.width - title_width) // 2, 50)

    date_position = (50, 175)
    description_position = (50, 250)
    
    # Define text colors
    title_color = (50, 25, 25)  # Very dark brown
    date_color = (50, 25, 25)
    description_color = (50, 25, 25)

    # Add title text
    draw.text(title_position, title_string, font=title_font, fill=title_color)

    # Add date text
    draw.text(date_position, date_string, font=date_font, fill=date_color)

    # Add description text, wrapped to fit within the image width
    max_width = background.width - 100  # Allow some margin
    description_lines = textwrap.fill(description_string, width=40)
    draw.text(description_position, description_lines, font=description_font, fill=description_color)
    
    # Save the output image
    background.save(output_path)

# Example usage
background_path = "paper_texture.jpg"
title_string = "Sample Title"
date_string = "June 29, 2024"
description_string = "This is a sample description that will be wrapped and placed on the image. Lalalala lalalal alalaal"
output_path = "output_image.jpg"

create_image_with_text(title_string, date_string, description_string)