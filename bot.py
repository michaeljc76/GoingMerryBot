import discord
from discord.ext import commands
import openai
import os


from dotenv import load_dotenv
from anytree import Node, RenderTree, search

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
openai.api_key = os.getenv('AI_KEY')

root = Node("root")

class Bot(discord.Client):
    async def on_ready(self):
        print(f'{self.user.name} is now running')

    async def on_message(self, message):
        print(f'{message.author} said: "{message.content}" ({message.channel})')

        if message.author == self.user:
            return

        command, user_message = None, None
        
        if message.content.startswith('!ai'):
            command = message.content.split(' ')[0]
            user_message = message.content.replace('!ai', '')
            print(command, user_message)

            if(user_message == ""):
                await message.channel.send("Please provide a prompt after !ai")
            elif command == '!ai':
                response = await generate_ai_response(prompt=user_message)
                await message.channel.send(response)

        if message.content.startswith('!translate'):
            command = message.content.split(' ')[0]
            user_message = message.content.replace('!translate', '')

            if(user_message == ""):
                await message.channel.send("Please provide a message after !translate")
            elif command == '!translate':
                language, sentence = user_message.split(' ', 1)
                translate_prompt = ("Translate the following text to " + language + ", only send the traslation:" + user_message)
                response = await generate_ai_response(prompt=translate_prompt)
                await message.channel.send(response)

        if message.content.startswith('!score'):
            (command, user_message) = get_command_and_message(message.content)
            channels = list(message.guild.text_channels)
            members = [member async for member in message.guild.fetch_members(limit=None)]
            root = Node("Data")

            for member in members:
                user_entry = Node(member.display_name, parent=root)

            for channel in channels:
                messages = [message async for message in channel.history(limit=None)]

                for message in messages:
                    author = message.author
                    node = search.find(root, lambda node: node.name is author.display_name)
                    value_points = 1

                    try:
                        name = node.children[0].name
                        value_points = int(name.replace('Score: ', ''))
                    except IndexError:
                        value_points = 1

                    roles_node = Node(name="Roles", parent=node)

                    for role in message.author.roles[1:]:
                        list_roles = list(roles_node.children)
                        list_roles.append(Node(name=role.name, parent=roles_node))
                        roles_node.children = list_roles

                    
                    node.children = [ Node(name="Score: " + str(1 + value_points), parent=node), roles_node]

            await message.channel.send(RenderTree(root).by_attr("name"))

        if message.content.startswith('!help'):
            await message.channel.send("""
                Available commands:
                `!ai`: Query the open api with a query
                `!help`: Display all available commands
                `!score`: Calculate the score of each user based on the last 300 messages
                `!translate`: Translate a sentence to English
            """)


def get_command_and_message(content):
    command = content.split(' ')[0]
    user_message = content.replace('!score ', '')

    return (command, user_message)

async def generate_ai_response(prompt):
    try:
        # Use OpenAI API to generate a response
        response = openai.completions.create(
            model="gpt-3.5-turbo-instruct",
            temperature=0.7,
            max_tokens=150,
            prompt=prompt,
        )

        response_dict = response.choices
        if response_dict and len(response_dict) > 0:
            prompt_response = response_dict[0].text
        return prompt_response

    except Exception as e:
        print(f"Error generating AI response: {e}")
        return "An error occurred while generating the response."

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = Bot(intents=intents)

print(client.guilds)
    
