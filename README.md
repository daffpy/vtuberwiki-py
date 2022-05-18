# vtuberwiki-py

**vtuberwiki-py** is a Python wrapper for [VirtualYoutuber](https://virtualyoutuber.fandom.com/wiki/Virtual_YouTuber_Wiki) Fandom API.

## Example

### → Searching for available fandom

```py
from vtuberwiki import AioVwiki
import asyncio

async def search_fandom():
    async with AioVwiki() as aio_vwiki:
        s = await aio_vwiki.search(vtuber="mythia batford",limit=3)
        print(s) #['Mythia Batford', 'Mythia Batford/Gallery', 'Mythia Batford/Discography']

asyncio.run(search_fandom())
```

_Note: the most relevant search is usually the first index_

### → Fetching data of a category from the fandom

```py
from vtuberwiki import AioVwiki
import asyncio

async def get_summary():
    async with AioVwiki() as aio_vwiki:
        s = await aio_vwiki.summary(vtuber="mythia batford",auto_correct=True)
        print(s) #Mythia Batford (ミシア ・バットフォード) is an Indonesian female Virtual Youtuber. She uses both Indonesian and English on her stream.

asyncio.run(get_summary())
```
