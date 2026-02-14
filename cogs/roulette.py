import random
import asyncio
import discord
from discord.ext import commands

class Roulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roulette")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def roulette(self, ctx):
        # Проверка голосового канала
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send("❌ Ты должен быть в голосовом канале, чтобы играть!")
            return

        await ctx.send("🎲 Крутим рулетку...")
        await asyncio.sleep(2)

        chamber = random.randint(1, 6)

        if chamber == 1:
            await ctx.send("💥 БАХ! Не повезло... Ты вылетаешь из голосового!")
            await ctx.author.move_to(None)
        else:
            await ctx.send("😎 Повезло! Ты остаёшься в голосовом.")

async def setup(bot):
    await bot.add_cog(Roulette(bot))
