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
    if member.voice and member.voice.channel:
        await member.move_to(None)
        try:
            await member.send(f"⏰ Время вышло! Ты был отключён от голосового канала ({minutes} мин).")
        except:
            pass
    timers.pop(member.id, None)

@bot.command()
async def timer(ctx):
    if not ctx.author.voice or not ctx.author.voice.channel:
        return await ctx.send("Ты должен быть в голосовом канале.")

    # если уже есть активный таймер — сразу говорим
    if ctx.author.id in timers:
        return await ctx.send("У тебя уже стоит таймер! Используй **!cancel**, если хочешь поставить новый.")

    view = discord.ui.View(timeout=60)

    options = [
        ("5 минут", 5),
        ("10 минут", 10),
        ("15 минут", 15),
        ("30 минут", 30),
        ("45 минут", 45),
        ("1 час", 60),
        ("1.5 часа", 90),
        ("2 часа", 120),
        ("3 часа", 180),
        ("4 часа", 240),
    ]

    for label, mins in options:
        button = discord.ui.Button(label=label, style=discord.ButtonStyle.green)

        async def callback(interaction, m=mins, l=label):
            if interaction.user != ctx.author:
                return await interaction.response.send_message("Это не твоя кнопка!", ephemeral=True)

            task = bot.loop.create_task(kick_after_delay(ctx.author, m))
            timers[ctx.author.id] = task

            time_text = l
            await interaction.response.edit_message(
                content=f"⏰ {ctx.author.mention}, через **{time_text}** тебя кикнет из голосовки.\nОтменить → **!cancel**",
                view=None
            )

        button.callback = callback
        view.add_item(button)

    await ctx.send("Выбери время отключения:", view=view)

# ─────── КОМАНДА ОТМЕНЫ ───────
@bot.command()
async def cancel(ctx):
    if ctx.author.id in timers:
        timers[ctx.author.id].cancel()
        timers.pop(ctx.author.id)
        await ctx.send(f"⏰ {ctx.author.mention}, таймер успешно отменён.")
    else:
        await ctx.send("У тебя нет активного таймера.")

@bot.event
async def on_ready():
    print(f"Бот {bot.user} онлайн!")
    print("Команды:")
    print("   !timer  → меню с кнопками")
    print("   !cancel → отменить текущий таймер")




import os
bot.run(os.getenv("TOKEN"))
