# this file is not needed if the scraped data is already saved in a file

from bs4 import BeautifulSoup
from urllib.request import urlopen
from spell import Spell

def scrape_spell(url):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # get div with class page-title
    div = soup.find("div", class_="page-title")
    name = div.text.strip()
    print(name)

    # get div with id "page-content"
    content = soup.find("div", {"id": "page-content"})
    # remove the last <p> tag
    content.find_all("p")[-1].decompose()

    # make all hyperlinks into normal text (no longer clickable)
    for link in content.find_all("a"):
        link.replaceWithChildren()

    # decrease bottom margin of first two <p> tags
    content.find_all("p")[0]["style"] = "margin-bottom: 8px;"
    content.find_all("p")[1]["style"] = "margin-bottom: 8px;"

    # add a line with the url
    # hyperlink
    url_line = soup.new_tag("a", href=url)
    url_line.string = url
    # make hyperlink less blue
    url_line["style"] = "color: #555555;"
    # add to end of content
    content.append(url_line)
    
    return Spell(name, str(content))

def scrape_class(class_name):
    url = f"http://dnd5e.wikidot.com/spells:{class_name}"

    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    spell_urls = []

    for tab in range(len(soup.find_all("div", {"id": lambda x: x and "wiki-tab-0-" in x}))):
        spell_list = soup.find_all("div", {"id": f"wiki-tab-0-{tab}"})
        for row in spell_list[0].find_all("tr")[1:]:
            spell_urls.append("http://dnd5e.wikidot.com" + row.find("a")["href"])

    return spell_urls

def scrape_property(description, property):
    soup = BeautifulSoup(description, "html.parser")
    match property:
        case "Level":
            # get first <p> in <div> with id page-content
            div = soup.find("div", id="page-content")
            p = div.find_all("p")[1]
            if "cantrip" in p.text:
                return 0
            return p.text[0]
        case "School":
            div = soup.find("div", id="page-content")
            p = div.find_all("p")[1]
            # remove (ritual) from p.text, capitalize first letters of each word
            p_text = p.text.replace("(ritual)", "").strip()
            # remove (dunamancy:graviturgy) from p_text
            p_text = p_text.replace("(dunamancy:graviturgy)", "").strip()
            p_text = " ".join([word.capitalize() for word in p_text.split(" ")])
            if "Cantrip" in p_text:
                return p_text.strip().split(" ")[0]
            return p_text.strip().split(" ")[-1]
        case "Casting Time":
            div = soup.find("div", id="page-content")
            p = div.find_all("p")[2]
            ct =  str(p).split("</strong> ")[1].split("<strong>")[0].replace("</p>", "").replace("<br/>", "").strip()
            ct = ct.split(",")[0]
            return ct
        case "Range":
            div = soup.find("div", id="page-content")
            p = div.find_all("p")[2]
            range = str(p).split("</strong> ")[2].split("<strong>")[0].replace("</p>", "").replace("<br/>", "").strip()
            range = range.replace("ft", " feet")
            return range
        case "Components":
            div = soup.find("div", id="page-content")
            p = div.find_all("p")[2]
            components = str(p).split("</strong> ")[3].split("<strong>")[0].replace("</p>", "").replace("<br/>", "").strip()
            # remove stuff in parentheses
            return components.split(" (")[0]
        case "Duration":
            div = soup.find("div", id="page-content")
            p = div.find_all("p")[2]
            p_text = str(p).replace("(see below)", "")
            return p_text.split("</strong> ")[4].split("<strong>")[0].replace("</p>", "").replace("<br/>", "").strip()
        case "Source":
            source = soup.find("p", text=lambda x: x and "Source:" in x).text.lower()
            if "player's handbook" in source:
                return "phb"
            elif "xanathar's guide to everything" in source:
                return "xge"
            elif "tasha's cauldron of everything" in source:
                return "tce"
            elif "unearthed arcana" in source:
                return "ua"
            else:
                return "other"
