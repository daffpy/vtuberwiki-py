# vtuberwiki-py
**vtuberwiki-py** is a Python wrapper for [VirtualYoutuber](https://virtualyoutuber.fandom.com/wiki/Virtual_YouTuber_Wiki) Fandom API.


## Example
### Searching for available fandom
```py
import vwiki
import asyncio

async def main():
    s = await vwiki.AsyncSearch(vtuber="mythia batford",limit=3)
    print(s) #['Mythia Batford', 'Mythia Batford/Gallery', 'Mythia Batford/Discography']

asyncio.run(main())
```
Note: the most relevant search is usually the first index
