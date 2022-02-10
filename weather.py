#! usr/bin/python
import os
from lib.waveshare_epd import epd7in5_V2
from datetime import datetime
import time
from PIL import Image, ImageDraw
import requests
import logging
from config import *


def write_screen(epd, image_file):
    # Write to screen
    h_image = Image.new("1", (epd.width, epd.height), 255)
    # Open the template
    screen_output_file = Image.open(image_file)
    # Initialize the drawing context with template as background
    h_image.paste(screen_output_file, (0, 0))
    epd.init()
    epd.display(epd.getbuffer(h_image))


def draw_error(epd):
    error_source = "INTERNAL"
    # Initialize drawing
    error_image = Image.new("1", (epd.width, epd.height), 255)
    # Initialize the drawing
    draw = ImageDraw.Draw(error_image)
    draw.text((100, 150), error_source + " ERROR", font=font50, fill=black)
    draw.text((100, 300), "Retrying in 30 seconds", font=font22, fill=black)
    current_time = datetime.now().strftime("%H:%M")
    draw.text((300, 365), "Last Refresh: " +
              str(current_time), font=font50, fill=black)
    # Save the error image
    error_image_file = f"{picdir}/error.png"
    error_image.save(error_image_file)
    # Close error image
    error_image.close()
    # Write error to screen
    return error_image_file


def draw_image(epd, display_data):
   # Open template file
    template = Image.open(os.path.join(picdir, "template.png"))
    # Initialize the drawing context with template as background
    draw = ImageDraw.Draw(template)
    # Draw top left box
    # Paste the image
    template.paste(display_data["icon_image"], (40, 15))
    # Place a black rectangle outline
    draw.rectangle((25, 20, 225, 180), outline=black)
    # Draw text
    draw.text((30, 200), display_data["report"], font=font22, fill=black)
    draw.text((30, 240), display_data["precip_prob"], font=font30, fill=black)
    # Draw top right box
    draw.text((375, 35), display_data["temperature"], font=font160, fill=black)
    draw.text((350, 210), display_data["feels_like"], font=font50, fill=black)
    # Draw bottom left box
    draw.text((35, 325), display_data["high"], font=font50, fill=black)
    draw.rectangle((170, 385, 265, 387), fill=black)
    draw.text((35, 390), display_data["low"], font=font50, fill=black)
    # Draw bottom middle box
    draw.text((345, 340), display_data["humidity"], font=font30, fill=black)
    draw.text((345, 400), display_data["wind"], font=font30, fill=black)
    # Draw bottom right box
    draw.text((627, 330), "UPDATED", font=font35, fill=white)
    draw.text(
        (627, 375), display_data["current_time"], font=font60, fill=white)
    # Save the image for display as PNG
    screen_output_file = f"{picdir}/screen_output.png"
    template.save(screen_output_file)
    # Close the template file
    template.close()
    # Write to screen
    return screen_output_file


def parse_response(response):
    degree_sign = u"\N{DEGREE SIGN}"
    data = response.json()
    current = data["current"]
    current_temp = int(current["temp"])
    feels_like = int(current["feels_like"])
    humidity = current["humidity"]
    wind = current["wind_speed"]
    weather = current["weather"]
    report = weather[0]["description"]
    icon_code = weather[0]["icon"]
    daily = data["daily"]
    daily_precip_float = daily[0]["pop"]
    daily_precip_percent = daily_precip_float * 100
    daily_temp = daily[0]["temp"]
    max_temp = int(daily_temp["max"])
    min_temp = int(daily_temp["min"])
    image_file = f"assets/pic/icons/{icon_code}.png"
    current_time = datetime.now(time_zone).strftime("%l:%M")

    return {
        "temperature": f"{current_temp}{degree_sign}F",
        "low": f"Low:  {min_temp}{degree_sign}F",
        "high": f"High: {max_temp}{degree_sign}F",
        "feels_like": f"Feels like: {feels_like}{degree_sign}F",
        "humidity": f"Humidity: {humidity}%",
        "wind": f"Wind: {wind} MPH",
        "precip_prob": f"Precip: {daily_precip_percent}%",
        "report": f"Now: {report.title()}",
        "icon_image": Image.open(image_file),
        "current_time": current_time
    }


def weather():
    logging.basicConfig(filename="weather.log",
                        encoding="utf-8", level=logging.DEBUG)
    logging.info("Awake: Initializing and Clearing screen")
    epd = epd7in5_V2.EPD()
    epd.init()
    epd.Clear()

    try:
        display_data = parse_response(requests.get(api_url))
        image_file = draw_image(epd, display_data)

    except Exception as e:
        logging.error(e)
        image_file = draw_error(epd)

    finally:
        logging.info("Attempting to write to screen")
        write_screen(epd, image_file)
        logging.info("Going back to sleep..")
        epd.sleep(refresh_seconds - 1)


if __name__ == "__main__":
    while True:
        weather()
        time.sleep(refresh_seconds)
