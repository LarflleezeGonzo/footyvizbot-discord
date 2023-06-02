import discord
import matplotlib.pyplot as plt
import io
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# Create a new Discord client
intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("Bot is ready.")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!plot"):
        # Parse the plot command and extract the data
        command, data = message.content.split(" ", 1)
        values = list(map(int, data.split()))

        # Generate the plot
        plt.plot(values)
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.title("Plot")

        # Save the plot image to a buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)

        # Send the plot image as a file
        await message.channel.send(file=discord.File(buffer, "plot.png"))

        # Clear the plot for the next command
        plt.clf()
    if message.content.startswith('!hi'):
        # Respond with "Hi"
        await message.channel.send('Hi')

    
    if 'dyanesh' in message.content:
        # Respond with "Hi"
        await message.channel.send('Harini says hi')

# Replace 'YOUR_TOKEN' with your actual bot token


client.run(TOKEN)
