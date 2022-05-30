import aiohttp
from bs4 import BeautifulSoup, SoupStrainer
import re
from typing import Optional, TypeVar, Any
import string

headers={'User-Agent':'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}

AioVwikiT = TypeVar("AioVwikiT", bound="AioVwiki")

class AioVwiki():

    def __init__(self,session: Optional[aiohttp.ClientSession] = None) -> None:
        self.session = session
        self.image = ""

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

    async def decompose_useless(self,body):
        infoboxes = body.find_all('aside', class_="portable-infobox")
        first_run = True
        for box in infoboxes:
            if first_run:
                exc = box.find('img',class_="pi-image-thumbnail")
                if exc is None:
                    box.decompose()
                    first_run= False
                    continue
                self.image = exc["src"]
                first_run= False
            box.decompose()

        toc = body.find('div', id='toc')
        if toc: toc.decompose()

        message_boxes = body.find_all('table', class_="messagebox")
        for box in message_boxes:
            box.decompose()

        captions = body.find_all('p', class_="caption")
        for caption in captions:
            caption.decompose()

        nav_boxes = body.find_all('table', class_="navbox")
        for box in nav_boxes:
            box.decompose()

        return body      

    async def validity_check(self,vtuber:str,auto_correct:bool,session:aiohttp.ClientSession): 
        params={
            'action':'query',
            'titles':vtuber,
            "format":"json",
            "formatversion":2
        }
        x=''
        if auto_correct is False:
            req = await session.get('https://virtualyoutuber.fandom.com/api.php',params=params)
            res = await req.json()
            try:
                fin = res["query"]["pages"][0]["missing"]
                if fin == True or fin == '':
                    return None
            except KeyError:
                x = string.capwords(vtuber).replace(' ','_')
                pass
        else:
            res = await self.search(vtuber=vtuber) 
            if res == []:
                return None 
            if res[0].startswith('List') is False:
                x = string.capwords(res[0]).replace(' ','_')
            else:
                return None   
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

    async def summary(self,vtuber:str,auto_correct :bool = True):
        session = await self._get_session()
        x = await self.validity_check(vtuber=vtuber,auto_correct=auto_correct,session=session)
        self.name = x
        if x is None:
            return "Make sure the names are correct, and use auto_correct if you haven't already"
        html_req = await session.get(f'https://virtualyoutuber.fandom.com/wiki/{x}')
        html = await html_req.content.read()
        html = html.decode('utf-8')
        cls_output = SoupStrainer(class_='mw-parser-output')
        soup = BeautifulSoup(html, 'lxml',parse_only=cls_output)
        body = soup.find(class_='mw-parser-output')
        img = body.find("img",class_="pi-image-thumbnail")
        if img is None:
            self.image = "None"
        else:
            self.image = img["src"]
        #body = await self.decompose_useless(body)
        para = body.find_all('p',recursive=False,limit=3)
        annoying_string = para[0].find('i')
        if annoying_string != None:
            para.pop(0)  

        summary = para[1].text
        return summary.strip()

    async def personality(self,vtuber:str,auto_correct :bool = True):
        session = await self._get_session()
        x = await self.validity_check(vtuber=vtuber,auto_correct=auto_correct,session=session)
        self.name = x
        if x is None:
            return f'No wiki results for Vtuber "{vtuber}"' 
        html_req = await session.get(f'https://virtualyoutuber.fandom.com/wiki/{x}')
        html = await html_req.content.read()
        html = html.decode('utf-8')
        cls_output = SoupStrainer(class_='mw-parser-output')
        soup = BeautifulSoup(html, 'lxml',parse_only=cls_output)
        body = soup.find(class_='mw-parser-output')
        img = body.find("img",class_="pi-image-thumbnail")
        if img is None:
            self.image = "None"
        else:
            self.image = img["src"]
        #body = await self.decompose_useless(body)
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
    
    async def quote(self,vtuber:str,auto_correct :bool = True):
        session = await self._get_session()
        x = await self.validity_check(vtuber=vtuber,auto_correct=auto_correct,session=session)
        self.name = x
        if x is None:
            return f'No wiki results for Vtuber "{vtuber}"' 
        html_req = await session.get(f'https://virtualyoutuber.fandom.com/wiki/{x}')
        html = await html_req.content.read()
        html = html.decode('utf-8')
        cls_output = SoupStrainer(class_='mw-parser-output')
        soup = BeautifulSoup(html, 'lxml',parse_only=cls_output)
        body = soup.find(class_='mw-parser-output')
        img = body.find("img",class_="pi-image-thumbnail")
        if img is None:
            self.image = "None"
        else:
            self.image = img["src"]
        #body = await self.decompose_useless(body)
        qts_tag = body.find("span",id="Quotes")
        qts = "None"
        if qts_tag != None:
            qts=""
            p_qts_tag = qts_tag.parent
            prnt = p_qts_tag.find_next_sibling().find_all('li')
            for z in prnt:
                if z.text != '':
                    real_t = re.sub("\[[0-9]+\]",'',z.text)
                    qts = qts + '\n' + real_t
                z.decompose()
        if qts == "None": 
            return qts 
        else: 
            return (qts.strip()).splitlines()
    
    async def history(self,vtuber:str,auto_correct :bool = True):
        session = await self._get_session()
        x = await self.validity_check(vtuber=vtuber,auto_correct=auto_correct,session=session)
        self.name = x
        if x is None:
            return f'No wiki results for Vtuber "{vtuber}"' 
        html_req = await session.get(f'https://virtualyoutuber.fandom.com/wiki/{x}')
        html = await html_req.content.read()
        html = html.decode('utf-8')
        cls_output = SoupStrainer(class_='mw-parser-output')
        soup = BeautifulSoup(html, 'lxml',parse_only=cls_output)
        body = soup.find(class_='mw-parser-output')
        img = body.find("img",class_="pi-image-thumbnail")
        if img is None:
            self.image = "None"
        else:
            self.image = img["src"]
        #body = await self.decompose_useless(body)
        hs_tag = body.find("span",id="History")
        section = ''
        res = {}
        hs = "None"
        first_run = True
        if hs_tag != None:
            hs=""
            p_hs_tag = hs_tag.parent
            next_node = p_hs_tag.find_next_sibling()
            #r_next_node = p_hs_tag.find_next_sibling()
            while True:
                if str(next_node).startswith('<h3>'):
                    if first_run is False:
                        res[section] = hs
                        hs = ''
                        section = next_node.text
                    else:
                        section = next_node.text 
                if str(next_node).startswith('<h2>'):
                    if hs != '':
                        res[section] = hs
                    break
  
                if next_node.name == "p":
                    if next_node.text != '':
                        real_t = re.sub("\[[0-9]+\]",'',next_node.text)
                        hs = hs + '\n' + real_t       
                        if first_run is True:
                            first_run = False
                next_node = next_node.find_next_sibling()  
        return res        

    async def trivia(self,vtuber:str,auto_correct :bool = True):
        session = await self._get_session()
        x = await self.validity_check(vtuber=vtuber,auto_correct=auto_correct,session=session)
        self.name = x
        if x is None:
            return f'No wiki results for Vtuber "{vtuber}"' 
        html_req = await session.get(f'https://virtualyoutuber.fandom.com/wiki/{x}')
        html = await html_req.content.read()
        html = html.decode('utf-8')
        cls_output = SoupStrainer(class_='mw-parser-output')
        soup = BeautifulSoup(html, 'lxml',parse_only=cls_output)
        body = soup.find(class_='mw-parser-output')
        img = body.find("img",class_="pi-image-thumbnail")
        if img is None:
            self.image = "None"
        else:
            self.image = img["src"]
        #body = await self.decompose_useless(body)
        msc_tag = body.find("span",id="Trivia")
        no_subhead = True
        msc = "None"
        if msc_tag != None:
            msc=""
            p_msc_tag = msc_tag.parent
            next_node = p_msc_tag.find_next_sibling()
            while True:
                if str(next_node).startswith('<ul>') and no_subhead is True:
                    prnt = next_node.find_all('li')
                    for z in prnt:
                        if z.text != '':
                            real_t = re.sub("\[[0-9]+\]",'',z.text)
                            msc = msc + '\n' + real_t  
                        z.decompose()  
                    break
                if str(next_node).startswith('<h2>'):
                    break
                prnt = next_node.find_next_sibling().find_all('li')
                for z in prnt:
                    if z.text != '':
                        real_t = re.sub("\[[0-9]+\]",'',z.text)
                        msc = msc + '\n' + real_t  
                    z.decompose()
                if no_subhead == True:    
                    no_subhead = False
                next_node = next_node.find_next_sibling()  
        if msc == "None":
            return msc
        else:
            return (msc.strip()).splitlines()

    async def image_link(self,vtuber:str,auto_correct :bool = True):
        session = await self._get_session()
        x = await self.validity_check(vtuber=vtuber,auto_correct=auto_correct,session=session)
        if x is None:
            return f'No wiki results for Vtuber "{vtuber}"' 
        html_req = await session.get(f'https://virtualyoutuber.fandom.com/wiki/{x}')
        html = await html_req.content.read()
        html = html.decode('utf-8')
        cls_output = SoupStrainer(class_='mw-parser-output')
        soup = BeautifulSoup(html, 'lxml',parse_only=cls_output)
        body = soup.find(class_='mw-parser-output')
        img = body.find("img",class_="pi-image-thumbnail")
        if img is None:
            self.image = "None"
        else:
            self.image = img["src"]
        #body = await self.decompose_useless(body)
        return self.image         

    async def all(self,vtuber :str,auto_correct :bool = True):
        session = await self._get_session()
        x = await self.validity_check(vtuber=vtuber,auto_correct=auto_correct,session=session)
        self.name = x
        if x is None:
            return f'No wiki results for Vtuber "{vtuber}"' 
        html_req = await session.get(f'https://virtualyoutuber.fandom.com/wiki/{x}')
        html = await html_req.content.read()
        html = html.decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        body = soup.find(class_='mw-parser-output')
        #body = await self.decompose_useless(body)
        img = body.find("img",class_="pi-image-thumbnail")
        if img is None:
            self.image = "None"
        else:
            self.image = img["src"]

        para = body.find_all('p',recursive=False,limit=3)
        annoying_string = para[0].find('i')
        if annoying_string != None:
            para.pop(0)  

        summary = (para[1].text).strip() 

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

        hs_tag = body.find("span",id="History")
        section = ''
        res = {}
        hs = "None"
        first_run = True
        if hs_tag != None:
            hs=""
            p_hs_tag = hs_tag.parent
            next_node = p_hs_tag.find_next_sibling()
            #r_next_node = p_hs_tag.find_next_sibling()
            while True:
                if str(next_node).startswith('<h3>'):
                    if first_run is False:
                        res[section] = hs
                        hs = ''
                        section = next_node.text
                    else:
                        section = next_node.text 
                if str(next_node).startswith('<h2>'):
                    if hs != '':
                        res[section] = hs
                    break
  
                if next_node.name == "p":
                    if next_node.text != '':
                        real_t = re.sub("\[[0-9]+\]",'',next_node.text)
                        hs = hs + '\n' + real_t       
                        if first_run is True:
                            first_run = False
                next_node = next_node.find_next_sibling()  


        msc_tag = body.find("span",id="Trivia")
        no_subhead = True
        msc = "None"
        if msc_tag != None:
            msc=""
            p_msc_tag = msc_tag.parent
            next_node = p_msc_tag.find_next_sibling()
            while True:
                if str(next_node).startswith('<ul>') and no_subhead is True:
                    prnt = next_node.find_all('li')
                    for z in prnt:
                        if z.text != '':
                            real_t = re.sub("\[[0-9]+\]",'',z.text)
                            msc = msc + '\n' + real_t  
                        z.decompose()  
                    break
                if str(next_node).startswith('<h2>'):
                    break
                prnt = next_node.find_next_sibling().find_all('li')
                for z in prnt:
                    if z.text != '':
                        real_t = re.sub("\[[0-9]+\]",'',z.text)
                        msc = msc + '\n' + real_t  
                    z.decompose()
                if no_subhead == True:    
                    no_subhead = False
                next_node = next_node.find_next_sibling()  
        if msc != "None":
            msc = msc.strip().splitlines()           

        return {
            "vtuber":self.name,
            "summary":summary,
            "personality":prsn.strip(),
            "history":res,
            "trivia":msc,
            "image_link": self.image
        }


                
            



