#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import requests
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V3
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:

    url = "https://api.carbonintensity.org.uk/intensity"
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Retrieve the carbon intensity index (e.g., 'low', 'moderate', etc.)
        carbon_intensity = data['data'][0]['intensity']['index']

        # Store the retrieved info as text in a variable
        carbon_intensity_status = f"The current carbon intensity is: {carbon_intensity}"

        # Print the result
        print(carbon_intensity_status)

        logging.info("epd2in13_V3 Demo")

        epd = epd2in13_V3.EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear(0xFF)

        font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 45)

        image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
        draw = ImageDraw.Draw(image)

        # num=0
        # while(True):
        draw.text((0,0), str(carbon_intensity), font = font15, fill = 0)
        draw.text((0,122), str(carbon_intensity), font = font15, fill = 0)
        epd.display(epd.getbuffer(image))
        time.sleep(15)
            # num=num+1
            # if(num==15):
            #     break


        logging.info("Clear...")
        epd.init()
        epd.Clear(0xFF)
    
        logging.info("Goto Sleep...")
        epd.sleep()
    
    else:
        # Handle errors
        print(f"Failed to retrieve data: {response.status_code}")


except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V3.epdconfig.module_exit(cleanup=True)
    exit()