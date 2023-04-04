
import os

from dotenv import load_dotenv
import discord

from discord import app_commands
from src.discordBot import DiscordClient, Sender
from src.logger import logger
from src.chatgpt import ChatGPT, DALLE
from src.models import OpenAIModel
from src.memory import Memory
from src.server import keep_alive

load_dotenv()

models = OpenAIModel(api_key=os.getenv('OPENAI_API'), model_engine=os.getenv('OPENAI_MODEL_ENGINE'))

memory = Memory(system_message=os.getenv('SYSTEM_MESSAGE'))
chatgpt = ChatGPT(models, memory)
dalle = DALLE(models)


def run():
    client = DiscordClient()
    sender = Sender()

    @client.tree.command(name="chat", description="Have a chat with ChatGPT")
    @app_commands.choices(choices=[
        app_commands.Choice(name="No Effect", value="None"),
        app_commands.Choice(name="Midjourney", value="Midjourney"),
        app_commands.Choice(name="BlockChain", value="BlockChain"),
    ])
    async def chat(interaction: discord.Interaction, *, message: str, choices: app_commands.Choice[str]):
        user_id = interaction.user.id
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        if choices.value == "None":
            receive = chatgpt.get_response(user_id, message)
        elif choices.value == "Midjourney":
            receive = chatgpt.get_midjourney_response(user_id, message)
        elif choices.value == "BlockChain":
            receive = chatgpt.get_block_response(user_id, message)
        else:
            receive = chatgpt.get_response(user_id, message)
        await sender.send_message(interaction, message, receive)

    # @client.tree.command(name="mj", description="Generate a chat with ChatGPT for midjourney")
    # async def midjourney(interaction: discord.Interaction, *, message: str):
    #     user_id = interaction.user.id
    #     if interaction.user == client.user:
    #         return
    #     await interaction.response.defer()
    #     receive = chatgpt.get_midjourney_response(user_id, message)
    #     await sender.send_message(interaction, message, receive)

    @client.tree.command(name="imagine", description="Generate image from text")
    async def imagine(interaction: discord.Interaction, *, prompt: str):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        image_url = dalle.generate(prompt)
        await sender.send_image(interaction, prompt, image_url)

    @client.tree.command(name="reset", description="Reset ChatGPT conversation history")
    async def reset(interaction: discord.Interaction):
        user_id = interaction.user.id
        logger.info(f"resetting memory from {user_id}")
        try:
            chatgpt.clean_history(user_id)
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send(f'> Reset ChatGPT conversation history < - <@{user_id}>')
        except Exception as e:
            logger.error(f"Error resetting memory: {e}")
            await interaction.followup.send('> Oops! Something went wrong. <')

    client.run(os.getenv('DISCORD_TOKEN'))


if __name__ == '__main__':
    keep_alive()
    run()
