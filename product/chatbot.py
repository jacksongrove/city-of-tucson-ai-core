from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, File
from responses import get_response
import asyncio
import re

# STEP 0: LOAD OUR TOKEN FROM SOMEWHERE SAFE
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# STEP 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
intents.messages = True
intents.reactions = True
intents.guilds = True
intents.members = True
client: Client = Client(intents=intents)

syllabus_content: Final[dict] = {}


# STEP 2: MESSAGE FUNCTIONALITY
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


# STEP 3: HANDLING THE STARTUP FOR OUR BOT
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')


# STEP 4: HANDLING INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')

    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.lower().endswith(('.pdf', '.docx', '.txt')):
                await process_syllabus(attachment)

    await send_message(message, user_message)


async def process_syllabus(attachment: File) -> None:
    # Download the file and process it based on its type
    try:
        syllabus_path = f'/tmp/{attachment.filename}'
        await attachment.save(syllabus_path)
        if attachment.filename.lower().endswith('.pdf'):
            await extract_pdf_content(syllabus_path)
        elif attachment.filename.lower().endswith('.docx'):
            await extract_docx_content(syllabus_path)
        elif attachment.filename.lower().endswith('.txt'):
            await extract_txt_content(syllabus_path)
    except Exception as e:
        print(e)


async def extract_pdf_content(file_path: str) -> None:
    # Implement PDF content extraction logic here
    pass


async def extract_docx_content(file_path: str) -> None:
    # Implement DOCX content extraction logic here
    pass


async def extract_txt_content(file_path: str) -> None:
    # Implement TXT content extraction logic here
    pass


# Update the response function to check for syllabus content
def get_response(user_message: str) -> str:
    if 'syllabus' in user_message.lower():
        # Implement logic to search for syllabus content and return a relevant response
        for key, value in syllabus_content.items():
            if re.search(user_message, key, re.IGNORECASE):
                return value
        return "Sorry, I couldn't find any relevant information in the syllabus."
    else:
        return "This is a general response."


# STEP 5: MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()
