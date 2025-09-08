import disnake as discord 
from disnake.ext import commands
from datetime import datetime
import sqlite3
import random
from sudoku_render import drawsudokuv2
from enum import Enum

print("openning a whole another db connection...")
con = sqlite3.connect("sudokus.db")
cur = con.cursor()

class diffemoj(Enum):
    Easy="🟩"
    Medium="🟨"
    Hard="🟥"
    WhatTheFuck="⬛"

class SudokuCommand(commands.Cog):
    """This will be sudoku in 2015"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.slash_command()
    async def sudoku(self,ctx):
        pass
    
    #@sudoku.sub_command()
    #async def test(self, ctx):
    #    """Description"""
    #    timestamp=datetime.now()
    #    embed = discord.Embed(title="🚩Testing", timestamp=timestamp)
    #    embed.set_image(file=discord.File("sudokus/sudoku_3x3_0.5_153498306488494359.png"))
    #    embed.set_footer(text="🌱 Seed: hsgkfsdhgjg | 🕹️ select a box... any box...")
    #    embed.add_field(name="🎨 Theme", value="This is a test", inline=True)
    #    embed.add_field(name="", value="", inline=True)
    #    embed.add_field(name="📊 Progress", value="0% (0/1)", inline=True)
    #    embed.add_field(name="🏁Difficulty", value="kreisler", inline=True)
    #    embed.add_field(name="", value="", inline=True)
    #    embed.add_field(name="⏱️ Time", value=f"Started <t:{int(timestamp.timestamp())}:R>", inline=True)
    #    await ctx.send(embed=embed)

    @sudoku.sub_command()
    async def play(self,ctx,difficulty=commands.Param(choices=["Easy","Medium","Hard","WhatTheFuck"])):
        """attempt to pull a random sudoku from the database i got god knows where"""
        # ok listen the data is in public domain okay
        
        if difficulty=="Easy":
            cur.execute("SELECT * FROM sudokus WHERE difficulty < 1.5 ORDER BY RANDOM() LIMIT 1;")
        elif difficulty=="Medium":
            cur.execute("SELECT * FROM sudokus WHERE difficulty >= 1.5 AND difficulty < 2.5 ORDER BY RANDOM() LIMIT 1;" )
        elif difficulty=="Hard":
            cur.execute("SELECT * FROM sudokus WHERE difficulty >= 2.5 AND difficulty < 5.0 ORDER BY RANDOM() LIMIT 1;")
        elif difficulty=="WhatTheFuck":
            cur.execute("SELECT * FROM sudokus WHERE difficulty >= 5.0 ORDER BY RANDOM() LIMIT 1;")
        sudoku1=list(cur.fetchone())
        sudoku1[1]=[int(i) for i in sudoku1[1]]
        sudokuboard=[sudoku1[1][i*9:(i+1)*9] for i in range(9)]
        sudoku_image=drawsudokuv2(3,board=sudokuboard)
        sudokuimagepath=f"sudokus/puzzle_bank/sudoku_{sudoku1[2]}_{sudoku1[0]}.png"
        sudoku_image.save(sudokuimagepath)
        
        sudokuprogress=0
        for i in sudoku1[1]:
            if i>0:
                sudokuprogress+=1
        
        
        timestamp=datetime.now()
        embed = discord.Embed(title=f"🚩Testing - {diffemoj[difficulty].value}{difficulty}", timestamp=timestamp)
        embed.set_image(file=discord.File(sudokuimagepath))
        embed.set_footer(text=f"🌱 Id: {sudoku1[0]} | 🕹️ select a box... any box... wait you cant do that yet actually")
        embed.add_field(name="🎨 Theme", value="This is a test", inline=True)
        embed.add_field(name="", value="", inline=True)
        embed.add_field(name="📊 Progress", value=f"{round((sudokuprogress/81)*100)}% ({sudokuprogress}/81)", inline=True)
        embed.add_field(name="🏁Difficulty", value=f"{sudoku1[2]} ({difficulty})", inline=True)
        embed.add_field(name="", value="", inline=True)
        embed.add_field(name="⏱️ Time", value=f"Started <t:{int(timestamp.timestamp())}:R>", inline=True)

        await ctx.send(sudoku1,embed=embed)
    

def setup(bot: commands.Bot):
    bot.add_cog(SudokuCommand(bot))