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
