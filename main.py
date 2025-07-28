import disnake as discord
from disnake.ext import commands
import random
import numpy as np
from enum import Enum
import sqlite3

intents=discord.Intents.all()
bot = commands.Bot(
    command_prefix='!', 
    intents=intents,
    default_install_types=discord.ApplicationInstallTypes(user=True,guild=True), 
    default_contexts=discord.InteractionContextTypes(bot_dm=True,guild=True,private_channel=True),
    #proxy="http://127.0.0.1:8830" # ignore this its just a leftover from me trying to get the bot working
    )

#db stuff
con = sqlite3.connect("gamble.db")
cur = con.cursor()

# actually making the table in the db
def init_db():
    print("initialising the db...")
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, 
        money INTEGER DEFAULT 0,
        slots_spins INTEGER DEFAULT 0,
        slots_wins INTEGER DEFAULT 0,
        slots_big_wins INTEGER DEFAULT 0,
        chicken_attempts INTEGER DEFAULT 0,
        chicken_wins INTEGER DEFAULT 0,
        chicken_losses INTEGER DEFAULT 0,
        chicken_attempts_since_last_win INTEGER DEFAULT 0,
        dice_rolls INTEGER DEFAULT 0,
        dice_cliped INTEGER DEFAULT 0
    )
    ''')
    con.commit()

def get_stats(user_id):
    cur.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    stats=cur.fetchone()
    return stats

#slots stuff
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
    init_db()
    print("if there is no error then i assume the db was initialised i might be wrong")

@bot.slash_command(description="roll a n sided dice")
async def dice(ctx: discord.ApplicationCommandInteraction,sides):
    ctx.response.defer()
    cur.execute('''INSERT OR IGNORE INTO users (id) VALUES (?)''', (ctx.author.id,))
    try:
        sides=int(sides)
    except:
        await ctx.send(f"erm actually thats not a valid integer",ephemeral=True)
        return
    if sides < 1:
        cur.execute('''UPDATE users SET dice_cliped = dice_cliped + 1  WHERE id = ?''', (ctx.author.id,))
        con.commit()
        try: print(f"{ctx.author.name} tried to roll a d{sides} (which clipped through the table)")
        except: pass
        await ctx.send(f"You roll a d{sides}\n...it cliped through the table.")
    else:
        result=random.randint(1,sides)
        cur.execute('''UPDATE users SET dice_rolls = dice_rolls + 1  WHERE id = ?''', (ctx.author.id,))
        con.commit()
        try: print(f"{ctx.author.name} rolled a d{sides} and it laned on {result}")
        except: pass
        await ctx.send(f"You roll a d{sides}\nit landed on {result}")


@bot.slash_command(description="chicken (WIP)")
async def chicken(ctx,guess: int):
    ctx.response.defer()
    cur.execute('''INSERT OR IGNORE INTO users (id) VALUES (?)''', (ctx.author.id,))
    stats=get_stats(ctx.author.id)
    number=random.randint(1,(20+(5*stats[6])))
    if guess<1 or guess>(20+(5*stats[6])):
        await ctx.send(f"why are you guessing numbers out of the 1 to {20+(5*stats[6])} range are you stupid")
    elif number==guess:
        cur.execute('''UPDATE users SET chicken_attempts = chicken_attempts + 1  WHERE id = ?''', (ctx.author.id,))
        cur.execute('''UPDATE users SET chicken_attempts_since_last_win = 0  WHERE id = ?''', (ctx.author.id,))
        cur.execute('''UPDATE users SET chicken_wins = chicken_wins + 1  WHERE id = ?''', (ctx.author.id,))
        con.commit()
        try: print(f"{ctx.author.name} ran chicken guessed {guess} and won")
        except: pass
        await ctx.send(f"Congratulations, You Won!\nyour guess:{guess}\ncorrect number:{number}\nnumber range: 1-{20+(5*stats[6])}\ntotal attempts: {stats[5]+1}"+(f"\nattempts since last win: 0" if stats[8]!=0 and stats[6]!=0 else ""))
    else:
        cur.execute('''UPDATE users SET chicken_attempts = chicken_attempts + 1  WHERE id = ?''', (ctx.author.id,))
        cur.execute('''UPDATE users SET chicken_attempts_since_last_win = chicken_attempts_since_last_win + 1  WHERE id = ?''', (ctx.author.id,))
        cur.execute('''UPDATE users SET chicken_losses = chicken_losses + 1  WHERE id = ?''', (ctx.author.id,))
        con.commit()
        try: print(f"{ctx.author.name} ran chicken guessed {guess} and lost (the correct number was {number})")
        except: pass
        await ctx.send(f"You Lost\nyour guess:{guess}\ncorrect number:{number}\nnumber range: 1-{20+(5*stats[6])}\ntotal attempts: {stats[5]+1}"+(f"\nattempts since last win: {stats[8]+1}" if stats[8]!=0 and stats[6]!=0 else ""))

@bot.slash_command(description="gamble (WIP)")
async def slots(ctx: discord.ApplicationCommandInteraction):
    ctx.response.defer()
    reel=spin(7)
    messag=""
    for i in reel:
        messag+=f"{items[i-1]} "
    await ctx.send(messag)

bot.run(open("token.txt").read(),reconnect=True)
con.close()