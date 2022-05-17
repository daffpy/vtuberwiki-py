import aiohttp
from bs4 import BeautifulSoup
import re

headers={'User-Agent':'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}

async def AsyncSearch(vtuber: str,limit=10):
    async with aiohttp.ClientSession(headers=headers) as session:
        params={
            'action':'query',
            'srsearch':vtuber,
            'srlimit':limit,
            "list":"search",
            "format":"json"
        }
        req = await session.get(f'https://virtualyoutuber.fandom.com/api.php',params=params)
        res = await req.json()
        fin = res["query"]["search"]
        result = list((object['title'] for object in fin))
        return result

async def AsyncFetchWiki(vtuber :str,auto_correct :bool = False):
    async with aiohttp.ClientSession(headers=headers) as session:
        params={
            'action':'query',
            'titles':vtuber,
            "format":"json",
            "formatversion":2
        }
        req = await session.get('https://virtualyoutuber.fandom.com/api.php',params=params)
        res = await req.json()
        x=''
        try:
            fin = res["query"]["pages"][0]["missing"]
            if fin == True or fin == '':
                if auto_correct is False:
                    return f'No wiki results for Vtuber "{vtuber}"'
                elif auto_correct is True:
                    res = await AsyncSearch(vtuber=vtuber)
                    if res == []:
                        return f'No wiki results for Vtuber "{vtuber}"' 
                    if res[0].startswith('List') is False:
                        x = res[0].replace(' ','_').title()
                    else:
                        return f'No wiki results for Vtuber "{vtuber}"'  
        except KeyError:
            x = vtuber.replace(' ','_').title()
            pass
        html_req = await session.get(f'https://virtualyoutuber.fandom.com/wiki/{x}')
        html = await html_req.text()
        soup = BeautifulSoup(html, 'lxml')
        body = soup.find(class_='mw-parser-output')
        img = body.find("img",class_="pi-image-thumbnail")
        if img is None:
            img = "None"
        else:
            img = img["src"]
        person_tag = body.find("span",id="Personality")
        bg_tag = body.find("span",id="Background")
        nm_tag = body.find("span",id="Name")
        msc_tag = body.find("span",id="Miscellaneous")
        prsn = "None"
        bg= "None"
        nm="None"
        msc="None"
        if person_tag != None:
            p_person_tag = person_tag.parent
            ph = p_person_tag.find_next_sibling()
            prsn = ""
            while True: 
                if str(ph)[:3] != "<p>":
                    break
                prsn = prsn + "\n" + ph.text
                ph = ph.find_next_sibling()

        if bg_tag != None:
            p_bg_tag = bg_tag.parent
            ph = p_bg_tag.find_next_sibling()
            bg = ""
            while True: 
                if str(ph)[:3] != "<p>":
                    break
                bg = bg + "\n" + ph.text
                ph = ph.find_next_sibling() 

        if nm_tag != None:
            nm=""
            p_nm_tag = nm_tag.parent
            prnt = p_nm_tag.find_next_sibling().find_all('li')
            for z in prnt:
                nm = nm + '\n' + z.text
        if msc_tag != None:
            msc=""
            p_msc_tag = msc_tag.parent
            prnt = p_msc_tag.find_next_sibling().find_all('li')
            for z in prnt:
                msc = msc + '\n' + "- " + z.text        


        para = body.find_all('p',recursive=False,limit=3)
        annoying_string = para[0].find('i')
        if annoying_string != None:
            para.pop(0)  

        summary= para[1].text

        return {
            "vtuber":vtuber,
            "summary":summary.replace(u'\xa0',' ').strip(),
            "personality":prsn.strip(),
            "background":bg.strip(),
            "trivia":{"name":nm.strip(),"misc":msc.strip()},
            "image_link": img

        }


                
            



