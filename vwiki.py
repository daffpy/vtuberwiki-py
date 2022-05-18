import aiohttp
from bs4 import BeautifulSoup, SoupStrainer
from typing import Optional, TypeVar, Any

headers={'User-Agent':'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}

AioVwikiT = TypeVar("AioVwikiT", bound="AioVwiki")

class AioVwiki():

    def __init__(self,session: Optional[aiohttp.ClientSession] = None) -> None:
        self.session = session

    async def __aenter__(self: AioVwikiT) -> AioVwikiT:
        return self

    async def __aexit__(self, *excinfo: Any) -> None:
        await self.close()

    async def close(self) -> None:
        if self.session is not None:
            await self.session.close()

    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None:
            self.session = aiohttp.ClientSession(headers=headers)
        return self.session   

    async def validity_check(self,vtuber:str,auto_correct:bool,session:aiohttp.ClientSession): 
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
                    res = await self.search(vtuber=vtuber)
                    if res == []:
                        return f'No wiki results for Vtuber "{vtuber}"' 
                    if res[0].startswith('List') is False:
                        x = res[0].replace(' ','_').title()
                    else:
                        return f'No wiki results for Vtuber "{vtuber}"'  
        except KeyError:
            x = vtuber.replace(' ','_').title()
            pass
        return x     

    async def search(self,vtuber: str,limit=10):
        session = await self._get_session()
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

    async def summary(self,vtuber:str,auto_correct :bool = False):
        session = await self._get_session()
        x = await self.validity_check(vtuber=vtuber,auto_correct=auto_correct,session=session)
        html_req = await session.get(f'https://virtualyoutuber.fandom.com/wiki/{x}')
        html = await html_req.content.read()
        cls_output = SoupStrainer(class_='mw-parser-output')
        soup = BeautifulSoup(html, 'lxml',parse_only=cls_output)
        body = soup.find(class_='mw-parser-output')
        para = body.find_all('p',recursive=False,limit=3)
        annoying_string = para[0].find('i')
        if annoying_string != None:
            para.pop(0)  

        summary = para[1].text
        return summary.strip()

    async def personality(self,vtuber:str,auto_correct :bool = False):
        session = await self._get_session()
        x = await self.validity_check(vtuber=vtuber,auto_correct=auto_correct,session=session)
        html_req = await session.get(f'https://virtualyoutuber.fandom.com/wiki/{x}')
        html = await html_req.content.read()
        cls_output = SoupStrainer(class_='mw-parser-output')
        soup = BeautifulSoup(html, 'lxml',parse_only=cls_output)
        body = soup.find(class_='mw-parser-output')
        person_tag = body.find("span",id="Personality")
        prsn = "None"
        if person_tag != None:
            p_person_tag = person_tag.parent
            ph = p_person_tag.find_next_sibling()
            prsn = ""
            while True: 
                if str(ph)[:3] != "<p>":
                    break
                prsn = prsn + "\n" + ph.text
                ph = ph.find_next_sibling()
        return prsn.strip()     

    async def background(self,vtuber:str,auto_correct :bool = False):
        session = await self._get_session()
        x = await self.validity_check(vtuber=vtuber,auto_correct=auto_correct,session=session)
        html_req = await session.get(f'https://virtualyoutuber.fandom.com/wiki/{x}')
        html = await html_req.content.read()
        cls_output = SoupStrainer(class_='mw-parser-output')
        soup = BeautifulSoup(html, 'lxml',parse_only=cls_output)
        body = soup.find(class_='mw-parser-output')
        bg_tag = body.find("span",id="Background")
        bg= "None"
        if bg_tag != None:
            p_bg_tag = bg_tag.parent
            ph = p_bg_tag.find_next_sibling()
            bg = ""
            while True: 
                if str(ph)[:3] != "<p>":
                    break
                bg = bg + "\n" + ph.text
                ph = ph.find_next_sibling() 
        return bg.strip()     

    async def trivia(self,vtuber:str,auto_correct :bool = False):
        session = await self._get_session()
        x = await self.validity_check(vtuber=vtuber,auto_correct=auto_correct,session=session)
        html_req = await session.get(f'https://virtualyoutuber.fandom.com/wiki/{x}')
        html = await html_req.content.read()
        cls_output = SoupStrainer(class_='mw-parser-output')
        soup = BeautifulSoup(html, 'lxml',parse_only=cls_output)
        body = soup.find(class_='mw-parser-output')
        msc_tag = body.find("span",id="Miscellaneous")
        nm_tag = body.find("span",id="Name")
        nm="None"
        msc= "None"
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
        return {"name":nm,"misc":msc}  

    async def trivia(self,vtuber:str,auto_correct :bool = False):
        session = await self._get_session()
        x = await self.validity_check(vtuber=vtuber,auto_correct=auto_correct,session=session)
        html_req = await session.get(f'https://virtualyoutuber.fandom.com/wiki/{x}')
        html = await html_req.content.read()
        cls_output = SoupStrainer(class_='mw-parser-output')
        soup = BeautifulSoup(html, 'lxml',parse_only=cls_output)
        body = soup.find(class_='mw-parser-output')
        msc_tag = body.find("span",id="Miscellaneous")
        nm_tag = body.find("span",id="Name")
        nm="None"
        msc= "None"
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
        return {"name":nm,"misc":msc} 

    async def image_link(self,vtuber:str,auto_correct :bool = False):
        session = await self._get_session()
        x = await self.validity_check(vtuber=vtuber,auto_correct=auto_correct,session=session)
        html_req = await session.get(f'https://virtualyoutuber.fandom.com/wiki/{x}')
        html = await html_req.content.read()
        cls_output = SoupStrainer(class_='mw-parser-output')
        soup = BeautifulSoup(html, 'lxml',parse_only=cls_output)
        body = soup.find(class_='mw-parser-output')
        img = body.find("img",class_="pi-image-thumbnail")
        if img is None:
            img = "None"
        else:
            img = img["src"] 
        return img 

    async def all(self,vtuber :str,auto_correct :bool = False):
        session = await self._get_session()
        x = await self.validity_check(vtuber=vtuber,auto_correct=auto_correct,session=session)
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


                
            



