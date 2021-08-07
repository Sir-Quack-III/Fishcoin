# Imports
import discord # Discord library
from discord.ext import commands # Commands library
import json
import random
import time
import math
from replit import db # Database library
import os
from keep_alive import keep_alive # Imports keep_alive.py

# Token
token = os.environ['TOKEN']

client = commands.Bot(command_prefix = ".") # Creates the object "client" and defines the command prefix. This variable will be used to control the bot.

data = db["data"] # All data will be stored in this variable.
print(client)

# Command to register a user
@client.command()
async def register(ctx):
    keys = []
    
    # Checks whether the author has an existing account. If so, it adds its user id to keys.
    for key in db["data"]["users"]:
        if key == str(ctx.message.author.id):
            keys.append(key)

    if len(keys) == 0: # "keys" will have a length of 0 if the author of the command doesn't have an existing account.
        # Accounts are dictionaries in a list called "users".
        db["data"]["users"].update({str(ctx.message.author.id) : {}}) # Adds an account dictionary to "users".
        user = db["data"]["users"][str(ctx.message.author.id)]
        
        # Adds base data.
        user.update({"fishcoins":1})
        user.update({"fishing":0})
        user.update({"fishcoinspending":0}) # Fishcoins pending will be used in fishing
        await ctx.send("User Registered!")
    else:
        await ctx.send("You have already registered! Speak to your administrator to reset your account.")

# Prints the number of fishcoins you have
@client.command()
async def fishcoins(ctx):
    user = db["data"]["users"][str(ctx.message.author.id)]
    await ctx.send(str(client.get_emoji(831749967722577960))) # Prints fishcoin emoji
    await ctx.send("You currently have **"+str(user["fishcoins"])+"** Fishcoins!")

# Pays target user an X amount of fishcoins
@client.command()
async def pay(ctx, user, amount):
    # You don't need to read all this code, basically all it does is subtract your fishcoins and add the subtracted fishcoins to the target account
    
    user = db["data"]["users"][str(ctx.message.author.id)]
    if user["fishing"] == 0: # Checks if user isn't fishing
        targetuserfishcoins = db["data"]["users"][str(user.replace("<", "").replace(">", "").replace("@", "").replace("!", ""))]["fishcoins"]
        yourfishcoins = user["fishcoins"]

        if str(str(user.replace("<", "").replace(">", "").replace("@", "").replace("!", ""))) == str(ctx.message.author.id): # Another infinite fishcoin glitch found by gubs (thanks!)
            await ctx.send("You cannot pay yourself!")
        elif (yourfishcoins - int(amount)) < 0: # Checks if you can afford the transaction
            await ctx.send("You cannot afford this!")
        elif "-" in str(amount): # Infinite fishcoin glitch with negative numbers found by gubs (thanks!)
            await ctx.send("You cannot do this!")
        else: # Command has passed all failsafes
            await ctx.send("https://i.postimg.cc/SKPQq45f/fishcoin-transaction.png") # Prints image
            await ctx.send("**Transaction Completed!**")
            user["fishcoins"] = yourfishcoins - int(amount) # Subtracts "amount" from your account
            db["data"]["users"][str(user.replace("<", "").replace(">", "").replace("@", "").replace("!", ""))]["fishcoins"] = targetuserfishcoins + int(amount) # Adds "amount" to target account
            await ctx.send("You cannot get your money back, btw.")
    else:
        await ctx.send("You are fishing at the moment! All Fishcoin transactions are restricted until you claim your fishcoins")

# Prints all users and their fishcoins
@client.command()
async def users(ctx):
    for x in db["data"]["users"]:
        await ctx.send(f'<@{x}>: {str(db["data"]["users"][x]["fishcoins"])}')

# Gambling
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
