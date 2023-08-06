"""
Module that contains the main functions for opening the websites
"""
import webbrowser
import time
import random

sites = [
    'https://web.whatsapp.com',
    'https://primevideo.com',
    'https://amazon.com','https://discord.com',
    'https://instagram.com','https://github.com',
    'https://google.com',
    'https://youtube.com',
    'https://facebook.com',
    'https://netflix.com',
    'https://gmail.com',
    'https://docs.google.com'
]


class Virus:
    def __open_website(duration):
        t = 0
        while t <= duration_:
            webbrowser.open(random.choice(sites))
            time.sleep(1)
            t += 1

    def start(duration = 10): #Default site type is 'sfw' and duration is 10 minutes
        __open_website(duration*60)
