import os
from dotenv import load_dotenv
from PIL import ImageFont
from datetime import timezone, timedelta
load_dotenv()

picdir = "assets/pic"
icondir = "assets/icons"
font = "assets/fonts/Font.ttc"
base_url = 'http://api.openweathermap.org/data/2.5/onecall?' 
key = os.getenv("API_KEY")
latitude = os.getenv("LATITUDE")
longitude = os.getenv("LONGITUDE")
units = os.getenv("UNITS")
utc_offset = int(os.getenv("UTC_OFFSET"))
time_zone = timezone(timedelta(hours=utc_offset))
api_url = f"{base_url}lat={latitude}&lon={longitude}&units={units}&appid={key}"
font22 = ImageFont.truetype(font, 22)
font30 = ImageFont.truetype(font, 30)
font35 = ImageFont.truetype(font, 35)
font50 = ImageFont.truetype(font, 50)
font60 = ImageFont.truetype(font, 60)
font100 = ImageFont.truetype(font, 100)
font160 = ImageFont.truetype(font, 160)
black = "rgb(0,0,0)"
white = "rgb(255,255,255)"
grey = "rgb(235,235,235)"