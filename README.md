# vtuberwiki-py

**vtuberwiki-py** is a Python wrapper for [VirtualYoutuber](https://virtualyoutuber.fandom.com/wiki/Virtual_YouTuber_Wiki) Fandom API.

## Example

### Searching for available fandom
→ **Asynchronous method (non-blocking)**

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

→ **Synchronous method (blocking)**
```py
from vtuberwiki import Vwiki
import asyncio
import time

def main():
    vwiki = Vwiki()
    s = vwiki.search(vtuber="mythia batford",limit=3)
    print(s) #['Mythia Batford', 'Mythia Batford/Gallery', 'Mythia Batford/Discography']

main()
```

### → Fetching data of a category from the fandom
→ **Asynchronous method (non-blocking)**
```py
from vtuberwiki import AioVwiki
import asyncio

async def get_summary():
    async with AioVwiki() as aio_vwiki:
        s = await aio_vwiki.summary(vtuber="mythia batford",auto_correct=True)
        print(s) #Mythia Batford (ミシア ・バットフォード) is an Indonesian female Virtual Youtuber. She uses both Indonesian and English on her stream.

asyncio.run(get_summary())
```
→ **Synchronous method (blocking)**
```py
from vtuberwiki import Vwiki

def main():
    vwiki = Vwiki()
    s = vwiki.summary(vtuber="mythia batford",limit=3)
    print(s) #Mythia Batford (ミシア ・バットフォード) is an Indonesian female Virtual Youtuber. She uses both Indonesian and English on her stream.

main()
```
