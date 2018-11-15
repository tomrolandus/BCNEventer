from bs4 import BeautifulSoup
import argparse
import requests
import pandas as pd

def scrape_xceed_city(city):
    """
    Scrape xceed web for events in your city
    """
    labels = ["description", "start time", "place", "musice style", "price", "category"]
    events_info = []
    city = city.lower()
     
    r  = requests.get("https://xceed.me/events/{}".format(city))
    data = r.text
    soup = BeautifulSoup(data, "lxml")

    print("Scraping https://xceed.me/events/{}".format(city))    
    events = soup.findAll("article")
    for event in events:
        start_time = event.findAll("time", {"itemprop":"startDate"})[0].text
        description = event.findAll("h2", {"class":"margin-0 text-bold grey-36-c cardTitle ellipsis"})[0].text
        place = event.findAll("span", {"itemprop":"name"})[0].text
        music_style = "".join(event.findAll("p", {"class":"margin-0 cardMusic grey-70-c"})[0].text.strip().split("\xa0|\xa0"))
        try:
            price = event.findAll("button", {"class":"actionB cardButton"})[0].text
        except:
            price = 'NA'
        category = 'Music'
        events_info.append([description, start_time, place, music_style, price, category])
    

    print("Writting xceed_{}.csv".format(city))
    df = pd.DataFrame.from_records(events_info, columns=labels)
    df.to_csv("xceed_{}.csv".format(city))
    return df

def parse_args():
    parser = argparse.ArgumentParser(description="Parse from xceed all events going on in a city and oput them as csv")
    parser.add_argument("city", help="City you want to get the event for", default="barcelona")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    scrape_xceed_city(args.city)
