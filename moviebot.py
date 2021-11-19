import os
import random
import json
import os.path

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

if os.path.exists("movies.json"):
    fd = open("movies.json", "r")
else:
    fd = open("movies.json", "x")
fd.seek(0, os.SEEK_END)
print(fd.tell())
if fd.tell() == 0:
    moviesdb = {"movies": list()}
else:
    fd.seek(0)
    moviesdb = json.load(fd)
fd.close()

members = ''
bot = commands.Bot(command_prefix='!')

@bot.command()
async def hello(ctx, arg1):
    await ctx.send(f"hello {arg1}")

@bot.command()
async def movie(ctx, *args):
    await ctx.send(f"{ctx.author}")
    cmd = args[0]
    print(moviesdb, f"start {cmd}")
    if cmd  == "add":
        movie = " ".join(args[1:])
        print(f"movie: {movie}")
        if movie not in moviesdb:
            moviesdb.get("movies").append(movie)
            print(moviesdb, "post add")
            await ctx.send(f"{movie} added to movie list")
        fd = open("movies.json", "w")
        json.dump(moviesdb, fd)
        fd.close()

    if cmd == "list":
        await ctx.send(f"{', '.join(moviesdb.get('movies'))}")

    if cmd == "random":
        movie = moviesdb.get("movies")[random.randint(0, len(moviesdb)-1)]
        await ctx.send(f"{movie}")

bot.run(TOKEN)
