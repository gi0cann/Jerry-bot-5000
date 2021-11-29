import os
import random
import json
import os.path

import discord
from discord.ext import commands
from dotenv import load_dotenv

def clean_input(in_str):
    in_split = in_str.split(" ")
    result = list()
    for word in in_split:
        if " " not in word and len(word) != 0:
            result.append(word)
    return " ".join(result)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
NEWLINE = "\n"

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

@bot.group()
async def movie(ctx):
    """Watch party movie list commands"""
    if ctx.invoked_subcommand is None:
        await ctx.send("Missing subcommand")

@movie.command(name="list")
async def list_movies(ctx):
    """List movies added to movie list"""
    await ctx.send(f"```{NEWLINE.join(moviesdb.get('movies'))}```")

@movie.command(name="add")
async def add_movie(ctx, *movie_name):
    """Add movie to movie list"""
    movie = clean_input(" ".join(movie_name))
    print(f"movie: {movie}")
    movies = moviesdb.get("movies")
    for m in movies:
        if m.upper() == movie.upper():
            await ctx.send(f"{movie} already added to movie list")
            return None
    moviesdb.get("movies").append(movie)
    await ctx.send(f"{movie} added to movie list")
    fd = open("movies.json", "w")
    json.dump(moviesdb, fd)
    fd.close()
    await ctx.send(f"{ctx.author} added {movie} to movie list")

@movie.command(name="del")
async def delete_movie(ctx, *movie_name):
    """Remove a movie from movie list"""
    print(ctx.author.id)
    if ctx.author.id == 159128365079592960:
        movie = " ".join(movie_name)
        if movie in moviesdb.get("movies"):
            moviesdb["movies"].remove(movie)
            fd = open("movies.json", "w")
            json.dump(moviesdb, fd)
            fd.close()
            await ctx.send(f"{ctx.author} removed {movie} from movie list")
        else:
            await ctx.send(
                f"{movie} not in movie list. Try one of the following: ```{NEWLINE.join(moviesdb.get('movies'))}```"
            )
    else:
        await ctx.send(
            f"Nice try asshole. User {ctx.author} is not allowed to remove movies from movie list. Better luck next time"
        )

@movie.command(name="random")
async def pick_random_movie(ctx):
    """Pick a random movie from movie list"""
    shuffled = moviesdb.get("movies")
    random.shuffle(shuffled)
    random.shuffle(shuffled)
    movie = shuffled[random.randint(0, len(moviesdb.get("movies"))-1)]
    await ctx.send(f"{movie}")

bot.run(TOKEN)
