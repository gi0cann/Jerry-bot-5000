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
movie_help = f"""!movie add <movie name>
!movie list
!movie del <movie name>
!movie random
"""


@bot.command(help=movie_help)
async def movie(ctx, *args):
    current_user = ctx.author.name + "#" + ctx.author.discriminator
    print(current_user, current_user == "gi0cann#0899", ctx.author.mention)
    cmd = args[0]
    print(moviesdb, f"start {cmd}")
    if cmd  == "add":
        movie = " ".join(args[1:])
        print(f"movie: {movie}")
        if movie not in moviesdb.get("movies"):
            moviesdb.get("movies").append(movie)
            print(moviesdb, "post add")
            await ctx.send(f"{movie} added to movie list")
            fd = open("movies.json", "w")
            json.dump(moviesdb, fd)
            fd.close()
            await ctx.send(f"{ctx.author} added {movie} to movie list")

    if cmd == "list":
        await ctx.send(f"{', '.join(moviesdb.get('movies'))}")

    if cmd == "random":
        shuffled = moviesdb.get("movies")
        random.shuffle(shuffled)
        movie = shuffled[random.randint(0, len(moviesdb.get("movies"))-1)]
        await ctx.send(f"{movie}")

    if cmd == "del":
        if current_user == "gi0cann#0889":
            movie = " ".join(args[1:])
            if movie in moviesdb.get("movies"):
                moviesdb["movies"].remove(movie)
                fd = open("movies.json", "w")
                json.dump(moviesdb, fd)
                fd.close()
                await ctx.send(f"{ctx.author} removed {movie} from movie list")
            else:
                newline = "\n"
                await ctx.send(f"{movie} not in movie list. Try one of the following {newline.join(moviesdb.get('movies'))}")
        else:
            await ctx.send(f"User {current_user} is not allowed to remove movies from movie list. Better luck next time")

bot.run(TOKEN)
