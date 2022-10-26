import requests
from bs4 import BeautifulSoup, SoupStrainer
from typing import Optional, TypeVar, Any
import re
import string

VwikiT = TypeVar("VwikiT", bound="Vwiki")

class Vwiki:
  __slots__ = ("image",)

  def __init__(self):
    self.image = ""

  def decompose_useless(self, body):
    infoboxes = body.find_all("aside", class_="portable-infobox")
    first_run = True
    
    for box in infoboxes:
      if first_run:
        exc = box.find("img", class_="pi-image-thumbnail")
        if exc is None:
          box.decompose()
          first_run = False
          continue
        
        self.image = exc["src"]
        first_run = False
      
      box.decompose()

    toc = body.find("div", id="toc")
    if toc:
      toc.decompose()

    message_boxes = body.find_all("table", class_="messagebox")
    for box in message_boxes:
      box.decompose()

    captions = body.find_all("p", class_="caption")
    for caption in captions:
      caption.decompose()

    nav_boxes = body.find_all("table", class_="navbox")
    for box in nav_boxes:
      box.decompose()

    return body

  def validity_check(self, vtuber: str, auto_correct: bool):
    x = ""
    
    if not auto_correct:
      req = requests.get(
        "https://virtualyoutuber.fandom.com/api.php", params={
        "action": "query",
        "titles": vtuber,
        "format": "json",
        "formatversion": 2,
      })
      
      res = req.json()
      try:
        fin = res["query"]["pages"][0]["missing"]
        if fin or fin == "":
          return None
      except KeyError:
        x = string.capwords(vtuber).replace(" ", "_")
        pass
    else:
      res = self.search(vtuber=vtuber)
      if res and not res[0].startswith("List"):
        x = string.capwords(res[0]).replace(" ", "_")
      else:
        return None
    return x

  def search(self, vtuber: str, limit=10):
    req = requests.get(f"https://virtualyoutuber.fandom.com/api.php", params={
      "action": "query",
      "srsearch": vtuber,
      "srlimit": limit,
      "list": "search",
      "format": "json",
    })
    
    res = req.json()
    
    return [object["title"] for object in res["query"]["search"]]

  def summary(self, vtuber: str, auto_correct: bool = True):
    x = self.validity_check(vtuber=vtuber, auto_correct=auto_correct)
    self.name = x
    
    if x is None:
      raise Exception(f'No wiki results for Vtuber "{vtuber}"')
    
    html = requests.get(f"https://virtualyoutuber.fandom.com/wiki/{x}").text

    cls_output = SoupStrainer(class_="mw-parser-output")
    soup = BeautifulSoup(html, "lxml", parse_only=cls_output)
    body = soup.find(class_="mw-parser-output")
    
    img = body.find("img", class_="pi-image-thumbnail")
    self.image = img["src"] if img else "None"
    # body = await self.decompose_useless(body)
    
    para = body.find_all("p", recursive=False, limit=3)
    
    annoying_string = para[0].find("i")
    if annoying_string:
      para.pop(0)

    return para[1].text.strip()

  def personality(self, vtuber: str, auto_correct: bool = True):
    x = self.validity_check(vtuber=vtuber, auto_correct=auto_correct)
    self.name = x
    if x is None:
      raise Exception(f'No wiki results for Vtuber "{vtuber}"')
    
    html = requests.get(f"https://virtualyoutuber.fandom.com/wiki/{x}").text
    
    cls_output = SoupStrainer(class_="mw-parser-output")
    
    soup = BeautifulSoup(html, "lxml", parse_only=cls_output)
    body = soup.find(class_="mw-parser-output")
    
    img = body.find("img", class_="pi-image-thumbnail")
    self.image = img["src"] if img else "None"
    
    # body = await self.decompose_useless(body)
    person_tag = body.find("span", id="Personality")
    prsn = "None"
    
    if person_tag:
      ph = person_tag.parent.find_next_sibling()
      prsn = ""
      while str(ph)[:3] == "<p>":
        prsn += "\n" + ph.text
        ph = ph.find_next_sibling()
    
    return prsn.strip()

  async def quote(self, vtuber: str, auto_correct: bool = True):
    x = await self.validity_check(
      vtuber=vtuber, auto_correct=auto_correct
    )
    self.name = x
    
    if x is None:
      raise Exception(f'No wiki results for Vtuber "{vtuber}"')
    
    html = requests.get(f"https://virtualyoutuber.fandom.com/wiki/{x}").text

    cls_output = SoupStrainer(class_="mw-parser-output")
    soup = BeautifulSoup(html, "lxml", parse_only=cls_output)
    body = soup.find(class_="mw-parser-output")
    
    img = body.find("img", class_="pi-image-thumbnail")
    self.image = img["src"] if img else "None"
    # body = await self.decompose_useless(body)
    
    qts_tag = body.find("span", id="Quotes")
    qts = "None"
    
    if qts_tag:
      qts = ""
      for z in qts_tag.parent.find_next_sibling().find_all("li"):
        if z.text:
          qts += "\n" + z.text
        z.decompose()
    
    # qts.strip() :^)
    return qts if qts == "None" else (qts.strip()).splitlines()

  def history(self, vtuber: str, auto_correct: bool = True):
    x = self.validity_check(vtuber=vtuber, auto_correct=auto_correct)
    self.name = x
    if x is None:
      raise Exception(f'No wiki results for Vtuber "{vtuber}"')
    
    html = requests.get(f"https://virtualyoutuber.fandom.com/wiki/{x}").text

    cls_output = SoupStrainer(class_="mw-parser-output")
    soup = BeautifulSoup(html, "lxml", parse_only=cls_output)
    body = soup.find(class_="mw-parser-output")
    
    img = body.find("img", class_="pi-image-thumbnail")
    self.image = img["src"] if img else "None"
    # body = await self.decompose_useless(body)
    
    hs_tag = body.find("span", id="History")
    section = ""
    res = {}
    hs = "None"
    first_run = True
    
    if hs_tag:
      hs = ""
      next_node = hs_tag.parent.find_next_sibling()
      # r_next_node = p_hs_tag.find_next_sibling()
      
      while True:
        if str(next_node).startswith("<h3>"):
          if not first_run:
            res[section] = hs
            hs = ""
           
           section = next_node.text
        elif str(next_node).startswith("<h2>"):
          if hs:
            res[section] = hs
          break

        if next_node.name == "p" and next_node.text:
          real_t = re.sub("\[[0-9]+\]", "", next_node.text)
          hs += "\n" + real_t
          if first_run:
            first_run = False
        next_node = next_node.find_next_sibling()
    return res

  def trivia(self, vtuber: str, auto_correct: bool = True):
    x = self.validity_check(vtuber=vtuber, auto_correct=auto_correct)
    self.name = x
    
    if x is None:
      raise Exception(f'No wiki results for Vtuber "{vtuber}"')
    html = requests.get(f"https://virtualyoutuber.fandom.com/wiki/{x}").text

    cls_output = SoupStrainer(class_="mw-parser-output")
    soup = BeautifulSoup(html, "lxml", parse_only=cls_output)
    body = soup.find(class_="mw-parser-output")
    
    img = body.find("img", class_="pi-image-thumbnail")
    self.image = img["src"] if img else "None"
    
    # body = await self.decompose_useless(body)
    msc_tag = body.find("span", id="Trivia")
    no_subhead = True
    msc = "None"
    
    if msc_tag:
      msc = ""
      next_node = msc_tag.parent.find_next_sibling()
      while True:
        if str(next_node).startswith("<ul>") and no_subhead:
          for z in next_node.find_all("li"):
            if z.text:
              real_t = re.sub("\[[0-9]+\]", "", z.text)
              msc += "\n" + real_t
            z.decompose()
          break
        
        if str(next_node).startswith("<h2>"):
          break
        
        for z in next_node.find_next_sibling().find_all("li"):
          if z.text:
            real_t = re.sub("\[[0-9]+\]", "", z.text)
            msc += "\n" + real_t
          z.decompose()
        if no_subhead:
          no_subhead = False
        next_node = next_node.find_next_sibling()
    
    return msc if msc == "None" else msc.strip().splitlines()

  def image_link(self, vtuber: str, auto_correct: bool = True):
    x = self.validity_check(vtuber=vtuber, auto_correct=auto_correct)
    self.name = x
    
    if x is None:
      raise Exception(f'No wiki results for Vtuber "{vtuber}"')
    
    html = requests.get(f"https://virtualyoutuber.fandom.com/wiki/{x}").text

    cls_output = SoupStrainer(class_="mw-parser-output")
    soup = BeautifulSoup(html, "lxml", parse_only=cls_output)
    body = soup.find(class_="mw-parser-output")
    
    img = body.find("img", class_="pi-image-thumbnail")
    self.image = img["src"] if img else "None"
    
    # body = await self.decompose_useless(body)
    return self.image

  def all(self, vtuber: str, auto_correct: bool = True):
    x = self.validity_check(vtuber=vtuber, auto_correct=auto_correct)
    self.name = x
    
    if x is None:
      raise Exception(f'No wiki results for Vtuber "{vtuber}"')
    
    html = requests.get(f"https://virtualyoutuber.fandom.com/wiki/{x}").text

    soup = BeautifulSoup(html, "lxml")
    body = soup.find(class_="mw-parser-output")
    
    img = body.find("img", class_="pi-image-thumbnail")
    self.image = img["src"] if img else "None"

    para = body.find_all("p", recursive=False, limit=3)
    annoying_string = para[0].find("i")
    if annoying_string:
      para.pop(0)

    summary = para[1].text.strip()

    person_tag = body.find("span", id="Personality")
    prsn = "None"
    
    if person_tag:
      ph = person_tag.parent.find_next_sibling()
      prsn = ""
      
      while str(ph)[:3] == "<p>":
        prsn += "\n" + ph.text
        ph = ph.find_next_sibling()

    hs_tag = body.find("span", id="History")
    section = ""
    res = {}
    hs = "None"
    first_run = True
    
    if hs_tag:
      hs = ""
      next_node = hs_tag.parent.find_next_sibling()
      # r_next_node = p_hs_tag.find_next_sibling()
      
      while True:
        if str(next_node).startswith("<h3>"):
          if not first_run:
            res[section] = hs
            hs = ""
          
          section = next_node.text
        elif str(next_node).startswith("<h2>"):
          if hs:
            res[section] = hs
          break

        if next_node.name == "p" and next_node.text:
          real_t = re.sub("\[[0-9]+\]", "", next_node.text)
          hs += "\n" + real_t
          if first_run:
            first_run = False
        next_node = next_node.find_next_sibling()

    msc_tag = body.find("span", id="Trivia")
    no_subhead = True
    msc = "None"
    
    if msc_tag:
      msc = ""
      next_node = msc_tag.parent.find_next_sibling()
      while True:
        if str(next_node).startswith("<ul>") and no_subhead:
          for z in next_node.find_all("li"):
            if z.text:
              real_t = re.sub("\[[0-9]+\]", "", z.text)
              msc += "\n" + real_t
            z.decompose()
          break
        if str(next_node).startswith("<h2>"):
          break
        
        for z in next_node.find_next_sibling().find_all("li"):
          if z.text:
            real_t = re.sub("\[[0-9]+\]", "", z.text)
            msc += "\n" + real_t
          z.decompose()
        
        if no_subhead:
          no_subhead = False
        
        next_node = next_node.find_next_sibling()
    
    if msc != "None":
      msc = msc.strip().splitlines()

    return {
      "vtuber": self.name,
      "summary": summary,
      "personality": prsn.strip(),
      "history": res,
      "trivia": msc,
      "image_link": self.image,
    }
