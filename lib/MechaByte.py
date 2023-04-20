import json
from typing import List

import discord
from discord import app_commands
from discord.ext import commands

import lib.sen_cmp_api as sc


class MechaByte(commands.Cog):
    def __init__(self, store):
        self.store = store
        self.response_gen = sc.SentenceComparator(store)
        # self.bot = bot

    # @commands.Cog.listener('on_message')
    # async def on_message(self, message):
    #     # If the message is from the bot itself, ignore it.
    #     if message.author == self.user:
    #         return
    #
    #     print(f"Received message from {message.author}: {message.content}")

    async def questions_autocomplete(self,
                                     interaction: discord.Interaction,
                                     current: str
                                     ) -> List[app_commands.Choice[str]]:
        questions = self.store.get_all_keys()
        print(questions)
        return [
            app_commands.Choice(name=question, value=question)
            for question in questions if current.lower() in question.lower()
        ]

    @app_commands.command(name='re')
    @app_commands.autocomplete(question=questions_autocomplete)
    async def re(self, interaction: discord.Interaction, question: str):
        print(f"Received command from {interaction.user}: {question}")
        try:
            response = await self.response_gen.get_response(question)
            await interaction.response.send_message(content=response)
        except Exception as e:
            print(f"Error: {e}")
            await interaction.response.send_message(content="Oops, something went wrong. Please try again later.")

    async def fruit_autocomplete(self,
            interaction: discord.Interaction,
            current: str,
    ) -> List[app_commands.Choice[str]]:
        fruits = ['Banana', 'Pineapple', 'Apple', 'Watermelon', 'Melon', 'Cherry']
        return [
            app_commands.Choice(name=fruit, value=fruit)
            for fruit in fruits if current.lower() in fruit.lower()
        ]

    @app_commands.command()
    @app_commands.autocomplete(fruit=fruit_autocomplete)
    async def fruits(self, interaction: discord.Interaction, fruit: str):
        await interaction.response.send_message(f'Your favourite fruit seems to be {fruit}')

    @commands.command(name='add')
    async def add(self, ctx, *, qa_string):
        print(f"Received command from {ctx.author}: {ctx.message.content}")

        # Parse the question and answer from the message
        try:
            qa_data = json.loads(qa_string)
        except ValueError:
            await ctx.send("Oops, I couldn't parse your question and answer. Please try again.")
            return

        try:
            # Store the question and answer in the key-value store
            for key, value in qa_data.items():
                self.store.set(key, value)

            response = "Successfully added question to my knowledge base."
            await ctx.send(response)
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send("Oops, something went wrong. Please try again later.")

    @app_commands.command(name='get')
    async def get_all(self, ctx):
        print(f"Received command from {ctx.author}: {ctx.message.content}")

        try:
            # Get all the questions and answers from the key-value store
            qa_data = self.store.get_all_keys()

            response = "Here are all the questions and answers I know:\n"
            for key in qa_data:
                response += f"{key}\n"

            await ctx.send(response)
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send("Oops, something went wrong. Please try again later.")

    @commands.command(name='delete', help='Delete a Question Answer pair from the knowledge base.')
    async def delete(self, ctx, *, question):
        print(f"Received command from {ctx.author}: {ctx.message.content}")
        try:
            # Delete the question and answer from the key-value store
            result = self.store.delete(question)
            if result:
                response = "Successfully deleted question from my knowledge base."
            else:
                response = "I don't know that question. I have not removed anything from my knowledge base."
            await ctx.send(response)
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send("Oops, something went wrong. Please try again later.")

    @commands.command(name='clear', help='Clear the knowledge base.')
    async def clear(self, ctx):
        print(f"Received command from {ctx.author}: {ctx.message.content}")
        try:
            # Prompt the user for confirmation
            response = "Are you sure you want to clear my knowledge base? This action cannot be undone. Reply 'yes' to confirm, or anything else to cancel."
            await ctx.send(response)

            # Wait for the user's response
            def check(msg1):
                return msg1.author == ctx.author and msg1.channel == ctx.channel

            msg = await self.bot.wait_for('message', check=check)

            if msg.content.lower() == 'yes':
                # Clear the key-value store
                self.store.clear()

                response = "Successfully cleared my knowledge base."
                await ctx.send(response)
            else:
                response = "Okay, I will not clear my knowledge base."
                await ctx.send(response)

        except Exception as e:
            print(f"Error: {e}")
            await ctx.send("Oops, something went wrong. Please try again later.")

    @commands.Cog.listener()
    async def on_ready(self):
        print('Connected to Discord!')

        from discord.ext.commands import is_owner, Context
