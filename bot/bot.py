import discord
import matplotlib.pyplot as plt
import io
import os
from dotenv import load_dotenv
from dependencies.database import Database
from query_repository.player_queries import player_queries_repo
import seaborn as sns
import numpy as np

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DB_PATH = "bot/db_files/fbref22_23_top_outfield.db"

db=Database(DB_PATH)
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

    if message.content.startswith("!player_data"):
        # Parse the plot command and extract the data
        command = message.content
        player_name = command.replace("!player_data ", "")
        player_data = player_queries_repo.get_player_data_all(player=player_name, session=db)
        # db.close()
        await message.channel.send(player_data)

    if message.content.startswith("!player_compare"):
        # Parse the plot command and extract the data
        command, player_names = message.content.split(" ", 1)
        player_names = player_names.split("|")
        player_list = [name.strip() for name in player_names]
        player_data = player_queries_repo.get_players_ga_dict(players=player_list, session=db)
        # Set the plot style to a minimalistic theme
        sns.set(style='whitegrid')

        # Generate the horizontal bar plot
        fig, ax = plt.subplots(figsize=(10, 6))
        bar_positions = np.arange(len(player_list))
        bar_values = player_data.values()
        ax.barh(bar_positions, bar_values, color='dodgerblue')

        # Customize the plot
        ax.set_xlabel('G+A')
        ax.set_ylabel('Player')
        ax.set_title('Goals + Assists Comparison')

        # Set y-axis tick labels
        ax.set_yticks(bar_positions)
        ax.set_yticklabels(player_data.keys())

        # Remove spines
        sns.despine()

        # Save the plot image to a buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Send the plot image as a file
        await message.channel.send(file=discord.File(buffer, 'plot.png'))

        # Clear the plot for the next command
        plt.clf()

    if message.content.startswith("!player_compare_xG_90"):
        # Parse the plot command and extract the data
        command, player_names = message.content.split(" ", 1)
        player_names = player_names.split("|")
        player_list = [name.strip() for name in player_names]
        player_data = player_queries_repo.get_players_npxg_dict(players=player_list, session=db)
        # Set the plot style to a minimalistic theme
        sns.set(style='whitegrid')

        # Generate the horizontal bar plot
        fig, ax = plt.subplots(figsize=(10, 6))
        bar_positions = np.arange(len(player_list))
        bar_values = player_data.values()
        ax.barh(bar_positions, bar_values, color='dodgerblue')

        # Customize the plot
        ax.set_xlabel('npxG per 90')
        ax.set_ylabel('Players')
        ax.set_title('Non-penalty xG Comparison')

        # Set y-axis tick labels
        ax.set_yticks(bar_positions)
        ax.set_yticklabels(player_data.keys())

        # Remove spines
        sns.despine()

        # Save the plot image to a buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Send the plot image as a file
        await message.channel.send(file=discord.File(buffer, 'plot.png'))

        # Clear the plot for the next command
        plt.clf()


@client.event
async def on_disconnect():
    # Close the database connection when the bot disconnects
    db.close()
    print("Bot has disconnected. Database connection closed.")



client.run(TOKEN)
