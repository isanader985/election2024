from flask import Flask, render_template, redirect, url_for

import requests

app = Flask(__name__)

HEADERS = {"Accept-Language": "en-US,en;q=0.5",
           "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:103.0) Gecko/20100101 "
                         "Firefox/103.0"}
URL_PRESIDENT = "https://ero.betfair.com/www/sports/exchange/readonly/v1/bymarket?_ak=nzIFcwyWhrlwYMrh&alt=json&currencyCode=EUR&locale=en_GB&marketIds=1.178176964&rollupLimit=10&rollupModel=STAKE&types=MARKET_STATE,MARKET_DESCRIPTION,EVENT,RUNNER_DESCRIPTION,RUNNER_STATE,RUNNER_EXCHANGE_PRICES_BEST"
URL_POPULAR = "https://ero.betfair.com/www/sports/exchange/readonly/v1/bymarket?_ak=nzIFcwyWhrlwYMrh&alt=json&currencyCode=EUR&locale=en_GB&marketIds=1.178176967&rollupLimit=10&rollupModel=STAKE&types=MARKET_STATE,MARKET_DESCRIPTION,EVENT,RUNNER_DESCRIPTION,RUNNER_STATE,RUNNER_EXCHANGE_PRICES_BEST"
URL_DEMOCRAT = "https://ero.betfair.com/www/sports/exchange/readonly/v1/bymarket?_ak=nzIFcwyWhrlwYMrh&alt=json&currencyCode=EUR&locale=en_GB&marketIds=1.178163685&rollupLimit=10&rollupModel=STAKE&types=MARKET_STATE,MARKET_DESCRIPTION,EVENT,RUNNER_DESCRIPTION,RUNNER_STATE,RUNNER_EXCHANGE_PRICES_BEST"
URL_REPUBLICAN = "https://ero.betfair.com/www/sports/exchange/readonly/v1/bymarket?_ak=nzIFcwyWhrlwYMrh&alt=json&currencyCode=EUR&locale=en_GB&marketIds=1.178163916&rollupLimit=10&rollupModel=STAKE&types=MARKET_STATE,MARKET_DESCRIPTION,EVENT,RUNNER_DESCRIPTION,RUNNER_STATE,RUNNER_EXCHANGE_PRICES_BEST"

class Fetcher:
    def __init__(self):
        self.list = []

    def scrape(self, url, number_of_items):
        response = requests.get(url)
        data = response.json()
        self.list = [[data["eventTypes"][0]["eventNodes"][0]["marketNodes"][0]["runners"][i]["description"]["runnerName"], max(float(data["eventTypes"][0]["eventNodes"][0]["marketNodes"][0]["runners"][i]["exchange"]["availableToLay"][0]["price"]), float(data["eventTypes"][0]["eventNodes"][0]["marketNodes"][0]["runners"][i]["exchange"]["availableToBack"][0]["price"]))] for i in range(number_of_items)]
        self.list.sort(key=lambda l: l[1])
        self.list = self.list[:3]


def edit_list3(lista):
    pm = 0
    for item in lista:
        pm += 1/item[1]
    pm = (2-pm)*100
    for item in lista:
        item[1] = str(round(pm/item[1]))
    return lista


def edit_list4(lista):
    p = 0
    for item in lista:
        item[1] = round(100 / item[1])
        p += item[1]
        item[1] = str(item[1])
    lista.append(["Any Other", str(100 - p)])
    return lista


fetch = Fetcher()
fetch.scrape(URL_PRESIDENT, 3)
#print(edit_list3(fetch.list))
l_president = edit_list3(fetch.list)
fetch.scrape(URL_DEMOCRAT, 6)
#print(edit_list4(fetch.list))
l_democrat = edit_list4(fetch.list)
fetch.scrape(URL_REPUBLICAN, 6)
#print(edit_list4(fetch.list))
l_republican = edit_list4(fetch.list)
fetch.scrape(URL_POPULAR, 3)
#print(edit_list3(fetch.list))
l_popular = edit_list3(fetch.list)




img_list = []

if l_president[0][0] == "Republican Party":
    img_list.append("static/img/"+l_republican[0][0]+".png")
    img_list.append("static/img/"+l_democrat[0][0]+".png")
else:
    img_list.append("static/img/" + l_democrat[0][0] + ".png")
    img_list.append("static/img/" + l_republican[0][0] + ".png")


img_list.append("static/img/"+l_democrat[0][0]+".png")
img_list.append("static/img/"+l_democrat[1][0]+".png")
img_list.append("static/img/"+l_democrat[2][0]+".png")
img_list.append("static/img/"+l_republican[0][0]+".png")
img_list.append("static/img/"+l_republican[1][0]+".png")
img_list.append("static/img/"+l_republican[2][0]+".png")

if l_popular[0][0] == "Republican Party":
    img_list.append("static/img/"+l_republican[0][0]+".png")
    img_list.append("static/img/"+l_democrat[0][0]+".png")
else:
    img_list.append("static/img/" + l_democrat[0][0] + ".png")
    img_list.append("static/img/" + l_republican[0][0] + ".png")


@app.route('/')
def home():
    return render_template("index.html", img_list=img_list, l_president=l_president, l_republican=l_republican, l_democrat=l_democrat, l_popular=l_popular)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
