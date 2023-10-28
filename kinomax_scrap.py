import requests
from bs4 import BeautifulSoup
from config import CFG

def cinema_primers_data(link):
    link = link
    movie = requests.get(link)
    movie_soup = BeautifulSoup(movie.content,"html.parser")
    results = movie_soup.find_all("div",{"class":"tworHzOyhuFiKSkFyXoR2g=="})
    result_items =  results[0].find_all("a",{"class":"yvN8CChhP5iAZAfnKMIscw== Yhe2mD+XDSNnzuukgsKHwA=="})
    data = []
    for item_count, item in enumerate(result_items,1):
        item_name =  item.find_all("h4",class_ = "syjY29n50XGKPXEYafAEJQ==")
        if len(item_name)!=0:
            item_name =  str(item.find_all("h4",class_ = "syjY29n50XGKPXEYafAEJQ==")[0]).split("<span>")[1].split("</span>")[0]
            # print(item_name)
            data.append(item_name)
    data_of_films = "Ты можешь посмтреть это в кинотеатре: \n"
    for i in range(len(data)):
        data_of_films+="●  "+(str(data[i]).replace("amp","")+"\n")
    return data_of_films

data = cinema_primers_data(CFG.kinomax_link)
f = open("primers_data.txt", "w", encoding="utf8")
f.write(data)
f.close()
