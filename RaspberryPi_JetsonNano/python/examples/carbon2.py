import time
import requests
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in13_V3

# Constants
API_URL = "https://api.carbonintensity.org.uk/intensity"
MIX_URL = "https://api.carbonintensity.org.uk/generation"
REFRESH_INTERVAL = 1800  # 30 minutes in seconds
FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

# Initialize e-ink display
epd = epd2in13_V3.EPD()
epd.init()
epd.Clear(0xFF)

# Utility functions
def fetch_carbon_intensity():
    response = requests.get(API_URL + "/")
    return response.json()['data'][0]

def fetch_energy_mix():
    response = requests.get(MIX_URL + "/")
    return response.json()['data']['generationmix']

def display_text(epd, text):
    image = Image.new('1', (epd.height, epd.width), 255)  # Create a white canvas
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_PATH, 20)
    draw.text((10, 10), text, font=font, fill=0)
    epd.display(epd.getbuffer(image))

def display_energy_mix(epd, mix):
    image = Image.new('1', (epd.height, epd.width), 255)  # Create a white canvas
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_PATH, 16)
    
    draw.text((10, 10), "Energy Mix:", font=font, fill=0)
    y = 30
    for source in mix:
        text = f"{source['fuel']}: {source['perc']}%"
        draw.text((10, y), text, font=font, fill=0)
        y += 20

    epd.display(epd.getbuffer(image))

def display_carbon_intensity(epd, intensity):
    image = Image.new('1', (epd.height, epd.width), 255)  # Create a white canvas
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_PATH, 20)
    
    draw.text((10, 10), "Carbon Intensity:", font=font, fill=0)
    text = f"{intensity['intensity']['actual']} gCO2/kWh"
    draw.text((10, 40), text, font=font, fill=0)

    epd.display(epd.getbuffer(image))

def main():
    screens = [display_energy_mix, display_carbon_intensity]
    screen_index = 0
    
    while True:
        current_time = datetime.now()
        
        if current_time.minute == 0 or current_time.minute == 30:
            try:
                # Fetch data
                energy_mix = fetch_energy_mix()
                carbon_intensity = fetch_carbon_intensity()

                # Display current screen
                if screen_index == 0:
                    display_energy_mix(epd, energy_mix)
                elif screen_index == 1:
                    display_carbon_intensity(epd, carbon_intensity)

                # Rotate screen index
                screen_index = (screen_index + 1) % len(screens)

            except Exception as e:
                display_text(epd, f"Error: {str(e)}")
        
        # Sleep until the next 30 minute mark
        time.sleep(REFRESH_INTERVAL - time.time() % REFRESH_INTERVAL)

if __name__ == "__main__":
    main()



