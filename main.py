import disnake as discord
from disnake.ext import commands
import random
import numpy as np
from enum import Enum
import sqlite3
import asyncio

intents=discord.Intents.all()
bot = commands.Bot(
    command_prefix='!', 
    intents=intents,
    default_install_types=discord.ApplicationInstallTypes(user=True,guild=True), 
    default_contexts=discord.InteractionContextTypes(bot_dm=True,guild=True,private_channel=True)
    )

global db_initialised; db_initialised = False

#db stuff
con = sqlite3.connect("gamble.db")
cur = con.cursor()

# actually making the table in the db
def init_db():
    print("initialising the db...")
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, 
        money INTEGER DEFAULT 500,
        slots_spins INTEGER DEFAULT 0,
        slots_small_wins INTEGER DEFAULT 0,
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
def spin(symbols_amount: int, size:int=3)->list[int]:
    reel = list(np.random.randint(low=1,high=symbols_amount+1,size=size,dtype=int))
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
    global db_initialised
    print(f'Logged in as {bot.user.name}')
    if not db_initialised:
        init_db()
        print("if there is no error then i assume the db was initialised i might be wrong")
        db_initialised=True

@bot.slash_command(description="roll a n sided dice")
async def dice(ctx: discord.ApplicationCommandInteraction,sides):
    await ctx.response.defer()
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


@bot.slash_command(description="guess a number from 1 to (20+(5*wins)) (WIP)")
async def chicken(ctx,guess: int):
    await ctx.response.defer()
    cur.execute('''INSERT OR IGNORE INTO users (id) VALUES (?)''', (ctx.author.id,))
    stats=get_stats(ctx.author.id)
    number=random.randint(1,(20+(5*stats[7])))
    if guess<1 or guess>(20+(5*stats[7])):
        await ctx.send(f"why are you guessing numbers out of the 1 to {20+(5*stats[7])} range are you stupid")
    elif number==guess:
        cur.execute('''UPDATE users SET chicken_attempts = chicken_attempts + 1  WHERE id = ?''', (ctx.author.id,))
        cur.execute('''UPDATE users SET chicken_attempts_since_last_win = 0  WHERE id = ?''', (ctx.author.id,))
        cur.execute('''UPDATE users SET chicken_wins = chicken_wins + 1  WHERE id = ?''', (ctx.author.id,))
        con.commit()
        try: print(f"{ctx.author.name} ran chicken guessed {guess} and won")
        except: pass
        await ctx.send(f"Congratulations, You Won!\nyour guess:{guess}\ncorrect number:{number}\nnumber range: 1-{20+(5*stats[7])}\ntotal attempts: {stats[6]+1}"+(f"\nattempts since previous win: {stats[9]+1}" if stats[7]>0 else ""))
    else:
        cur.execute('''UPDATE users SET chicken_attempts = chicken_attempts + 1  WHERE id = ?''', (ctx.author.id,))
        cur.execute('''UPDATE users SET chicken_attempts_since_last_win = chicken_attempts_since_last_win + 1  WHERE id = ?''', (ctx.author.id,))
        cur.execute('''UPDATE users SET chicken_losses = chicken_losses + 1  WHERE id = ?''', (ctx.author.id,))
        con.commit()
        try: print(f"{ctx.author.name} ran chicken guessed {guess} and lost (the correct number was {number})")
        except: pass
        await ctx.send(f"You Lost\nyour guess:{guess}\ncorrect number:{number}\nnumber range: 1-{20+(5*stats[7])}\ntotal attempts: {stats[6]+1}"+(f"\nattempts since last win: {stats[9]+1}" if stats[7]>0 and (stats[9])>0 else ""))

@bot.slash_command(description="gamble (WIP)")
async def slots(ctx: discord.ApplicationCommandInteraction):
    await ctx.response.defer()
    cur.execute('''INSERT OR IGNORE INTO users (id) VALUES (?)''', (ctx.author.id,))

    embed = discord.Embed(
        title=":slot_machine: Slots Machine Thingy",
        description="Thingy go spinny\n# :arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise:",
        color=discord.Colour.red(),
    )

    frames = 5 # amount of frames until the actual reel
    delay_between_frames = 0.5  # seconds
    await ctx.send(embed=embed)
    message = await ctx.original_response()

    # animation thingy
    for i in range(frames):
        spinning_reel=spin(7)
        spinnygospin=""
        for i in spinning_reel:
            spinnygospin+=f"{items[i-1]}"
        embed = discord.Embed(
            title=":slot_machine: Slots Machine Thingy",
            description=f"thingy go spinny\n# {spinnygospin}",
            color=discord.Colour.red(),
        )
        await message.edit(embed=embed)
        await asyncio.sleep(delay_between_frames)

    reel=spin(7)
    reel_emojified=""
    for i in reel:
        reel_emojified+=f"{items[i-1]}"
    
    # win condition check
    if reel[0]==reel[1] and reel[1]==reel[2]:
        cur.execute('''UPDATE users SET slots_spins = slots_spins + 1  WHERE id = ?''', (ctx.author.id,))
        cur.execute('''UPDATE users SET slots_wins = slots_wins + 1  WHERE id = ?''', (ctx.author.id,))
        if reel[0]==7:
            cur.execute('''UPDATE users SET slots_big_wins = slots_big_wins + 1  WHERE id = ?''', (ctx.author.id,))
            win_text="HOLY SJIT JACKPOT"
            try: print(f"{ctx.author.name} gambled in slots and hit the jackpot")
            except: pass
        else:
            win_text="You Won!"
            try: print(f"{ctx.author.name} gambled in slots and won")
            except: pass
        con.commit()
    elif reel[0]==reel[1] or reel[0]==reel[2] or reel[1]==reel[2]:
        cur.execute('''UPDATE users SET slots_spins = slots_spins + 1  WHERE id = ?''', (ctx.author.id,))
        cur.execute('''UPDATE users SET slots_wins = slots_wins + 1  WHERE id = ?''', (ctx.author.id,))
        cur.execute('''UPDATE users SET slots_small_wins = slots_small_wins + 1  WHERE id = ?''', (ctx.author.id,))
        con.commit()
        win_text="small win idk"
        try: print(f"{ctx.author.name} gambled in slots and won small")
        except: pass
    else:
        cur.execute('''UPDATE users SET slots_spins = slots_spins + 1  WHERE id = ?''', (ctx.author.id,))
        con.commit()
        win_text="congratulations you lost"
        try: print(f"{ctx.author.name} gambled in slots and lost")
        except: pass
    
    embed = discord.Embed(
        title=":slot_machine: Slots Machine Thingy",
        description=f"{win_text}\n# {reel_emojified}",
        color=discord.Colour.red())
    await message.edit(embed=embed)


@bot.slash_command(description="View Your Stats or smth like that (WIP)")
async def stats(ctx: discord.ApplicationCommandInteraction):
    await ctx.response.defer()
    stats=get_stats(ctx.author.id)
    embed = discord.Embed(
        title=f"{ctx.author.name}'s Stats",
        description=f"Money:{stats[1]}\nTotal Slots Spins:{stats[2]}\nSlots small wins:{stats[3]}\nSlots wins:{stats[4]}\nSlots big wins/jackpots:{stats[5]}\nChicken Attempts:{stats[6]}\nChicken wins:{stats[7]}\nChicken losses:{stats[8]}\nAttempts since last chicken win:{stats[9]}\nDice rolls:{stats[10]}\nDice clipped:{stats[11]}\n",
        color=discord.Colour.red(),
    )
    await ctx.send(embed=embed)


bot.run(open("token.txt").read(),reconnect=True)
print("ok shutting down")
con.close()
print("connection closed")