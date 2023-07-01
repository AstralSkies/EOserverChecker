# Made by Smoker 7/1/2023


# Import required libraries
import discord
import requests
from bs4 import BeautifulSoup
import asyncio

# Your bot's token and channel ID. Be sure to replace these with your own.
TOKEN = ' '
CHANNEL_ID =   # replace with your channel ID

# Discord Intents are a feature on Discord that allows bots to track and monitor certain events and actions.
intents = discord.Intents.default()

# Initializing the discord client
client = discord.Client(intents=intents)

# Function to check the status of the server
def check_server_status():
    # URL of the website you want to check
    url = "https://game.endless-online.com/server.html"
    
    # Send a GET request
    response = requests.get(url)

    # If the GET request is successful, status_code will be 200
    if response.status_code == 200:
        # Parse the html response
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Finding the 'font' tag with color attribute set to '#cc0000'
        server_status_element = soup.find('font', {'color': '#cc0000'})

        # Check if the server status element is found
        if server_status_element:
            # Get the server status
            server_status = server_status_element.text.strip().lower()
            
            # Check if the server status is online or offline
            if server_status == 'online':
                return 'The server is online.'
            elif server_status == 'offline':
                return 'The server is offline.'
            else:
                return f'Unexpected server status: {server_status}'
        else:
            return 'Server status element not found.'
    else:
        return 'Website not accessible.'

# Function to handle the event when the bot has successfully connected to the discord server
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    # An infinite loop that checks the server status every 20 seconds
    while True:
        status = check_server_status()
        channel = client.get_channel(CHANNEL_ID)
        
        # Send the server status to the channel
        await channel.send(status)
        
        # Wait for 20 seconds before the next check
        await asyncio.sleep(20)

# Start the bot
client.run(TOKEN)
