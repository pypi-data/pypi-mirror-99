import discord
import asyncio
import aiohttp

async def get_verse(verse_id, language, channel):
  chapter = int(verse_id.split(':')[0])
  verse = int(verse_id.split(':')[1])
  if language == "english":
    async with aiohttp.ClientSession() as cs:
      async with cs.get(f"http://quranapi.azurewebsites.net/api/verse/?chapter={chapter}&number={verse}&lang=en") as r:
        res = await r.json()
        embed = discord.Embed(
          color = discord.Color.purple()
        )
        embed.set_author(name=res["ChapterName"])
        embed.add_field(name="Verse:", value=res["Text"])
        embed.set_footer(text="Powered by QuranAPI")
        await channel.send(embed=embed)
  if language == "arabic":
    async with aiohttp.ClientSession() as cs:
      async with cs.get(f"http://quranapi.azurewebsites.net/api/verse/?chapter={chapter}&number={verse}") as r:
        res = await r.json()
        embed = discord.Embed(
        color = discord.Color.purple()
        )
        embed.set_author(name=res["ChapterName"])
        embed.add_field(name="Verse:", value=res["Text"])
        embed.set_footer(text="Powered by QuranAPI")
        await channel.send(embed=embed)
        
async def random_verse(language, channel):
  if language == "english":
    async with aiohttp.ClientSession() as cs:
      async with cs.get("http://quranapi.azurewebsites.net/api/verse/?lang=en") as r:
        res = await r.json()
        embed = discord.Embed(
          color = discord.Color.purple()
        )
        embed.set_author(name=res["ChapterName"])
        embed.add_field(name="Verse:", value=res["Text"])
        embed.set_footer(text="Powered by QuranAPI")
        await channel.send(embed=embed)
  if language == "arabic":
    async with aiohttp.ClientSession() as cs:
      async with cs.get("http://quranapi.azurewebsites.net/api/verse/") as r:
        res = await r.json()
        embed = discord.Embed(
          color = discord.Color.purple()
        )
        embed.set_author(name=res["ChapterName"])
        embed.add_field(name="Verse:", value=res["Text"])
        embed.set_footer(text="Powered by QuranAPI")
        await channel.send(embed=embed)