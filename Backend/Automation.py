from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

# Load environment variables from .env file
load_dotenv()

GroqAPIKey = os.getenv("GROQ_API_KEY")

# Define CSS classes for parsing specific elements in HTML content
classes = ["zCubwf", "hgKElc", "LTKOO sy7ric", "Z0Lcw", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta", "IZ6rdc",
           "O5uRd LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers_table", "dDoNo ikb4Bb gsrt", "sXLaOe", "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

# Define a web agent for making web requests
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 "

# Initialize groq client 
client = Groq(api_key = GroqAPIKey)

# Predefined professional responses for user interactions
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there anything else I can help you with",
    "I'm at your service for any additional questions or supports you may need. Don't hesitate to ask ",
]

# List of messages 
messages = []

# System messages for providing context to chatbot
