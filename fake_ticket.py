from PIL import Image, ImageDraw, ImageFont, ImageFilter

def blur_region(image, left, upper, right, lower, blur=5):
    # Extract the region
    region = image.crop((left, upper, right, lower))

    # Apply a blur effect to the region
    blurred_region = region.filter(ImageFilter.GaussianBlur(radius=blur))

    # Paste the blurred region back into the original image
    image.paste(blurred_region, (left, upper))
    return image

def create_ticket(time_string, date_string):
    print("starting")
    # Define the dimensions of the ticket
    width, height = 800, 300
    ticket_color = (255, 255, 255)  # White background for the ticket

    image = Image.open("ticket.jpeg")

    # Resize the image to fit the specified dimensions
    r_width, r_height = 650,300
    resized_image = image.resize((r_width, r_height))
    # Apply a blur effect
    blurred_image = resized_image.filter(ImageFilter.GaussianBlur(radius=2))

    # Create a new image with white background
    img = Image.new('RGB', (width, height), color=ticket_color)
    draw = ImageDraw.Draw(img)

    # Define colors
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Define fonts
    try:
        font_large = ImageFont.truetype("arial.ttf", 40)
        font_medium = ImageFont.truetype("arial.ttf", 30)
        font_small = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Draw the black part of the ticket
    draw.rectangle([(0, 0), (600, 300)], fill=black)

    # Create the white part as a separate image and rotate it
    white_part = Image.new('RGB', (200, 300), color=white)
    white_draw = ImageDraw.Draw(white_part)

    # Add the vertical text "TICKET"
    white_draw.text((0, 50), "TICKET", fill=black, font=font_medium)
    white_draw.text((15, 100), "SEC", fill=black, font=font_small)
    white_draw.text((65, 100), "5", fill=black, font=font_medium)
    white_draw.text((10, 150), "ROW", fill=black, font=font_small)
    white_draw.text((70, 150), "12", fill=black, font=font_medium)
    white_draw.text((20, 200), "SEAT", fill=black, font=font_small)
    white_draw.text((70, 200), "28", fill=black, font=font_medium)

    # Rotate the white part by 90 degrees
    rotated_white_part = white_part.rotate(90, expand=1)

    # Paste the rotated white part onto the original image
    img.paste(rotated_white_part, (600, 0))

    img.paste(blurred_image)

    # Add "TICKET" text on black part
    img = blur_region(img, 50, 20, 200, 60)
    draw.text((50, 20), "TICKET", fill=white, font=font_large)

    # Add "ADMIT ONE" text on black part
    draw.text((450, 20), "ADMIT ONE", fill=white, font=font_medium)

    # Add section with Sec, Row, Seat and Price on black part
    img = blur_region(img, 50, 100, 550, 180, blur=7)
    draw.rectangle([(50, 100), (550, 180)], outline=white)
    draw.text((60, 110), "SEC", fill=white, font=font_small)
    draw.text((60, 140), "5", fill=white, font=font_medium)
    draw.text((160, 110), "ROW", fill=white, font=font_small)
    draw.text((160, 140), "12", fill=white, font=font_medium)
    draw.text((260, 110), "SEAT", fill=white, font=font_small)
    draw.text((260, 140), "28", fill=white, font=font_medium)
    draw.text((360, 110), "PRICE:", fill=white, font=font_small)
    draw.text((360, 140), "$8.99", fill=white, font=font_medium)

    # Add the date and time on black part
    img = blur_region(img, 50, 200, 150, 240)
    img = blur_region(img, 250, 200, 400, 240)
    draw.text((50, 200), time_string, fill=white, font=font_large)
    draw.text((250, 200), date_string, fill=white, font=font_large)

    draw.text((720, 30), "*", fill=black, font=font_medium)
    draw.text((720, 250), "*", fill=black, font=font_medium)

    # Display the image
    img.save("ticket_generated.jpg")

    # Optionally, save the image
    # img.save("ticket.png")
