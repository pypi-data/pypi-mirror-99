import discord
import discord.ext
from discord.ext import commands
import DiscordUtils
import random
import os
import asyncio



def bot(prefix, description, token, status):
    botprefix = prefix
    botdescription = description
    bottoken = token
    botstatus = status
    client = commands.Bot(command_prefix=botprefix, description=botdescription)

    @client.event
    async def on_ready():
        print(
            f"Le bot {client.user.name} a été lancé ! \nStatistiques \nServeurs : {len(client.guilds)}\n\n----------\n\nChargement ...\nStatus : {botstatus}\nPréfix : {botprefix}\nDescription : {botdescription}\n\n----------"
        )
        await client.change_presence(activity=discord.Game(name=botstatus))

    @client.command()
    async def ping(ctx):
        latence = client.latency * 1000
        await ctx.send(f"Pong , je t'ai répondu en {round(latence)}ms !")

    @client.command()
    async def kick(ctx, member: discord.Member):
        try:
            ctx.delete()
            await member.kick(reason=f"Banned by {client.user.name}")
            await ctx.send("J'ai expulser" + member.mention + "!")
        except:
            await ctx.send("Une erreur s'est produite")

    @client.remove_command("help")
    @client.command()
    async def help(ctx):
        embed = discord.Embed(title="Page d'aide",
                              description="Création de la page en cours !",
                              colour=0x5ad2d6)
        embed2 = discord.Embed(title="Test", description="test")
        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx)
        paginator.add_reaction("⬅", "back")
        paginator.add_reaction("🔲", "lock")
        paginator.add_reaction("➡", "next")
        embeds = [embed, embed2]
        await paginator.run(embeds)

    client.run(bottoken)
