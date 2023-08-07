# QuranAPI

## Details
QuranAPI was built so you can get single verses into your discord server through your discord bot!
For any suggestions of concerns please email nooby xviii: xviii2008@gmail.com

## Features
  * Modern module to get single verses for your discord bot
  * Built with ```asyncio``` and ```aiohttp```
  * Trusted backend Quran API

## How It Works
  * Install the module: ```pip install QuranAPI```
  * Import the module to your code: ```import QuranAPI```
  * Write this function in this format for an event or command: ```await QuranAPI.get_verse({verse ID}, "{language}", {channel}) 
    - Explanation for the function:
        - {verse ID} stands for the Ayah you want
          - For Example: {verse ID} can be 1:1, which will give us the first Ayah in the first Surah. Remember it is formatted Surah:Ayah
        - "{language}" stands for the Language you want the Ayah's to be displayed
          - For Example: "{language}" can be "arabic" or "english"
            - Note that only english and arabic are available as of version 0.0.7
        - {channel} stands for the channel in your server or a server your bots in where you want the verse to be sent
          - For Example: {channel} can be ctx.channel if you are using the module for an quran command and can be message.channel when you are using the module for an on_message event
    - Examples of the function:
      - Quran Command (English Translation):
       ```python
      @client.command()
      async def quran(ctx, ayah): #ayah will be the ayah your bot gets from a surah
        await QuranAPI.get_verse(ayah, "english", ctx.channel)
        ```
        - The Command Usage Will Be:
          ```~quran 1:2```
            * Using this command, your bot will give you the translation for the second ayah from the first surah in english
            
      - Quran Command (Arabic Translation):
       ```python
      @client.command()
      async def quran(ctx, ayah): #ayah will be the ayah your bot gets from a surah
        await QuranAPI.get_verse(ayah, "arabic", ctx.channel)
        ```
        - The Command Usage Will Be:
          ```~quran 1:3```
            * Using this command, your bot will give you the translation for the third ayah from the first surah in arabic
            
## Random Verse 
If you want a random verse to be sent, do everything the same as above, but instead use this function: ```await QuranAPI.random_verse("{language}", channel)```
  - Examples:
    - Random Verse Function (english):
      ```await QuranAPI.random_verse("english", ctx.channel)```
    - Random Verse Function (arabic):
      ```await QuranAPI.random_verse("arabic", ctx.channel)```