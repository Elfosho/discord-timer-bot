import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

timers = {}

async def kick_after_delay(member, minutes):
    await asyncio.sleep(minutes * 60)
    # Просто кикаем, без всяких сообщений в ЛС
    if member.voice and member.voice.channel:
        await member.move_to(None)
    timers.pop(member.id, None)

class TimerView(discord.ui.View):
    def __init__(self, author):
        super().__init__(timeout=120)
        self.author = author

    @discord.ui.button(label="5 минут", style=discord.ButtonStyle.green)
    async def five(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.start_timer(interaction, 5)

    @discord.ui.button(label="10 минут", style=discord.ButtonStyle.green)
    async def ten(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.start_timer(interaction, 10)

    @discord.ui.button(label="15 минут", style=discord.ButtonStyle.green)
    async def fifteen(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.start_timer(interaction, 15)

    @discord.ui.button(label="30 минут", style=discord.ButtonStyle.green)
    async def thirty(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.start_timer(interaction, 30)

    @discord.ui.button(label="1 час", style=discord.ButtonStyle.blurple)
    async def one_hour(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.start_timer(interaction, 60)

    @discord.ui.button(label="2 часа", style=discord.ButtonStyle.blurple)
    async def two_hours(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.start_timer(interaction, 120)

    @discord.ui.button(label="4 часа", style=discord.ButtonStyle.blurple)
    async def four_hours(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.start_timer(interaction, 240)

    @discord.ui.button(label="Своё время", style=discord.ButtonStyle.gray)
    async def custom(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(CustomTimerModal(self.author))

    @discord.ui.button(label="Отмена", style=discord.ButtonStyle.red, row=4)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.author.id:
            await interaction.response.edit_message(content="Выбор отменён.", view=None)
        else:
            await interaction.response.send_message("Это не твоё меню!", ephemeral=True)

    async def start_timer(self, interaction: discord.Interaction, minutes: int):
        if interaction.user.id != self.author.id:
            return await interaction.response.send_message("Не твоя кнопка!", ephemeral=True)

        if self.author.id in timers:
            timers[self.author.id].cancel()

        task = bot.loop.create_task(kick_after_delay(self.author, minutes))
        timers[self.author.id] = task

        time_text = f"{minutes} мин" if minutes < 60 else f"{minutes//60} ч {minutes%60} мин" if minutes%60 else f"{minutes//60} ч"
        await interaction.response.edit_message(
            content=f"⏰ {self.author.mention}, через **{time_text}** тебя молча кикнет из голосовки.\nОтменить → `!cancel`",
            view=None
        )

class CustomTimerModal(discord.ui.Modal, title="Своё время (в минутах)"):
    def __init__(self, author):
        super().__init__()
        self.author = author

    minutes = discord.ui.TextInput(
        label="Через сколько минут кикнуть?",
        placeholder="Например: 37",
        max_length=4
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            mins = int(self.minutes.value)
            if not 1 <= mins <= 1440:
                return await interaction.response.send_message("От 1 до 1440 минут.", ephemeral=True)
        except ValueError:
            return await interaction.response.send_message("Введи число.", ephemeral=True)

        if self.author.id in timers:
            timers[self.author.id].cancel()

        task = bot.loop.create_task(kick_after_delay(self.author, mins))
        timers[self.author.id] = task

        time_text = f"{mins} мин" if mins < 60 else f"{mins//60} ч {mins%60} мин" if mins%60 else f"{mins//60} ч"
        await interaction.response.send_message(
            f"⏰ {self.author.mention}, через **{time_text}** тебя кикнет из голоса.\nОтменить → `!cancel`"
        )

@bot.command()
async def timer(ctx):
    if not ctx.author.voice or not ctx.author.voice.channel:
        return await ctx.send("Ты не в голосовом канале.")

    if ctx.author.id in timers:
        return await ctx.send("У тебя уже стоит таймер. Используй `!cancel`.")

    view = TimerView(ctx.author)
    await ctx.send("Выбери время отключения:", view=view)

@bot.command()
async def cancel(ctx):
    if ctx.author.id in timers:
        timers[ctx.author.id].cancel()
        timers.pop(ctx.author.id)
        await ctx.send(f"⏰ {ctx.author.mention}, таймер отменён.")
    else:
        await ctx.send("Нет активного таймера.")

@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Game(name="кикну через !timer")
    )
    print(f"Бот {bot.user} онлайн — статус установлен")

import os
bot.run(os.getenv("TOKEN"))



