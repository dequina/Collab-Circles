import bs4
import requests
import csv
import time

youtuber = {}
curPages = []
count = 0;

link_pre = "https://youtube.fandom.com/wiki/Category:Gaming_YouTubers?from="

cat_links = ["","Angry+Birds", "BAKCHODI+wala+TECH", "Boom+Beach","CiBoiv", "DAGames",
    "Doni+Bobes", "EvanMCGaming", "FusRoFran+Cosplay", "Greenbeak","Iggy+Fresh", "JC+the+Caster", "KeitaroTime",
    "Let%E2%80%99s+Game+It+Out", "Manni-Gaming","Minecraftme+Lol", "NecroVMX","OneCheesyMofo", "Polarcub",
    "Realed","Saladthetroll006", "Skallagrim", "Stellarr+1","TechPoint", "TheNextGenius","Two+Angry+Gamers+TV",
    "Welyn","ZeroDucksGiven", "%E9%AD%94%E7%95%8C%E3%83%8E%E3%82%8A%E3%82%8A%E3%82%80",     
]

# Getting YouTubers on one category page
def extractFromCategory(link, arr):
    # Get category
    html = requests.get(link).text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    members = soup.find('div', 'category-page__members')
    members_links = members.find_all('a',"category-page__member-link")
    for tag in members_links:
        if '/wiki/' in tag['href']:
            arr.append("https://youtube.fandom.com" + tag['href'])

# Get the associates and collaborators of one YouTuber
def getAssociates(link):
    # Get article
    html = requests.get(link).text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    youtuber = {}

    # Finding 'Minecraft' in the article
    ptags = soup.find_all('p')
    isMinecraft = any("Minecraft" in tag.text.split() for tag in ptags)
    if (isMinecraft == False):
        #print ("Not a Minecraft YouTuber")
        return
    try:
        yter_info = soup.find('aside') # Get infobox   
        youtuber["YouTuber"] = yter_info.h2.text.strip()
        collab = yter_info.find('div',{"data-source":"collab"}) # Go to collab section
        if (collab != None):
            section = collab.find('div', {"class":"mw-collapsible mw-collapsed"})
            if (section != None):
                associates = section.get_text().split(' • ')
                youtuber["Associates"] = associates
    except:
        print("Can't scrape:", link)
    return youtuber

# Writing the data into a csv file
if __name__ == "__main__":
    with open('YTers.csv', 'w', newline='') as csvfile:
        fieldnames = ["YouTuber", "Associates"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for cat in cat_links:
            curPages = []
            extractFromCategory(link_pre+cat, curPages)
            for page in curPages:
                count +=1
                print(count)
                yter_data = getAssociates(page)
                if not yter_data: continue
                else:
                    writer.writerow(yter_data)
    print("Done! :)")

