# vtuberwiki-py
[![](https://img.shields.io/pypi/v/vtuberwiki-py.svg?style=for-the-badge&logo=pypi&color=yellowgreen&logoColor=white)](https://pypi.org/project/vtuberwiki-py/)
[![](https://img.shields.io/pypi/dm/vtuberwiki-py?color=blueviolet&logo=pypi&logoColor=white&style=for-the-badge)](https://pypi.org/project/vtuberwiki-py/)

**vtuberwiki-py** is a Python library wrapper for [VirtualYoutuber](https://virtualyoutuber.fandom.com/wiki/Virtual_YouTuber_Wiki) Fandom API.

This package supports both Asynchronous (async/non-blocking) and Synchronous (sync/blocking) programming.

## Installation

To install vtuberwiki-py, simply run:

```
$ pip install vtuberwiki-py
```

## Breaking Changes

- to increase ease of use, `auto_correct` parameter will now defaults to `True`
- `trivia()` now returns a `List`
- removing `misc` and `name` key from dict, so `trivia()` will now fetch all of the trivia without classifying the segment
- `background()` method is now changed into `history()`
- adding a new `quote()` method to fetch vtuber's quotes
- `quote()` method returns a `List`
- now you can get the name & image of a Vtuber by calling the `.name` and `.image` Class property

to understand more please read vtuberwiki-py documentations, thanks.

## Documentation

You can find the full documentation and example for vtuberwiki-py [here](https://vtuberwiki.daffak.xyz).

## Examples

→ Asynchronous (non-blocking)

```py
from vtuberwiki import AioVwiki
import asyncio

async def search_fandom():
    async with AioVwiki() as aio_vwiki:
        await aio_vwiki.search(vtuber="mythia batford",limit=3)
        # ['Mythia Batford', 'Mythia Batford/Gallery', 'Mythia Batford/Discography']
        await aio_vwiki.summary(vtuber="mythia batford",auto_correct=True)
        # Mythia Batford (ミシア ・バットフォード) is an Indonesian female Virtual Youtuber. She uses both Indonesian and English on her stream.

asyncio.run(search_fandom())
```

→ Synchronous (blocking)

```py
from vtuberwiki import Vwiki

def search_fandom():
    vwiki = Vwiki()
    vwiki.search(vtuber="mythia batford",limit=3)
    # ['Mythia Batford', 'Mythia Batford/Gallery', 'Mythia Batford/Discography']
    vwiki.summary(vtuber="mythia batford",auto_correct=True)
    # Mythia Batford (ミシア ・バットフォード) is an Indonesian female Virtual Youtuber. She uses both Indonesian and English on her stream.

search_fandom()
```

## License

MIT licensed. See the [LICENSE file](https://github.com/daffpy/vtuberwiki-py/blob/main/LICENSE) for full details.

## Credits

- Special thanks to MediaWiki API and Fandom for making this project possible
