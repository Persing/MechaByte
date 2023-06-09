import asyncio
import json
import logging
from typing import List

import discord
from discord import app_commands
from discord.ext import commands

import MechaByte.SentenceComparatorApi as sc
import MechaByte.MechaByteImpl as mb


class MechaByte(commands.Cog):
    def __init__(self, bot, store):
        self.impl = mb.MechaByteImpl(bot, store)
        self.bot = bot
        self.store = store
        self.response_gen = sc.SentenceComparator(store)

    async def questions_autocomplete(self,
                                     interaction: discord.Interaction,
                                     current: str
                                     ) -> List[app_commands.Choice[str]]:
        questions = self.store.get_all_keys(interaction.guild_id, "question")
        logging.debug(questions)
        return [
            app_commands.Choice(name=question, value=question)
            for question in questions if current.lower() in question.lower()
        ]

    @app_commands.command(name='ask')
    @app_commands.autocomplete(question=questions_autocomplete)
    async def ask(self, interaction: discord.Interaction, question: str):
        logging.info(f"Received command from {interaction.user}: {question}")
        await interaction.response.send_message(self.impl.ask_impl(interaction.guild_id, question))
        # try:
        #     response = await self.response_gen.get_response(interaction.guild_id, question)
        #     await interaction.response.send_message(content=response)
        # except Exception as e:
        #     logging.error(f"Error: {e}")
        #     await interaction.response.send_message(content="Oops, something went wrong. Please try again later.")

    @commands.command(name='add')
    async def add(self, ctx, *, qa_string):
        logging.info(f"Received command from {ctx.author}: {ctx.message.content}")

        # Parse the question and answer from the message
        # try:
        #     qa_data = json.loads(qa_string)
        # except ValueError:
        #     await ctx.send("Oops, I couldn't parse your question and answer. Please try again.")
        #     return
        #
        # try:
        #     # Store the question and answer in the key-value store
        #     for key, value in qa_data.items():
        #         self.store.set(ctx.guild.id, question, key, value)
        #
        #     response = "Successfully added question to my knowledge base."
        #     await ctx.send(response)
        # except Exception as e:
        #     logging.error(f"Error: {e}")
        #     await ctx.send("Oops, something went wrong. Please try again later.")

    @app_commands.command(name='get')
    async def get_all(self, interaction: discord.Interaction):
        logging.info(f"Received command from {interaction.user}: GETALL")
        await interaction.response.send_message(self.impl.get_impl(interaction.guild_id))
        # try:
        #     # Get all the questions and answers from the key-value store
        #     qa_data = self.store.get_all_keys(interaction.guild.id, "question")
        #
        #     if len(qa_data) == 0:
        #         await interaction.response.send_message("I haven't learned anything yet.")
        #         return
        #
        #     response = "Here are all the questions and answers I know:\n"
        #     for key in qa_data:
        #         response += f"{key}\n"
        #
        #     await interaction.response.send_message(response)
        # except Exception as e:
        #     logging.error(f"Error: {e}")
        #     await interaction.response.send_message("Oops, something went wrong. Please try again later.")

    @commands.command(name='delete', help='Delete a Question Answer pair from the knowledge base.')
    async def delete(self, ctx, *, question):
        logging.info(f"Received command from {ctx.author}: {ctx.message.content}")
        try:
            # Delete the question and answer from the key-value store
            result = self.store.delete(ctx.guild.id, question)
            if result:
                response = "Successfully deleted question from my knowledge base."
            else:
                response = "I don't know that question. I have not removed anything from my knowledge base."
            await ctx.send(response)
        except Exception as e:
            logging.error(f"Error: {e}")
            await ctx.send("Oops, something went wrong. Please try again later.")

    @commands.command(name='clear', help='Clear the knowledge base.')
    async def clear(self, ctx):
        logging.info(f"Received command from {ctx.author}: {ctx.message.content}")
        try:
            # Prompt the user for confirmation
            response = "Are you sure you want to clear my knowledge base? This action cannot be undone. Reply 'yes' to confirm, or anything else to cancel."
            await ctx.reply(response)

            # Wait for the user's response
            def check(msg1):
                return msg1.author == ctx.author and msg1.channel == ctx.channel

            try:
                msg = await self.bot.wait_for('message', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                response = "Okay, I will not clear my knowledge base."
                await ctx.send(response)
                return

            if msg.content.lower() == 'yes':
                # Clear the key-value store
                self.store.delete_all(ctx.guild.id)

                response = "Successfully cleared my knowledge base."
                await ctx.send(response)
            else:
                response = "Okay, I will not clear my knowledge base."
                await ctx.send(response)

        except Exception as e:
            logging.error(f"Error: {e}")
            await ctx.send("Oops, something went wrong. Please try again later.")

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('Connected to Discord!')
