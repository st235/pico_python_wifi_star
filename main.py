import uasyncio as asyncio
import time

import plasma
from plasma import plasma_stick

from machine import Pin

from color_animation import ColorAnimation
from snowflake_animation import SnowflakeAnimation
from sparkling_animation import SparklingAnimation
from no_op_animation import NoOpAnimation

from wifi_credentials import WifiCredentials
from wifi_connector import WifiConnector

from http_server import HttpServer
from url_utils import HTTP_CODE_200_OK, HTTP_CODE_400_BAD_REQUEST

led = Pin(15, Pin.OUT)

NUM_LEDS = 50
led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma_stick.DAT, color_order=plasma.COLOR_ORDER_RGB)
led_strip.start()

animation = NoOpAnimation(led_strip)

def clear_strip():
    for i in range(NUM_LEDS):
        led_strip.set_rgb(i, 0, 0, 0)

def on_connecting_to_wifi():
    for i in range(NUM_LEDS):
        led_strip.set_rgb(i, 255, 255, 255)
        time.sleep(0.02)
    for i in range(NUM_LEDS):
        led_strip.set_rgb(i, 0, 0, 0)

def connect_to_wifi():
    wifi_credentials = WifiCredentials.from_ini('wifi_credentials.ini')
    wifi_connector = WifiConnector(network_ssid=wifi_credentials.network_ssid,
                                network_password=wifi_credentials.network_password)

    connected = wifi_connector.connect(on_connecting_to_wifi)

    if not connected:
        # Live lock if is not connected.
        while True:
            for i in range(NUM_LEDS):
                led_strip.set_rgb(i, 255, 0, 0)
            time.sleep(1)
            clear_strip()
            time.sleep(1)

    clear_strip()
    return wifi_connector

def on_play_snowflake(queries):
    global animation
    animation = SnowflakeAnimation(led_strip)

    return HTTP_CODE_200_OK, { 'started': True, 'playing': 'snowflake' }

def on_play_sparkling(queries):
    global animation

    color = [240, 250, 255]
    if 'sparkling_color' in queries:
        color = queries['sparkling_color']

    animation = SparklingAnimation(led_strip, sparkle_colour=color)

    return HTTP_CODE_200_OK, { 'started': True, 'playing': 'sparkling', 'color': color }

def on_play_solid_color(queries):
    global animation

    if 'value' not in queries:
        return HTTP_CODE_400_BAD_REQUEST, { 'error_message': 'value query parameter is missing.' }

    color = queries['value']
    animation = ColorAnimation(led_strip, color)

    return HTTP_CODE_200_OK, { 'started': True, 'playing': 'solid color', 'color': color }

def on_play_stop(queries):
    global animation
    animation = NoOpAnimation(led_strip)
    return HTTP_CODE_200_OK, { 'started': False }

async def main():
    print('Connecting to WiFi...')
    wifi_connector = connect_to_wifi()
    print('Connected to:', wifi_connector.public_interface)

    http_server = HttpServer()

    http_server.on('/strip/play/snowflake', on_play_snowflake)
    http_server.on('/strip/play/sparkling', on_play_sparkling)
    http_server.on('/strip/play/color', on_play_solid_color)
    http_server.on('/strip/stop', on_play_stop)

    print('Setting up webserver...')
    asyncio.create_task(http_server.create_async())
    while True:
        if animation is not None:
            animation.next_step()
        await asyncio.sleep(0.01)
        
try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()

