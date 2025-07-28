import disnake as discord
from disnake.ext import commands
import random
import numpy as np
from enum import Enum

intents=discord.Intents.all()
bot = commands.Bot(
    command_prefix='!', 
    intents=intents,
    default_install_types=discord.ApplicationInstallTypes(user=True,guild=True), 
    default_contexts=discord.InteractionContextTypes(bot_dm=True,guild=True,private_channel=True),
    #proxy="http://127.0.0.1:8830" # ignore this its just a leftover from me trying to get the bot working
    )

#slots functions
def spin(symbols_amount: int)->list[int]:
    reel = list(np.random.randint(low=1,high=symbols_amount+1,size=3))
    return reel

items = ["🍋","🍒","🍊","🍍","🥭","<:cantaloupe:1398171149359120426>","7️⃣"]

class Reel(Enum):
        LEMON = 1
        CHERRY = 2
        ORANGE = 3
        ANANAS = 4
        MANGO = 5
        CANTALOUPE = 6
        SEVEN = 7


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.slash_command(description="roll a n sided dice")
async def dice(ctx: discord.ApplicationCommandInteraction,sides):
    try:
        sides=int(sides)
    except:
        await ctx.send(f"erm actually thats not a valid integer",ephemeral=True)
        return
    if sides < 1:
        await ctx.send(f"You roll a d{sides}\n...it cliped through the table.")
    else:
        await ctx.send(f"You roll a d{sides}\nit landed on {random.randint(1,sides)}")


@bot.slash_command(description="chicken (WIP)")
async def chicken(ctx,guess: int):
    number=random.randint(1,20)
    if guess<1 or guess>20:
        await ctx.send(f"why are you guessing numbers out of the 1 to 20 range are you stupid")
    elif number==guess:
        await ctx.send(f"Congratulations, You Won!\nyour guess:{guess}\ncorrect number:{number}\ntotal attempts: not tracked yet")
    else:
        await ctx.send(f"You Lost\nyour guess:{guess}\ncorrect number:{number}\ntotal attempts: not tracked yet")

@bot.slash_command(description="gamble (WIP)")
async def slots(ctx: discord.ApplicationCommandInteraction):
    reel=spin(7)
    messag=""
    for i in reel:
        messag+=f"{items[i-1]} "
    await ctx.send(messag)

bot.run(open("token.txt").read(),reconnect=True)