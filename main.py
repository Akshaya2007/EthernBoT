import discord
from discord.ext import commands, tasks
import asyncio
import keep_alive
import os
import datetime
import random
from random import choice
import time
import config
import os
import sqlite3 
from discord.ext.commands import CommandOnCooldown, BucketType
import json
from discord import asset



intents = discord.Intents.default() #default intents
intents.all()

#main code starts here!



client = commands.Bot(command_prefix='%', intents=intents, case_insensitive=True, allowed_mentions=discord.AllowedMentions(everyone=True))#% is your prefix
client.remove_command("help")

@client.group(invoke_without_command=True)
async def help(ctx):
  em = discord.Embed(title = "Help", description = "Type %help <command> for more info on a command.",color = ctx.author.color)
  em.add_field(name = "Moderation", value = "kick , ban , unban , clear , addrole , removerole , unlock , lock , massrole , rename")
  em.add_field(name = "Fun", value = "avatar, ping")
  em.add_field(name = "Games", value = "truth, dare")
  em.add_field(name = "More", value = "[Invite the bot](https://discord.com/api/oauth2/authorize?client_id=1000350335312863252&permissions=8&scope=bot) • [Support Server](https://discord.gg/RM6qp5pNj2)")
  await ctx.reply(embed = em)


  
@help.command()
async def kick(ctx):

  em = discord.Embed(title="Kick", description = "Kicks a member from the guild.",color = ctx.author.color)
  em.add_field( name = "**Syntax**", value = "%kick <member> [reason]")
  await ctx.reply(embed = em)

@help.command()
async def ban(ctx):

  em = discord.Embed(title="Ban", description = "Bans a member from the guild.",color = ctx.author.color)
  em.add_field( name = "**Syntax**", value = "%ban <member> [reason]")
  await ctx.reply(embed = em)

@help.command()
async def clear(ctx):

  em = discord.Embed(title="Clear", description = "Clears messages.",color = ctx.author.color)
  em.add_field( name = "**Syntax**", value = "%clear <amount>")
  await ctx.reply(embed = em)

@help.command()
async def addrole(ctx):

  em = discord.Embed(title="Addrole", description = "Adds a role to a member of the guild. ",color = ctx.author.color)
  em.add_field( name = "**Syntax**", value = "%addrole <membermention> <rolename or mention>")
  await ctx.reply(embed = em)

@help.command()
async def removerole(ctx):

  em = discord.Embed(title="Removerole", description = "Removed a role from a member of the giuld. ",color = ctx.author.color)
  em.add_field( name = "**Syntax**", value = "%removerole <membermention> <rolename or mention>")
  await ctx.reply(embed = em)

@help.command()
async def massrole(ctx):

  em = discord.Embed(title="Massrole", description = "Gives a role to many users at same time. Might take some seconds to give role. ",color = ctx.author.color)
  em.add_field( name = "**Syntax**", value = "%massrole <role> <members> ")
  await ctx.reply(embed = em)

@help.command()
async def lock(ctx):

  em = discord.Embed(title="Lock", description = "Locks a channel. ",color = ctx.author.color)
  em.add_field( name = "**Syntax**", value = "%lock")
  await ctx.reply(embed = em)

@help.command()
async def unlock(ctx):

  em = discord.Embed(title="Unlock", description = "Unlocks a channel. ",color = ctx.author.color)
  em.add_field( name = "**Syntax**", value = "%unlock")
  await ctx.reply(embed = em)

@help.command()
async def unban(ctx):

  em = discord.Embed(title="Unban", description = "Unbans a member",color = ctx.author.color)
  em.add_field( name = "**Syntax**", value = "%unban <Username>#<discriminator>")
  await ctx.reply(embed = em)

@help.command()
async def avatar(ctx):

  em = discord.Embed(title="Avatar", description = "Shows the avatar of a member",color = ctx.author.color)
  em.add_field( name = "**Syntax**", value = "%avatar / %av <mention member>")
  await ctx.reply(embed = em)

@help.command()
async def ping(ctx):

  em = discord.Embed(title="Ping", description = "Ping....Pong!",color = ctx.author.color)
  em.add_field( name = "**Syntax**", value = "%ping")
  await ctx.reply(embed = em)

@help.command()
async def rename(ctx):

  em = discord.Embed(title="Rename", description = "Renames a member",color = ctx.author.color)
  em.add_field( name = "**Syntax**", value = "%rename <mention member> <newname> ")
  await ctx.reply(embed = em)

@help.command()
async def truth(ctx):

  em = discord.Embed(title="Truth", description = "Sends a truth",color = ctx.author.color)
  em.add_field( name = "**Syntax**", value = "%truth")
  await ctx.reply(embed = em)

@help.command()
async def dare(ctx):

  em = discord.Embed(title="Dare", description = "Sends a dare",color = ctx.author.color)
  em.add_field( name = "**Syntax**", value = "%dare")
  await ctx.reply(embed = em)
#whatever code you want to add, do it after this line


@client.event
async def on_ready():
  
  await client.change_presence(activity=discord.Game(name="%help"))
  
  print("Ready")

async def ch_pr():
  await client.wait_until_ready()

  statuses = ["%help"]

  while not client.is_closed():
    status = random.choice(statuses)
    await client.change_presence(activity=discord.Game(name=status))

    await asyncio.sleep(60)
client.loop.create_task(ch_pr())


@client.command()
@commands.has_permissions(kick_members=True)
@commands.cooldown(1,30,commands.BucketType.user)
async def kick(ctx, member:discord.Member,*, reason=None):
  await member.kick(reason=reason)
  await ctx.reply(f"{member.mention} has been kicked!")

@client.command()
@commands.has_permissions(ban_members=True)
@commands.cooldown(1,30,commands.BucketType.user)
async def ban(ctx, member:discord.Member, *, reason=None):
  await member.ban(reason=reason)
  await ctx.reply(f"{member.mention} has been banned!")

@client.command()
@commands.has_permissions(ban_members=True)
@commands.cooldown(1,30,commands.BucketType.user)
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')

  for ban_entry in banned_users:
    user = ban_entry.user

    if(user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.reply(f"Unbanned {user.mention}!")
    

@client.command(aliases = ['ar'])
@commands.cooldown(1,15,commands.BucketType.user)
async def addrole(ctx,  user: discord.Member, role: discord.Role,):
  if ctx.author.guild_permissions.manage_roles:
    await user.add_roles(role)
    await ctx.reply(f"Successfully given the role to {user.mention}.")


@client.command(aliases = ['rr'])
@commands.cooldown(1,15,commands.BucketType.user)
async def removerole(ctx, user: discord.Member, role: discord.Role):
  if ctx.author.guild_permissions.manage_roles:
    await user.remove_roles(role)
    await ctx.reply(f"Successfully removed the role from {user.mention}")



@client.command(aliases = ['madd'])
@commands.cooldown(1,60,commands.BucketType.user)
async def massrole(ctx, role: discord.Role, members: commands.Greedy[discord.Member]):
    for m in members:
      if ctx.author.guild_permissions.manage_roles:
        await m.add_roles(role)
        await asyncio.sleep(1)  # You don't want to get ratelimited!
    await ctx.reply("Given role to mentioned members!")



@client.command(aliases= ['purge','delete','clean'])
@commands.cooldown(1,120,commands.BucketType.user)
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount = 2):
   await ctx.channel.purge(limit = amount)
   await ctx.reply("Cleared the messages!")



@client.command(aliases = ['l'])
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel : discord.TextChannel=None):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.reply('Channel locked.')

@client.command(aliases = ['ul'])
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel : discord.TextChannel=None):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.reply('Channel unlocked.')
  

@client.command(aliases = ['av'])
@commands.cooldown(1,30,commands.BucketType.user)
async def avatar(ctx, member : discord.Member = None):
  if member == None:
    member = ctx.author

  memberAvatar = member.avatar_url

  avEmbed = discord.Embed(title = f"{member.name}'s Avatar")
  avEmbed.set_image(url = memberAvatar)
  await ctx.reply(embed = avEmbed)

def convert(time):
  pos = ["s","min","hr","d"]

  time_dict = {"s":1, "min":60, "hr":3600, "d":3600*24}

  unit = time[-1]

  if unit not in pos:
    return -1
  try:
    val = int(time[:-1])
  except:
    return -2

  return val * time_dict[unit]

  
@client.command()
@commands.cooldown(1,30,commands.BucketType.user)
async def ping(ctx):
  await ctx.reply(f"Pong! {round(client.latency * 1000)}ms")

@client.command()
@commands.cooldown(1,15,commands.BucketType.user)
async def rename(ctx, user: discord.Member, *, newName=""):
    if ctx.message.author.guild_permissions.manage_nicknames:
        renameduser = user.nick
        await user.edit(nick=newName)
        await ctx.reply("Renamed the user!")

Truthh = ["When was the last time you lied?","When was the last time you cried?","What's your biggest fear?","Have you ever cheated on someone?","What's the worst thing you've ever done?","What's a secret you've never told anyone?","Who was your first celebrity crush?","Have you ever cheated in an exam?","What's the most drunk you've ever been?","Have you ever broken the law?","Who would you like to kiss in this server?","What's the worst thing you've ever said to anyone?","Who would you like to marry in this server?","Have you ever been caught doing something you shouldn't have?","Why did your last relationship break down?","Who is your last date?","Did you fail in any subjects in exam?","What's the strangest dream you've had?","What's your biggest regret?","What's the biggest misconception about you?","What's the most trouble you've been in?","Who is your most recent date?","How long have you been in relation with someone?","Do you regret after leaving someone?","Who in this server knows your secret?","How do you introduce you to someone new?","What's the most embarassing thing you have done?","Have your sibling/s walked in while you were changing?","Do you know who has a crush on you?","Do your sibling/s know your secret?","What was the last time you failed in exams?","If you could be any celebrity, who would you be and why?","What makes you happy?","If you had the money and resources to start a business, what would it be?","What's your childhood nickname?","Have you ever danced on a table when you were drunk?","Have you ever shared your best friend’s secrets with anyone else?","How would you want someone to propose to you?","Have you ever bunked a class or schoolday?","What would you do if the world was going to end?","What would you do if you had only 24 hours to live?","When did you learn to ride a bike?","When did you learn to ride a car?","If you could hire someone to do one thing for you, what would it be?","What is your greatest insecurities in relationship?","Have you had your first kiss?","Do you have an imaginary friend?","What is your favourite sports?","What is your favourite game?","What would be your reaction if you met your favourite person randomly?","If you could be invisible for a day, what’s the first thing you would do?","What’s the biggest secret you’ve kept from your parents?","What’s the most embarrassing music you listen to?","Whom did you last stalk?","When was the last time you wet the bed?","If you could swap gender for one day, what's the first thing you would do?","Have you ever ghosted on someone?","Where is the weirdest place you've ever gone to the bathroom?","Describe your first kiss","What excuse have you used before to get out plans?","When was the last time you lied?","How many selfies do you take a day?","What celebrity do you think you most look like?","What is the boldest pickup line you've ever used?","What's the most embarrassing thing you ever did on a date?","When was the last time you cried?","If you had to change your name, what would your new first name be?","If you could date a fictional character, who would it be?","What's one silly thing you can't live without?","Who do you text the most?","What is the weirdest trend you've ever participated in?","Have you ever sexted anyone?","Have you ever been fired from a job?","What’s an instant deal breaker in a potential love interest?","Which player knows you the best?","What's your favorite part of your body?","If you could only eat one thing for the rest of your life, what would you choose?","Tell us about the biggest romantic fail you’ve ever experienced","What is your worst habit?","When’s the last time you said you were sorry? For what?","Do you still have feelings for any of your exes?","What’s the last movie that made you cry?","What’s the last song that made you cry?","What gross smell do you actually enjoy?","If you were handed $1,000 right now, what would you spend it on?","What unexpected part of the body do you find attractive?","Have you ever flirted with a close friend’s sibling?","Where do you see yourself in 10 years?","Even if you’d be paid $1 million for it, what’s something you would never do?","Have you ever slid into a celebrity’s DMs?","What’s the weirdest place you’ve kissed with someone?","What’s the most embarrassing nickname you’ve ever been given?","What superstitions do you believe in?","What app do you check first in the morning?","What’s the most embarrassing thing you’ve ever purchased?","What’s the longest you’ve ever gone without brushing your teeth?","What’s the weirdest thing you have in your bedroom?","Do you sing in the shower? What was the last song you belted out?","Have you ever given a fake number?","What’s more important to you: love or money?"]

Daree = ["Show your most embarrassing photo/video on your phone","Show the most embarrassing photo/video on your phone","Show the last five people you texted and what the messages said","Do 100 squats","Let the rest of the server DM someone from your Instagram account","Keep three ice cubes in your mouth until they melt","Give a lap dance to someone of your choice","Type out the first word that comes to your mind","Like the first 15 posts on your newsfeed","Send a sext to the last person you texted","Twerk for a minute","Tell everyone an embarrassing story about yourself","Draw a mustache on yourself without a mirror","Post the oldest selfie on your phone on stories","Pole dance with an imaginary pole","Let someone else tickle you and try not to laugh","Prank someone with serious matter","Post a video of you right now in stories","Act like you don't care to your brothers/sisters","Do 50 pushups","Show recent 5 calls by you","Show your browsing history today","Sing a song in a VC","Join a VC and yell out","Read the last text you sent your best friend or significant other out loud in a VC","Roast someone for one minute straight","Mention the person whom you hate the most","Mention the person whom you want to take on a date right now","Bite into a raw onion without slicing it","Prank call one of your family members","Put five ice cubes in your mouth (you can't chew them, you just have to let them melt)","Demonstrate how you style your hair in the mirror (without actually using the mirror)","Go on Instagram Live and do a dramatic reading of one of your textbooks","Lick a cake of soap","Attempt the first TikTok dance on your FYP","Go to your crush’s Instagram page and like something from several weeks ago","Find your very first crush on social and DM them","Stand outside your house and wave to everyone who passes in the next minute","Pretend to be underwater for the next 10 minutes","Post a flirty comment on the post of your cursh","Go outside and howl at the moon","Reveal your screen time report to your friends","Read aloud in VC the most personal text you’ve sent in recent days"]


@client.command()
async def truth(ctx):
  truth = random.choice(Truthh)
  await ctx.reply(truth)

@client.command()
async def dare(ctx):
  dare = random.choice(Daree)
  await ctx.reply(dare)

@client.event
async def on_command_error(ctx, error):
  await ctx.reply(f"An error occured: {str(error)}")

keep_alive.keep_alive()
token = os.environ.get("TOKEN")
# Run the client on the server
client.run(os.environ["DISCORD_TOKEN"])
