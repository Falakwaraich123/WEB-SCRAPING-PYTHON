import re
import bs4
import time
import requests
import json
from fake_useragent import UserAgent
ua = UserAgent()
headers = {'user-agent': ua.random, "referer": "https://www.imdb.com/chart/moviemeter?ref_=nv_mv_mpm"}
url = "https://www.imdb.com/chart/moviemeter?ref_=nv_mv_mpm"

data = requests.get(url)
soup = bs4.BeautifulSoup(data.text, 'lxml')
all_td = soup.find_all('td', {'class':['titleColumn']})
dict_ = {}
array_ = []
for td in all_td:
    link = 'https://www.imdb.com' + td.find('a').get('href')
    movie_res = requests.get(link, headers=headers)
    movie_soup = bs4.BeautifulSoup(movie_res.text, 'lxml')
    # all movie list
    title = movie_soup.find('div', {'class':['title_wrapper']}).find("h1").text.strip()
    title = " ".join(title.split())
    #user views and critic views
    review_bar = movie_soup.find_all('div', {'class':['titleReviewBarSubItem']})[-1]
    current_positon = review_bar.find('span',{'class':['subText']}).text
    current_positon = current_positon.split("(")[0].strip()

    try:
        popularity = review_bar.find('span', {'class': ['subText']}).find('span', {'class': ['popularityUpOrFlat']})
        popularity = int(popularity.text)
    except:
        try:
            popularity = review_bar.find('span', {'class': ['subText']}).find('span', {'class': ['popularityDown']})
            popularity = int("-"+popularity.text)
        except:
            popularity = 0

    try:
        user_reviews_item = movie_soup.find('div', {'class': ['titleReviewbarItemBorder']}).find('span', {'class': ['subText']})
        reviews = user_reviews_item.find("a").text
        user_reviews = int(re.sub("[^\d]", "", reviews))
    except:
        user_reviews = 0

    try:
        critic_reviews_item = movie_soup.find('div', {'class': ['titleReviewbarItemBorder']}).find('span', {'class': ['subText']})
        reviews = critic_reviews_item.find_all("a")[-1].text
        critic_reviews = int(re.sub("[^\d]", "", reviews))
    except:
        critic_reviews = 0

    try:
        genres = movie_soup.find_all("div", {"class":["canwrap"]})[-1].text
        genres = re.sub("[\s]", "", genres[8:])
    except:
        genres = ""

    txt_block = movie_soup.find_all("div", {"class": ["txt-block"]})
    budget = None
    for block in txt_block:
        try:
            heading = block.find("h4").text.strip()
        except:
            continue
        if heading == "Budget:":
            budget = re.sub("[^$\d,]", "", block.text)
            break

    data = {
         "Positon": current_positon,
         "Title": title,
         "Popularity": popularity,
         "User reviews": user_reviews,
         "Critic reviews": critic_reviews,
         "Budget": budget,
         "Genres": genres
         }
    array_.append(data)
    print(data)
    time.sleep(3)

dict_['data'] = array_
file = open("Data_collection.json", "w")
json.dump(dict_,file, indent=4)
file.close()
