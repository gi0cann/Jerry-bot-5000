import os
import random
import json
import os.path
import time

import discord
from discord.ext import commands
from dotenv import load_dotenv

#intents = discord.Intents(message_content=True)
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

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
help_command = commands.DefaultHelpCommand(dm_help=True)
bot = commands.Bot(command_prefix='!', intents=intents, help_command=help_command)

@bot.group()
async def movie(ctx):
    """Watch party movie list commands"""
    if ctx.invoked_subcommand is None:
        await ctx.send("Missing subcommand")

@bot.group()
async def audio(ctx):
    """Audio commands"""
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

async def play_audio(source, ctx, executable="/usr/bin/ffmpeg"):
    """play audio file"""
    voice_channel = ctx.author.voice.channel
    channel = None
    if voice_channel != None:
        channel = voice_channel.name
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable=executable, source=source))
        while vc.is_playing():
            time.sleep(.1)
        await vc.disconnect()
    else:
        await ctx.send(str(ctx.author.name) + "you are not in a voice channel. You dumb fuck. And I'm supposed to be the Jerry.")
    await ctx.message.delete()

@audio.command(name="evan")
async def play_evan(ctx):
    """Play evan audio"""
    await play_audio(source="audio/evan_stfu.mp3", ctx=ctx)

@audio.command(name="hothothot")
async def play_hothothot(ctx):
    """Play hothothot audio"""
    await play_audio(source="audio/hot hot hot hot.mp3", ctx=ctx)

@audio.command(name="kevdamn")
async def play_kevdamn(ctx):
    """Play kevin hart damn audio"""
    await play_audio(source="audio/Kevin hart high damn.mp3", ctx=ctx)

@audio.command(name="kevdamnlong")
async def play_kevdamnlong(ctx):
    """Play kevin hart damn long audio"""
    await play_audio(source="audio/kevin hart high damn & im sorry.mp3", ctx=ctx)

@audio.command(name="animemoan")
async def play_animemoan(ctx):
    """Play moan audio"""
    await play_audio(source="audio/Anime Moan  Sound Effect.mp3", ctx=ctx)

@audio.command(name="moan")
async def play_moan(ctx):
    """Play moan audio"""
    await play_audio(source="audio/moan.mp3", ctx=ctx)

@audio.command(name="notthatguy")
async def play_notthatguy(ctx):
    """Play Bill your not that guy audio"""
    await play_audio(source="audio/Youre not that guy pal trust me youre not that guy SOUND EFFECT.mp3", ctx=ctx)

@audio.command(name="perfect")
async def play_perfect(ctx):
    """Play Street figher perfect"""
    await play_audio(source="audio/Perfect Street Fighter Sound Effect.mp3", ctx=ctx)

@audio.command(name="peterlaugh")
async def play_peterlaugh(ctx):
    """Play Peter Grifin laugh"""
    await play_audio(source="audio/peter griffin laugh.mp3", ctx=ctx)

bot.run(TOKEN)
