import discord
from discord.ext import commands
import json
import random
import time
import math
from replit import db
import os
from keep_alive import keep_alive

token = os.environ['TOKEN']

client = commands.Bot(command_prefix = ".")

data = db["data"]
print(client)

@client.command()
async def register(ctx):

    keys = []
    for key in db["data"]["users"]:
        if key == str(ctx.message.author.id):
            keys.append(key)

    if len(keys) == 0:
        db["data"]["users"].update({str(ctx.message.author.id) : {}})
        user = db["data"]["users"][str(ctx.message.author.id)]
        user.update({"fishcoins":1})
        user.update({"fishing":0})
        user.update({"fishcoinspending":0})
        await ctx.send("User Registered!")
    else:
        await ctx.send("You have already registered! Speak to your administrator to reset your account.")

@client.command()
async def fishcoins(ctx):
    user = db["data"]["users"][str(ctx.message.author.id)]
    await ctx.send(str(client.get_emoji(831749967722577960)))
    await ctx.send("You currently have **"+str(user["fishcoins"])+"** Fishcoins!")

@client.command()
async def pay(ctx, user, amount):
    user = db["data"]["users"][str(ctx.message.author.id)]
    if user["fishing"] == 0:
        stufftopay = db["data"]["users"][str(user.replace("<", "").replace(">", "").replace("@", "").replace("!", ""))]["fishcoins"]
        yourfishcoins = user["fishcoins"]

        if str(str(user.replace("<", "").replace(">", "").replace("@", "").replace("!", ""))) == str(ctx.message.author.id):
            await ctx.send("You cannot pay yourself!")
        elif (yourfishcoins - int(amount)) < 0:
            await ctx.send("You cannot afford this!")
        elif "-" in str(amount):
            await ctx.send("You cannot do this!")
        else:
            await ctx.send("https://i.postimg.cc/SKPQq45f/fishcoin-transaction.png")
            await ctx.send("**Transaction Completed!**")
            user["fishcoins"] = yourfishcoins - int(amount)
            db["data"]["users"][str(user.replace("<", "").replace(">", "").replace("@", "").replace("!", ""))]["fishcoins"] = stufftopay + int(amount)
            await ctx.send("You cannot get your money back, btw.")
    else:
        await ctx.send("You are fishing at the moment! All Fishcoin transactions are restricted until you claim your fishcoins")


@client.command()
async def users(ctx):
    for x in db["data"]["users"]:
        await ctx.send(f'<@{x}>: {str(db["data"]["users"][x]["fishcoins"])}')

@client.command()
async def dice(ctx, coins):
    user = db["data"]["users"][str(ctx.message.author.id)]
    if user["fishing"] == 0:
        user = db["data"]["users"][str(ctx.message.author.id)]
        yourfishcoins = user["fishcoins"]
        yourfishcoins = user["fishcoins"]
        dicey = random.randint(1,7) + random.randint(1,7)
        diceo = random.randint(1,7) + random.randint(1,7)

        if "-" in str(coins):
            await ctx.send("That is not a valid number!")
        elif int(coins) > yourfishcoins:
            await ctx.send("You cannot afford this!")
        else:
            await ctx.send(f"You roll a {dicey}...")
            time.sleep(2)
            await ctx.send(f"Your opponent rolls a {diceo}!")

            if dicey > diceo:
                await ctx.send("you win!")
                user.update({"fishcoins":yourfishcoins + int(coins)})
            elif dicey < diceo:
                await ctx.send("you lose!")
                user.update({"fishcoins":yourfishcoins - int(coins)})
            elif dicey == diceo:
                await ctx.send("tie!")
    else:
        await ctx.send("You are fishing at the moment! All Fishcoin games are restricted until you stop fishing.")

@client.command()
async def fish(ctx, arg, minutes):
    global timeout
    user = db["data"]["users"][str(ctx.message.author.id)]
    if arg == "start":
        if user["fishing"] == 0:
            if int(minutes) > 30:
                await ctx.send("You cannot fish for this amount of time!")
            else:
                timeout = time.time() + int(minutes) * 60
                user["fishcoinspending"] = 0
                user["fishing"] = 1

                
                for x in range(int(minutes)):
                    if random.randint(0,9) == 2:
                        user["fishcoinspending"] = user["fishcoinspending"] + 1

                await ctx.send(f"A fishing spree has begun! You will not be able to do **anything** with Fishcoins for {minutes} minutes.")
                await ctx.send("To claim your Fishcoins, type in `.fish claim 0`.")
        else:
            await ctx.send("You are already fishing! Type in `.fish claim 0` to claim your Fishcoins and to stop fishing!")
    elif arg == "claim":
        if user["fishing"] == 1:
            if time.time() > timeout:
                fishcoinspending = user["fishcoinspending"]
                user["fishcoins"] = user["fishcoins"] + user["fishcoinspending"]
                user["fishing"] = 0

                await ctx.send(f"You have now claimed your {fishcoinspending} Fishcoins!")

                user["fishcoinspending"] = 0
            else:
                await ctx.send("You are still fishing!")

@client.command()
async def admin(ctx, arg1, arg2 = None):
    user = db["data"]["users"][str(ctx.message.author.id)]
    if ctx.message.author.id != 746959257030623281:
        await ctx.send("_imagine trying to hack fishcoin lmao_")
    else:
        if arg1 == "clrfish":
            users = 0
            await ctx.send("```\nThis may take a while...\n```")
            for x in data["users"]:
                print(data["users"][str(x)]["fishing"])
                data["users"][str(x)]["fishing"] = 0
                users += 1
            
            await ctx.send(f"```\nDONE. {users} users affected.\n```")
        elif arg1 == "userdata":
            await ctx.send(data["users"])

        elif arg1 == "forceclaim":
            target = str(arg2).replace("<", "").replace(">", "").replace("@", "").replace("!", "")
            target = data["users"][str(target)]
            fishcoinspending = target["fishcoinspending"]
            target["fishcoins"] = target["fishcoins"] + target["fishcoinspending"]
            target["fishing"] = 0

            await ctx.send(f"You have now claimed your {fishcoinspending} Fishcoins!")

            target["fishcoinspending"] = 0




keep_alive()
client.run(token)