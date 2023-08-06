# QuranAPI
QuranAPI was built so you don't have to scrape Quran API's for your discord bot!
  You can now setup a quran command with less than one minute!

For more information, questions or regards on this module please email nooby xviii. His Email: ```xviii2008@gmail.com```

## Features
  • Modern discord.py module using ```asyncio``` and ```aiohttp```
  • Powered by an powerful Quran API
  
## Installation
You can install QuranAPI from [PyPi](#):
  ```import QuranAPI```
Module is available for python versions 3.7+
  
## Usage
In order to get a verse you must write this phase in your code:
  ```await QuranAPI.get_verse(verse, channel)```
As you can see the part in the function called "verse", is what the API uses to get a verse. And the "channel" part is where you want the verse to be sent in your discord server. 

## Examples
Quran Command:

```python
import discord
from discord.ext import commands
import QuranAPI

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
  print("hello")
  
@client.command()
async def quran(ctx, verse):
  await QuranAPI.get_quran(verse, ctx.channel) #As you can see this is a quran command, so I put the channel as "ctx.channel" so the bot will send the verse it gets into the channel the command was used on!
```
## Discord Command Example

If we use the quran command above, we must use the command like this:
  ```!quran 1:1```
This will give us the first Ayah in the first Surah. It is formatted like this:
  ```Surah:Ayah```
The outcome of 1:1 will be:
  ```Praise be to Allah, Lord of the Worlds```